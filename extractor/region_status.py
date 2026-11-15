"""Per company of a region's report list: is it in the CDP bucket, and which values did
the runs not find, and why.

    python -m extractor.region_status "<...>/Nordics_Companies_Reports_FY2025.xlsx"
        [--out output/Nordics_status_FY2025.xlsx] [--no-sync]

Input: the region's company workbook (Country, Company Name, Company ID, GCS path Annual
Report, GCS path Remuneration, Other reports, LEI, FY). A path may say "(not in GCS yet)"
for a report staged but not uploaded, and the remuneration column "Inside annual report".

1. **Bucket**: the region's objects are listed live (gcloud), so the check is against what
   is there now, not the index (rebuilt only after a push). A company is "in GCS" when
   its folder exists; each listed gs:// path is checked to exist.
2. **Runs**: the company's rows in output/*_datapoints.csv (the newest run of it), matched
   by LEI, the CDP id (with or without its 8-hex suffix), then the name without legal words
   in the same country.
3. **Missing values**: each empty value gets its failures.Failure code; the field's
   requirement comes from accuracy/inputs/field_requirements.json ("Required", "Optional",
   conditional). headcount and fte count as one: either fills it.

Writes one workbook: Summary, Companies (one row each), Missing values (one row per
company and field, pay fields once per field with the roles missing it), Not in GCS.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from . import failures as fl
from . import gcs
from .cdp_slug import strip_legal
from .config import PROJECT_ROOT

COUNTRY = {"sweden": "SE", "norway": "NO", "denmark": "DK", "finland": "FI", "iceland": "IS",
           "united kingdom": "GB", "germany": "DE", "austria": "AT", "switzerland": "CH",
           "netherlands": "NL", "belgium": "BE", "luxembourg": "LU", "spain": "ES", "italy": "IT",
           "portugal": "PT", "greece": "GR"}
REQUIREMENTS = PROJECT_ROOT / "accuracy" / "inputs" / "field_requirements.json"
COMBINED = ("fy2025_runs_datapoints.csv", "all_runs_datapoints.csv")


def _country(v: str) -> str:
    v = (v or "").strip()
    return COUNTRY.get(v.lower(), v.upper()[:2])


def read_workbook(path: Path) -> list[dict]:
    """One dict per company (name + country); a company listed twice (another FY row)
    keeps its FY2025 row, with the other row's paths added."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    head = [str(h or "").strip() for h in rows[0]]

    def col(prefix):
        return next((i for i, h in enumerate(head) if h.lower().startswith(prefix)), None)
    ix = {"country": col("country"), "name": col("company name"), "id": col("company id"),
          "ar": col("gcs path annual"), "rem": col("gcs path remuneration"), "other": col("other"),
          "lei": col("lei"), "fy": col("fy")}
    out: dict[tuple, dict] = {}
    for r in rows[1:]:
        g = {k: (str(r[i]).strip() if i is not None and i < len(r) and r[i] is not None else "")
             for k, i in ix.items()}
        if not g["name"]:
            continue
        key = (g["name"].lower(), _country(g["country"]))
        g["country_code"] = key[1]
        if key not in out:
            out[key] = g
            continue
        keep = out[key]
        if g["fy"].upper() == "FY2025" and keep["fy"].upper() != "FY2025":
            g, keep = keep, g
            out[key] = keep
        for k in ("id", "lei", "ar", "rem", "other"):
            if g[k] and g[k] not in keep[k]:
                keep[k] = f"{keep[k]}\n{g[k]}".strip()
    return list(out.values())


def _paths(text: str) -> tuple[list[str], list[str]]:
    """(gs:// paths, staged '(not in GCS yet)' paths) in a cell."""
    gs, staged = [], []
    for part in re.split(r"[\n;]+", text or ""):
        part = part.strip()
        if part.startswith("gs://"):
            gs.append(part)
        elif part.lower().startswith("(not in gcs yet)"):
            staged.append(part)
    return gs, staged


def bucket_objects(region: str) -> set[str]:
    out = gcs._run(["ls", "-r", f"gs://{gcs.BUCKET}/{gcs.PREFIX}/{region}/**"])
    return {line.strip() for line in out.splitlines() if line.strip().startswith("gs://")}


def load_runs() -> dict[str, list[dict]]:
    """company_id -> its rows from the newest run that has it (by retrieved_at; the
    combined files win a tie)."""
    best: dict[str, tuple] = {}
    files = sorted(glob.glob(str(PROJECT_ROOT / "output" / "*_datapoints.csv")))
    for f in files:
        rank = 1 if Path(f).name in COMBINED else 0
        per = defaultdict(list)
        with open(f, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("company_id"):
                    per[r["company_id"]].append(r)
        for cid, rows in per.items():
            when = max((r.get("retrieved_at") or "")[:10] for r in rows)
            key = (when, rank)
            if cid not in best or key > best[cid][0]:
                best[cid] = (key, rows, Path(f).name)
    return {cid: (rows, name) for cid, (_, rows, name) in best.items()}


class RunMatcher:
    def __init__(self, runs: dict):
        self.ids = set(runs)
        self.by_lei, self.by_name, self.by_bare = defaultdict(set), defaultdict(set), defaultdict(set)
        # the newest run first when one company has two run ids (a validation id "T0539")
        self.when = {cid: max((r.get("retrieved_at") or "") for r in rows)
                     for cid, (rows, _) in runs.items()}
        for cid, (rows, _) in runs.items():
            r0 = rows[0]
            leis = {r["lei"].upper() for r in rows if r.get("lei")}
            leis |= {r["value"].upper() for r in rows if r.get("data_point") == "lei" and r.get("value")}
            for lei in leis:
                self.by_lei[lei].add(cid)
            self.by_name[f"{(r0.get('country') or '').upper()}|{strip_legal(r0.get('company_name') or '')}"].add(cid)
            self.by_bare[re.sub(r"-[0-9a-f]{8}$", "", cid)].add(cid)

    def newest(self, ids) -> str:
        return max(ids, key=lambda i: self.when.get(i, ""))

    def __call__(self, c: dict) -> tuple[str | None, str]:
        if c["lei"] and self.by_lei.get(c["lei"].upper()):
            return self.newest(self.by_lei[c["lei"].upper()]), "LEI"
        cid = c["id"].split("\n")[0]
        if cid in self.ids:
            return cid, "company id"
        bare = re.sub(r"-[0-9a-f]{8}$", "", cid)
        if cid and self.by_bare.get(bare):
            return self.newest(self.by_bare[bare]), "company id without suffix"
        for name in (c["name"], re.sub(r"\s+\d$", "", c["name"])):
            hits = self.by_name.get(f"{c['country_code']}|{strip_legal(name)}", set())
            if hits:
                return self.newest(hits), "name"
        return None, "no run found"


def requirements() -> dict[str, str]:
    try:
        return {f["d"]: f["req"] for f in json.loads(REQUIREMENTS.read_text(encoding="utf-8"))["fields"]}
    except (OSError, ValueError, KeyError):
        return {}


def is_required(requirement: str) -> bool:
    """'Required' and 'Required (one of headcount/fte)'; not the conditional ones
    ('Required if LTI plan exists', 'Required if aggregate line'), which are listed with
    the optional fields since the run can't tell whether the condition holds."""
    return requirement == "Required" or requirement.startswith("Required (one of")


def missing_values(rows: list[dict], req: dict[str, str]) -> list[dict]:
    """The company's real failures, pay fields once per field (roles listed)."""
    fails = [f for f in fl.failures(rows) if f["is_failure"] == "yes"]
    have = {r["data_point"] for r in rows if (r.get("value") or "").strip()}
    if have & {"headcount", "fte"}:
        fails = [f for f in fails if f["data_point"] not in ("headcount", "fte")]
    out: dict[tuple, dict] = {}
    for f in fails:
        key = (f["data_point"], f["failure_code"])
        if key in out:
            if f["role_row"] and f["role_row"] not in out[key]["roles"]:
                out[key]["roles"].append(f["role_row"])
            continue
        out[key] = {**f, "requirement": req.get(f["data_point"], "Optional"),
                    "roles": [f["role_row"]] if f["role_row"] else []}
    return list(out.values())


def build(workbook: Path, out: Path, sync: bool = True) -> dict:
    companies = read_workbook(workbook)
    region = "nordics"
    if companies:
        from_country = {c: r for r, cs in {"nordics": ("se", "no", "dk", "fi", "is"), "uk": ("gb",),
                        "dach": ("de", "at", "ch"), "benelux": ("nl", "be", "lu"),
                        "southern-europe": ("es", "it", "pt", "gr")}.items() for c in cs}
        region = Counter(from_country.get(c["country_code"].lower(), "nordics")
                         for c in companies).most_common(1)[0][0]
    objects = bucket_objects(region) if sync else set()
    folders = {o.split(f"/{gcs.PREFIX}/", 1)[1].split("/")[3] for o in objects
               if o.count("/") >= 7}
    bucket_ids = {f.split("--")[0]: f for f in folders}
    if sync:
        gcs.sync()
    gmatch = gcs.Matcher(gcs.records())
    runs = load_runs()
    rmatch = RunMatcher(runs)
    req = requirements()

    company_rows, value_rows = [], []
    for c in companies:
        ar, ar_staged = _paths(c["ar"])
        rem, rem_staged = _paths(c["rem"])
        other, other_staged = _paths(c["other"])
        listed = ar + rem + other
        absent = [p for p in listed if objects and p not in objects]
        cid = c["id"].split("\n")[0]
        folder = bucket_ids.get(cid)
        how = "company id" if folder else ""
        if not folder:
            rec, how2 = gmatch(company_id=cid, name=c["name"], country=c["country_code"], lei=c["lei"])
            if rec and rec["_folder"].split("/")[3] in folders:
                folder, how = rec["_folder"].split("/")[3], how2
                cid = cid or rec["company_id"]
        if folder:
            status = "In GCS"
        elif ar_staged or rem_staged or other_staged:
            status = "Staged, not in GCS yet"
        elif cid:
            status = "Has CDP id, no reports in GCS"
        else:
            status = "No CDP id, no reports"
        rem_note = "inside annual report" if "inside annual report" in c["rem"].lower() else ""
        run_id, run_how = rmatch(c)
        rows, run_file = runs[run_id] if run_id else ([], "")
        miss = missing_values(rows, req) if rows else []
        req_miss = sorted({m["data_point"] for m in miss if is_required(m["requirement"])})
        opt_miss = sorted({m["data_point"] for m in miss if not is_required(m["requirement"])})
        fy = next((r["value"] for r in rows if r["data_point"] == "fiscal_year" and r.get("value")), "")
        codes = Counter(m["failure_code"] for m in miss if is_required(m["requirement"]))
        company_rows.append({
            "Country": c["country_code"], "Company": c["name"], "Company ID": cid,
            "LEI": c["lei"], "GCS status": status, "Bucket folder": folder or "",
            "Annual report in GCS": "yes" if any(p in objects for p in ar) else ("staged" if ar_staged else "no"),
            "Remuneration report in GCS": "yes" if any(p in objects for p in rem) else (
                rem_note or ("staged" if rem_staged else "no")),
            "Listed paths missing in bucket": len(absent),
            "Run": "yes" if rows else "not run yet", "Run company id": run_id or "",
            "Run matched by": run_how if rows else "", "Run file": run_file,
            "Fiscal year read": fy,
            "Required values missing": len(req_miss), "Required fields missing": ", ".join(req_miss),
            "Main reasons (required)": ", ".join(f"{k} {v}" for k, v in codes.most_common(3)),
            "Optional / conditional values missing": len(opt_miss),
            "Optional / conditional fields missing": ", ".join(opt_miss),
        })
        for m in sorted(miss, key=lambda m: (not is_required(m["requirement"]), m["data_point"])):
            value_rows.append({
                "Country": c["country_code"], "Company": c["name"], "Company ID": cid,
                "GCS status": status, "Field": m["data_point"], "Requirement": m["requirement"],
                "Roles missing it": ", ".join(m["roles"]), "Failure code": m["failure_code"],
                "Failure": m["failure"], "Retry may help": m["retry_may_help"],
                "What to do": m["action"], "Sources checked": m["sources_checked"],
                "Note from the run": m["reason"][:500]})
    # one bucket folder claimed by two rows of the list: the same company listed twice
    seen = Counter(r["Bucket folder"] for r in company_rows if r["Bucket folder"])
    for r in company_rows:
        twin = [o["Company"] for o in company_rows
                if r["Bucket folder"] and o is not r and o["Bucket folder"] == r["Bucket folder"]]
        r["List note"] = f"same bucket folder as {', '.join(twin)}: listed twice?" if twin else ""
    del seen
    index_rows, index_summary = [], []
    if sync:
        index_rows, index_summary = index_sheet(region, company_rows)
    summary = _summary(company_rows, value_rows, workbook, region, len(folders)) + index_summary
    _write(out, summary, company_rows, value_rows, index_rows)
    return {"companies": len(company_rows), "summary": summary, "out": out}


def bucket_index(region: str) -> tuple[list[dict], dict]:
    """The bucket's own index.jsonl (the region's lines) and its manifest, read live."""
    lines = gcs._run(["cat", f"gs://{gcs.BUCKET}/{gcs.PREFIX}/index.jsonl"], timeout=180)
    manifest = json.loads(gcs._run(["cat", f"gs://{gcs.BUCKET}/{gcs.PREFIX}/index_manifest.json"], timeout=180))
    entries = [json.loads(l) for l in lines.splitlines() if l.strip()]
    return [e for e in entries if e.get("region") == region], manifest


def index_sheet(region: str, company_rows: list[dict]) -> tuple[list[dict], list[tuple]]:
    """One row per company in the bucket index, with its coverage and review reason (from
    its metadata.json), and the list row it belongs to. Also fills the index columns of
    the Companies sheet."""
    entries, manifest = bucket_index(region)
    gcs.sync(force=True)                      # review reasons and files as of now
    meta = {r["company_id"]: r for r in gcs.records()}
    by_folder = defaultdict(list)
    for r in company_rows:
        if r["Bucket folder"]:
            by_folder[r["Bucket folder"]].append(r)
    rows = []
    for e in sorted(entries, key=lambda e: (e["country"], e["name"].lower())):
        m = meta.get(e["company_id"], {})
        fy = e.get("latest_fiscal_year") or ""
        cov = (m.get("coverage") or {}).get(fy) or {}
        files = [f for f in m.get("files") or [] if f.get("fiscal_year") == fy and f.get("is_current")]
        review = m.get("needs_review") or {}
        reason = review.get("reason") or ""

        def where(kind):
            c = cov.get(kind) or {}
            return c.get("file") or c.get("covered_by") or ""
        folder = e["path"].rstrip("/").split("/")[-1]
        mine = by_folder.get(folder, [])
        for r in mine:
            r["Index: annual report"] = e["latest_coverage"]["annual-report"]
            r["Index: remuneration report"] = e["latest_coverage"]["remuneration-report"]
            r["Index: needs review"] = "yes" if e.get("needs_review") else "no"
            r["Index: review reason"] = reason
        rows.append({
            "Country": e["country"].upper(), "Company (index)": e["name"],
            "Company ID": e["company_id"], "Path": e["path"], "Tier": e.get("tier"),
            "Status": e.get("status"), "Fiscal year end": e.get("fiscal_year_end") or "",
            "Latest FY": fy,
            "Annual report": e["latest_coverage"]["annual-report"],
            "Annual report file": where("annual-report"),
            "Remuneration report": e["latest_coverage"]["remuneration-report"],
            "Remuneration file / covered by": where("remuneration-report"),
            "Current files in latest FY": len(files),
            "Needs review": "yes" if e.get("needs_review") else "no",
            "Review reason": reason,
            "Metadata updated": e.get("metadata_updated_at") or "",
            "In your list as": ", ".join(r["Company"] for r in mine) or "not in the list",
            "Run": "yes" if any(r["Run"] == "yes" for r in mine) else "not run yet",
            "Required values missing": max((r["Required values missing"] for r in mine), default=""),
        })
    for r in company_rows:
        for k in ("Index: annual report", "Index: remuneration report", "Index: needs review",
                  "Index: review reason"):
            r.setdefault(k, "")
    ar = Counter(r["Annual report"] for r in rows)
    rem = Counter(r["Remuneration report"] for r in rows)
    reasons = Counter(part.strip() for r in rows for part in r["Review reason"].split(";") if part.strip())
    summary = [("", ""), ("Bucket index (uploads/index.jsonl)", ""),
               ("  Built", f"{manifest.get('generated_at')} (schema {manifest.get('schema_version')})"),
               ("  All companies in the index", manifest.get("company_count")),
               (f"  {region} companies in the index", len(rows)),
               ("  Not in your list", sum(1 for r in rows if r["In your list as"] == "not in the list")),
               ("  Needs review", sum(1 for r in rows if r["Needs review"] == "yes"))]
    summary += [(f"  Annual report: {k}", v) for k, v in ar.most_common()]
    summary += [(f"  Remuneration report: {k}", v) for k, v in rem.most_common()]
    summary += [("  Review reasons", "")] + [(f"    {k}", v) for k, v in reasons.most_common(10)]
    return rows, summary


def _summary(cos: list[dict], vals: list[dict], workbook: Path, region: str, n_folders: int) -> list[tuple]:
    st = Counter(c["GCS status"] for c in cos)
    run = [c for c in cos if c["Run"] == "yes"]
    rows = [("Source", workbook.name), ("Companies in the list", len(cos)),
            (f"Company folders in the bucket ({region}), listed live", n_folders), ("", "")]
    rows += [("GCS status: " + k, v) for k, v in st.most_common()]
    rows += [("", ""), ("Companies run", len(run)), ("Companies not run yet", len(cos) - len(run)),
             ("Run companies with no required value missing",
              sum(1 for c in run if not c["Required values missing"])),
             ("Run companies missing a required value", sum(1 for c in run if c["Required values missing"])),
             ("Run, but an older fiscal year read",
              sum(1 for c in run if c["Fiscal year read"] and c["Fiscal year read"][:4] < "2025")),
             ("", ""), ("Required fields missing (company count)", "")]
    req_field = Counter(v["Field"] for v in vals if is_required(v["Requirement"]))
    rows += [(f"  {k}", v) for k, v in req_field.most_common()]
    rows += [("", ""), ("Missing values by failure code (required / all)", "")]
    by_code = Counter(v["Failure code"] for v in vals)
    by_code_req = Counter(v["Failure code"] for v in vals if is_required(v["Requirement"]))
    rows += [(f"  {k} ({fl.Failure(k).info.label})", f"{by_code_req[k]} / {n}") for k, n in by_code.most_common()]
    return rows


def _write(out: Path, summary, cos, vals, index_rows=None) -> None:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"
    for r in summary:
        ws.append(list(r))
    ws.column_dimensions["A"].width = 70
    ws.column_dimensions["B"].width = 30
    sheets = [("Companies", cos), ("Missing values", vals),
              ("Not in GCS", [c for c in cos if c["GCS status"] != "In GCS"])]
    if index_rows is not None:
        sheets.append(("Bucket index", index_rows))
    for title, rows in sheets:
        s = wb.create_sheet(title)
        if not rows:
            s.append(["(none)"])
            continue
        head = list(rows[0])
        s.append(head)
        for r in rows:
            s.append([r[h] for h in head])
        for i, h in enumerate(head, 1):
            s.cell(1, i).font = Font(bold=True, color="FFFFFF")
            s.cell(1, i).fill = PatternFill("solid", fgColor="1F3864")
            width = max(len(h), *(len(str(r[h])) for r in rows[:300]))
            s.column_dimensions[get_column_letter(i)].width = min(60, max(10, width + 2))
        s.freeze_panes = "C2"
        s.auto_filter.ref = s.dimensions
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.region_status",
                                description="Bucket status and missing values per company of a region list")
    p.add_argument("workbook", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--no-sync", action="store_true", help="Don't list the bucket (offline)")
    args = p.parse_args(argv)
    out = args.out or PROJECT_ROOT / "output" / f"{args.workbook.stem}_status.xlsx"
    try:
        res = build(args.workbook, out, sync=not args.no_sync)
    except (OSError, ValueError, gcs.GcsError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    for k, v in res["summary"]:
        if k:
            print(f"{k}: {v}")
    print(f"-> {res['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
