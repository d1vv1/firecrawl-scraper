"""Re-run the number checks on saved results, without new LLM calls or credits.

When a check improves (e.g. decimal commas in "number in quote"), results already in
output/ keep their old verdicts. This re-checks each saved figure (value, unit, quote)
with the current check_value_in_quote and balance check, applies the same in-place
correction for pre-multiplied values, and recomputes the status.

    python -m extractor.recheck            # show what would change
    python -m extractor.recheck --apply    # write it (originals backed up first)
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

from .config import CACHE_DIR, OUTPUT_DIR
from .schemas import UNIT_MULTIPLIERS, MoneyFigure
from .scraper import markdown_to_pages
from .sections import split_chunks
from .validate import DESCRIPTIVE_TARGETS, check_balance, check_quote, check_value_in_quote

BACKUP_DIR = OUTPUT_DIR / "_before_recheck"
_FIG_FIELDS = ("value", "unit", "currency", "label_in_report", "scope", "quote", "chunk_id",
               "not_found_reason")


def _figure(d: dict | None) -> MoneyFigure | None:
    if not d:
        return None
    try:
        return MoneyFigure(**{k: d.get(k) for k in _FIG_FIELDS})
    except ValueError:
        return None


def _report_chunks(result: dict):
    """The report text the result was extracted from (the markdown cache), as chunks."""
    name = (result.get("debug") or {}).get("markdown_file")
    path = CACHE_DIR / name if name else None
    if not path or not path.exists():
        return None
    return split_chunks(markdown_to_pages(path.read_text(encoding="utf-8")))


def recheck(result: dict) -> list[str]:
    """Update the result in place; return what changed (empty if nothing)."""
    changes = []
    chunks = None
    slots = {"revenue": result.get("revenue"), "total_assets": result.get("total_assets"),
             "total_equity_and_liabilities": (result.get("cross_check") or {}).get(
                 "total_equity_and_liabilities")}
    figs = {name: _figure(d) for name, d in slots.items()}
    checks = result.get("checks") or []
    for c in checks:
        name, d, fig = c.get("target"), slots.get(c.get("target")), figs.get(c.get("target"))
        if fig is None or d.get("method") == "xbrl_tag":
            continue
        if c.get("name") == "quote" and c.get("result") == "fail" and fig.quote:
            # Chunk ids may differ from the original run: search the whole report.
            chunks = chunks if chunks is not None else (_report_chunks(result) or [])
            if chunks:
                new = check_quote(name, fig.quote, None, chunks)
                if new.result == "pass":
                    new.detail = new.detail.split(" in all chunks")[0] + " in the report (recheck)"
                    changes.append(f"{name} quote fail -> pass ({new.detail})")
                    c["result"], c["detail"] = new.result, new.detail
            continue
        if c.get("name") != "value_in_quote":
            continue
        new = check_value_in_quote(name, fig)
        if fig.value != d.get("value"):
            changes.append(f"{name} value {d['value']:g} -> {fig.value:g} ({new.detail})")
            d["value"] = fig.value
            d["value_full"] = fig.value * UNIT_MULTIPLIERS.get(fig.unit or "units", 1)
        if new.result != c.get("result"):
            changes.append(f"{name} value_in_quote {c.get('result')} -> {new.result}"
                           + (f" ({new.detail})" if new.detail else ""))
            c["result"], c["detail"] = new.result, new.detail
    if any("value " in ch for ch in changes):
        bal = check_balance(figs["total_assets"] or _figure({"scope": "unclear"}),
                            figs["total_equity_and_liabilities"] or _figure({"scope": "unclear"}))
        for c in checks:
            if c.get("name") == "balance" and c.get("result") != bal.result:
                changes.append(f"balance {c.get('result')} -> {bal.result}")
                c["result"], c["detail"] = bal.result, bal.detail
    if not changes:
        return []
    if (slots["revenue"] or {}).get("value") is None and (slots["total_assets"] or {}).get("value") is None:
        status = "not_found"
    else:
        blocking = [c for c in checks if c.get("target") not in DESCRIPTIVE_TARGETS]
        status = "needs_review" if any(c.get("result") == "fail" for c in blocking) else "ok"
    if status != result.get("status"):
        changes.append(f"status {result.get('status')} -> {status}")
        result["status"] = status
    return changes


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--apply", action="store_true", help="write the changes (backs up originals)")
    args = p.parse_args(argv)
    changed = moved = 0
    for path in sorted(OUTPUT_DIR.glob("*.json")):
        if path.name.endswith(".error.json"):
            continue
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(result, dict) or "checks" not in result:
            continue
        before = result.get("status")
        changes = recheck(result)
        if not changes:
            continue
        changed += 1
        moved += before != "ok" and result["status"] == "ok"
        print(f"{result.get('input_name', path.stem)}:")
        for ch in changes:
            print(f"   {ch}")
        if args.apply:
            BACKUP_DIR.mkdir(exist_ok=True)
            backup = BACKUP_DIR / path.name
            if not backup.exists():
                shutil.copy2(path, backup)
            path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{changed} result(s) changed, {moved} now ok."
          + ("" if args.apply else " Nothing written: add --apply."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
