"""The Delivery pages' data (Dashboard/SPEC.md 6.4): where every FY2025 company stands.

Reads the pipeline tracker, every data-point run and its checks, the per-company run outputs
(runs, failures, Firecrawl credits) and the hand-kept CSVs in accuracy/inputs/delivery/, and
returns report.json["delivery"]. extractor.dashboard calls build() on every build and rerender.

    python -m extractor.delivery          prints the stage counts
"""

import csv
import datetime as dt
import glob
import json
import logging
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from .config import PROJECT_ROOT

log = logging.getLogger(__name__)

CONFIG = PROJECT_ROOT / "accuracy" / "inputs" / "delivery.json"
STAGES = ["Required", "Document found", "Extracted", "Required fields 100%",
          "Rules passed", "Spot-checked", "Done"]
PASS_WORDS = {"pass", "correct", "ok", "yes"}
NEXT_STEP = {
    "OpenAPI": "Open API: fetch company data",
    "Find Remuneration": "Find FY2025 remuneration report",
    "Find Annual reports": "Find FY2025 annual report",
}


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def day(s) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", str(s or ""))
    return m.group(1) if m else ""


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items() if k} for r in csv.DictReader(f)]


def files(globs: list[str]) -> list[Path]:
    seen, out = set(), []
    for g in globs:
        for f in sorted(glob.glob(str(PROJECT_ROOT / g))):
            p = Path(f).resolve()
            if p not in seen:
                seen.add(p)
                out.append(p)
    return out


def load_tracker(path: Path) -> list[dict]:
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = list(wb["Companies"].iter_rows(values_only=True))
    wb.close()
    head = [str(h or "").strip() for h in rows[0]]
    idx = {}
    for i, h in enumerate(head):
        if h and h not in ("Link", "Date") and h not in idx:
            idx[h] = i
    out = []
    for r in rows[1:]:
        if not r[0]:
            continue

        def g(k):
            v = r[idx[k]] if k in idx and idx[k] < len(r) else None
            return str(v).strip() if v is not None else ""
        m = re.search(r"Status:\s*([^;]+)", g("Remarks"))
        out.append({"id": slug(g("Company Name")), "name": g("Company Name"), "country": g("Country"),
                    "batch": g("Region") or "Unknown", "pipeline_run": g("Pipeline Run"),
                    "run_required": g("Run required"), "find_required": g("Find Required") or "NA",
                    "status": m.group(1).strip() if m else ""})
    return out


def build(config: Path = CONFIG) -> dict:
    """report.json["delivery"]; {"error": ...} when the config or tracker can't be read."""
    try:
        cfg = json.loads(config.read_text(encoding="utf-8"))
        src = cfg["sources"]
        tracker = load_tracker(PROJECT_ROOT / src["tracker"])
    except Exception as e:  # noqa: BLE001 - a missing tracker must never stop a run
        log.warning("Delivery pages skipped: %s", e)
        return {"error": f"Delivery data not built: {e}"}
    plan, fy = cfg["plan"], str(cfg.get("fiscal_year", "2025"))
    pass_line = plan["pass_line"]
    by_id = {c["id"]: c for c in tracker}
    inputs = PROJECT_ROOT / src["inputs_dir"]

    # extracted values: which data points have a value, and when each company was extracted
    present, extracted = defaultdict(set), {}
    for f in files(src["datapoints_globs"]):
        for r in read_csv(f):
            cid = r.get("company_id", "")
            if r.get("value"):
                present[cid].add(r.get("data_point", ""))
            d = day(r.get("retrieved_at"))
            if d and d > extracted.get(cid, ""):
                extracted[cid] = d

    # value status and failed checks (one row per value x check)
    fmap = cfg.get("failure_categories", {})
    cur = re.compile("|".join(map(re.escape, cfg.get("currency_reason_patterns", []))) or r"$^", re.I)
    vstatus, fails, examples = {}, defaultdict(Counter), defaultdict(dict)
    for f in files(src["checks_globs"]):
        for r in read_csv(f):
            cid = r.get("company_id", "")
            vstatus[(cid, r.get("data_point"), r.get("role_row", ""), r.get("value", ""))] = r.get("status", "")
            if r.get("outcome") == "fail":
                cat = fmap.get(r.get("check", "")) or ("Wrong currency" if cur.search(r.get("reason", ""))
                                                      else "Other rule failure")
                fails[cid][cat] += 1
                examples[cid].setdefault(cat, f'{r.get("data_point")}: {r.get("reason", "")} ({r.get("check")})')
    values = defaultdict(lambda: {"n": 0, "pass": 0, "review": 0, "fail": 0})
    for (cid, *_), st in vstatus.items():
        v = values[cid]
        v["n"] += 1
        v["pass" if st == "Pass" else "review" if st == "Review" else "fail"] += 1

    # per-company run outputs: runs, failures, credits, the fiscal year of the report read
    runs, last_run = [], {}
    for f in sorted((PROJECT_ROOT / src["run_outputs_dir"]).glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(d, dict) or "company_id" not in d:
            continue
        failed = f.name.endswith(".error.json")
        try:
            credits = float(d.get("firecrawl_credits_used") or 0)
        except (TypeError, ValueError):
            credits = 0.0
        run = {"id": d["company_id"], "name": d.get("input_name") or d.get("company_name") or d["company_id"],
               "date": day(d.get("extracted_at") or d.get("at")),
               "status": "failed" if failed else (d.get("status") or "unknown"),
               "error": f'{d.get("error_type", "")}: {str(d.get("error", ""))[:160]}' if failed else "",
               "credits": credits, "fy": str(d.get("fiscal_year") or "")}
        runs.append(run)
        if run["date"] >= last_run.get(run["id"], {}).get("date", ""):
            last_run[run["id"]] = run
    for cid, r in last_run.items():
        if r["status"] in ("ok", "needs_review") and r["date"]:
            extracted[cid] = max(extracted.get(cid, ""), r["date"])

    def old_year(r):
        return bool(r and re.fullmatch(r"\d{4}", r["fy"]) and int(r["fy"]) < int(fy))

    # spot-check sample
    spot_co = defaultdict(lambda: {"n": 0, "pass": 0, "last": ""})
    spot_batch = defaultdict(lambda: {"n": 0, "pass": 0, "last": ""})
    for r in read_csv(inputs / "spot_checks.csv"):
        cid = slug(r.get("company_id", ""))
        if not cid:
            continue
        b = r.get("batch") or by_id.get(cid, {}).get("batch", "Unknown")
        ok = r.get("result", "").lower() in PASS_WORDS
        for a in (spot_co[cid], spot_batch[b]):
            a["n"] += 1
            a["pass"] += ok
            a["last"] = max(a["last"], day(r.get("checked_on")))
    cleared_batch = {b: s["last"] for b, s in spot_batch.items() if s["n"] and s["pass"] / s["n"] >= pass_line}

    companies = []
    for c in tracker:
        if c["pipeline_run"] != "required":
            continue
        cid = c["id"]
        req = [f for grp, fl in cfg["required_fields"].items() if grp in c["run_required"] for f in fl]
        is_ex = cid in extracted
        missing = [f for f in req if f not in present.get(cid, set())] if is_ex else []
        v = values.get(cid, {"n": 0, "pass": 0, "review": 0, "fail": 0})
        cats, ex = dict(fails.get(cid, {})), dict(examples.get(cid, {}))
        if missing:
            cats["Missing field"] = cats.get("Missing field", 0) + len(missing)
            ex.setdefault("Missing field", "missing: " + ", ".join(missing))
        wrong = ""
        if c["status"].startswith("Wrong document: replace"):
            wrong = "Tracker: wrong document, to replace"
        elif old_year(last_run.get(cid)):
            wrong = f'Run read the FY{last_run[cid]["fy"]} report, not FY{fy}'
        if wrong:
            cats["Wrong document"] = cats.get("Wrong document", 0) + 1
            ex.setdefault("Wrong document", wrong)
        sc = spot_co.get(cid)
        if sc and sc["n"]:
            cleared, cleared_on = sc["pass"] == sc["n"], sc["last"]
        else:
            cleared, cleared_on = c["batch"] in cleared_batch, cleared_batch.get(c["batch"], "")
        flags = [True, c["find_required"] == "NA", is_ex, is_ex and not missing,
                 is_ex and v["n"] > 0 and v["fail"] == 0 and not wrong, cleared, cleared]
        stage = 0
        while stage + 1 < len(flags) and flags[stage + 1]:
            stage += 1
        companies.append({"id": cid, "o": c["name"], "c": c["country"], "b": c["batch"], "rr": c["run_required"],
                          "stage": stage, "ex": extracted.get(cid, ""),
                          "done": max(extracted.get(cid, ""), cleared_on) if stage == len(STAGES) - 1 else "",
                          "v": v, "spot": dict(sc) if sc else None, "fc": cats, "fx": ex})

    disc_over = {slug(r.get("company_id", "")): r for r in read_csv(inputs / "discovery.csv") if r.get("company_id")}
    discovery = []
    for c in tracker:
        if c["find_required"] == "NA":
            continue
        o = disc_over.get(c["id"], {})
        discovery.append({"id": c["id"], "o": c["name"], "c": c["country"], "b": c["batch"], "need": c["find_required"],
                          "next": o.get("next_step") or NEXT_STEP.get(c["find_required"], c["find_required"]),
                          "owner": o.get("owner", ""), "status": (o.get("status") or "open").lower(),
                          "updated": o.get("updated_on", ""), "note": o.get("note", "")})

    exc = {}

    def add(cid, c, cat, reason, source):
        exc.setdefault((cid, cat), {"id": cid, "o": c.get("name", cid), "c": c.get("country", ""),
                                    "b": c.get("batch", "Unknown"), "cat": cat, "reason": reason,
                                    "source": source, "accepted": "pending", "note": ""})
    for c in tracker:
        s = c["status"]
        if s.startswith("FY2025 not published"):
            add(c["id"], c, "No FY2025 report", "FY2025 report not published yet", "Tracker")
        elif s.startswith("Still to find"):
            need = c["find_required"] if c["find_required"] != "NA" else "document"
            add(c["id"], c, "Document missing", "Still to find: " + need, "Tracker")
        elif s.startswith("Wrong document: replace"):
            add(c["id"], c, "Wrong document", "Wrong document held; replacement needed", "Tracker")
    for cid, r in last_run.items():
        c = by_id.get(cid, {"name": r["name"]})
        if r["status"] == "not_found":
            add(cid, c, "Document missing", "Run found no FY2025 report", "Run " + r["date"])
        if old_year(r):
            add(cid, c, "Wrong document", f'Run read the FY{r["fy"]} report, not FY{fy}', "Run " + r["date"])
    for d in discovery:
        if d["status"] in ("not available", "not published"):
            add(d["id"], by_id[d["id"]], "No FY2025 report", d["note"] or "Discovery: document not available",
                "Discovery queue")
    for r in read_csv(inputs / "exceptions.csv"):
        cid = slug(r.get("company_id", ""))
        if not cid:
            continue
        cat = r.get("category") or "Other"
        add(cid, by_id.get(cid, {"name": r.get("company_id")}), cat, r.get("reason", ""), "Manual")
        e = exc[(cid, cat)]
        e["reason"] = r.get("reason") or e["reason"]
        e["accepted"] = (r.get("accepted") or "pending").lower()
        e["note"] = r.get("note", "")

    return {
        "built": dt.date.today().isoformat(),
        "fiscalYear": fy,
        "plan": {k: v for k, v in plan.items() if not k.startswith("_")},
        "stages": STAGES,
        "batches": [b["name"] for b in plan["batches"]],
        "companies": companies,
        "discovery": discovery,
        "exceptions": sorted(exc.values(), key=lambda e: (e["cat"], e["b"], e["o"])),
        "runs": runs,
        "scheduled": read_csv(inputs / "scheduled_runs.csv"),
        "spotByBatch": {b: dict(s) for b, s in spot_batch.items()},
        "firecrawl": {k: v for k, v in cfg.get("firecrawl", {}).items() if not k.startswith("_")},
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    d = build()
    if "error" in d:
        print(d["error"])
        return
    st = Counter(c["stage"] for c in d["companies"])
    for i, s in enumerate(d["stages"]):
        print(f"{s:<22} {sum(v for k, v in st.items() if k >= i):>5}")
    print(f'discovery {len(d["discovery"])}, exceptions {len(d["exceptions"])}, runs {len(d["runs"])}')


if __name__ == "__main__":
    main()
