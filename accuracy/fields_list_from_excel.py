"""Turn the 'Company Data' and 'Pay Data' sheets of allshares_fields_list.xlsx into
accuracy/inputs/fields_list.json, the field list the dashboard's Field coverage page uses.

    python accuracy/fields_list_from_excel.py path/to/allshares_fields_list.xlsx

Re-run it when the Excel changes, then rebuild the dashboard (python -m extractor.dashboard --rerender).
"""

import json
import sys
from pathlib import Path

import openpyxl

OUT = Path(__file__).parent / "inputs" / "fields_list.json"
SHEETS = ["Company Data", "Pay Data"]
COLS = {"#": "n", "Data point": "d", "Protocol ID": "f", "Category": "k", "Grain": "g", "What it is": "what",
        "Format": "format", "Read from": "readFrom", "Method": "method", "Checks applied": "checks", "Note": "note"}


def read(path: Path) -> list[dict]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    for sheet in SHEETS:
        rows = list(wb[sheet].iter_rows(values_only=True))
        head = [str(h or "").strip() for h in rows[0]]
        for r in rows[1:]:
            if not isinstance(r[0], (int, float)):      # category header rows such as "Identity (8)"
                continue
            rec = {"sheet": sheet}
            for h, v in zip(head, r):
                if h in COLS:
                    rec[COLS[h]] = "" if v is None else (int(v) if h == "#" else str(v).strip())
            rec["checks"] = [c.strip() for c in rec.get("checks", "").split(",") if c.strip()]
            out.append(rec)
    return out


def main(argv=None) -> None:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    fields = read(Path(args[0]))
    OUT.write_text(json.dumps(fields, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(fields)} fields ({', '.join(f'{s}: {sum(f['sheet'] == s for f in fields)}' for s in SHEETS)}) -> {OUT}")


if __name__ == "__main__":
    main()
