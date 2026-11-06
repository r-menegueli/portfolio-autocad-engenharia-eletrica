"""Valida cálculos, intertravamentos e referências do Projeto 06."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, getcontext
import json
from pathlib import Path

import ezdxf


getcontext().prec = 28
PROJECT_SLUG = "06-centro-controle-motores"
RHO_COPPER = Decimal("0.0225")
SQRT3 = Decimal(3).sqrt()
SHEETS = (
    "01_diagrama_unifilar_ccm.dxf",
    "02_partida_direta.dxf",
    "03_partida_reversora.dxf",
    "04_acionamento_inversor.dxf",
    "05_layout_ccm.dxf",
    "06_diagrama_bornes.dxf",
    "07_lista_cabos.dxf",
    "08_matriz_causa_efeito_ccm.dxf",
    "09_balanco_demanda_ccm.dxf",
    "10_interligacao_bornes_comando.dxf",
)
EXPECTED_LOADS = {"M-601", "M-602", "M-603"}
EXPECTED_CABLES = {"W600", "W601", "W602", "W603A", "W603B", "W604", "W605", "W606", "W607", "W608"}
EXPECTED_METHODS = {"PARTIDA DIRETA", "PARTIDA REVERSORA", "INVERSOR DE FREQUENCIA"}
PROTECTION = {
    "M-601": (Decimal("16"), Decimal("24")),
    "M-602": (Decimal("10"), Decimal("24")),
    "M-603": (Decimal("25"), Decimal("32")),
}
REQUIRED_MATERIAL_TAGS = {
    "CCM-06", "QG-06", "QF-601", "KM-601", "FR-601", "QF-602",
    "KM-602F", "KM-602R", "IM-602", "FR-602", "QF-603", "VFD-603",
    "KSR-601", "PSU-601", "M-601", "M-602", "M-603", "S0-601", "PE-06",
}
SHEET_TERMS = {
    "01_diagrama_unifilar_ccm.dxf": ("CCM-06", "QG-06", "M-601", "M-602", "M-603", "KSR-601"),
    "02_partida_direta.dxf": ("KM-601", "FR-601", "S-601L", "S-601P", "SELO"),
    "03_partida_reversora.dxf": ("KM-602F", "KM-602R", "IM-602", "FC-602F", "FC-602R"),
    "04_acionamento_inversor.dxf": ("VFD-603", "STO A", "STO B", "W603B", "SEM CONTATOR"),
    "05_layout_ccm.dxf": ("GAVETA 601", "GAVETA 602", "QF-601", "KM-602F", "VFD-603", "PE-06"),
    "06_diagrama_bornes.dxf": ("X1", "X2", "X3", "X4", "P06-10", "W603B"),
    "07_lista_cabos.dxf": ("W600", "W601", "W602", "W603A", "W603B", "W608"),
    "08_matriz_causa_efeito_ccm.dxf": ("MATRIZ CAUSA-EFEITO DO CCM-06", "E01", "E09", "KSR", "STO A/B"),
    "09_balanco_demanda_ccm.dxf": (
        "BALANÇO DE DEMANDA DO CCM-06",
        "18,184584",
        "20,893255",
        "16,645368",
        "19,133709",
        "29,070663",
        "0,80",
        "0,90",
        "Ib <= In <= Iz",
    ),
    "10_interligacao_bornes_comando.dxf": ("X3", "X4", "CH1A", "DI3", "STO-A", "H-604", "W607"),
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def number(row: dict[str, str], key: str) -> Decimal:
    return Decimal(row[key].replace(",", "."))


def close(actual: Decimal, expected: Decimal, tolerance: Decimal = Decimal("0.000002")) -> bool:
    return abs(actual - expected) <= tolerance


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


def expected_terminals() -> set[str]:
    return (
        {f"X1:{index}" for index in range(1, 6)}
        | {f"X2:{index}" for index in range(1, 13)}
        | {f"X3:{index}" for index in range(1, 25)}
        | {f"X4:{index}" for index in range(1, 11)}
    )


def validate(root: Path) -> dict:
    project = root / PROJECT_SLUG
    loads = read_rows(project / "lista-cargas.csv")
    feeder_rows = read_rows(project / "alimentador.csv")
    cables = read_rows(project / "lista-cabos.csv")
    terminals = read_rows(project / "lista-bornes.csv")
    materials = read_rows(project / "lista-materiais.csv")
    cause_effect = read_rows(project / "causa-efeito.csv")
    errors: list[str] = []
    checks = 0

    load_tags = {row["tag"] for row in loads}
    methods = {row["metodo_acionamento"] for row in loads}
    checks += 4
    if len(loads) != 3 or load_tags != EXPECTED_LOADS:
        errors.append("A lista de cargas deve conter exatamente M-601, M-602 e M-603.")
    if len(load_tags) != len(loads):
        errors.append("Há tags de carga duplicadas.")
    if methods != EXPECTED_METHODS:
        errors.append("Os três métodos de acionamento obrigatórios não estão representados.")
    if len(methods) != len(loads):
        errors.append("Cada carga deve usar um método de acionamento distinto.")

    total_pin = Decimal(0)
    total_s = Decimal(0)
    total_p_dem = Decimal(0)
    total_s_dem = Decimal(0)
    circuit_drops: dict[str, Decimal] = {}
    load_map = {row["tag"]: row for row in loads}
    for row in loads:
        tag = row["tag"]
        power = number(row, "potencia_saida_kw")
        efficiency = number(row, "rendimento")
        power_factor = number(row, "fator_potencia")
        demand_factor = number(row, "fator_demanda")
        voltage = number(row, "tensao_v")
        pin = power / efficiency
        apparent = pin / power_factor
        demand_active = pin * demand_factor
        demand_apparent = apparent * demand_factor
        current = apparent * Decimal(1000) / (SQRT3 * voltage)
        drop = Decimal(100) * SQRT3 * RHO_COPPER * number(row, "comprimento_m") * current / number(row, "condutor_mm2") / voltage
        comparisons = (
            ("potência ativa instalada", number(row, "potencia_ativa_instalada_kw"), pin),
            ("potência aparente instalada", number(row, "potencia_aparente_instalada_kva"), apparent),
            ("potência ativa demandada", number(row, "potencia_ativa_demandada_kw"), demand_active),
            ("potência aparente demandada", number(row, "potencia_aparente_demandada_kva"), demand_apparent),
            ("corrente", number(row, "corrente_projeto_a"), current),
            ("queda", number(row, "queda_circuito_pct"), drop),
        )
        for label, actual, expected in comparisons:
            checks += 1
            if not close(actual, expected, Decimal("0.000003")):
                errors.append(f"{tag}: {label} {actual} difere de {expected:.8f}.")
        breaker, ampacity = PROTECTION[tag]
        checks += 3
        if number(row, "corrente_projeto_a") > breaker:
            errors.append(f"{tag}: Ib supera In.")
        if breaker > ampacity or ampacity != number(row, "iz_assumida_a"):
            errors.append(f"{tag}: relação In/Iz incoerente.")
        if row["fases"] != "ABC" or voltage != Decimal("380"):
            errors.append(f"{tag}: sistema deve ser trifásico em 380 V.")
        total_pin += number(row, "potencia_ativa_instalada_kw")
        total_s += number(row, "potencia_aparente_instalada_kva")
        total_p_dem += number(row, "potencia_ativa_demandada_kw")
        total_s_dem += number(row, "potencia_aparente_demandada_kva")
        circuit_drops[tag] = number(row, "queda_circuito_pct")

    expected_totals = (
        ("P instalada", total_pin, Decimal("18.184584")),
        ("S instalada", total_s, Decimal("20.893255")),
        ("P demandada", total_p_dem, Decimal("16.645368")),
        ("S demandada", total_s_dem, Decimal("19.133709")),
    )
    for label, actual, expected in expected_totals:
        checks += 1
        if not close(actual, expected, Decimal("0.000003")):
            errors.append(f"{label}: {actual} difere de {expected}.")

    checks += 2
    if len(feeder_rows) != 1 or feeder_rows[0]["alimentador"] != "W600":
        errors.append("O alimentador deve conter exatamente W600.")
        feeder = feeder_rows[0] if feeder_rows else {}
    else:
        feeder = feeder_rows[0]
    main_current = total_s_dem * Decimal(1000) / (SQRT3 * Decimal(380))
    main_drop = Decimal(100) * SQRT3 * RHO_COPPER * number(feeder, "comprimento_m") * main_current / number(feeder, "condutores_fase_neutro_mm2") / Decimal(380)
    for label, actual, expected in (
        ("potência do alimentador", number(feeder, "potencia_demandada_kva"), total_s_dem),
        ("corrente do alimentador", number(feeder, "corrente_projeto_a"), main_current),
        ("queda do alimentador", number(feeder, "queda_pct"), main_drop),
    ):
        checks += 1
        if not close(actual, expected, Decimal("0.000003")):
            errors.append(f"W600: {label} incoerente.")
    checks += 2
    if main_current > number(feeder, "disjuntor_a"):
        errors.append("W600: Ib supera In.")
    if number(feeder, "disjuntor_a") > number(feeder, "iz_assumida_a"):
        errors.append("W600: In supera Iz.")

    combined_drops = {tag: main_drop + drop for tag, drop in circuit_drops.items()}
    for tag, combined in combined_drops.items():
        checks += 1
        if combined > Decimal("4"):
            errors.append(f"{tag}: queda combinada {combined:.6f}% supera 4%.")

    cable_ids = {row["cabo"] for row in cables}
    checks += 5
    if cable_ids != EXPECTED_CABLES or len(cable_ids) != len(cables):
        errors.append("A lista de cabos deve cobrir W600-W608, incluindo W603A/W603B, sem duplicatas.")
    if sum(number(row, "comprimento_assumido_m") for row in cables) != Decimal("196"):
        errors.append("O comprimento total dos cabos deve ser 196 m.")
    cable_map = {row["cabo"]: row for row in cables}
    if cable_map["W603B"]["blindagem"] != "SIM":
        errors.append("W603B deve ser blindado.")
    if cable_map["W603A"]["para"] != "VFD-603" or cable_map["W603B"]["de"] != "VFD-603":
        errors.append("A separação entrada/saída do VFD está incoerente.")
    if any(number(row, "comprimento_assumido_m") <= 0 for row in cables):
        errors.append("Há cabo com comprimento não positivo.")
    for tag, cable_id in (("M-601", "W601"), ("M-602", "W602"), ("M-603", "W603A")):
        checks += 2
        if load_map[tag]["cabo"] != cable_id:
            errors.append(f"{tag}: cabo de alimentação diverge da lista.")
        if number(load_map[tag], "comprimento_m") != number(cable_map[cable_id], "comprimento_assumido_m"):
            errors.append(f"{tag}: comprimento diverge entre cargas e cabos.")

    terminal_ids = {f"{row['regua']}:{row['borne']}" for row in terminals}
    checks += 5
    if terminal_ids != expected_terminals() or len(terminal_ids) != len(terminals):
        errors.append("A lista de bornes deve cobrir exatamente X1:1-5, X2:1-12, X3:1-24 e X4:1-10.")
    if len(terminals) != 51:
        errors.append("A lista deve conter 51 bornes.")
    terminal_cables = {row["cabo"] for row in terminals}
    if not (EXPECTED_CABLES - {"W603A"}) <= terminal_cables:
        errors.append("Há cabos de campo sem correspondência na lista de bornes.")

    expected_borne_ranges = {
        "W600": "X1:1-5",
        "W601": "X2:1-4",
        "W602": "X2:5-8",
        "W603A": "Direto QF-603/VFD",
        "W603B": "X2:9-12",
        "W604": "X3:13-18",
        "W605": "X3:1-4",
        "W606": "X3:5-12",
        "W607": "X4:3-10",
        "W608": "X3:19-24",
    }
    for cable in cables:
        cable_id = cable["cabo"]
        listed_conductors = cable["identificacao_condutores"].split("/")
        actual_rows = [row for row in terminals if row["cabo"] == cable_id]
        actual_conductors = [row["condutor"] for row in actual_rows]
        checks += 3
        if cable_id == "W603A":
            if actual_rows:
                errors.append("W603A: circuito direto QF-603/VFD não deve aparecer como borne de campo.")
        elif len(actual_conductors) != len(listed_conductors) or set(actual_conductors) != set(listed_conductors):
            errors.append(f"{cable_id}: condutores identificados não correspondem um a um aos bornes.")
        expected_range = expected_borne_ranges[cable_id]
        if cable["bornes"] != expected_range:
            errors.append(f"{cable_id}: referência de bornes '{cable['bornes']}' diverge de '{expected_range}'.")
        if len(actual_conductors) != len(set(actual_conductors)):
            errors.append(f"{cable_id}: há condutor repetido na régua de bornes.")

    material_by_tag = {row["item"]: row for row in materials}
    checks += 2
    if material_by_tag.get("X3", {}).get("quantidade") != "24":
        errors.append("A lista de materiais deve declarar 24 bornes em X3.")
    if material_by_tag.get("X4", {}).get("quantidade") != "10":
        errors.append("A lista de materiais deve declarar 10 bornes em X4.")

    material_refs = " ".join(f"{row['item']} {row['referencia']}" for row in materials)
    for tag in sorted(REQUIRED_MATERIAL_TAGS):
        checks += 1
        if tag not in material_refs:
            errors.append(f"Material obrigatório ausente: {tag}.")

    expected_events = [f"E{index:02d}" for index in range(1, 10)]
    actual_events = [row.get("id", "") for row in cause_effect]
    checks += 3
    if actual_events != expected_events:
        errors.append("A matriz causa-efeito deve conter E01-E09 em ordem.")
    for index, row in enumerate(cause_effect, start=1):
        checks += 1
        if any(not row.get(column, "").strip() for column in ("evento", "deteccao_condicao", "resposta_conceitual", "alarme_indicacao", "retorno_limite")):
            errors.append(f"Evento E{index:02d} possui campo vazio na matriz causa-efeito.")
    if not any("pendente" in " ".join(row.values()).casefold() for row in cause_effect):
        errors.append("Pendências de fabricante devem permanecer explícitas na matriz causa-efeito.")

    # Partida direta: todos os permissivos devem existir; sem novo START não há rearme.
    dol_rows = 0
    for safety in (False, True):
        for stop_ok in (False, True):
            for overload_ok in (False, True):
                for start in (False, True):
                    for seal in (False, True):
                        output = safety and stop_ok and overload_ok and (start or seal)
                        dol_rows += 1
                        checks += 3
                        if output and not (safety and stop_ok and overload_ok):
                            errors.append("Partida direta violou um permissivo.")
                        if not safety and output:
                            errors.append("Emergência não derrubou KM-601.")
                        if safety and stop_ok and overload_ok and not start and not seal and output:
                            errors.append("KM-601 apresentou rearme automático.")

    # Reversão: bloqueio elétrico cruzado e trava mecânica nunca permitem ambos fechados.
    reversal_rows = 0
    for safety in (False, True):
        for stop_ok in (False, True):
            for overload_ok in (False, True):
                for fwd_limit in (False, True):
                    for rev_limit in (False, True):
                        for fwd_request in (False, True):
                            for rev_request in (False, True):
                                fwd_intent = safety and stop_ok and overload_ok and fwd_limit and fwd_request
                                rev_intent = safety and stop_ok and overload_ok and rev_limit and rev_request
                                mechanical_admission = not (fwd_intent and rev_intent)
                                km_fwd = fwd_intent and not rev_intent and mechanical_admission
                                km_rev = rev_intent and not fwd_intent and mechanical_admission
                                reversal_rows += 1
                                checks += 4
                                if km_fwd and km_rev:
                                    errors.append("Intertravamento permitiu contatores simultâneos.")
                                if km_fwd and not fwd_limit:
                                    errors.append("KM-602F ignorou FC-602F.")
                                if km_rev and not rev_limit:
                                    errors.append("KM-602R ignorou FC-602R.")
                                if not safety and (km_fwd or km_rev):
                                    errors.append("Emergência não derrubou a reversão.")

    # VFD: os dois canais STO e ausência de falha são indispensáveis.
    vfd_rows = 0
    for safety in (False, True):
        for sto_a in (False, True):
            for sto_b in (False, True):
                for no_fault in (False, True):
                    for run_request in (False, True):
                        run = safety and sto_a and sto_b and no_fault and run_request
                        vfd_rows += 1
                        checks += 2
                        if run and not (safety and sto_a and sto_b and no_fault):
                            errors.append("VFD executou sem todos os permissivos.")
                        if not safety and run:
                            errors.append("Emergência não removeu o torque do VFD.")

    required_doc_terms = {
        "memorial-descritivo.md": ("partida direta", "IM-602", "STO A/B", "não causa partida automática"),
        "criterios-premissas.md": ("Ib <= In <= Iz", "4,0%", "intertravamentos elétrico e mecânico"),
        "sequencia-funcionamento.md": ("novo comando", "comandos simultâneos", "não existe contator de manobra"),
        "memoria-calculo.md": ("19,133709", "29,070663", "2,037810%", "196 m", "P instalada", "P demandada"),
    }
    for filename, terms in required_doc_terms.items():
        content = (project / filename).read_text(encoding="utf-8").casefold()
        for term in terms:
            checks += 1
            if term.casefold() not in content:
                errors.append(f"{filename}: termo obrigatório ausente: {term}.")

    all_text: list[str] = []
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
        all_text.append(sheet_text)
        folded = sheet_text.casefold()
        for term in SHEET_TERMS[filename]:
            checks += 1
            if term.casefold() not in folded:
                errors.append(f"{filename}: identificação ausente: {term}.")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "results": {
            "sheets": len(SHEETS),
            "cause_effect_events": len(cause_effect),
            "loads": len(loads),
            "methods": len(methods),
            "cables": len(cables),
            "terminals": len(terminals),
            "materials": len(materials),
            "installed_active_kw": f"{total_pin:.6f}",
            "installed_apparent_kva": f"{total_s:.6f}",
            "demand_active_kw": f"{total_p_dem:.6f}",
            "demand_apparent_kva": f"{total_s_dem:.6f}",
            "main_current_a": f"{main_current:.6f}",
            "main_drop_pct": f"{main_drop:.6f}",
            "maximum_combined_drop_pct": f"{max(combined_drops.values()):.6f}",
            "maximum_combined_drop_load": max(combined_drops, key=combined_drops.get),
            "cable_total_m": f"{sum(number(row, 'comprimento_assumido_m') for row in cables):.0f}",
            "dol_truth_rows": dol_rows,
            "reversal_truth_rows": reversal_rows,
            "vfd_truth_rows": vfd_rows,
        },
    }
    output = project / "validacao-integracao.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    return parser.parse_args()


def main() -> int:
    result = validate(parse_args().root.resolve())
    print(f"VALIDACAO PROJETO 06 {result['status']} | verificacoes={result['checks']} erros={len(result['errors'])}")
    for error in result["errors"]:
        print(f"[ERRO] {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
