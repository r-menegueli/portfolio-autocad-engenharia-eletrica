"""Valida a coerencia matematica das tabelas do Projeto 02."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import json
from pathlib import Path

import ezdxf

PROJECT_SLUG = "02-projeto-eletrico-residencial"
RHO_COPPER = Decimal("0.0225")
PHASE_ANALYSIS_CSV = "analise-corrente-por-fase.csv"


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
    openings = read_rows(project / "esquadrias.csv")
    errors: list[str] = []
    checks = 0

    expected_circuits = {f"C{index}" for index in range(1, 9)}
    checks += 1
    if set(circuits) != expected_circuits:
        errors.append("Circuitos esperados C1 a C8 não coincidem com o CSV.")

    phase_neutral_va = {"A": Decimal("0"), "B": Decimal("0")}
    phase_neutral_current = {"A": Decimal("0"), "B": Decimal("0")}
    phase_neutral_tags = {"A": [], "B": []}
    phase_phase_va = Decimal("0")
    phase_phase_current = Decimal("0")
    phase_phase_tags: list[str] = []

    for tag, row in circuits.items():
        voltage = number(row, "tensao_v")
        apparent = number(row, "potencia_aparente_va")
        phases = row["fases"].strip().upper()
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

        checks += 1
        if voltage == Decimal("127") and phases in phase_neutral_va:
            phase_neutral_va[phases] += apparent
            phase_neutral_current[phases] += apparent / voltage
            phase_neutral_tags[phases].append(tag)
        elif voltage == Decimal("220") and phases == "AB":
            phase_phase_va += apparent
            phase_phase_current += apparent / voltage
            phase_phase_tags.append(tag)
        else:
            errors.append(f"{tag}: par tensão/fases fora do cenário 127 V A/B ou 220 V AB.")

    phase_results: dict[str, dict[str, str]] = {}
    analysis_rows = read_rows(project / PHASE_ANALYSIS_CSV)
    checks += 1
    if {row.get("fase") for row in analysis_rows} != {"A", "B"} or len(analysis_rows) != 2:
        errors.append("Análise de corrente por fase: esperado um registro único para A e B.")
    for row in analysis_rows:
        phase = row.get("fase", "")
        if phase not in phase_neutral_va:
            continue
        neutral_current = phase_neutral_current[phase]
        upper_bound = neutral_current + phase_phase_current
        expected_fields = {
            "ramais_fase_neutro": "+".join(phase_neutral_tags[phase]),
            "va_fase_neutro": phase_neutral_va[phase],
            "tensao_fase_neutro_v": Decimal("127"),
            "soma_magnitudes_fase_neutro_a": neutral_current,
            "ramais_fase_fase": "+".join(phase_phase_tags),
            "va_fase_fase": phase_phase_va,
            "tensao_fase_fase_v": Decimal("220"),
            "soma_magnitudes_fase_fase_a": phase_phase_current,
            "cota_superior_aritmetica_a": upper_bound,
        }
        for field, expected in expected_fields.items():
            checks += 1
            actual_text = row.get(field, "")
            try:
                if isinstance(expected, Decimal):
                    actual = Decimal(actual_text)
                    if abs(actual - expected) > Decimal("0.000002"):
                        errors.append(f"Análise fase {phase}: {field} {actual} difere de {expected}.")
                elif actual_text != expected:
                    errors.append(f"Análise fase {phase}: {field} {actual_text!r} difere de {expected!r}.")
            except ArithmeticError:
                errors.append(f"Análise fase {phase}: valor inválido em {field}.")
        checks += 1
        if "nao e demanda" not in row.get("metodo", "").casefold():
            errors.append(f"Análise fase {phase}: método deve identificar o limite como não sendo demanda.")
        phase_results[phase] = {
            "phase_neutral_va": str(phase_neutral_va[phase]),
            "phase_neutral_sum_a": f"{neutral_current:.6f}",
            "phase_phase_va": str(phase_phase_va),
            "phase_phase_sum_a": f"{phase_phase_current:.6f}",
            "arithmetic_upper_bound_a": f"{upper_bound:.6f}",
        }

    dxf_path = project / "fonte" / "10_corrente_por_fase.dxf"
    checks += 1
    try:
        doc = ezdxf.readfile(dxf_path)
        metadata = doc.ezdxf_metadata()
        if metadata.get("PORTFOLIO_SHEET") != "10/10":
            errors.append("P02-10: metadado de prancha deve ser 10/10.")
        drawing_text = " ".join(
            entity.dxf.text if entity.dxftype() == "TEXT" else entity.text
            for entity in doc.modelspace().query("TEXT MTEXT")
        ).casefold()
        checks += 3
        for term in ("análise aritmética de corrente por fase", "63 a antiga", "não demanda"):
            if term not in drawing_text:
                errors.append(f"P02-10: termo obrigatório ausente: {term}.")
    except (OSError, ezdxf.DXFError) as exc:
        errors.append(f"P02-10: não foi possível ler o DXF: {exc}.")

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
    opening_ids = {row["id"] for row in openings}
    if opening_ids != {*(f"D{index:02d}" for index in range(1, 9)), *(f"W{index:02d}" for index in range(1, 8))}:
        errors.append("Esquadrias: IDs devem cobrir D01-D08 e W01-W07.")
    checks += 1
    if any(row["status"] != "PREMISSA" for row in openings):
        errors.append("Esquadrias: dimensões devem permanecer PREMISSA até levantamento.")
    checks += 1
    if room_by_name.get("Closet Q1", {}).get("ambiente_lista_pontos") != "Closet Q1":
        errors.append("Closet Q1 deve estar ligado à lista de pontos para rastrear L09.")
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
    for label, actual, expected, tolerance in (
        ("potência instalada", installed, Decimal("15558.6955"), Decimal("0.001")),
    ):
        checks += 1
        if abs(actual - expected) > tolerance:
            errors.append(f"{label}: {actual} difere do esperado {expected}.")

    material_expectations = {
        "QD1": Decimal("1"), "QG1": Decimal("1"), "DPS1": Decimal("2"), "DR1": Decimal("1"),
        "LUM1": Decimal("6"), "LUM2": Decimal("4"), "LUM3": Decimal("1"),
        "INT1": Decimal("7"), "INT2": Decimal("2"), "TUG1": Decimal("24"), "TUE1": Decimal("2"),
        "CX1": Decimal("11"), "CX2": Decimal("35"),
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
            "phase_current_upper_bounds": phase_results,
            "demand_and_main_breaker_status": "PENDING_METHOD_AND_REAL_DATA",
            "withdrawn_qg1_reference_a": "63",
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
