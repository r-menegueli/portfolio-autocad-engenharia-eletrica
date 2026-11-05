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


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def number(row: dict[str, str], key: str) -> Decimal:
    return Decimal(row[key].replace(",", "."))


def validate(root: Path) -> dict:
    project = root / PROJECT_SLUG
    circuits = rows_by(project / "quadro-cargas.csv", "circuito")
    points = rows_by(project / "lista-pontos.csv", "id")
    materials = rows_by(project / "lista-materiais.csv", "item")
    room_rows = read_rows(project / "rastreabilidade-ambientes.csv")
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

    room_by_name = {row["ambiente"]: row for row in room_rows}
    room_by_point_name = {
        row["ambiente_lista_pontos"]: row
        for row in room_rows
        if row["ambiente_lista_pontos"]
    }
    checks += 1
    if len(room_rows) != 8:
        errors.append(f"Rastreabilidade por ambiente: {len(room_rows)} linhas; esperadas 8.")
    checks += 1
    if len(room_by_name) != len(room_rows):
        errors.append("Há nomes de ambiente duplicados na rastreabilidade.")
    checks += 1
    point_room_names = {row["ambiente"] for row in points.values()}
    if set(room_by_point_name) != point_room_names or len(room_by_point_name) != len(
        [row for row in room_rows if row["ambiente_lista_pontos"]]
    ):
        errors.append("Os ambientes da lista de pontos não têm correspondência única na rastreabilidade.")

    declared_area = Decimal("0")
    tracked_point_ids: list[str] = []
    tracked_point_va = Decimal("0")
    for room in room_rows:
        dimensions_area = Decimal("0")
        try:
            for rectangle in room["dimensoes_adotadas_m"].split("+"):
                width, height = (Decimal(value.strip()) for value in rectangle.split("x"))
                dimensions_area += width * height
        except (ValueError, ArithmeticError):
            errors.append(f"{room['ambiente']}: dimensões inválidas em rastreabilidade.")
        area = number(room, "area_declarada_m2")
        declared_area += area
        checks += 1
        if abs(dimensions_area - area) > Decimal("0.0001"):
            errors.append(f"{room['ambiente']}: área declarada {area} m² difere das dimensões {dimensions_area} m².")
        checks += 1
        if room["status"] != "PREMISSA":
            errors.append(f"{room['ambiente']}: estado deve permanecer PREMISSA até haver levantamento.")
        point_name = room["ambiente_lista_pontos"]
        if not point_name:
            continue
        for point in points.values():
            if point["ambiente"] == point_name:
                tracked_point_ids.append(point["id"])
                tracked_point_va += number(point, "potencia_total_va")

    checks += 1
    if declared_area != Decimal("75.00"):
        errors.append(f"Área total dos ambientes: {declared_area} m²; esperados 75.00 m².")
    checks += 1
    if set(tracked_point_ids) != set(points) or len(tracked_point_ids) != len(points):
        errors.append("As linhas da lista de pontos não estão rastreadas uma única vez por ambiente.")
    checks += 1
    if abs(tracked_point_va - sum(point_totals.values(), Decimal("0"))) > Decimal("0.0002"):
        errors.append("A potência rastreada por ambiente difere da soma da lista de pontos.")

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
            "room_count": len(room_rows),
            "declared_area_m2": str(declared_area),
            "tracked_points": len(tracked_point_ids),
            "tracked_point_va": str(tracked_point_va),
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
