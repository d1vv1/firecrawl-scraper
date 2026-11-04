"""Compare an engine run with the v1 report baseline, cell by cell.

python accuracy/tests/diff_baseline.py   -> prints differences, exit 1 if any
"""
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from engine import scoring as E  # noqa: E402

EXPECTED = {"values": 2584,
            "status": {"Pass": 683, "Review": 493, "Fail": 8, "Fail (hard)": 404, "Incomplete": 996},
            "gates": {"PASS": 15311, "FAIL": 1287, "NOT RUN": 2433}, "hard_fail": 438}


def run():
    rows = E.load_tracker(os.path.join(ROOT, "inputs", "tracker_first50.csv"))
    reg = E.load_register(os.path.join(ROOT, "inputs", "field_register.json"))
    return rows, reg, E.score_tracker(rows, reg)


def main():
    rows, reg, scored = run()
    t = json.load(open(os.path.join(HERE, "baseline", "v1_targets.json"), encoding="utf-8"))
    diffs = []
    s = E.summarise(scored)
    for k in ("values", "hard_fail"):
        if s[k] != EXPECTED[k]:
            diffs.append("%s: got %s want %s" % (k, s[k], EXPECTED[k]))
    for grp in ("status", "gates"):
        for k, want in EXPECTED[grp].items():
            if s[grp].get(k, 0) != want:
                diffs.append("%s %s: got %s want %s" % (grp, k, s[grp].get(k, 0), want))

    bc = defaultdict(lambda: [0, 0, 0])
    bf = defaultdict(lambda: [0, 0, 0])
    co = defaultdict(lambda: defaultdict(int))
    for x in scored:
        r = x["row"]
        if not x["result"]:
            co[r["company_id"]]["blank"] += 1
            continue
        key = {"Pass": "pass", "Review": "review", "Fail": "fail", "Fail (hard)": "hard", "Incomplete": "inc"}
        co[r["company_id"]][key[x["result"]["status"]]] += 1
        co[r["company_id"]]["n"] += 1
        for g in x["gates"]:
            for tab, k in ((bc, (r["country"], g["gate"])), (bf, (r["country"], r["data_point"]))):
                tab[k][0] += 1
                tab[k][1] += g["result"] == E.FAIL
                tab[k][2] += g["result"] == E.NOT_RUN
    for c, g, a, f, n in t["byCheck"]:
        if bc[(c, g)] != [a, f, n]:
            diffs.append("byCheck %s %s: got %s want %s" % (c, g, bc[(c, g)], [a, f, n]))
    for c, d, _, _, a, f, n in t["byField"]:
        if bf[(c, d)] != [a, f, n]:
            diffs.append("byField %s %s: got %s want %s" % (c, d, bf[(c, d)], [a, f, n]))
    for cs in t["companySummary"]:
        got = co[cs["cid"]]
        for k in ("n", "pass", "review", "fail", "hard", "inc", "blank"):
            if got[k] != cs[k]:
                diffs.append("company %s %s: got %s want %s" % (cs["cid"], k, got[k], cs[k]))
    # value status (found / partial / not_found) per row
    mine = defaultdict(list)
    for x in scored:
        r = x["row"]
        mine[(r["company_id"], r["data_point"], r["role_row"])].append(x["value_status"])
    theirs = defaultdict(list)
    for cid, dp, role, st in t["valueStatus"]:
        theirs[(cid, dp, role)].append(st)
    for k in theirs:
        if sorted(mine[k]) != sorted(theirs[k]):
            diffs.append("value status %s: got %s want %s" % (k, mine[k], theirs[k]))
    print("summary", json.dumps({k: s[k] for k in ("values", "status", "gates", "hard_fail")}))
    for d in diffs[:80]:
        print(d)
    print("%d differences" % len(diffs))
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
