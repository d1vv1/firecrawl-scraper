"""A spot-check sheet for a run: a sample of its companies, one line per value to compare
with the source by hand.

    python -m extractor.spot_check output/uk_remaining_datapoints.csv
        [--share 0.1] [--seed 1] [--skip sti,lti] [--out <run>_spot_check.csv]

The sample is a share of the run's companies (10%), drawn from every country in turn so
the countries are mixed. A third of it comes from the companies with the least pay data
(the fewest role values), since those fail most often. The same seed gives the same sample.

Each line has the value, its unit, year end and role, the link that opens the source at
the page, the quote, and the status the automatic checks gave it (from `<run>_checks.csv`
when it is there). The reviewer fills in `result` (Correct / Wrong / Missing / Not in
source) and, for a wrong value, `expected` and `comment`. Fields that do not apply or were
not asked for are left out; an empty field that was asked for is a line too.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

COLUMNS = ["company_id", "company_name", "country", "grain", "role_row", "data_point", "value",
           "unit", "period_end", "source", "endpoint", "note", "confidence", "checks",
           "result", "expected", "comment"]
RESULTS = "Correct / Wrong / Missing / Not in source"


def sample(rows: list[dict], share: float = 0.1, seed: int = 1) -> list[str]:
    """The company ids to check: `share` of the companies (at least one), every country in
    turn, a third of them from the companies with the fewest role values."""
    by_country: dict[str, list[str]] = defaultdict(list)
    pay: dict[str, int] = defaultdict(int)
    for r in rows:
        cid = r["company_id"]
        if cid not in by_country[r.get("country") or ""]:
            by_country[r.get("country") or ""].append(cid)
        pay[cid] += bool(r["grain"] == "role" and r["value"])
    ids = [c for cs in by_country.values() for c in cs]
    want = max(1, math.ceil(share * len(ids)))
    rng = random.Random(seed)
    least = sorted(ids, key=lambda c: (pay[c], c))[:max(1, len(ids) // 4)]
    picked = rng.sample(least, min(len(least), want // 3))
    pools = {k: rng.sample(v, len(v)) for k, v in sorted(by_country.items())}
    while len(picked) < want:
        for pool in pools.values():
            while pool and pool[-1] in picked:
                pool.pop()
            if pool and len(picked) < want:
                picked.append(pool.pop())
    return sorted(picked)


def sheet(rows: list[dict], ids: list[str], status: dict[tuple, str],
          skip: tuple[str, ...] = ()) -> list[dict]:
    """The lines to check for the sampled companies."""
    out = []
    for r in rows:
        note = r.get("note") or ""
        if r["company_id"] not in ids or any(r["data_point"].startswith(p) for p in skip):
            continue
        if not r["value"] and (note.startswith("not applicable") or note.startswith("not collected")):
            continue
        key = (r["company_id"], r["role_row"], r["data_point"])
        out.append({**{k: r.get(k, "") for k in COLUMNS}, "checks": status.get(key, ""),
                    "result": "", "expected": "", "comment": ""})
    return out


def read_status(checks: Path) -> dict[tuple, str]:
    """(company, role, field) -> the checks' status of the value ("Pass", "Fail (hard)")."""
    if not checks.exists():
        return {}
    with open(checks, encoding="utf-8-sig", newline="") as fh:
        return {(r["company_id"], r["role_row"], r["data_point"]): r["status"]
                for r in csv.DictReader(fh)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run", type=Path, help="a run's datapoints CSV")
    ap.add_argument("--share", type=float, default=0.1, help="share of the companies (0.1)")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--skip", default="", help="field name prefixes to leave out, e.g. sti,lti")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    with open(a.run, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    ids = sample(rows, a.share, a.seed)
    stem = a.run.with_suffix("")
    lines = sheet(rows, ids, read_status(Path(f"{stem}_checks.csv")),
                  tuple(p.strip() for p in a.skip.split(",") if p.strip()))
    out = a.out or Path(f"{stem}_spot_check.csv")
    with open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, COLUMNS)
        w.writeheader()
        w.writerows(lines)
    empty = sum(1 for r in lines if not r["value"])
    print(f"{len(ids)} of {len({r['company_id'] for r in rows})} companies, {len(lines)} lines "
          f"({empty} empty): {out}\nresult: {RESULTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
