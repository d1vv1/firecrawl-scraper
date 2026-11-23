"""Merge runs into one combined file, safely (several people, several machines).

    python -m extractor.combine output/run7_datapoints.csv [more runs ...]
        --into output/fy2025_runs_datapoints.csv [--no-dashboard]

For each company in a run, its rows replace that company's rows in the combined file (in
place; a new company goes at the end), with one exception: a row the run did not collect
("not collected: this run asked only for pay") never replaces a value already there. The
same is done for the checks (<name>_checks.csv): the run's checks replace the company's,
and a value kept from before keeps its checks. And a run that got under half the values
already there for a company's facts or its pay (a site that blocked the run) leaves that
block as it was, unless --take-newer.

Then the combined file is scored again (output_checks.rescore): every value under the
current rules, but a check whose source text is not cached on this machine keeps the result
saved in the checks file, so a run merged here from another machine keeps its quote checks.

Every company's rows are also put under the current rules for saved rows
(datapoints.refresh: a "Total" line taken for a role, an owner's name where there is no
controlling owner, ...), so a rule added after a run reaches the companies whose caches
are on another machine. With no run given, only that and the scoring are done.
"""

import argparse
import csv
import logging
import os
import sys
from collections import defaultdict
from pathlib import Path

from . import fields
from .datapoints import COLUMNS, refresh
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


# A run whose block (the company's facts, or its pay) has under half the values of the block
# already in the combined file is taken for a failed run (ABB's site answered 503 in DACH
# Set 2: 3 pay values instead of 118), and the old block stays. Not for small blocks.
WORSE_SHARE = 0.5
WORSE_MIN_VALUES = 5


def filled(rows: list[dict]) -> int:
    return sum(1 for r in rows if r.get("value", "").strip())


def pay_fields_asked(old: list[dict], new: list[dict]) -> set[str] | None:
    """The pay fields a run for some pay fields asked for, or None when it asked for all
    pay (or none). Read from its "not collected: this run asked only for benefits_value,
    pension_contribution" rows: such a run writes pay rows for those fields only."""
    labels = {r["note"][len(NOT_COLLECTED):] for r in new if r["note"].startswith(NOT_COLLECTED)}
    if len(labels) != 1:
        return None
    try:
        asked = fields.parse(labels.pop())
    except ValueError:
        return None
    pay = set(fields.GROUPS["pay"])
    if asked is None or pay <= asked:
        return None
    return set(asked & pay) or None


def worse_blocks(old: list[dict], new: list[dict]) -> set[str]:
    """The grains ("company", "role") where the run has clearly fewer values than before.
    Company facts: compared on the fields the run collected (a pay-only run's "not
    collected" rows are kept from before anyway). Pay: the whole block (role names change
    between runs: "CEO", "Vorstand")."""
    out = set()
    collected = {key(r) for r in new if r["grain"] == "company" and not r["note"].startswith(NOT_COLLECTED)}
    asked = pay_fields_asked(old, new)
    for grain in ("company", "role"):
        if grain == "company":
            o = filled([r for r in old if r["grain"] == grain and key(r) in collected])
        else:
            # a run for some pay fields is compared on those fields only
            o = filled([r for r in old if r["grain"] == grain
                        and (asked is None or r["data_point"] in asked)])
        n = filled([r for r in new if r["grain"] == grain])
        if o >= WORSE_MIN_VALUES and n < WORSE_SHARE * o:
            out.add(grain)
    return out


def merge_company(old: list[dict], new: list[dict], keep_better: bool = True
                  ) -> tuple[list[dict], set[Key]]:
    """A company's rows after a run: the run's, except where the run did not collect a
    value the combined file has. Role rows go as a block: a run that collected no pay
    keeps the old role rows. With `keep_better`, a block where the run has under half the
    old values (worse_blocks) stays as it was. Returns (rows, keys kept from before)."""
    worse = worse_blocks(old, new) if keep_better else set()
    if worse:
        new = ([r for r in new if r["grain"] not in worse]
               + [r for r in old if r["grain"] in worse])
        kept_worse = {key(r) for r in old if r["grain"] in worse}
    else:
        kept_worse = set()
    before = {key(r): r for r in old}
    kept: set[Key] = set(kept_worse)
    out = []
    new_roles = [r for r in new if r["grain"] == "role"]
    roles_skipped = bool(new_roles) and all(r["note"].startswith(NOT_COLLECTED) for r in new_roles)
    old_roles = [r for r in old if r["grain"] == "role"]
    if ("role" not in kept_worse_grains(kept_worse) and old_roles and not roles_skipped
            and pay_fields_asked(old, new) is not None):
        # a run for some pay fields: the old pay rows stay, and the run fills their empty fields
        roles, filled_keys = fill_roles(old_roles, new_roles)
        rest, kept_rest = merge_company([r for r in old if r["grain"] != "role"],
                                        [r for r in new if r["grain"] != "role"], keep_better)
        return rest + roles, kept_rest | ({key(r) for r in old_roles} - filled_keys)
    for r in new:
        if key(r) in kept_worse:
            out.append(r)
            continue
        if r["grain"] == "role" and roles_skipped:
            continue
        o = before.get(key(r))
        # a value entered by hand (manual_prices) stays unless the run read one itself
        if o and o.get("value") and (r["note"].startswith(NOT_COLLECTED)
                                     or (o.get("method") == "MANUAL" and not r["value"])):
            out.append(o)
            kept.add(key(r))
        else:
            out.append(r)
    if roles_skipped:
        out += old_roles or new_roles
        kept |= {key(r) for r in old_roles}
    return out, kept


def kept_worse_grains(kept_worse: set[Key]) -> set[str]:
    return {k[0] for k in kept_worse}


def fill_roles(old_roles: list[dict], new_roles: list[dict]) -> tuple[list[dict], set[Key]]:
    """The old pay rows, with the run's values for the fields it collected where the old row
    is empty. A role the old rows don't have is left out (role names change between runs:
    "CEO", "Chief Executive Officer"), as is a value the old row already has. Returns
    (rows, keys filled from the run)."""
    have = {r["role_row"] for r in old_roles}
    fill = {key(r): r for r in new_roles
            if r.get("value", "").strip() and not r["note"].startswith(NOT_COLLECTED)
            and r["role_row"] in have}
    out, done = [], set()
    for r in old_roles:
        n = fill.get(key(r))
        if n and not r.get("value", "").strip():
            out.append(n)
            done.add(key(r))
        else:
            out.append(r)
    added = [n for k, n in fill.items() if k not in done and k not in {key(r) for r in old_roles}]
    for n in added:                       # a field the old role had no row for: next to its role
        at = max(i for i, r in enumerate(out) if r["role_row"] == n["role_row"]) + 1
        out.insert(at, n)
        done.add(key(n))
    return out, done


def splice(groups: dict[str, list[dict]], order: list[str], incoming: dict[str, list[dict]]) -> list[dict]:
    """Every company's rows in the combined file's order, new companies at the end."""
    out = []
    for cid in order + [c for c in incoming if c not in groups]:
        out += incoming.get(cid, groups.get(cid, []))
    return out


def combine(runs: list[Path], into: Path, keep_better: bool = True, gleif: bool = False,
            esef: bool = False) -> dict:
    """Merge the runs (in order) into `into`, and their checks into its checks file.
    `keep_better`: a block a run got clearly fewer values for stays (merge_company).
    `gleif`: ask GLEIF level 2 again for every empty ultimate parent (datapoints.refresh).
    `esef`: fill an empty EBITDA, share count or ultimate parent from the ESEF filing's tags."""
    rows, cols = read(into) if into.exists() else ([], COLUMNS)
    checks_path = into.with_name(into.stem + "_checks.csv")
    checks, ccols = read(checks_path) if checks_path.exists() else ([], [])
    stats = {"replaced": 0, "added": 0, "kept": 0, "worse": []}
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
            worse = worse_blocks(groups.get(cid, []), new) if keep_better else set()
            if worse:
                name = new[0].get("company_name") or cid
                stats["worse"].append(f"{name} ({', '.join(sorted(worse))})")
                log.warning("%s: the run has under half the values before for %s; kept the old rows "
                            "(--take-newer to replace them)", name, " and ".join(sorted(worse)))
            merged[cid], kept = merge_company(groups.get(cid, []), new, keep_better)
            stats["replaced" if cid in groups else "added"] += 1
            stats["kept"] += len(kept)
            def ckey(c):
                return "role" if c["role_row"] else "company", c["role_row"], c["data_point"]
            old_checks = [c for c in cgroups.get(cid, []) if ckey(c) in kept]
            run_own = [c for c in run_cby.get(cid, []) if ckey(c) not in kept and ckey(c)[0] not in worse]
            merged_checks[cid] = run_own + old_checks
        rows = splice(groups, order, merged)
        if ccols:
            corder = list(dict.fromkeys(c["company_id"] for c in checks))
            checks = splice(cgroups, corder, merged_checks)
        log.info("Merged %s: %d companies replaced, %d added", run.name, stats["replaced"], stats["added"])
    rows = refreshed(rows, gleif, esef)
    write(into, rows, cols)
    if ccols:
        write(checks_path, checks, ccols)
    return stats


def refreshed(rows: list[dict], gleif: bool = False, esef: bool = False) -> list[dict]:
    """Every company's rows under the current rules for saved rows, in the same order.
    `gleif`: an empty ultimate parent is asked of GLEIF again (online, cached a week)."""
    from .apis import gleif_parent
    from .esef import extras_for
    lookup = gleif_parent if gleif else None
    extras = extras_for if esef else None
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        groups[r["company_id"]].append(r)
    return [r for block in groups.values() for r in refresh(block, lookup, extras)]


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m extractor.combine", description=__doc__.split("\n\n")[0])
    p.add_argument("runs", nargs="*", type=Path,
                   help="Run CSVs (<name>_datapoints.csv), merged in order; none: only apply the "
                        "current rules to the combined file and score it again")
    p.add_argument("--into", type=Path, required=True, help="The combined CSV (created if missing)")
    p.add_argument("--no-dashboard", action="store_true",
                   help="Don't score the combined file again or rebuild the dashboard")
    p.add_argument("--take-newer", action="store_true",
                   help="Replace a company's facts or pay even when the run has under half "
                        "the values already there (default: the old block stays)")
    p.add_argument("--gleif", action="store_true",
                   help="Ask GLEIF level 2 again for every empty ultimate parent (a parent added "
                        "since, or a reporting exception that gives one)")
    p.add_argument("--esef", action="store_true",
                   help="Fill an empty EBITDA (else operating profit), share count or ultimate "
                        "parent from the tags of the ESEF filing for the fiscal year (online)")
    args = p.parse_args(argv)
    missing = [r for r in args.runs if not r.exists()]
    if missing:
        print(f"ERROR: not found: {', '.join(map(str, missing))}", file=sys.stderr)
        return 1
    stats = combine(args.runs, args.into, keep_better=not args.take_newer, gleif=args.gleif,
                    esef=args.esef)
    print(f"{args.into}: {stats['replaced']} companies replaced, {stats['added']} added, "
          f"{stats['kept']} values kept that the runs did not collect")
    if stats["worse"]:
        print(f"Kept the old rows where the run got under half the values: {'; '.join(stats['worse'])}")
    if not args.no_dashboard:
        from . import dashboard
        print(f"Scored again, dashboard: {dashboard.build(args.into, rescore=True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
