"""A targeted re-run input for one batch of the FY2025 re-run queue.

    python -m extractor.rerun_list Nordics
        [--queue FY2025_rerun_queue_2026-11-14.csv] [--out data/rerun_nordics.csv]

Reads the queue (one row per company and missing field, made from the dashboard's
not-found analysis) and writes one row per company in the batch, ready for

    python -m extractor.datapoints data/rerun_nordics.csv

Its `fields` column lists only the fields that company still needs: "all" for a first run
or a full re-run (wrong-year report), "pay" when all pay is missing, else the field names.
The collector reads that column per company (fields.py): it looks only for those fields
and replaces only them in the saved rows, and `combine` never lets a "not collected" row
replace a value, so a company run on another machine keeps its other values on merge.

Report links come first from the CDP bucket (gcs.py): a company found there gets the gs://
link of its FY2025 annual and remuneration report, so no search is needed (`--no-bucket`
skips it). Without a bucket file, the tracker's link is kept.

`company_id` is the id the company has in the earlier runs (output/*_datapoints.csv), so
the new rows merge onto the old ones; a company never run gets its tracker id. Report
links, website and run_required come from the pipeline tracker. `before_run` says what
must be done by hand first (find a document, replace a wrong-year report).
"""

import argparse
import csv
import glob
import sys
from collections import defaultdict
from pathlib import Path

from . import fields as selection
from . import gcs
from .config import PROJECT_ROOT
from .delivery import IdMap, slug

TRACKER = PROJECT_ROOT.parent / "Excel_Documents" / "FY2025_Company_Pipeline_Tracker.xlsx"
QUEUE = PROJECT_ROOT / "FY2025_rerun_queue_2026-11-14.csv"
COLUMNS = ["company_id", "company_name", "country", "lei", "isin", "website",
           "annual_report_url", "remuneration_report_url", "run_required", "fields",
           "field_count", "buckets", "before_run", "tracker_id", "bucket_company_id", "bucket_match"]


def read_tracker(path: Path) -> dict[str, dict]:
    """Tracker id -> name, ISIN, LEI, run required, website and report links. The sheet
    repeats "Link" and "Date": each Link belongs to the file column before it."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = list(wb["Companies"].iter_rows(values_only=True))
    wb.close()
    head = [str(h or "").strip() for h in rows[0]]

    def at(name, offset=0):
        return head.index(name) + offset if name in head else None
    cols = {"name": at("Company Name"), "isin": at("ISIN"), "lei": at("LEI"),
            "run_required": at("Run required"), "website": at("Company URL"),
            "rem": at("Remuneration Files", 1), "ar": at("Annual Link"),
            "extra_type": at("Additional Files_1"), "extra": at("Additional Files_1", 1)}
    out = {}
    for r in rows[1:]:
        if not r or not r[0]:
            continue
        g = {k: (str(r[i]).strip() if i is not None and i < len(r) and r[i] is not None else "")
             for k, i in cols.items()}
        kind = g["extra_type"].lower()
        if g["extra"].startswith("http"):
            if "remuneration" in kind and not g["rem"].startswith("http"):
                g["rem"] = g["extra"]
            elif "annual" in kind and not g["ar"].startswith("http"):
                g["ar"] = g["extra"]
        out[slug(g["name"])] = g
    return out


def run_ids(tracker_ids: list[dict]) -> dict[str, dict]:
    """Tracker id -> the company's id, name and LEI in the earlier runs. Two run ids for
    one company (a validation id "T0123" and a named one): the named one, the newer run."""
    imap = IdMap(tracker_ids)
    found: dict[str, dict] = defaultdict(dict)
    for f in sorted(glob.glob(str(PROJECT_ROOT / "output" / "*_datapoints.csv"))):
        with open(f, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                cid = r.get("company_id") or ""
                if not cid:
                    continue
                tid = imap(cid, r.get("company_name") or "")
                info = found[tid].setdefault(cid, {"name": r.get("company_name") or "",
                                                   "lei": "", "isin": "", "website": ""})
                if r.get("lei") and not info["lei"]:
                    info["lei"] = r["lei"]
                if r.get("data_point") in ("isin", "website") and r.get("value") \
                        and not info[r["data_point"]]:
                    info[r["data_point"]] = r["value"].split(";")[0].split(",")[0].strip()
    out = {}
    for tid, by_id in found.items():
        cid = sorted(by_id, key=lambda c: (c.startswith("T0") and c[2:].isdigit(), c))[0]
        out[tid] = {"id": cid, **by_id[cid]}
    return out


def fields_for(rows: list[dict]) -> str:
    """The queue's fields for one company -> the collector's fields value."""
    names = {r["field"] for r in rows}
    if "ALL in scope" in names:
        return "all"
    out = ["pay"] if "ALL pay fields" in names else []
    out += sorted(n for n in names if n != "ALL pay fields")
    selection.parse(",".join(out))           # an unknown name fails here, not in the run
    return ",".join(out)


def before_run(rows: list[dict], has_website: bool, bucket_report: bool = False) -> str:
    notes = []
    buckets = " ".join(r["bucket"] for r in rows)
    if bucket_report:
        if "B1" in buckets:
            notes.append("the FY2025 report is in the bucket: run it with --redo")
        return "; ".join(notes)
    if "A2" in buckets:
        notes.append("find the FY2025 documents first (tracker: "
                     + next(r["reason"] for r in rows if r["bucket"].startswith("A2"))
                     .replace("to find: ", "") + ")")
    if "B1" in buckets:
        year = next(r["reason"] for r in rows if r["bucket"].startswith("B1"))
        notes.append(f"{year}: put the FY2025 report link in annual_report_url, "
                     "then run it with --redo")
    if not has_website and any("WebsiteNotFoundError" in r["reason"] for r in rows):
        notes.append("no website found last time: fill in website")
    return "; ".join(notes)


def build(batch: str, queue: Path, out: Path, tracker_path: Path = TRACKER,
          bucket: bool = True) -> list[dict]:
    with open(queue, encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["batch"].lower() == batch.lower()]
    if not rows:
        raise ValueError(f"no rows for batch {batch!r} in {queue}")
    tracker = read_tracker(tracker_path)
    runs = run_ids([{"id": t, "name": g["name"]} for t, g in tracker.items()])
    match = None
    if bucket:
        gcs.sync()
        match = gcs.Matcher(gcs.records())
    per = defaultdict(list)
    for r in rows:
        per[r["company_id"]].append(r)
    out_rows = []
    for tid, rs in per.items():
        t, run = tracker.get(tid, {}), runs.get(tid, {})
        website = t.get("website") or run.get("website", "")
        if website and not website.startswith("http"):
            website = "https://" + website
        f = fields_for(rs)
        isin = t.get("isin") or run.get("isin", "")
        lei = run.get("lei") or t.get("lei", "")
        rec, how = (match(run.get("id") or tid, run.get("name") or t.get("name") or rs[0]["company"],
                          rs[0]["country"], isin, lei, tid) if match else (None, "bucket not used"))
        docs = gcs.documents(rec) if rec else {"annual": None, "remuneration": None}
        ar = docs["annual"] or (t.get("ar", "") if t.get("ar", "").startswith("http") else "")
        rem = docs["remuneration"] or (t.get("rem", "") if t.get("rem", "").startswith("http") else "")
        out_rows.append({
            "company_id": run.get("id") or tid,
            "company_name": run.get("name") or t.get("name") or rs[0]["company"],
            "country": rs[0]["country"],
            "lei": lei,
            "isin": isin,
            "website": website,
            "annual_report_url": ar,
            "remuneration_report_url": rem,
            "run_required": t.get("run_required") or rs[0]["scope"],
            "fields": f,
            "field_count": "" if f in ("all", "pay") else len(f.split(",")),
            "buckets": "; ".join(sorted({r["bucket"] for r in rs})),
            "before_run": before_run(rs, bool(website), bool(docs["annual"])),
            "tracker_id": tid,
            "bucket_company_id": rec["company_id"] if rec else "",
            "bucket_match": (how + ": " + ", ".join(k for k, v in docs.items() if v)) if rec else how,
        })
    out_rows.sort(key=lambda r: (r["fields"] != "all", r["country"], r["company_name"].lower()))
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(out_rows)
    return out_rows


# A missing value a re-run can't change: the report states it in another form.
NOT_RERUN = {"STATED_IN_OTHER_FORM"}


def from_region_list(workbook: Path, out: Path, bucket: bool = True) -> list[dict]:
    """Targeted re-run input for the companies of a region list that have been run: per
    company, the fields its newest run did not find (region_status), under its run id so
    the new values merge onto the old ones. A company whose run read an older report than
    last year's gets "all" (a full re-run, --redo for one saved on this machine)."""
    from . import failures as fl
    from . import region_status as rs
    companies = rs.read_workbook(workbook)
    runs = rs.load_runs()
    rmatch = rs.RunMatcher(runs)
    req = rs.requirements()
    match = None
    if bucket:
        gcs.sync()
        match = gcs.Matcher(gcs.records())
    out_rows, seen = [], set()
    for c in companies:
        run_id, _ = rmatch(c)
        if not run_id or run_id in seen:
            continue
        seen.add(run_id)
        rows, _ = runs[run_id]
        miss = rs.missing_values(rows, req)
        codes = {m["failure_code"] for m in miss}
        # the old-report flag sits on fiscal_year, which has a value: not a field to re-run
        names = sorted({m["data_point"] for m in miss
                        if m["failure_code"] not in NOT_RERUN | {"WRONG_YEAR_REPORT"}})
        wrong_year = "WRONG_YEAR_REPORT" in codes
        if not names and not wrong_year:
            continue
        fields = "all" if wrong_year else ",".join(names)
        selection.parse(fields)
        value = {r["data_point"]: r["value"] for r in rows if r.get("grain") == "company" and r.get("value")}
        cid = c["id"].split("\n")[0]
        rec, how = (match(company_id=cid, name=c["name"], country=c["country_code"], lei=c["lei"])
                    if match else (None, "bucket not used"))
        docs = gcs.documents(rec) if rec else {"annual": None, "remuneration": None}
        website = value.get("website", "")
        out_rows.append({
            "company_id": run_id, "company_name": rows[0].get("company_name") or c["name"],
            "country": c["country_code"],
            "lei": value.get("lei") or rows[0].get("lei") or c["lei"],
            "isin": (value.get("isin") or "").split(";")[0].split(",")[0].strip(),
            "website": website if not website or website.startswith("http") else f"https://{website}",
            "annual_report_url": docs["annual"] or "", "remuneration_report_url": docs["remuneration"] or "",
            "run_required": "", "fields": fields,
            "field_count": "" if fields == "all" else len(fields.split(",")),
            "buckets": "; ".join(sorted(codes - {"WRONG_YEAR_REPORT"})),
            "before_run": "run read an older report than FY2025: full re-run (--redo if saved here)"
                          if wrong_year else "",
            "tracker_id": cid, "bucket_company_id": rec["company_id"] if rec else "",
            "bucket_match": (how + ": " + ", ".join(k for k, v in docs.items() if v)) if rec else how,
        })
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(out_rows)
    return out_rows


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.rerun_list",
                                description="Targeted re-run input for one batch of the re-run queue, "
                                            "or for the run companies of a region list")
    p.add_argument("batch", nargs="?", help="Batch (region) in the queue: Nordics, UK, DACH, Benelux, ...")
    p.add_argument("--region-list", type=Path,
                   help="A region's company workbook (Nordics_Companies_Reports_FY2025.xlsx): re-run "
                        "the fields its run companies did not find")
    p.add_argument("--queue", type=Path, default=QUEUE)
    p.add_argument("--out", type=Path)
    p.add_argument("--tracker", type=Path, default=TRACKER)
    p.add_argument("--no-bucket", action="store_true", help="Don't take report links from the CDP bucket")
    args = p.parse_args(argv)
    if args.region_list:
        region = args.region_list.stem.split("_")[0].lower()
        out = args.out or PROJECT_ROOT / "data" / f"rerun_{region}_run_companies.csv"
        try:
            rows = from_region_list(args.region_list, out, bucket=not args.no_bucket)
        except (OSError, ValueError, KeyError, gcs.GcsError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        full = sum(r["fields"] == "all" for r in rows)
        print(f"{len(rows)} run companies with fields to re-run: {full} full (older report), "
              f"{len(rows) - full} targeted; bucket report links for "
              f"{sum(1 for r in rows if r['annual_report_url'])} -> {out}")
        return 0
    if not args.batch:
        p.error("give a batch or --region-list")
    out = args.out or PROJECT_ROOT / "data" / f"rerun_{slug(args.batch).replace('-', '_')}.csv"
    try:
        rows = build(args.batch, args.queue, out, args.tracker, bucket=not args.no_bucket)
    except (OSError, ValueError, KeyError, gcs.GcsError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    full = sum(r["fields"] == "all" for r in rows)
    in_bucket = sum(1 for r in rows if r["bucket_company_id"])
    with_ar = sum(1 for r in rows if r["annual_report_url"].startswith("gs://"))
    with_rem = sum(1 for r in rows if r["remuneration_report_url"].startswith("gs://"))
    print(f"CDP bucket: {in_bucket} companies found; annual report from it for {with_ar}, "
          f"remuneration report for {with_rem}")
    print(f"{len(rows)} companies: {full} full runs, {len(rows) - full} targeted -> {out}")
    todo = [r for r in rows if r["before_run"]]
    if todo:
        print(f"{len(todo)} need something done by hand first (before_run column)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
