"""Valida dados, cálculos, documentação e DXFs do Projeto 09."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, getcontext
import json
from pathlib import Path
import re
import sys

import ezdxf


getcontext().prec = 28
PROJECT_SLUG = "09-fonte-bancada"
PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from portfolio_config import load_config, required_layers  # noqa: E402


SHEETS = (
    "01_diagrama_blocos.dxf",
    "02_diagrama_eletrico.dxf",
    "03_painel_frontal.dxf",
    "04_layout_interno.dxf",
    "05_detalhes_mecanicos.dxf",
    "06_interligacoes.dxf",
    "07_topologia_regulador_cc_cv.dxf",
    "08_predimensionamento_buck.dxf",
    "09_descarga_saida_parametrica.dxf",
)
REQUIRED_EQUIPMENT = {
    "X1", "PS1", "REG1", "PS2", "M1", "SH1", "K1", "FAN1", "TH1", "TS1",
    "RV1", "RV2", "S2", "X2", "X3", "U1", "QH", "QL", "L1", "RCS",
    "KD1", "RD1", "KD2", "RD2",
}
REQUIRED_PROTECTIONS = {"F1", "S1", "MOV1", "FL1", "F2", "ILIM", "TS1", "PE1"}
REQUIRED_INTERCONNECTIONS = {f"W{index:02d}" for index in range(1, 32)}
REQUIRED_CUTOUTS = {
    "S1", "M1", "RV1", "RV2", "LED-CV", "LED-CC", "S2", "X2-PLUS", "X2-MINUS",
    "X3-PE", "X1", "FAN1", "FAN1-H1", "FAN1-H2", "FAN1-H3", "FAN1-H4",
}
REQUIRED_MATERIALS = {
    "GAB-01", "PNL-01", "X1", "F1", "S1", "MOV1", "FL1", "PS1", "F2",
    "PS2", "M1", "SH1", "K1", "FAN1", "TH1", "TS1", "RV1", "RV2", "S2",
    "LED-01", "LED-02", "LED-03", "X2", "X3", "PE1", "CB-LN", "CB-PE", "CB-POT",
    "CB-SIN", "ETQ-01", "GRD-01", "U1", "QH", "QL", "L1", "RCS", "RIMON", "REG-PASSIVOS",
    "KD1", "RD1", "KD2", "RD2",
}
REQUIRED_REFERENCES = (
    "IEC 61010-1:2010+A1:2016",
    "IEC 60445:2021",
    "IEC 60320-1:2021",
    "IEC 61558-1:2017",
    "IEC 61558-2-16:2021",
    "IEC 60529:1989+A1:1999+A2:2013",
    "IEC 60617",
    "NR-10",
    "2027-05-31",
    "2027-06-01",
    "Portaria MTE 737/2026",
    "LM5190",
    "SNVSCG7",
    "5-80 V",
    "0,8-79 V",
)
SHEET_TERMS = {
    "01_diagrama_blocos.dxf": (
        "90-264 Vca", "0.8-30 Vcc regulados", "PS1", "REG1", "PS2", "M1",
        "PE PERMANENTE NO CHASSI", "SAÍDA CC FLUTUANTE",
    ),
    "02_diagrama_eletrico.dxf": (
        "F1 T4 A", "S1 2P 10 A", "FL1", "MOV1", "PS1", "F2 7,5 A", "REG1",
        "K1 NO", "SH1", "X2 +", "X2 -", "X3 PE", "0,8-30 V REGULADOS", "PE NÃO SECCIONADO",
    ),
    "03_painel_frontal.dxf": (
        "320 mm", "150 mm", "S1", "M1", "RV1", "RV2", "S2", "X2+", "X2-", "X3",
        "SAÍDA FLUTUANTE", "CHASSI", "ESPESSURA PROPOSTA: 3 mm",
    ),
    "04_layout_interno.dxf": (
        "ZONA PRIMÁRIA", "X1/F1/S1", "FL1", "PS1", "REG1", "PS2", "CTRL/M1",
        "FAN1 80 mm", "BARRA PE", "FLUXO DE AR", "NÃO UTILIZAR COMO INSTRUÇÃO DE MONTAGEM",
    ),
    "05_detalhes_mecanicos.dxf": (
        "PAINEL FRONTAL", "PAINEL TRASEIRO", "X1 28x20", "FAN1 D76 / 4xD4", "260 mm REAL",
        "150 mm REAL", "SEM TOLERÂNCIAS GERAIS",
    ),
    "06_interligacoes.dxf": (
        "W01-W06", "W08-W09", "W10-W12", "W13-W16", "0,8-30 V regulados", "W17/W18 SENSE KELVIN",
        "W19-W21", "W22-W24", "W25", "W26-W28", "W29-W31", "W01-W31", "SEÇÕES EM mm²",
    ),
    "07_topologia_regulador_cc_cv.dxf": (
        "U1 | LM5190 (CANDIDATO)", "QH", "QL", "L1", "75 uH", "RCS", "9.1 mOhm",
        "CC e CV", "ISNS+ / VOUT", "0V36", "K1 aberto",
    ),
    "08_predimensionamento_buck.dxf": (
        "100 kHz", "75 uH", "1.20 A / 24%", "1.40 A / 28%", "5.70 A",
        "9.1 mOhm", "6.59 A pico", "8.62 kOhm", "42 V é apenas um cenário",
    ),
    "09_descarga_saida_parametrica.dxf": (
        "C_INT", "C_EXT", "V0_INT_MAX", "V0_PORT_MAX", "V_SAFE", "T_REQ",
        "R_INT_MIN", "R_PORT_MIN", "KD1", "KD2", "A DEFINIR",
        "FONTE EXTERNA CONECTADA", "NÃO GARANTE 0 V",
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


def close(actual: Decimal, expected: Decimal, tolerance: Decimal = Decimal("0.000001")) -> bool:
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


def validate(root: Path) -> dict:
    project = root / PROJECT_SLUG
    config = load_config(root)
    parameters = read_rows(project / "parametros.csv")
    equipment = read_rows(project / "lista-equipamentos.csv")
    protections = read_rows(project / "lista-protecoes.csv")
    interconnections = read_rows(project / "lista-interligacoes.csv")
    cutouts = read_rows(project / "lista-recortes.csv")
    materials = read_rows(project / "lista-materiais.csv")
    calculations = read_rows(project / "resultados-calculo.csv")
    regulator_calculations = read_rows(project / "dimensionamento-regulador.csv")
    discharge_calculations = read_rows(project / "dimensionamento-descarga.csv")
    errors: list[str] = []
    checks = 0

    expected_parameters = {
        "ENTRADA_V_MIN": "90", "ENTRADA_V_MAX": "264", "ENTRADA_F_MIN": "47",
        "ENTRADA_F_MAX": "63", "SAIDA_V_MIN": "0.8", "SAIDA_V_MAX": "30",
        "SAIDA_I_MAX": "5", "SAIDA_P_MAX": "150", "PS1_V_OUT": "36",
        "PS1_I_OUT": "7", "PS1_P_OUT": "252", "PS1_EFICIENCIA": "0.90",
        "REG1_EFICIENCIA": "0.92", "FATOR_POTENCIA": "0.90", "POTENCIA_AUX": "8",
        "F1_CORRENTE": "4", "S1_CORRENTE": "10", "FL1_CORRENTE": "10",
        "MOV1_TENSAO": "275", "F2_CORRENTE": "7.5", "SH1_CORRENTE": "10",
        "SH1_TENSAO": "75", "FAN_TENSAO": "12", "FAN_VAZAO": "20",
        "FAN_DERATING": "0.50", "DELTA_T_ALVO": "15", "TH1_LIGA": "40",
        "TS1_CORTE": "75", "AMBIENTE_T_MIN": "0", "AMBIENTE_T_MAX": "40",
        "ALTITUDE_MAX": "2000", "GRAU_POLUICAO": "2", "GAB_LARGURA": "320",
        "GAB_ALTURA": "150", "GAB_PROFUNDIDADE": "260", "PAINEL_ESPESSURA": "3",
        "RHO_CU": "0.0175", "COMPRIMENTO_36V": "0.5", "SECAO_36V": "2.5",
        "COMPRIMENTO_SAIDA": "0.5", "SECAO_SAIDA": "2.5", "SECAO_LN": "0.75",
        "SECAO_PE": "1.5", "SECAO_SINAL": "0.5",
    }
    parameter_map = {row["parametro"]: row for row in parameters}
    checks += 4
    if set(parameter_map) != set(expected_parameters) or len(parameter_map) != len(parameters):
        errors.append("parametros.csv deve conter exatamente os parâmetros esperados sem duplicatas.")
    if {row["classificacao"] for row in parameters} - {"PREMISSA", "PROPOSTA", "DERIVADO"}:
        errors.append("Parâmetro sem classificação epistemológica permitida.")
    if any(not row["unidade"] or not row["descricao"] for row in parameters):
        errors.append("Parâmetro sem unidade ou descrição.")
    if any(row["classificacao"] in {"CERTIFICADO", "ENSAIADO"} for row in parameters):
        errors.append("Parâmetro não pode declarar certificação ou ensaio.")
    for key, value in expected_parameters.items():
        checks += 1
        if key not in parameter_map or decimal(parameter_map[key]["valor"]) != decimal(value):
            errors.append(f"Parâmetro {key} ausente ou diferente de {value}.")

    p_out = Decimal(30) * Decimal(5)
    p_reg_in = p_out / Decimal("0.92")
    p_ps1_out = p_reg_in + Decimal(8)
    p_input = p_ps1_out / Decimal("0.90")
    i90 = p_input / (Decimal(90) * Decimal("0.90"))
    i127 = p_input / (Decimal(127) * Decimal("0.90"))
    i220 = p_input / (Decimal(220) * Decimal("0.90"))
    ps1_load = p_ps1_out / Decimal(252) * Decimal(100)
    ps1_margin = Decimal(100) - ps1_load
    losses = p_input - p_out
    airflow_min = Decimal("1.76") * losses / Decimal(15)
    airflow_effective = Decimal(20) * Decimal("0.50")
    airflow_margin = airflow_effective / airflow_min
    i36 = p_ps1_out / Decimal(36)
    drop36 = Decimal(2) * Decimal("0.5") * i36 * Decimal("0.0175") / Decimal("2.5")
    drop_output = Decimal(2) * Decimal("0.5") * Decimal(5) * Decimal("0.0175") / Decimal("2.5")
    drop_shunt = Decimal("0.075") * Decimal(5) / Decimal(10)
    loss_shunt = drop_shunt * Decimal(5)
    drop_total = drop_output + drop_shunt
    drop_pct = drop_total / Decimal(30) * Decimal(100)
    derived = {
        "POTENCIA_SAIDA": p_out,
        "POTENCIA_ENTRADA_REG": p_reg_in,
        "POTENCIA_SAIDA_PS1": p_ps1_out,
        "POTENCIA_ENTRADA_TOTAL": p_input,
        "CORRENTE_ENTRADA_90V": i90,
        "CORRENTE_ENTRADA_127V": i127,
        "CORRENTE_ENTRADA_220V": i220,
        "CARGA_PS1": ps1_load,
        "MARGEM_PS1": ps1_margin,
        "PERDAS_INTERNAS": losses,
        "VAZAO_MINIMA": airflow_min,
        "VAZAO_EFETIVA": airflow_effective,
        "MARGEM_VAZAO": airflow_margin,
        "CORRENTE_BARRAMENTO_36V": i36,
        "QUEDA_BARRAMENTO_36V": drop36,
        "QUEDA_CABO_SAIDA": drop_output,
        "QUEDA_SHUNT_5A": drop_shunt,
        "PERDA_SHUNT_5A": loss_shunt,
        "QUEDA_INTERNA_TOTAL": drop_total,
        "QUEDA_INTERNA_30V_PCT": drop_pct,
    }
    result_map = {row["calculo"]: row for row in calculations}
    checks += 4
    if set(result_map) != set(derived) or len(result_map) != len(calculations):
        errors.append("resultados-calculo.csv deve conter exatamente os 20 resultados esperados.")
    if any(row["classificacao"] != "DERIVADO" for row in calculations):
        errors.append("Todo resultado numérico deve estar classificado como DERIVADO.")
    if any(not row["formula"] or not row["observacao"] for row in calculations):
        errors.append("Resultado sem fórmula ou observação.")
    if any(row["classificacao"] == "RESULTADO_EXPERIMENTAL" for row in calculations):
        errors.append("Não há resultados experimentais neste projeto.")
    for key, value in derived.items():
        checks += 1
        if key not in result_map or not close(decimal(result_map[key]["resultado"]), value):
            errors.append(f"Resultado {key} divergente: esperado {value}.")

    design_map = {row["calculo"]: row for row in regulator_calculations}
    fsw = Decimal(100000)
    ripple_target = Decimal(5) * Decimal("0.30")
    l1_h = Decimal(75) / Decimal(1_000_000)
    vin36, vin42 = Decimal(36), Decimal(42)
    vout36, vout42 = vin36 / 2, vin42 / 2
    l_min36 = vout36 * (Decimal(1) - vout36 / vin36) / (ripple_target * fsw)
    l_min42 = vout42 * (Decimal(1) - vout42 / vin42) / (ripple_target * fsw)
    ripple36 = vout36 * (Decimal(1) - vout36 / vin36) / (l1_h * fsw)
    ripple42 = vout42 * (Decimal(1) - vout42 / vin42) / (l1_h * fsw)
    rcs = Decimal("0.0091")
    peak_normal = Decimal(5) + ripple42 / 2
    peak_cbc = Decimal("0.060") / rcs
    average_cbc = peak_cbc - ripple42 / 2
    rimon = Decimal(1) / (rcs * Decimal("0.002") * Decimal(5) + Decimal("0.000025"))
    iset_5a = Decimal(8620) * (Decimal(5) * rcs * Decimal("0.002") + Decimal("0.000025"))
    design_derived = {
        "F_SW": fsw,
        "RIPPLE_ALVO": ripple_target,
        "L_MIN_36V": l_min36 * Decimal(1_000_000),
        "L_MIN_42V": l_min42 * Decimal(1_000_000),
        "L1_PROPOSTA": Decimal(75),
        "DELTA_IL_36V": ripple36,
        "DELTA_IL_42V": ripple42,
        "RCS_PROPOSTA": rcs,
        "I_PEAK_NORMAL": peak_normal,
        "I_PEAK_CBC": peak_cbc,
        "I_MEDIA_CBC": average_cbc,
        "RIMON_CALC": rimon,
        "RIMON_PROPOSTA": Decimal(8620),
        "ISET_5A": iset_5a,
        "P_RCS_5A": Decimal(5) ** 2 * rcs,
        "P_RCS_CBC": average_cbc ** 2 * rcs,
        "V_REG_MIN": Decimal("0.8"),
    }
    design_classes = {
        "F_SW": "PREMISSA", "RIPPLE_ALVO": "DERIVADO", "L_MIN_36V": "DERIVADO",
        "L_MIN_42V": "DERIVADO", "L1_PROPOSTA": "PROPOSTA", "DELTA_IL_36V": "DERIVADO",
        "DELTA_IL_42V": "DERIVADO", "RCS_PROPOSTA": "PROPOSTA", "I_PEAK_NORMAL": "DERIVADO",
        "I_PEAK_CBC": "DERIVADO", "I_MEDIA_CBC": "DERIVADO", "RIMON_CALC": "DERIVADO",
        "RIMON_PROPOSTA": "PROPOSTA", "ISET_5A": "DERIVADO", "P_RCS_5A": "DERIVADO",
        "P_RCS_CBC": "DERIVADO", "V_REG_MIN": "REFERENCIA",
    }
    checks += 4 + len(design_derived)
    if set(design_map) != set(design_derived) or len(regulator_calculations) != len(design_map):
        errors.append("dimensionamento-regulador.csv deve conter os 17 cálculos esperados sem duplicatas.")
    for key, expected in design_derived.items():
        if key not in design_map or not close(decimal(design_map[key]["resultado"]), expected, Decimal("0.00001")):
            errors.append(f"Pré-dimensionamento {key} divergente: esperado {expected}.")
        if key in design_map and design_map[key]["classificacao"] != design_classes[key]:
            errors.append(f"Classificação de pré-dimensionamento incorreta em {key}.")
    if any(not row["formula"] or not row["observacao"] for row in regulator_calculations):
        errors.append("Pré-dimensionamento sem fórmula ou observação.")

    discharge_map = {row["calculo"]: row for row in discharge_calculations}
    expected_discharge = {
        "C_INT_MAX", "C_EXT_MAX", "V_NOM_INT_MAX", "V0_INT_MAX", "V0_PORT_MAX",
        "V_SAFE", "T_REQ", "PULSE_RD1_MAX", "PULSE_RD2_MAX", "E_INT_MAX",
        "E_EXT_MAX", "R_INT_MAX", "R_PORT_MAX", "R_INT_MIN", "R_PORT_MIN",
        "E_RD1_MIN", "E_RD2_MIN", "I_INT_0", "I_PORT_0", "P_INT_0", "P_PORT_0",
        "FEASIBILITY",
    }
    checks += len(expected_discharge) + 4
    if set(discharge_map) != expected_discharge or len(discharge_calculations) != len(discharge_map):
        errors.append("dimensionamento-descarga.csv deve conter exatamente os 22 cálculos esperados sem duplicatas.")
    if any(not row["formula"] or not row["observacao"] for row in discharge_calculations):
        errors.append("Dimensionamento de descarga sem fórmula ou observação.")
    for key, row in discharge_map.items():
        checks += 1
        if key == "V_NOM_INT_MAX":
            if decimal(row["resultado"]) != Decimal(30) or row["classificacao"] != "PROPOSTA":
                errors.append("V_NOM_INT_MAX deve registrar apenas o setpoint nominal proposto de 30 V.")
        elif row["resultado"] != "A DEFINIR" or row["classificacao"] != "PENDENTE":
            errors.append(f"{key} deve permanecer A DEFINIR/PENDENTE sem dados de projeto.")
    expected_formulas = {
        "E_INT_MAX": "0.5*C_INT_MAX*V0_INT_MAX*V0_INT_MAX",
        "E_EXT_MAX": "0.5*C_EXT_MAX*V0_PORT_MAX*V0_PORT_MAX",
        "R_INT_MAX": "T_REQ/[C_INT_MAX*ln(V0_INT_MAX/V_SAFE)]",
        "R_PORT_MAX": "T_REQ/[C_EXT_MAX*ln(V0_PORT_MAX/V_SAFE)]",
        "R_INT_MIN": "V0_INT_MAX*V0_INT_MAX/PULSE_RD1_MAX",
        "R_PORT_MIN": "V0_PORT_MAX*V0_PORT_MAX/PULSE_RD2_MAX",
    }
    for key, formula in expected_formulas.items():
        checks += 1
        if key not in discharge_map or discharge_map[key]["formula"] != formula:
            errors.append(f"Equação paramétrica incorreta ou ausente em {key}.")

    checks += 10
    if p_out != Decimal(150):
        errors.append("Potência máxima de saída deve ser 150 W.")
    if i90 >= Decimal(4):
        errors.append("Corrente estimada a 90 V não deixa margem para F1 de 4 A.")
    if p_ps1_out >= Decimal(252) or ps1_margin <= Decimal(30):
        errors.append("PS1 não apresenta a margem acadêmica mínima de 30%.")
    if airflow_effective <= airflow_min or airflow_margin <= Decimal(2):
        errors.append("Premissa de ventilação não apresenta margem superior a 2.")
    if drop_pct >= Decimal(1):
        errors.append("Queda interna indicativa deve permanecer abaixo de 1% a 30 V.")
    if Decimal("0.75") >= Decimal("1.5"):
        errors.append("PE deve ter seção maior que L/N na premissa adotada.")
    if Decimal(75) <= Decimal(40):
        errors.append("Corte térmico deve estar acima do acionamento do ventilador.")
    if Decimal(36) <= Decimal(30):
        errors.append("Barramento de entrada do buck deve exceder a saída máxima.")
    if Decimal(7) <= i36:
        errors.append("Corrente nominal de PS1 deve exceder a corrente de barramento.")
    if Decimal("7.5") <= Decimal(5):
        errors.append("F2 deve exceder a corrente máxima de saída na proposta.")

    checks += 12
    equipment_tags = {row["tag"] for row in equipment}
    if equipment_tags != REQUIRED_EQUIPMENT or len(equipment) != 24:
        errors.append("lista-equipamentos.csv deve conter exatamente os 24 tags previstos.")
    if any(row["classificacao"] != "PROPOSTA" for row in equipment):
        errors.append("Equipamentos devem ser classificados como PROPOSTA.")
    if any(not row["especificacao"] or not row["observacoes"] for row in equipment):
        errors.append("Equipamento sem especificação ou observação.")

    protection_tags = {row["tag"] for row in protections}
    if protection_tags != REQUIRED_PROTECTIONS or len(protections) != 8:
        errors.append("lista-protecoes.csv deve conter exatamente as oito funções previstas.")
    if any(row["classificacao"] != "PROPOSTA" for row in protections):
        errors.append("Proteções devem ser classificadas como PROPOSTA.")
    if any(not row["funcao"] or not row["observacoes"] for row in protections):
        errors.append("Proteção sem função ou limitação.")

    wire_ids = {row["id"] for row in interconnections}
    if wire_ids != REQUIRED_INTERCONNECTIONS or len(interconnections) != 31:
        errors.append("lista-interligacoes.csv deve conter W01 a W31 sem duplicatas.")
    if any(not row["cor_identificacao"] or not row["terminal"] for row in interconnections):
        errors.append("Interligação sem cor de identificação ou terminal.")
    if any(row["classificacao"] != "PROPOSTA" for row in interconnections):
        errors.append("Interligações devem ser classificadas como PROPOSTA.")

    cutout_ids = {row["item"] for row in cutouts}
    if cutout_ids != REQUIRED_CUTOUTS or len(cutouts) != 16:
        errors.append("lista-recortes.csv deve conter exatamente os 16 recortes.")
    if any(row["classificacao"] != "PROPOSTA" for row in cutouts):
        errors.append("Recortes devem ser classificados como PROPOSTA.")

    material_ids = {row["item"] for row in materials}
    if material_ids != REQUIRED_MATERIALS or len(materials) != 42:
        errors.append("lista-materiais.csv deve conter exatamente os 42 itens esperados.")
    if any(decimal(row["quantidade"]) <= 0 or not row["referencia"] or not row["observacoes"] for row in materials):
        errors.append("Material sem quantidade positiva, referência ou observação.")

    # Envelope completo de V/I da saída: a potência não pode exceder V x I nem 150 W.
    operating_points = 0
    for voltage_tenth in range(0, 301):
        voltage = Decimal(voltage_tenth) / Decimal(10)
        for current_tenth in range(0, 51):
            current = Decimal(current_tenth) / Decimal(10)
            power = voltage * current
            checks += 1
            operating_points += 1
            if power < 0 or power > p_out:
                errors.append(f"Ponto V/I inválido: {voltage} V, {current} A.")

    # Envelope declarado de entrada e frequência para a estimativa de corrente aparente.
    input_points = 0
    for voltage in range(90, 265):
        for frequency in range(47, 64):
            estimated_current = p_input / (Decimal(voltage) * Decimal("0.90"))
            checks += 1
            input_points += 1
            if estimated_current <= 0 or frequency <= 0:
                errors.append(f"Ponto de entrada inválido: {voltage} V, {frequency} Hz.")

    docs = {
        name: (project / name).read_text(encoding="utf-8")
        for name in (
            "README.md", "criterios-premissas.md", "memorial-descritivo.md",
            "memoria-calculo.md", "referencias-normativas.md", "inspecao-visual.md",
        )
    }
    checks += 12
    for name in ("README.md", "criterios-premissas.md", "memorial-descritivo.md"):
        if WARNING not in docs[name]:
            errors.append(f"Aviso obrigatório ausente em {name}.")
    if any(reference not in docs["referencias-normativas.md"] for reference in REQUIRED_REFERENCES):
        errors.append("Referências oficiais ou transição da NR-10 incompletas.")
    if "não um produto desenvolvido, certificado ou liberado para" not in docs["memorial-descritivo.md"]:
        errors.append("Memorial não limita explicitamente fabricação e certificação.")
    if "LM5190 como candidato de referência" not in docs["README.md"] or "compensação" not in docs["README.md"]:
        errors.append("README não explica o status preliminar do controlador e das redes de compensação.")
    if "saída CC é flutuante" not in docs["criterios-premissas.md"]:
        errors.append("Critérios não declaram a saída flutuante.")
    if "0-40 °C" not in docs["criterios-premissas.md"] or "2.000 m" not in docs["criterios-premissas.md"]:
        errors.append("Premissas ambientais incompletas.")
    if re.search(r"\]\(https?://", "\n".join(docs.values()), flags=re.IGNORECASE):
        errors.append("Documentação interna deve usar links Markdown locais relativos.")
    if re.search(r"\b(CPF|RG|telefone|endereço residencial)\b", "\n".join(docs.values()), flags=re.IGNORECASE):
        errors.append("Documentação contém categoria de dado pessoal proibida.")
    if "resultado experimental" in "\n".join(docs.values()).casefold():
        errors.append("Projeto não pode alegar resultado experimental.")
    if "pronto para fabricação" in "\n".join(docs.values()).casefold():
        errors.append("Projeto não pode alegar aptidão para fabricação.")

    source_dir = project / "fonte"
    for index, filename in enumerate(SHEETS, start=1):
        path = source_dir / filename
        checks += 10 + len(SHEET_TERMS[filename])
        try:
            doc = ezdxf.readfile(path)
        except Exception as exc:  # pragma: no cover - evidência externa
            errors.append(f"Falha ao abrir {filename}: {exc}")
            continue
        audit = doc.audit()
        if audit.errors:
            errors.append(f"{filename} contém {len(audit.errors)} erros de auditoria.")
        if doc.dxfversion != "AC1027":
            errors.append(f"{filename} não está em AC1027.")
        if int(doc.header.get("$INSUNITS", 0)) != 4:
            errors.append(f"{filename} não declara milímetros em $INSUNITS.")
        if not set(required_layers(config)) <= {layer.dxf.name for layer in doc.layers}:
            errors.append(f"{filename} não contém todos os layers obrigatórios.")
        if any(entity.dxf.layer == "0" for entity in doc.modelspace()):
            errors.append(f"{filename} contém entidade de produção no layer 0.")
        metadata = doc.ezdxf_metadata()
        if metadata.get("PORTFOLIO_PROJECT") != PROJECT_SLUG:
            errors.append(f"Metadado de projeto incorreto em {filename}.")
        if metadata.get("PORTFOLIO_SHEET") != f"{index:02d}/{len(SHEETS):02d}":
            errors.append(f"Metadado de prancha incorreto em {filename}.")
        if metadata.get("PORTFOLIO_EPISTEMIC_STATUS") != "ACADEMIC_CONCEPT_NOT_FOR_EXECUTION":
            errors.append(f"Status epistemológico incorreto em {filename}.")
        text = extract_text(doc)
        if WARNING not in text:
            errors.append(f"Aviso obrigatório ausente em {filename}.")
        if f"{index:02d}/{len(SHEETS):02d}" not in text:
            errors.append(f"Número de prancha ausente em {filename}.")
        for term in SHEET_TERMS[filename]:
            if term.casefold() not in text.casefold():
                errors.append(f"Termo obrigatório ausente em {filename}: {term}.")

    result = {
        "checks": checks,
        "errors": errors,
        "results": {
            "airflow_effective_cfm": f"{airflow_effective:.6f}",
            "airflow_min_cfm": f"{airflow_min:.6f}",
            "input_current_90v_a": f"{i90:.6f}",
            "input_envelope_points": input_points,
            "internal_loss_w": f"{losses:.6f}",
            "materials": len(materials),
            "operating_envelope_points": operating_points,
            "output_power_w": f"{p_out:.6f}",
            "sheets": len(SHEETS),
            "wires": len(interconnections),
        },
        "status": "PASS" if not errors else "FAIL",
    }
    report = project / "validacao-fonte.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return parser.parse_args()


def main() -> int:
    result = validate(parse_args().root.resolve())
    print(f"VALIDACAO PROJETO 09 {result['status']} | verificacoes={result['checks']} erros={len(result['errors'])}")
    for error in result["errors"]:
        print(f"- {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
