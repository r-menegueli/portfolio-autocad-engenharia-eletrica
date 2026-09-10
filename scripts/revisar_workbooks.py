"""Valida estrutura, fórmulas e metadados dos workbooks do portfólio."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re

from openpyxl import load_workbook


EXPECTED = {
    "04-controle-nivel-reservatorio/tabelas-projeto-04.xlsx": [
        "Resumo",
        "Instrumentos",
        "IO",
        "Cabos",
        "Materiais",
        "Bornes",
    ],
    "05-instalacao-eletrica-industrial/tabelas-projeto-05.xlsx": [
        "Resumo",
        "Quadro Cargas",
        "Circuitos",
        "Alimentadores",
        "Cabos",
        "Materiais",
        "Auditoria",
    ],
}
FORMULA_ERROR = re.compile(r"#(?:REF!|DIV/0!|VALUE!|NAME\?|N/A|NUM!|NULL!|SPILL!|CALC!)")
LOCAL_PATH = re.compile(r"(?i)(?:[A-Z]:[\\/](?:Users|Documents and Settings)[\\/]|/(?:home|Users)/)")
EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
FIXED_DATE = datetime(2026, 9, 10, 12, 0, 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", type=Path, default=Path("work/revisao-workbooks/resultado.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    summaries: list[dict] = []

    for relative, expected_sheets in EXPECTED.items():
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Arquivo ausente ou vazio: {relative}")
            continue
        try:
            workbook = load_workbook(path, data_only=False, read_only=False)
        except Exception as exc:  # pragma: no cover - mensagem de diagnóstico
            errors.append(f"Falha ao abrir {relative}: {type(exc).__name__}")
            continue

        if workbook.sheetnames != expected_sheets:
            errors.append(
                f"Abas divergentes em {relative}: {workbook.sheetnames!r} != {expected_sheets!r}"
            )

        formulas = 0
        formula_errors = 0
        external_formulas = 0
        literal_errors = 0
        nonempty_cells = 0
        sheets: list[dict] = []
        for sheet in workbook.worksheets:
            sheet_formulas = 0
            sheet_nonempty = 0
            for row in sheet.iter_rows():
                for cell in row:
                    if cell.value is None:
                        continue
                    nonempty_cells += 1
                    sheet_nonempty += 1
                    value = str(cell.value)
                    if cell.data_type == "f":
                        formulas += 1
                        sheet_formulas += 1
                        if FORMULA_ERROR.search(value):
                            formula_errors += 1
                        if "[" in value and "]" in value:
                            external_formulas += 1
                    elif cell.data_type == "e" or FORMULA_ERROR.fullmatch(value):
                        literal_errors += 1
            if sheet.max_row < 1 or sheet.max_column < 1 or sheet_nonempty == 0:
                errors.append(f"Aba vazia: {relative}!{sheet.title}")
            sheets.append(
                {
                    "name": sheet.title,
                    "rows": sheet.max_row,
                    "columns": sheet.max_column,
                    "nonempty_cells": sheet_nonempty,
                    "formulas": sheet_formulas,
                }
            )

        if formula_errors or literal_errors:
            errors.append(
                f"Erros de fórmula em {relative}: fórmulas={formula_errors}, literais={literal_errors}"
            )
        if external_formulas or getattr(workbook, "_external_links", []):
            errors.append(f"Referências externas em {relative}: {external_formulas}")

        properties = workbook.properties
        metadata = {
            "creator": properties.creator,
            "last_modified_by": properties.lastModifiedBy,
            "title": properties.title,
            "subject": properties.subject,
            "description": properties.description,
            "created": properties.created.isoformat() if properties.created else None,
            "modified": properties.modified.isoformat() if properties.modified else None,
        }
        for key, value in metadata.items():
            if value and (LOCAL_PATH.search(str(value)) or EMAIL.search(str(value))):
                errors.append(f"Metadado indesejado em {relative}[{key}]")

        summaries.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sheet_count": len(workbook.sheetnames),
                "formulas": formulas,
                "nonempty_cells": nonempty_cells,
                "formula_errors": formula_errors + literal_errors,
                "external_formulas": external_formulas,
                "metadata": metadata,
                "sheets": sheets,
            }
        )
        workbook.close()

    result = {
        "schema_version": 1,
        "generated_on": FIXED_DATE.date().isoformat(),
        "status": "PASS" if not errors else "FAIL",
        "workbooks": summaries,
        "errors": errors,
    }
    output = args.json if args.json.is_absolute() else root / args.json
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        f"WORKBOOK_REVIEW={result['status']} | arquivos={len(summaries)} "
        f"abas={sum(item['sheet_count'] for item in summaries)} "
        f"formulas={sum(item['formulas'] for item in summaries)} erros={len(errors)}"
    )
    print(f"RESULTADO={output.relative_to(root)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
