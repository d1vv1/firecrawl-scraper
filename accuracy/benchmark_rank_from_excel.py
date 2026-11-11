"""Take each field's benchmarking rank (1 = most critical for benchmarking) from the 'Benchmarking Fields'
sheet of Allshares_Benchmarking_Field_Severity.xlsx into accuracy/inputs/benchmark_rank.json. The dashboard
merges it into report.json fieldList as "rank" and shows it on the Not found page.

    python accuracy/benchmark_rank_from_excel.py path/to/Allshares_Benchmarking_Field_Severity.xlsx

Re-run it when the Excel changes, then rebuild the dashboard (python -m extractor.dashboard --rerender).
"""

import json
import sys
from pathlib import Path

import openpyxl

OUT = Path(__file__).parent / "inputs" / "benchmark_rank.json"
SHEET = "Benchmarking Fields"


def read(path: Path) -> list[dict]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[SHEET] if SHEET in wb.sheetnames else wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h or "").strip() for h in rows[0]]
    i_rank, i_d = head.index("Rank"), head.index("Data point")
    out = []
    for r in rows[1:]:
        rank, d = r[i_rank], r[i_d]
        if isinstance(rank, (int, float)) and d:           # the summary and notes rows below have no rank
            out.append({"d": str(d).strip(), "rank": int(rank)})
    return sorted(out, key=lambda x: x["rank"])


def main(argv=None) -> None:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        sys.exit(__doc__)
    src = Path(args[0])
    fields = read(src)
    OUT.write_text(json.dumps({"_about": f"Benchmarking rank per field (1 = most critical), from {src.name} "
                                         f"sheet '{SHEET}' by accuracy/benchmark_rank_from_excel.py.",
                               "fields": fields}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(fields)} ranked fields -> {OUT}")


if __name__ == "__main__":
    main()
