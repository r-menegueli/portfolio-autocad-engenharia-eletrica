"""Valida calculos, referencias e DXFs do Projeto 05."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, getcontext
import json
from pathlib import Path

import ezdxf


getcontext().prec = 28
PROJECT_SLUG = "05-instalacao-eletrica-industrial"
RHO_COPPER = Decimal("0.0225")
SQRT3 = Decimal(3).sqrt()
SHEETS = (
    "01_layout_industrial.dxf",
    "02_distribuicao_forca.dxf",
    "03_distribuicao_iluminacao.dxf",
    "04_eletrocalhas_rotas.dxf",
    "05_diagrama_unifilar.dxf",
    "06_quadro_cargas.dxf",
    "07_detalhes_instalacao.dxf",
    "08_coordenacao_protecoes.dxf",
    "09_plano_dados_coordenacao.dxf",
)
EXPECTED_CIRCUITS = {f"C{number:02d}" for number in range(1, 17)}
EXPECTED_FEEDERS = {"AL-QGBT", "AL-QDF", "AL-QDL", "AL-QADM"}
REQUIRED_TAGS = {
    "QGBT-05", "QDF-05", "QDL-05", "QADM-05", "M-501", "M-502",
    "M-503", "M-504", "M-505", "TUE-501", "TI-501", "TI-506",
    "E-501", "E-502", "E-503", "C01", "C08", "C09", "C13", "C16",
    "DJ-G", "QF-QDF", "QF-QDL", "QF-QADM", "TCC", "PENDENTE",
}
EXPECTED_PROTECTION_PAIRS = {
    "DJ-G > QF-QDF",
    "DJ-G > QF-QDL",
    "DJ-G > QF-QADM",
    "QF-QDF > C01-C08",
    "QF-QDL > C09-C13",
    "QF-QADM > C14-C16",
}
EXPECTED_STUDY_STAGES = (
    "ENTRADA", "ENTRADA", "ENTRADA", "ENTRADA", "ENTRADA", "ENTRADA",
    "CALCULO", "CALCULO", "CALCULO", "CALCULO", "CALCULO", "REVISAO",
)
REQUIRED_STUDY_TERMS = (
    "PLANO DE DADOS PARA CURTO-CIRCUITO E COORDENACAO",
    "D01", "D06", "D07", "D11", "D12", "Icc MAX",
    "I2t", "PENDENTE", "REDE, TRAFO, CABOS",
    "ROTEIRO DE VERIFICACAO", "D01-D06 | ENTRADAS", "D07 | MODELO",
    "D08 | CALCULO", "D09-D11 | TESTES", "D12 | FECHAMENTO",
    "CAPACIDADE / SUPORTABILIDADE", "CURVAS, PARES E RETAGUARDA",
    "MODELO, AJUSTES, REVISAO", "Icu/Ics de disjuntores", "Icw/Ipk de conjuntos",
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def number(row: dict[str, str], key: str) -> Decimal:
    return Decimal(row[key].replace(",", "."))


def extract_text(doc: ezdxf.document.Drawing) -> str:
    values: list[str] = []
    for entity in doc.modelspace():
        if entity.dxftype() == "TEXT":
            values.append(entity.dxf.text)
        elif entity.dxftype() == "MTEXT":
            values.append(entity.plain_text())
        elif entity.dxftype() == "INSERT":
            values.extend(attrib.dxf.text for attrib in entity.attribs)
    return " ".join(values)


def close(actual: Decimal, expected: Decimal, tolerance: Decimal = Decimal("0.00001")) -> bool:
    return abs(actual - expected) <= tolerance


def validate(root: Path) -> dict:
    project = root / PROJECT_SLUG
    loads = read_rows(project / "quadro-cargas.csv")
    feeders = read_rows(project / "alimentadores.csv")
    cables = read_rows(project / "lista-cabos.csv")
    materials = read_rows(project / "lista-materiais.csv")
    protection_pairs = read_rows(project / "matriz-coordenacao-protecoes.csv")
    study_inputs = read_rows(project / "dados-estudo-coordenacao.csv")
    errors: list[str] = []
    checks = 0

    protection_pair_ids = {row["par"] for row in protection_pairs}
    checks += 3
    if len(protection_pairs) != 6 or protection_pair_ids != EXPECTED_PROTECTION_PAIRS:
        errors.append("A matriz de protecoes deve cobrir exatamente os seis pares montante-jusante.")
    for row in protection_pairs:
        checks += 3
        if row["status"] != "PENDENTE":
            errors.append(f"{row['par']}: estudo de coordenacao nao pode ser declarado aprovado sem evidencias.")
        if not row["verificacoes"].strip() or not row["dados_necessarios"].strip():
            errors.append(f"{row['par']}: verificacoes e dados necessarios devem ser rastreados.")

    expected_study_ids = [f"D{index:02d}" for index in range(1, 13)]
    checks += 2 + len(expected_study_ids) * 3
    if [row.get("id") for row in study_inputs] != expected_study_ids:
        errors.append("O plano de coordenacao deve conter D01 a D12 em ordem, sem duplicatas.")
    if len(study_inputs) != len(expected_study_ids):
        errors.append("O plano de coordenacao deve conter exatamente 12 grupos de dados.")
    if [row.get("etapa") for row in study_inputs] != list(EXPECTED_STUDY_STAGES):
        errors.append("Os grupos D01-D06, D07-D11 e D12 devem separar entrada, calculo e revisao.")
    for row in study_inputs:
        if any(not row.get(field, "").strip() for field in ("entrada_ou_verificacao", "evidencia")):
            errors.append(f"{row.get('id', 'ID ausente')}: dado e evidencia devem estar descritos.")
        if row.get("status") != "PENDENTE":
            errors.append(f"{row.get('id', 'ID ausente')}: nao ha dados/evidencias suficientes para fechar o estudo.")

    circuits = {row["circuito"] for row in loads}
    checks += 2
    if len(circuits) != len(loads):
        errors.append("Ha circuitos duplicados no quadro de cargas.")
    if circuits != EXPECTED_CIRCUITS:
        errors.append("O quadro de cargas nao cobre exatamente C01 a C16.")

    board_totals: dict[str, dict[str, Decimal]] = {}
    combined_drops: dict[str, Decimal] = {}
    for row in loads:
        tag = row["circuito"]
        voltage = number(row, "tensao_v")
        output_kw = number(row, "potencia_saida_kw")
        efficiency = number(row, "rendimento")
        pf = number(row, "fator_potencia")
        installed_kw = number(row, "potencia_ativa_instalada_kw")
        installed_kva = number(row, "potencia_aparente_instalada_kva")
        demand_factor = number(row, "fator_demanda")
        demand_kw = number(row, "potencia_ativa_demandada_kw")
        demand_kva = number(row, "potencia_aparente_demandada_kva")
        current = number(row, "corrente_circuito_a")
        length = number(row, "comprimento_m")
        section = number(row, "condutor_mm2")
        breaker = number(row, "disjuntor_a")
        ampacity = number(row, "iz_assumida_a")
        drop = number(row, "queda_circuito_pct")

        expected_kw = output_kw / efficiency
        expected_kva = expected_kw / pf
        expected_demand_kw = expected_kw * demand_factor
        expected_demand_kva = expected_kva * demand_factor
        divisor = SQRT3 * voltage if row["fases"] == "ABC" else voltage
        expected_current = expected_kva * Decimal(1000) / divisor
        factor = SQRT3 if row["fases"] == "ABC" else Decimal(2)
        expected_drop = Decimal(100) * factor * RHO_COPPER * length * expected_current / section / voltage

        comparisons = (
            ("potencia ativa instalada", installed_kw, expected_kw),
            ("potencia aparente instalada", installed_kva, expected_kva),
            ("potencia ativa demandada", demand_kw, expected_demand_kw),
            ("potencia aparente demandada", demand_kva, expected_demand_kva),
            ("corrente", current, expected_current),
            ("queda", drop, expected_drop),
        )
        for label, actual, expected in comparisons:
            checks += 1
            if not close(actual, expected, Decimal("0.00001")):
                errors.append(f"{tag}: {label} {actual} difere de {expected:.8f}.")
        checks += 2
        if current > breaker:
            errors.append(f"{tag}: Ib {current} A supera In {breaker} A.")
        if breaker > ampacity:
            errors.append(f"{tag}: In {breaker} A supera Iz {ampacity} A.")

        totals = board_totals.setdefault(row["quadro"], {"p": Decimal(0), "s": Decimal(0), "pd": Decimal(0), "sd": Decimal(0)})
        totals["p"] += installed_kw
        totals["s"] += installed_kva
        totals["pd"] += demand_kw
        totals["sd"] += demand_kva

    expected_totals = {
        "QDF-05": (Decimal("61.265248"), Decimal("72.429944"), Decimal("42.458716"), Decimal("50.241811")),
        "QDL-05": (Decimal("3.180000"), Decimal("3.347367"), Decimal("3.180000"), Decimal("3.347367")),
        "QADM-05": (Decimal("4.050000"), Decimal("4.500000"), Decimal("2.430000"), Decimal("2.700000")),
    }
    for board, expected in expected_totals.items():
        for key, value in zip(("p", "s", "pd", "sd"), expected):
            checks += 1
            if not close(board_totals[board][key], value, Decimal("0.000003")):
                errors.append(f"{board}: total {key} {board_totals[board][key]} difere de {value}.")

    total_p = sum((row["p"] for row in board_totals.values()), Decimal(0))
    total_s = sum((row["s"] for row in board_totals.values()), Decimal(0))
    total_pd = sum((row["pd"] for row in board_totals.values()), Decimal(0))
    total_sd = sum((row["sd"] for row in board_totals.values()), Decimal(0))
    for label, actual, expected in (
        ("P instalada", total_p, Decimal("68.495248")),
        ("S instalada", total_s, Decimal("80.277311")),
        ("P demandada", total_pd, Decimal("48.068716")),
        ("S demandada", total_sd, Decimal("56.289178")),
    ):
        checks += 1
        if not close(actual, expected, Decimal("0.000003")):
            errors.append(f"{label}: {actual} difere de {expected}.")

    feeder_map = {row["alimentador"]: row for row in feeders}
    checks += 2
    if len(feeder_map) != len(feeders):
        errors.append("Ha alimentadores duplicados.")
    if set(feeder_map) != EXPECTED_FEEDERS:
        errors.append("Alimentadores esperados nao coincidem com o CSV.")

    qdf_current = board_totals["QDF-05"]["sd"] * Decimal(1000) / (SQRT3 * Decimal(380))
    phase_currents = {phase: qdf_current for phase in "ABC"}
    for row in loads:
        if row["fases"] in phase_currents:
            phase_currents[row["fases"]] += number(row, "potencia_aparente_demandada_kva") * Decimal(1000) / Decimal(220)
    main_current = max(phase_currents.values())
    qdl_phase = {phase: Decimal(0) for phase in "ABC"}
    for row in loads:
        if row["quadro"] == "QDL-05":
            qdl_phase[row["fases"]] += number(row, "potencia_aparente_demandada_kva") * Decimal(1000) / Decimal(220)
    qadm_current = Decimal("0.900000") * Decimal(1000) / Decimal(220)
    calculated_feeders = {
        "AL-QGBT": (total_sd, main_current, Decimal(2)),
        "AL-QDF": (board_totals["QDF-05"]["sd"], qdf_current, SQRT3),
        "AL-QDL": (board_totals["QDL-05"]["sd"], max(qdl_phase.values()), Decimal(2)),
        "AL-QADM": (board_totals["QADM-05"]["sd"], qadm_current, Decimal(2)),
    }
    for tag, (expected_kva, expected_current, drop_factor) in calculated_feeders.items():
        row = feeder_map[tag]
        actual_kva = number(row, "potencia_demandada_kva")
        actual_current = number(row, "corrente_projeto_a")
        section = number(row, "condutores_fase_neutro_mm2")
        voltage = Decimal(220) if drop_factor == 2 else Decimal(380)
        expected_drop = Decimal(100) * drop_factor * RHO_COPPER * number(row, "comprimento_m") * expected_current / section / voltage
        checks += 5
        if not close(actual_kva, expected_kva, Decimal("0.000003")):
            errors.append(f"{tag}: potencia demandada nao reconcilia com os circuitos.")
        if not close(actual_current, expected_current, Decimal("0.000003")):
            errors.append(f"{tag}: corrente nao reconcilia com as fases/cargas.")
        if not close(number(row, "queda_pct"), expected_drop, Decimal("0.000003")):
            errors.append(f"{tag}: queda registrada difere de {expected_drop:.8f}%.")
        if actual_current > number(row, "disjuntor_a"):
            errors.append(f"{tag}: Ib supera In.")
        if number(row, "disjuntor_a") > number(row, "iz_assumida_a"):
            errors.append(f"{tag}: In supera Iz.")

    cable_map = {row["cabo"]: row for row in cables}
    checks += 3
    if len(cable_map) != len(cables):
        errors.append("Ha cabos duplicados.")
    if set(cable_map) != EXPECTED_FEEDERS | EXPECTED_CIRCUITS:
        errors.append("Lista de cabos deve conter quatro alimentadores e C01-C16.")
    if len(cables) != 20:
        errors.append("Lista de cabos deve conter 20 registros.")
    for row in loads:
        cable = cable_map.get(row["circuito"])
        checks += 3
        if not cable:
            continue
        if cable["de"] != row["quadro"]:
            errors.append(f"{row['circuito']}: origem do cabo diverge do quadro.")
        if not close(number(cable, "comprimento_assumido_m"), number(row, "comprimento_m")):
            errors.append(f"{row['circuito']}: comprimento diverge entre tabelas.")
        if not close(number(cable, "queda_pct"), number(row, "queda_circuito_pct")):
            errors.append(f"{row['circuito']}: queda diverge entre tabelas.")

    feeder_drop = {row["alimentador"]: number(row, "queda_pct") for row in feeders}
    board_feeder = {"QDF-05": "AL-QDF", "QDL-05": "AL-QDL", "QADM-05": "AL-QADM"}
    for row in loads:
        combined = feeder_drop["AL-QGBT"] + feeder_drop[board_feeder[row["quadro"]]] + number(row, "queda_circuito_pct")
        combined_drops[row["circuito"]] = combined
        checks += 1
        if combined > Decimal("4.0"):
            errors.append(f"{row['circuito']}: queda combinada {combined}% excede 4,0%.")

    material_refs = " ".join(row["referencia"] for row in materials)
    for tag in ("QGBT-05", "QDF-05", "QDL-05", "QADM-05", "M-501", "M-505", "TUE-501", "TI-501", "E-501", "E-503"):
        checks += 1
        if tag not in material_refs:
            errors.append(f"Referencia de material ausente: {tag}.")

    dxf_texts: list[str] = []
    for index, filename in enumerate(SHEETS, start=1):
        path = project / "fonte" / filename
        checks += 4
        if not path.is_file():
            errors.append(f"DXF ausente: {filename}.")
            continue
        try:
            doc = ezdxf.readfile(path)
            auditor = doc.audit()
        except Exception as exc:
            errors.append(f"Falha ao abrir {filename}: {exc}")
            continue
        if auditor.has_errors:
            errors.append(f"{filename}: auditoria ezdxf encontrou {len(auditor.errors)} erro(s).")
        metadata = doc.ezdxf_metadata()
        if metadata.get("PORTFOLIO_PROJECT") != PROJECT_SLUG:
            errors.append(f"{filename}: metadado de projeto incorreto.")
        if metadata.get("PORTFOLIO_SHEET") != f"{index:02d}/{len(SHEETS):02d}":
            errors.append(f"{filename}: metadado de prancha incorreto.")
        sheet_text = extract_text(doc)
        dxf_texts.append(sheet_text)
        checks += 2
        if "6 kA" in sheet_text or "10 kA" in sheet_text:
            errors.append(f"{filename}: capacidade de curto/interrupcao nao pode permanecer como valor presumido.")
        if index == 9:
            sheet_text = sheet_text.casefold()
            checks += len(REQUIRED_STUDY_TERMS)
            for term in REQUIRED_STUDY_TERMS:
                if term.casefold() not in sheet_text:
                    errors.append(f"{filename}: informacao do plano de coordenacao ausente: {term}.")

    merged_text = " ".join(dxf_texts).casefold()
    for tag in sorted(REQUIRED_TAGS):
        checks += 1
        if tag.casefold() not in merged_text:
            errors.append(f"Identificacao nao localizada no conjunto DXF: {tag}.")

    mean_phase = sum(phase_currents.values(), Decimal(0)) / Decimal(3)
    imbalance_pct = (max(phase_currents.values()) - min(phase_currents.values())) / mean_phase * Decimal(100)
    checks += 1
    if imbalance_pct > Decimal(5):
        errors.append(f"Desequilibrio total de fases {imbalance_pct:.3f}% excede criterio interno de 5%.")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "results": {
            "sheets": len(SHEETS),
            "protection_pairs": len(protection_pairs),
            "coordination_study_inputs": len(study_inputs),
            "circuits": len(loads),
            "feeders": len(feeders),
            "cables": len(cables),
            "materials": len(materials),
            "installed_active_kw": f"{total_p:.6f}",
            "installed_apparent_kva": f"{total_s:.6f}",
            "demand_active_kw": f"{total_pd:.6f}",
            "demand_apparent_kva": f"{total_sd:.6f}",
            "equivalent_demand_current_a": f"{total_sd * Decimal(1000) / (SQRT3 * Decimal(380)):.6f}",
            "phase_currents_a": {phase: f"{value:.6f}" for phase, value in phase_currents.items()},
            "phase_imbalance_pct": f"{imbalance_pct:.6f}",
            "maximum_combined_drop_pct": f"{max(combined_drops.values()):.6f}",
            "maximum_combined_drop_circuit": max(combined_drops, key=combined_drops.get),
        },
    }
    output = project / "validacao-calculos.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    return parser.parse_args()


def main() -> int:
    result = validate(parse_args().root.resolve())
    print(f"VALIDACAO PROJETO 05 {result['status']} | verificacoes={result['checks']} erros={len(result['errors'])}")
    for error in result["errors"]:
        print(f"[ERRO] {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
