"""Merge runs into one combined file, safely (several people, several machines).

    python -m extractor.combine output/run7_datapoints.csv [more runs ...]
        --into output/fy2025_runs_datapoints.csv [--no-dashboard]

For each company in a run, its rows replace that company's rows in the combined file (in
place; a new company goes at the end), with one exception: a row the run did not collect
("not collected: this run asked only for pay") never replaces a value already there. The
same is done for the checks (<name>_checks.csv): the run's checks replace the company's,
and a value kept from before keeps its checks.

Then the combined file is scored again (output_checks.rescore): every value under the
current rules, but a check whose source text is not cached on this machine keeps the result
saved in the checks file, so a run merged here from another machine keeps its quote checks.
"""

import argparse
import csv
import logging
import os
import sys
from collections import defaultdict
from pathlib import Path

from .datapoints import COLUMNS
from .fields import NOT_COLLECTED

log = logging.getLogger(__name__)

Key = tuple[str, str, str]          # (grain, role_row, data_point)


def read(path: Path) -> tuple[list[dict], list[str]]:
    rd = csv.DictReader(open(path, encoding="utf-8-sig"))
    return list(rd), list(rd.fieldnames or [])


def write(path: Path, rows: list[dict], cols: list[str]) -> None:
    """Through a temporary file; when the target is open elsewhere (Excel) and can't be
    replaced, written over in place."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    try:
        os.replace(tmp, path)
    except PermissionError:
        path.write_bytes(tmp.read_bytes())
        tmp.unlink()


def key(r: dict) -> Key:
    return r["grain"], r["role_row"], r["data_point"]


def merge_company(old: list[dict], new: list[dict]) -> tuple[list[dict], set[Key]]:
    """A company's rows after a run: the run's, except where the run did not collect a
    value the combined file has. Role rows go as a block: a run that collected no pay
    keeps the old role rows. Returns (rows, keys kept from before)."""
    before = {key(r): r for r in old}
    kept: set[Key] = set()
    out = []
    new_roles = [r for r in new if r["grain"] == "role"]
    roles_skipped = bool(new_roles) and all(r["note"].startswith(NOT_COLLECTED) for r in new_roles)
    for r in new:
        if r["grain"] == "role" and roles_skipped:
            continue
        o = before.get(key(r))
        if r["note"].startswith(NOT_COLLECTED) and o and o.get("value"):
            out.append(o)
            kept.add(key(r))
        else:
            out.append(r)
    if roles_skipped:
        old_roles = [r for r in old if r["grain"] == "role"]
        out += old_roles or new_roles
        kept |= {key(r) for r in old_roles}
    return out, kept


def splice(groups: dict[str, list[dict]], order: list[str], incoming: dict[str, list[dict]]) -> list[dict]:
    """Every company's rows in the combined file's order, new companies at the end."""
    out = []
    for cid in order + [c for c in incoming if c not in groups]:
        out += incoming.get(cid, groups.get(cid, []))
    return out


def combine(runs: list[Path], into: Path) -> dict:
    """Merge the runs (in order) into `into`, and their checks into its checks file."""
    rows, cols = read(into) if into.exists() else ([], COLUMNS)
    checks_path = into.with_name(into.stem + "_checks.csv")
    checks, ccols = read(checks_path) if checks_path.exists() else ([], [])
    stats = {"replaced": 0, "added": 0, "kept": 0}
    for run in runs:
        groups, order = defaultdict(list), []
        for r in rows:
            if r["company_id"] not in groups:
                order.append(r["company_id"])
            groups[r["company_id"]].append(r)
        cgroups = defaultdict(list)
        for c in checks:
            cgroups[c["company_id"]].append(c)
        new_rows, _ = read(run)
        new_by = defaultdict(list)
        for r in new_rows:
            new_by[r["company_id"]].append(r)
        run_checks_path = run.with_name(run.stem + "_checks.csv")
        run_checks, rcols = read(run_checks_path) if run_checks_path.exists() else ([], [])
        ccols = ccols or rcols
        run_cby = defaultdict(list)
        for c in run_checks:
            run_cby[c["company_id"]].append(c)
        merged, merged_checks = {}, {}
        for cid, new in new_by.items():
            merged[cid], kept = merge_company(groups.get(cid, []), new)
            stats["replaced" if cid in groups else "added"] += 1
            stats["kept"] += len(kept)
            old_checks = [c for c in cgroups.get(cid, [])
                          if ("role" if c["role_row"] else "company", c["role_row"], c["data_point"]) in kept]
            merged_checks[cid] = run_cby.get(cid, []) + old_checks
        rows = splice(groups, order, merged)
        if ccols:
            corder = list(dict.fromkeys(c["company_id"] for c in checks))
            checks = splice(cgroups, corder, merged_checks)
        log.info("Merged %s: %d companies replaced, %d added", run.name, stats["replaced"], stats["added"])
    write(into, rows, cols)
    if ccols:
        write(checks_path, checks, ccols)
    return stats


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.combine", description=__doc__.split("\n\n")[0])
    p.add_argument("runs", nargs="+", type=Path, help="Run CSVs (<name>_datapoints.csv), merged in order")
    p.add_argument("--into", type=Path, required=True, help="The combined CSV (created if missing)")
    p.add_argument("--no-dashboard", action="store_true",
                   help="Don't score the combined file again or rebuild the dashboard")
    args = p.parse_args(argv)
    missing = [r for r in args.runs if not r.exists()]
    if missing:
        print(f"ERROR: not found: {', '.join(map(str, missing))}", file=sys.stderr)
        return 1
    stats = combine(args.runs, args.into)
    print(f"{args.into}: {stats['replaced']} companies replaced, {stats['added']} added, "
          f"{stats['kept']} values kept that the runs did not collect")
    if not args.no_dashboard:
        from . import dashboard
        print(f"Scored again, dashboard: {dashboard.build(args.into, rescore=True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
