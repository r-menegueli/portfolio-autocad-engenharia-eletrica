"""Valida a coerencia matematica das tabelas do Projeto 02."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import json
from pathlib import Path


PROJECT_SLUG = "02-projeto-eletrico-residencial"
RHO_COPPER = Decimal("0.0225")


def rows_by(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return {row[key]: row for row in csv.DictReader(stream)}


def number(row: dict[str, str], key: str) -> Decimal:
    return Decimal(row[key].replace(",", "."))


def validate(root: Path) -> dict:
    project = root / PROJECT_SLUG
    circuits = rows_by(project / "quadro-cargas.csv", "circuito")
    points = rows_by(project / "lista-pontos.csv", "id")
    materials = rows_by(project / "lista-materiais.csv", "item")
    errors: list[str] = []
    checks = 0

    expected_circuits = {f"C{index}" for index in range(1, 9)}
    checks += 1
    if set(circuits) != expected_circuits:
        errors.append("Circuitos esperados C1 a C8 não coincidem com o CSV.")

    for tag, row in circuits.items():
        voltage = number(row, "tensao_v")
        apparent = number(row, "potencia_aparente_va")
        current = number(row, "corrente_projeto_a")
        length = number(row, "comprimento_m")
        section = number(row, "condutor_mm2")
        drop_recorded = number(row, "queda_circuito_pct")
        expected_current = apparent / voltage
        expected_drop = Decimal("2") * RHO_COPPER * length * current / section / voltage * Decimal("100")
        checks += 2
        if abs(current - expected_current) > Decimal("0.002"):
            errors.append(f"{tag}: corrente {current} A difere de S/V = {expected_current:.6f} A.")
        if abs(drop_recorded - expected_drop) > Decimal("0.002"):
            errors.append(f"{tag}: queda {drop_recorded}% difere do cálculo = {expected_drop:.6f}%.")

    point_totals: dict[str, Decimal] = {tag: Decimal("0") for tag in expected_circuits}
    for row in points.values():
        point_totals[row["circuito"]] += number(row, "potencia_total_va")
    for tag in sorted(expected_circuits):
        checks += 1
        table_value = number(circuits[tag], "potencia_aparente_va")
        if abs(point_totals[tag] - table_value) > Decimal("0.0002"):
            errors.append(f"{tag}: soma dos pontos {point_totals[tag]} VA difere do quadro {table_value} VA.")

    installed = sum((number(row, "potencia_aparente_va") for row in circuits.values()), Decimal("0"))
    general = sum((number(circuits[f"C{index}"], "potencia_aparente_va") for index in range(1, 6)), Decimal("0"))
    demand_general = Decimal("1000") + Decimal("0.35") * (general - Decimal("1000"))
    tue = sum((number(circuits[tag], "potencia_aparente_va") for tag in ("C6", "C7", "C8")), Decimal("0"))
    demand = demand_general + tue
    service_current = demand / Decimal("220")
    for label, actual, expected, tolerance in (
        ("potência instalada", installed, Decimal("15548.913"), Decimal("0.001")),
        ("demanda geral", demand_general, Decimal("2592.11955"), Decimal("0.00001")),
        ("demanda total", demand, Decimal("12592.11955"), Decimal("0.00001")),
        ("corrente de demanda", service_current, Decimal("57.236907"), Decimal("0.00001")),
    ):
        checks += 1
        if abs(actual - expected) > tolerance:
            errors.append(f"{label}: {actual} difere do esperado {expected}.")

    material_expectations = {
        "QD1": Decimal("1"), "QG1": Decimal("1"), "DPS1": Decimal("2"), "DR1": Decimal("1"),
        "LUM1": Decimal("6"), "LUM2": Decimal("3"), "LUM3": Decimal("1"),
        "INT1": Decimal("6"), "INT2": Decimal("2"), "TUG1": Decimal("24"), "TUE1": Decimal("2"),
    }
    for item, expected in material_expectations.items():
        checks += 1
        actual = number(materials[item], "quantidade") if item in materials else Decimal("-1")
        if actual != expected:
            errors.append(f"{item}: quantidade {actual} difere de {expected}.")

    breaker_count = sum((number(materials[item], "quantidade") for item in ("DJ1", "DJ2", "DJ3", "DJ4", "DJ5")), Decimal("0"))
    checks += 1
    if breaker_count != Decimal("8"):
        errors.append(f"Disjuntores de circuitos: {breaker_count}; esperados 8 dispositivos.")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "results": {
            "installed_va": str(installed),
            "general_demand_va": f"{demand_general:.5f}",
            "total_demand_va": f"{demand:.5f}",
            "service_current_a": f"{service_current:.6f}",
            "point_totals_va": {tag: str(point_totals[tag]) for tag in sorted(point_totals)},
        },
    }
    output = project / "validacao-matematica.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    return parser.parse_args()


def main() -> int:
    result = validate(parse_args().root.resolve())
    print(f"VALIDAÇÃO MATEMÁTICA {result['status']} | verificações={result['checks']} erros={len(result['errors'])}")
    for error in result["errors"]:
        print(f"[ERRO] {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
