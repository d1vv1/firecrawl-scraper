"""Check that Module Check weights sum to 1 and every Field Checks row has a valid protocol ID.

python accuracy/tests/check_field_checks.py [path ...]
Default: the corrected out/allshares_field_checks.xlsx and, for comparison, the original input.
Exit code 1 if any file given (or the corrected output) has errors.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine.excel import check_field_checks  # noqa: E402


def main(paths):
    worst = 0
    for p in paths:
        errors, warnings, sums = check_field_checks(p)
        print("==", os.path.relpath(p, ROOT))
        for mod, s in sorted(sums.items()):
            print("   module %-22s weights sum %.4f" % (mod, s))
        for w in warnings:
            print("   warning:", w)
        for e in errors[:25]:
            print("   ERROR:", e)
        if len(errors) > 25:
            print("   ... %d more errors" % (len(errors) - 25))
        print("   %s (%d errors, %d warnings)" % ("FAIL" if errors else "OK", len(errors), len(warnings)))
        if errors and "inputs" not in p:
            worst = 1
    return worst


if __name__ == "__main__":
    args = sys.argv[1:] or [os.path.join(ROOT, "inputs", "allshares_field_checks.xlsx"),
                            os.path.join(ROOT, "out", "allshares_field_checks.xlsx")]
    sys.exit(main(args))
