"""Valida arquitetura, cálculos e intertravamentos do Projeto 07."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, getcontext
import itertools
import json
import math
from pathlib import Path
import sys

import ezdxf


getcontext().prec = 28
PROJECT_SLUG = "07-arquitetura-veiculo-eletrico"
PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from portfolio_config import load_config, required_layers  # noqa: E402


SHEETS = (
    "01_arquitetura_geral.dxf",
    "02_circuito_alta_tensao.dxf",
    "03_circuito_baixa_tensao.dxf",
    "04_pre_carga_contatores.dxf",
    "05_inversor_motor.dxf",
    "06_sensores_controle.dxf",
    "07_rede_comunicacao.dxf",
    "08_layout_componentes.dxf",
    "09_interfaces_resposta_falhas.dxf",
    "10_estudo_pre_carga_parametrico.dxf",
    "11_sequencia_temporal_pre_carga.dxf",
)
REQUIRED_MATERIAL_TAGS = {
    "BAT-HV-701", "BMS-701", "MSD-701", "F701", "KMN-701", "KMP-701",
    "KPR-701", "RPR-701", "CCDC-701", "PDU-HV-701", "F711", "F712",
    "INV-701", "IM-701", "DCDC-701", "BAT-LV-701", "PDU-LV-701",
    "VCU-701", "IMD-701", "SDE-701", "HVIL-701", "SEN-VBAT-701",
    "SEN-VDC-701", "SEN-IDC-701", "APPS1-701", "APPS2-701", "BPS1-701",
    "BPS2-701", "RES-701", "RT-CAN-701A", "RT-CAN-701B",
}
REQUIRED_SIGNALS = {
    "SEN-VBAT-701", "SEN-VDC-701", "SEN-IDC-701", "IMD-701", "HVIL-701",
    "SDE-701", "CRASH-701", "APPS1-701", "APPS2-701", "BPS1-701",
    "BPS2-701", "IU-701", "IV-701", "IW-701", "RES-701", "TMOT-701",
    "TINV-701", "TBAT-701",
}
REQUIRED_CABLES = {
    "WHV01", "WHV02", "WHV03", "WHV04", "WHV05", "WHV06",
    "WLV01", "WLV02", "WLV03", "WCAN01", "WSEN01", "WHVIL01",
}
REQUIRED_MESSAGES = {
    "BMS_STATUS", "BMS_LIMITS", "VCU_TORQUE_CMD", "INV_STATUS",
    "DCDC_STATUS", "VCU_STATE", "DIAG_REQUEST", "DIAG_RESPONSE",
}
SHEET_TERMS = {
    "01_arquitetura_geral.dxf": (
        "BAT-HV-701", "INV-701", "IM-701", "DCDC-701", "BAT-LV-701",
        "VCU-701", "BMS-701", "CAN-PT", "RESULTADO EXPERIMENTAL: NENHUM",
    ),
    "02_circuito_alta_tensao.dxf": (
        "MSD-701", "F701 250 A", "KMP-701", "KMN-701", "KPR-701",
        "RPR", "PDU-HV-701", "IMD-701", "POLOS HV NÃO ATERRADOS",
    ),
    "03_circuito_baixa_tensao.dxf": (
        "BAT-LV-701", "DCDC-701", "PDU-LV-701", "VCU-701", "BMS-701",
        "SDE-701", "HVIL-701", "CRASH-701", "DRV-KM",
    ),
    "04_pre_carga_contatores.dxf": (
        "OFF", "CHECK", "PRECHARGE", "READY", "FAULT", "VDC/VBAT",
        "KMP-701", "KMN-701", "KPR-701", "0,506569",
    ),
    "05_inversor_motor.dxf": (
        "V/f", "FOC", "CLARKE/PARK", "SVPWM", "id*", "iq*", "IM-701",
        "RESULTADO EXPERIMENTAL",
    ),
    "06_sensores_controle.dxf": (
        "APPS1/2", "BPS1/2", "SDE-701", "CRASH-701", "HVIL-701",
        "IU / IV / IW", "SEN-VDC", "RES-701", "TMOT / TINV",
    ),
    "07_rede_comunicacao.dxf": (
        "CAN-PT", "500 kbit/s", "120 ohm", "BMS_STATUS", "VCU_TORQUE_CMD",
        "INV_STATUS", "CAN-DIAG", "SOBD-701",
    ),
    "08_layout_componentes.dxf": (
        "BAT-HV-701", "PDU-HV", "INV-701", "IM-701", "DCDC", "BAT-LV",
        "VCU-701", "BMS-701", "ROTA HV", "CAN-PT",
    ),
    "09_interfaces_resposta_falhas.dxf": (
        "MATRIZ DE FALHAS", "SDE / HVIL", "SEN-VDC-701", "APPS1-701",
        "BMS_LIMITS", "RES-701", "NAO E HARA", "PENDENCIA REAL",
    ),
    "10_estudo_pre_carga_parametrico.dxf": (
        "RESPOSTA RC NORMALIZADA", "VDC / VBAT [%]", "t90 = 0,507 s",
        "VDC @90% [V]", "I0 [A]", "P0 [kW]", "EC FINAL [J]", "ER @90% [J]",
        "0,993431 s", "RPR-701",
    ),
    "11_sequencia_temporal_pre_carga.dxf": (
        "SEQUÊNCIA TEMPORAL DA PRÉ-CARGA", "VDC / VBAT [%]",
        "VDC/VBAT - R=100 ohm / C=2,2 mF", "SEQ PRE-CARGA 04",
        "t90 ideal = 0,506569 s", "Timeout proposto = 1,50 s",
        "PRECHARGE | t = 0", "VDC/VBAT >= 90%", "KMP CONFIRMADO",
        "FAULT", "0,993431 s", "TBD",
    ),
}
WARNING = (
    "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, "
    "instalação ou execução de serviços sem revisão, dimensionamento e "
    "responsabilidade de profissional legalmente habilitado."
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def decimal(value: str) -> Decimal:
    return Decimal(value.replace(",", "."))


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


def validate(root: Path) -> dict:
    project = root / PROJECT_SLUG
    config = load_config(root)
    parameters = read_rows(project / "parametros.csv")
    signals = read_rows(project / "lista-sinais.csv")
    messages = read_rows(project / "rede-can.csv")
    faults = read_rows(project / "matriz-interfaces-falhas.csv")
    cables = read_rows(project / "lista-cabos.csv")
    materials = read_rows(project / "lista-materiais.csv")
    errors: list[str] = []
    checks = 0

    parameter_map = {row["parametro"]: row for row in parameters}
    expected_parameters = {
        "VBAT_NOMINAL", "VBAT_MIN", "VBAT_MAX", "ENERGIA_BATERIA", "P_MOTOR",
        "ETA_INVERSOR", "P_DCDC", "C_ELO_CC", "R_PRE_CARGA",
        "LIMIAR_PRE_CARGA", "TIMEOUT_PRE_CARGA", "FUSIVEL_PRINCIPAL",
        "TENSAO_AUXILIAR", "TENSAO_DCDC", "CAN_PT_BITRATE",
    }
    checks += 3
    if set(parameter_map) != expected_parameters or len(parameter_map) != len(parameters):
        errors.append("parametros.csv deve conter os 15 parâmetros esperados sem duplicatas.")
    if {row["classificacao"] for row in parameters} - {"PREMISSA", "PROPOSTA"}:
        errors.append("Parâmetro numérico sem classificação PREMISSA ou PROPOSTA.")
    if any(not row["unidade"] or not row["descricao"] for row in parameters):
        errors.append("Parâmetro sem unidade ou descrição.")

    expected_values = {
        "VBAT_NOMINAL": Decimal("400"),
        "VBAT_MIN": Decimal("320"),
        "VBAT_MAX": Decimal("450"),
        "ENERGIA_BATERIA": Decimal("60"),
        "P_MOTOR": Decimal("60000"),
        "ETA_INVERSOR": Decimal("0.95"),
        "P_DCDC": Decimal("3000"),
        "C_ELO_CC": Decimal("0.0022"),
        "R_PRE_CARGA": Decimal("100"),
        "LIMIAR_PRE_CARGA": Decimal("0.90"),
        "TIMEOUT_PRE_CARGA": Decimal("1.5"),
        "FUSIVEL_PRINCIPAL": Decimal("250"),
        "TENSAO_AUXILIAR": Decimal("12"),
        "TENSAO_DCDC": Decimal("14"),
        "CAN_PT_BITRATE": Decimal("500"),
    }
    for key, expected in expected_values.items():
        checks += 1
        if key not in parameter_map or decimal(parameter_map[key]["valor"]) != expected:
            errors.append(f"Parâmetro {key} ausente ou diferente de {expected}.")

    p_motor = expected_values["P_MOTOR"]
    eta = expected_values["ETA_INVERSOR"]
    p_dcdc = expected_values["P_DCDC"]
    vmin = expected_values["VBAT_MIN"]
    vnom = expected_values["VBAT_NOMINAL"]
    vmax = expected_values["VBAT_MAX"]
    resistance = expected_values["R_PRE_CARGA"]
    capacitance = expected_values["C_ELO_CC"]
    target = expected_values["LIMIAR_PRE_CARGA"]
    bus_current = (p_motor / eta + p_dcdc) / vmin
    tau = resistance * capacitance
    t90 = -tau * Decimal(str(math.log(float(Decimal(1) - target))))
    initial_current = vnom / resistance
    initial_power = vnom * vnom / resistance
    energy_nominal = Decimal("0.5") * capacitance * vnom * vnom
    energy_max = Decimal("0.5") * capacitance * vmax * vmax
    expected_calculations = (
        ("corrente HV", bus_current, Decimal("206.743421"), Decimal("0.000001")),
        ("tau", tau, Decimal("0.220000"), Decimal("0.000001")),
        ("t90", t90, Decimal("0.506569"), Decimal("0.000001")),
        ("corrente inicial", initial_current, Decimal("4.000000"), Decimal("0.000001")),
        ("potência inicial", initial_power, Decimal("1600.000000"), Decimal("0.000001")),
        ("energia nominal", energy_nominal, Decimal("176.000000"), Decimal("0.000001")),
        ("energia máxima", energy_max, Decimal("222.750000"), Decimal("0.000001")),
    )
    for label, actual, expected, tolerance in expected_calculations:
        checks += 1
        if abs(actual - expected) > tolerance:
            errors.append(f"Cálculo de {label} incoerente: {actual}.")

    precharge_voltage_cases = (
        (vmin, Decimal("288"), Decimal("3.2"), Decimal("1.024"), Decimal("112.64"), Decimal("111.5136")),
        (vnom, Decimal("360"), Decimal("4.0"), Decimal("1.600"), Decimal("176.00"), Decimal("174.2400")),
        (vmax, Decimal("405"), Decimal("4.5"), Decimal("2.025"), Decimal("222.75"), Decimal("220.5225")),
    )
    calculated_cases: list[dict[str, str]] = []
    for voltage, expected_vdc, expected_i0, expected_p0_kw, expected_ec, expected_er90 in precharge_voltage_cases:
        vdc90 = target * voltage
        current0 = voltage / resistance
        power0_kw = voltage * voltage / resistance / Decimal("1000")
        capacitor_energy = Decimal("0.5") * capacitance * voltage * voltage
        resistor_energy90 = capacitor_energy * (Decimal("1") - (Decimal("1") - target) ** 2)
        expected_row = (expected_vdc, expected_i0, expected_p0_kw, expected_ec, expected_er90)
        actual_row = (vdc90, current0, power0_kw, capacitor_energy, resistor_energy90)
        for label, actual, expected in zip(("VDC90", "I0", "P0", "Ec", "Er90"), actual_row, expected_row):
            checks += 1
            if abs(actual - expected) > Decimal("0.000001"):
                errors.append(f"Caso de pré-carga {voltage} V: {label}={actual}, esperado {expected}.")
        calculated_cases.append({
            "vbat_v": f"{voltage:.0f}",
            "vdc_90_v": f"{vdc90:.2f}",
            "initial_current_a": f"{current0:.6f}",
            "initial_power_kw": f"{power0_kw:.6f}",
            "capacitor_energy_j": f"{capacitor_energy:.6f}",
            "resistor_energy_at_90_j": f"{resistor_energy90:.6f}",
        })
    ideal_time_margin = expected_values["TIMEOUT_PRE_CARGA"] - t90
    checks += 2
    if abs(ideal_time_margin - Decimal("0.993431")) > Decimal("0.000001"):
        errors.append(f"Margem de tempo ideal incoerente: {ideal_time_margin}.")
    if ideal_time_margin <= 0:
        errors.append("Timeout deve exceder o tempo RC ideal até o limiar.")
    checks += 3
    if bus_current >= expected_values["FUSIVEL_PRINCIPAL"]:
        errors.append("Corrente estimada deve ser inferior ao fusível conceitual.")
    if not (expected_values["VBAT_MIN"] < vnom < expected_values["VBAT_MAX"]):
        errors.append("Faixa de tensão da bateria incoerente.")
    if t90 >= expected_values["TIMEOUT_PRE_CARGA"]:
        errors.append("Timeout proposto não excede o tempo RC ideal até 90%.")

    signal_tags = {row["tag"] for row in signals}
    checks += 5
    if signal_tags != REQUIRED_SIGNALS or len(signal_tags) != len(signals):
        errors.append("lista-sinais.csv não contém exatamente os 18 sinais esperados.")
    if len(signals) != 18:
        errors.append("A lista de sinais deve conter 18 registros.")
    if not {"APPS1-701", "APPS2-701", "BPS1-701", "BPS2-701"} <= signal_tags:
        errors.append("Canais duplos de acelerador e freio estão incompletos.")
    if any(not row["reacao_falha"] or not row["prancha"] for row in signals):
        errors.append("Sinal sem reação de falha ou referência de prancha.")
    valid_sheet_refs = {f"{index:02d}/{len(SHEETS):02d}" for index in range(1, len(SHEETS) + 1)}
    if any(row["prancha"] not in valid_sheet_refs for row in signals):
        errors.append("Referência de prancha inválida na lista de sinais.")

    expected_fault_fields = {
        "evento", "entrada_deteccao", "reacao_proposta", "estado_resultante",
        "lacuna_validacao", "rastreio",
    }
    valid_fault_schema = bool(faults) and set(faults[0]) == expected_fault_fields
    checks += 4
    if not valid_fault_schema:
        errors.append("A matriz de interfaces e falhas deve conter os campos rastreáveis esperados.")
    if valid_fault_schema and (len(faults) < 8 or len({row["evento"] for row in faults}) != len(faults)):
        errors.append("A matriz deve ter ao menos oito eventos únicos.")
    if valid_fault_schema and any(not all(row[field].strip() for field in expected_fault_fields) for row in faults):
        errors.append("Evento da matriz sem detecção, resposta, estado, lacuna ou rastreio.")

    cable_ids = {row["cabo"] for row in cables}
    checks += 6
    if cable_ids != REQUIRED_CABLES or len(cable_ids) != len(cables):
        errors.append("lista-cabos.csv não contém exatamente os 12 cabos esperados.")
    if len(cables) != 12:
        errors.append("A lista de cabos deve conter 12 registros.")
    if any(decimal(row["comprimento_assumido_m"]) <= 0 for row in cables):
        errors.append("Há cabo com comprimento não positivo.")
    if next(row for row in cables if row["cabo"] == "WHV05")["blindagem"] != "SIM":
        errors.append("WHV05 deve ser identificado como blindado.")
    if any("Laranja" not in row["observacoes"] for row in cables if row["dominio"] in {"HV", "HV_AC"}):
        errors.append("Cabo HV sem identificação laranja nas observações.")
    if next(row for row in cables if row["cabo"] == "WCAN01")["formacao"] != "1 par trançado":
        errors.append("WCAN01 deve ser par trançado.")

    message_names = {row["mensagem"] for row in messages}
    message_ids = {row["id_can_assumido"] for row in messages}
    checks += 7
    if message_names != REQUIRED_MESSAGES or len(message_names) != len(messages):
        errors.append("rede-can.csv não contém exatamente as oito mensagens esperadas.")
    if len(message_ids) != len(messages):
        errors.append("Há identificadores CAN duplicados.")
    if any(not row["id_can_assumido"].startswith("0x") for row in messages):
        errors.append("ID CAN fora da representação hexadecimal proposta.")
    if any(int(row["periodo_ms_assumido"]) <= 0 for row in messages):
        errors.append("Período CAN não positivo.")
    if any(int(row["timeout_ms_assumido"]) <= int(row["periodo_ms_assumido"]) for row in messages):
        errors.append("Timeout CAN deve exceder o período da mensagem.")
    if any(not row["acao_timeout"] for row in messages):
        errors.append("Mensagem CAN sem ação de timeout.")
    if decimal(parameter_map["CAN_PT_BITRATE"]["valor"]) != Decimal("500"):
        errors.append("Taxa CAN-PT diverge da premissa de 500 kbit/s.")

    material_text = " ".join(f"{row['referencia']} {row['descricao']}" for row in materials)
    for tag in sorted(REQUIRED_MATERIAL_TAGS):
        checks += 1
        if tag not in material_text:
            errors.append(f"Material obrigatório ausente: {tag}.")
    checks += 4
    if len(materials) != 35:
        errors.append("A lista de materiais deve conter 35 registros.")
    if len({row["item"] for row in materials}) != len(materials):
        errors.append("Há itens duplicados na lista de materiais.")
    if "RT-CAN-701A/RT-CAN-701B" not in material_text:
        errors.append("As duas terminações CAN não estão materializadas.")
    if any(decimal(row["quantidade"]) <= 0 for row in materials):
        errors.append("Há material com quantidade não positiva.")

    precharge_rows = 0
    for values in itertools.product((False, True), repeat=9):
        lv_ok, bms_ok, hvil_ok, iso_ok, no_emergency, no_crash, request, voltage_ok, timeout = values
        permissive = lv_ok and bms_ok and hvil_ok and iso_ok and no_emergency and no_crash and request
        ready = permissive and voltage_ok and not timeout
        precharge = permissive and not voltage_ok and not timeout
        kmn = ready or precharge
        kmp = ready
        kpr = precharge
        precharge_rows += 1
        checks += 7
        if kmp and kpr:
            errors.append("KMP e KPR fecharam simultaneamente.")
        if kmp and not voltage_ok:
            errors.append("KMP fechou sem confirmação de VDC/VBAT.")
        if kpr and voltage_ok:
            errors.append("KPR permaneceu fechado após confirmação de tensão.")
        if timeout and (kmn or kmp or kpr):
            errors.append("Timeout não abriu todos os contatores.")
        if not no_emergency and (kmn or kmp or kpr):
            errors.append("Emergência não abriu todos os contatores.")
        if (not hvil_ok or not iso_ok or not no_crash) and (kmn or kmp or kpr):
            errors.append("Permissivo crítico não bloqueou a alta tensão.")
        if ready and not (kmn and kmp and not kpr):
            errors.append("Estado READY gerou combinação incorreta de contatores.")

    torque_rows = 0
    for values in itertools.product((False, True), repeat=7):
        ready, inverter_ready, apps_valid, brake_allows, bms_allows, comm_ok, torque_request = values
        torque_enabled = all(values)
        torque_rows += 1
        checks += 3
        if torque_enabled and not ready:
            errors.append("Torque habilitado fora de READY.")
        if torque_enabled and not (apps_valid and brake_allows and bms_allows and comm_ok):
            errors.append("Torque habilitado com permissivo inválido.")
        if not torque_request and torque_enabled:
            errors.append("Torque habilitado sem solicitação.")

    required_doc_terms = {
        "README.md": ("Resultado experimental | nenhum", "V/f", "FOC", "matriz-interfaces-falhas.csv", "10_estudo_pre_carga_parametrico.dxf", "11_sequencia_temporal_pre_carga.dxf", WARNING),
        "criterios-premissas.md": ("Fatos técnicos", "Premissas acadêmicas", "Propostas conceituais", "Limitações"),
        "memorial-descritivo.md": ("Fluxo de energia", "Pré-carga", "Interfaces e falhas", "Não afirma", "TCC"),
        "estrategias-controle.md": ("controle escalar", "controle vetorial", "Clarke", "Park", "resultados experimentais"),
        "sequencia-funcionamento.md": ("OFF", "PRECHARGE", "READY", "FAULT", "novo ciclo de chave", "prancha 11", "0,506569 s", "0,993431 s"),
        "memoria-calculo.md": ("206,743421", "0,506569", "176,000000", "222,750000", "Faixa de tensão proposta", "111,51 J", "220,52 J", "0,993431 s", "não resultados experimentais"),
        "referencias-normativas.md": ("ISO 6469-3:2021", "ISO 26262:2018", "ISO 11898-2:2026", "Regulamento ONU nº 100"),
    }
    for filename, terms in required_doc_terms.items():
        content = (project / filename).read_text(encoding="utf-8")
        folded = content.casefold()
        for term in terms:
            checks += 1
            if term.casefold() not in folded:
                errors.append(f"{filename}: termo obrigatório ausente: {term}.")

    all_text: list[str] = []
    required_layer_names = set(required_layers(config))
    for index, filename in enumerate(SHEETS, start=1):
        path = project / "fonte" / filename
        checks += 9
        if not path.is_file():
            errors.append(f"DXF ausente: {filename}.")
            continue
        try:
            doc = ezdxf.readfile(path)
            audit = doc.audit()
        except Exception as exc:
            errors.append(f"Falha ao abrir {filename}: {exc}")
            continue
        if audit.has_errors:
            errors.append(f"{filename}: auditoria ezdxf encontrou {len(audit.errors)} erro(s).")
        if doc.dxfversion != "AC1027":
            errors.append(f"{filename}: versão DXF não é AC1027.")
        if int(doc.header.get("$INSUNITS", -1)) != 4:
            errors.append(f"{filename}: $INSUNITS não é milímetro.")
        if (float(doc.header["$LIMMAX"][0]), float(doc.header["$LIMMAX"][1])) != (420.0, 297.0):
            errors.append(f"{filename}: limites não correspondem à folha A3.")
        if not required_layer_names <= {layer.dxf.name for layer in doc.layers}:
            errors.append(f"{filename}: layers obrigatórios ausentes.")
        metadata = doc.ezdxf_metadata()
        if metadata.get("PORTFOLIO_PROJECT") != PROJECT_SLUG:
            errors.append(f"{filename}: metadado de projeto incorreto.")
        if metadata.get("PORTFOLIO_SHEET") != f"{index:02d}/{len(SHEETS):02d}":
            errors.append(f"{filename}: metadado de prancha incorreto.")
        if metadata.get("PORTFOLIO_EPISTEMIC_STATUS") != "ACADEMIC_CONCEPT_NO_EXPERIMENTAL_RESULTS":
            errors.append(f"{filename}: metadado epistemológico ausente.")
        sheet_text = extract_text(doc)
        all_text.append(sheet_text)
        folded = sheet_text.casefold()
        if WARNING.casefold() not in folded:
            errors.append(f"{filename}: aviso obrigatório ausente.")
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
            "parameters": len(parameters),
            "signals": len(signals),
            "can_messages": len(messages),
            "cables": len(cables),
            "materials": len(materials),
            "fault_scenarios": len(faults),
            "estimated_hv_current_a": f"{bus_current:.6f}",
            "precharge_tau_s": f"{tau:.6f}",
            "precharge_t90_s": f"{t90:.6f}",
            "precharge_initial_current_a": f"{initial_current:.6f}",
            "precharge_initial_power_w": f"{initial_power:.6f}",
            "dc_link_energy_400v_j": f"{energy_nominal:.6f}",
            "dc_link_energy_450v_j": f"{energy_max:.6f}",
            "precharge_voltage_cases": calculated_cases,
            "precharge_ideal_time_margin_s": f"{ideal_time_margin:.6f}",
            "precharge_truth_rows": precharge_rows,
            "torque_truth_rows": torque_rows,
            "experimental_results_claimed": False,
        },
    }
    output = project / "validacao-arquitetura.json"
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return parser.parse_args()


def main() -> int:
    result = validate(parse_args().root.resolve())
    print(
        f"VALIDACAO PROJETO 07 {result['status']} | "
        f"verificacoes={result['checks']} erros={len(result['errors'])}"
    )
    for error in result["errors"]:
        print(f"[ERRO] {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
