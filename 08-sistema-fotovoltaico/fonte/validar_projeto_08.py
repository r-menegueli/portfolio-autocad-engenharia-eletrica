"""Valida configuração, cálculos e documentação do Projeto 08."""

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
PROJECT_SLUG = "08-sistema-fotovoltaico"
PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from portfolio_config import load_config, required_layers  # noqa: E402


SHEETS = (
    "01_disposicao_modulos.dxf",
    "02_diagrama_unifilar_cc.dxf",
    "03_diagrama_unifilar_ca.dxf",
    "04_string_box.dxf",
    "05_aterramento.dxf",
    "06_layout_equipamentos.dxf",
)
REQUIRED_PROTECTIONS = {
    "F-S1-P", "F-S1-N", "F-S2-P", "F-S2-N", "DPS-CC-1", "DPS-CC-2",
    "QDC-1", "QDC-2", "QSD-CA", "DPS-CA", "QF-CA",
}
REQUIRED_CABLES = {"FV-S1", "FV-S2", "CA-INV", "CA-PCC", "PE-MOD", "PE-EQP", "COM-INV"}
REQUIRED_MATERIAL_ITEMS = {
    "MOD-FV", "INV-FV", "SB-FV", "F-GPV", "PF-GPV", "DPS-CC", "SEC-CC",
    "DPS-CA", "SEC-CA", "DJ-CA", "QD-FV", "BEP", "CB-CC", "CB-CA", "CB-PE",
    "CON-FV", "EST-MOD", "ETQ-CC", "ELET-CC", "ELET-CA", "MED-BI",
}
REQUIRED_REFERENCES = (
    "ABNT NBR 16690:2019",
    "ABNT NBR 5410:2004",
    "ABNT NBR 5419",
    "2026",
    "IEC 62548-1:2023",
    "IEC 60364-7-712:2025",
    "IEC 61643-31:2018",
    "Lei nº 14.300",
    "REN ANEEL nº 1.000/2021",
    "REN nº 1.059/2023",
    "PRODIST",
    "Portarias Inmetro nº 140/2022",
    "nº 515/2023",
)
SHEET_TERMS = {
    "01_disposicao_modulos.dxf": (
        "6,60 kWp", "12 x 550 Wp", "S1: 6 MÓDULOS EM SÉRIE",
        "S2: 6 MÓDULOS EM SÉRIE", "NORTE", "M01", "M12",
    ),
    "02_diagrama_unifilar_cc.dxf": (
        "SEM PARALELISMO", "2 x gPV 20 A", "DPS T2 FV 600 V",
        "QDC 2P 32 A", "MPPT 1", "MPPT 2", "POLOS CC NÃO ATERRADOS",
        "324,550 V", "216,942 V",
    ),
    "03_diagrama_unifilar_ca.dxf": (
        "INV-FV-801", "QSD-CA 2P 40 A", "DPS-CA T2", "QF-CA 2P 40 A",
        "MED-801 BIDIRECIONAL", "PCC-801", "ANTI-ILHAMENTO",
    ),
    "04_string_box.dxf": (
        "SB-FV-801", "F-S1-P", "F-S1-N", "F-S2-P", "F-S2-N",
        "DPS-CC-1", "DPS-CC-2", "QDC-1", "QDC-2", "BARRA PE",
    ),
    "05_aterramento.dxf": (
        "MOLDURAS", "EST-FV-801", "SB-FV-801", "INV-FV-801", "QD-FV-801",
        "BEP-801", "SPDA EXISTENTE", "NBR 5419:2026", "POLOS CC NÃO INTENCIONALMENTE ATERRADOS",
    ),
    "06_layout_equipamentos.dxf": (
        "12 MÓDULOS", "SB-FV-801", "INV-FV-801", "QD-FV-801", "MED-801",
        "PCC-801", "R-CC-801/802", "R-CA-801", "ROTAS CC E CA SEGREGADAS",
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


def close(actual: Decimal, expected: Decimal, tolerance: Decimal = Decimal("0.000001")) -> bool:
    return abs(actual - expected) <= tolerance


def validate(root: Path) -> dict:
    project = root / PROJECT_SLUG
    config = load_config(root)
    parameters = read_rows(project / "parametros.csv")
    modules = read_rows(project / "lista-modulos.csv")
    protections = read_rows(project / "lista-protecoes.csv")
    cables = read_rows(project / "lista-cabos.csv")
    materials = read_rows(project / "lista-materiais.csv")
    calculations = read_rows(project / "resultados-calculo.csv")
    errors: list[str] = []
    checks = 0

    parameter_map = {row["parametro"]: row for row in parameters}
    expected_parameters = {
        "MODULO_POTENCIA": "550", "QUANTIDADE_MODULOS": "12", "MODULOS_POR_STRING": "6",
        "QUANTIDADE_STRINGS": "2", "VMP_MODULO": "41.8", "IMP_MODULO": "13.16",
        "VOC_MODULO": "49.9", "ISC_MODULO": "13.92", "COEF_VOC": "-0.0028",
        "COEF_VMP": "-0.0030", "COEF_ISC": "0.0005", "TEMP_REF": "25",
        "TEMP_MIN": "-5", "TEMP_CEL_MAX": "70", "IRRAD_MAX": "1100",
        "INV_POT_CA": "6000", "INV_TENSAO_CA": "220", "INV_MPPT_MIN": "90",
        "INV_MPPT_MAX": "550", "INV_VDC_MAX": "600", "INV_CORRENTE_MPPT_MAX": "16",
        "INV_ISC_MPPT_MAX": "20", "HSP": "5.2", "PR": "0.78",
        "COMPRIMENTO_CC": "20", "SECAO_CC": "6", "COMPRIMENTO_CA": "15",
        "SECAO_CA": "10", "RHO_CU": "0.0175", "DISJUNTOR_CA": "40",
        "FUSIVEL_STRING": "20", "FUSIVEL_SERIE_MODULO": "25", "DPS_CC_UCPV": "600",
        "DPS_CA_UC": "275", "PE_SECAO": "6",
    }
    checks += 4
    if set(parameter_map) != set(expected_parameters) or len(parameter_map) != len(parameters):
        errors.append("parametros.csv deve conter os 35 parâmetros esperados sem duplicatas.")
    if {row["classificacao"] for row in parameters} - {"PREMISSA", "PROPOSTA"}:
        errors.append("Parâmetro numérico sem classificação PREMISSA ou PROPOSTA.")
    if any(not row["unidade"] or not row["descricao"] for row in parameters):
        errors.append("Parâmetro sem unidade ou descrição.")
    if len(parameters) != 35:
        errors.append("Quantidade de parâmetros diferente de 35.")
    for key, value in expected_parameters.items():
        checks += 1
        if key not in parameter_map or decimal(parameter_map[key]["valor"]) != decimal(value):
            errors.append(f"Parâmetro {key} ausente ou diferente de {value}.")

    pmod = decimal(expected_parameters["MODULO_POTENCIA"])
    nmod = decimal(expected_parameters["QUANTIDADE_MODULOS"])
    nseries = decimal(expected_parameters["MODULOS_POR_STRING"])
    nstrings = decimal(expected_parameters["QUANTIDADE_STRINGS"])
    vmp = decimal(expected_parameters["VMP_MODULO"])
    imp = decimal(expected_parameters["IMP_MODULO"])
    voc = decimal(expected_parameters["VOC_MODULO"])
    isc = decimal(expected_parameters["ISC_MODULO"])
    beta_voc = decimal(expected_parameters["COEF_VOC"])
    beta_vmp = decimal(expected_parameters["COEF_VMP"])
    alpha_isc = decimal(expected_parameters["COEF_ISC"])
    tref = decimal(expected_parameters["TEMP_REF"])
    tmin = decimal(expected_parameters["TEMP_MIN"])
    tmax = decimal(expected_parameters["TEMP_CEL_MAX"])
    gmax = decimal(expected_parameters["IRRAD_MAX"])
    pac = decimal(expected_parameters["INV_POT_CA"])
    vac = decimal(expected_parameters["INV_TENSAO_CA"])
    rho = decimal(expected_parameters["RHO_CU"])

    pdc = pmod * nmod
    ratio = pdc / pac
    vmp_string = vmp * nseries
    voc_string = voc * nseries
    voc_cold = voc_string * (Decimal(1) + beta_voc * (tmin - tref))
    vmp_hot = vmp_string * (Decimal(1) + beta_vmp * (tmax - tref))
    isc_corrected = isc * (gmax / Decimal(1000)) * (Decimal(1) + alpha_isc * (tmax - tref))
    design_current = Decimal("1.25") * isc_corrected
    iac = pac / vac
    dc_drop = Decimal(2) * Decimal("20") * imp * rho / Decimal("6")
    dc_drop_pct = dc_drop / vmp_string * Decimal(100)
    ac_drop = Decimal(2) * Decimal("15") * iac * rho / Decimal("10")
    ac_drop_pct = ac_drop / vac * Decimal(100)
    total_drop_pct = dc_drop_pct + ac_drop_pct
    annual_energy = (pdc / Decimal(1000)) * Decimal("5.2") * Decimal(365) * Decimal("0.78")
    monthly_energy = annual_energy / Decimal(12)
    derived = {
        "POTENCIA_CC": pdc,
        "RELACAO_CC_CA": ratio,
        "VMP_STRING_STC": vmp_string,
        "VOC_STRING_STC": voc_string,
        "VOC_STRING_FRIO": voc_cold,
        "VMP_STRING_QUENTE": vmp_hot,
        "ISC_CORRIGIDA": isc_corrected,
        "CORRENTE_PROJETO_CC": design_current,
        "CORRENTE_CA": iac,
        "QUEDA_CC": dc_drop,
        "QUEDA_CC_PCT": dc_drop_pct,
        "QUEDA_CA": ac_drop,
        "QUEDA_CA_PCT": ac_drop_pct,
        "QUEDA_TOTAL_PCT": total_drop_pct,
        "ENERGIA_ANUAL": annual_energy,
        "ENERGIA_MENSAL_MEDIA": monthly_energy,
    }
    result_map = {row["calculo"]: row for row in calculations}
    checks += 3
    if set(result_map) != set(derived) or len(result_map) != len(calculations):
        errors.append("resultados-calculo.csv não contém exatamente os 16 resultados esperados.")
    if any(row["classificacao"] not in {"DERIVADO", "ESTIMATIVA"} for row in calculations):
        errors.append("Resultado sem classificação DERIVADO ou ESTIMATIVA.")
    if any(not row["formula"] or not row["observacao"] for row in calculations):
        errors.append("Resultado sem fórmula ou observação.")
    for key, value in derived.items():
        checks += 1
        if key not in result_map or not close(decimal(result_map[key]["resultado"]), value):
            errors.append(f"Resultado {key} divergente: esperado {value}.")

    checks += 11
    if nseries * nstrings != nmod:
        errors.append("Formação das strings não reconcilia a quantidade de módulos.")
    if not (voc_cold < Decimal("600")):
        errors.append("Voc corrigida não é inferior ao limite CC do inversor.")
    if not (Decimal("90") <= vmp_hot <= Decimal("550")):
        errors.append("Vmp quente está fora da faixa MPPT.")
    if imp > Decimal("16"):
        errors.append("Imp da string excede a corrente operacional do MPPT.")
    if isc_corrected > Decimal("20"):
        errors.append("Isc corrigida excede o limite de curto-circuito do MPPT.")
    if not (design_current <= Decimal("20") <= Decimal("25")):
        errors.append("Fusível gPV não está coordenado com a premissa de corrente.")
    if Decimal("40") <= iac:
        errors.append("Disjuntor CA não excede a corrente nominal calculada.")
    if ratio != Decimal("1.1"):
        errors.append("Relação CC/CA diferente de 1,10.")
    if dc_drop_pct >= Decimal(2) or ac_drop_pct >= Decimal(2):
        errors.append("Queda preliminar individual igual ou superior a 2%.")
    if annual_energy <= Decimal(0):
        errors.append("Estimativa de energia não positiva.")
    if any(row["classificacao"] == "RESULTADO_EXPERIMENTAL" for row in calculations):
        errors.append("O projeto não pode declarar resultado experimental.")

    module_tags = {row["modulo"] for row in modules}
    checks += 6
    if module_tags != {f"M{index:02d}" for index in range(1, 13)} or len(modules) != 12:
        errors.append("lista-modulos.csv deve conter M01 a M12 sem duplicatas.")
    if {row["string"] for row in modules} != {"S1", "S2"}:
        errors.append("Strings S1 e S2 não estão completas.")
    if any(sum(1 for row in modules if row["string"] == string) != 6 for string in ("S1", "S2")):
        errors.append("Cada string deve possuir seis módulos.")
    if any(decimal(row["potencia_wp"]) != pmod for row in modules):
        errors.append("Potência de módulo divergente na lista.")
    if sum(decimal(row["potencia_wp"]) for row in modules) != pdc:
        errors.append("Soma das potências dos módulos divergente.")
    if any(row["orientacao"] != "Norte" or row["inclinacao_graus"] != "20" for row in modules):
        errors.append("Orientação ou inclinação divergente da premissa.")

    protection_tags = {row["tag"] for row in protections}
    checks += 8
    if protection_tags != REQUIRED_PROTECTIONS or len(protections) != 11:
        errors.append("lista-protecoes.csv não contém exatamente as 11 proteções.")
    if any(row["classificacao"] != "PROPOSTA" for row in protections):
        errors.append("Proteção sem classificação PROPOSTA.")
    if any(not row["observacoes"] or not row["prancha"] for row in protections):
        errors.append("Proteção sem observação ou referência de prancha.")
    if sum(1 for row in protections if row["tipo"] == "Fusivel gPV") != 4:
        errors.append("Devem existir quatro fusíveis gPV.")
    if sum(1 for row in protections if "DPS" in row["tipo"]) != 3:
        errors.append("Devem existir dois DPS CC e um DPS CA.")
    if sum(1 for row in protections if "Seccionador" in row["tipo"]) != 3:
        errors.append("Devem existir dois seccionadores CC e um CA.")
    if not {"CC", "CA"} <= {row["lado"] for row in protections}:
        errors.append("Proteções CC e CA não estão ambas representadas.")
    if any(row["prancha"] not in {f"{index:02d}/06" for index in range(1, 7)} for row in protections):
        errors.append("Referência de prancha inválida em lista-protecoes.csv.")

    cable_tags = {row["cabo"] for row in cables}
    checks += 6
    if cable_tags != REQUIRED_CABLES or len(cables) != 7:
        errors.append("lista-cabos.csv não contém exatamente os sete cabos esperados.")
    if any(not row["identificacao_condutores"] or not row["rota"] for row in cables):
        errors.append("Cabo sem identificação de condutores ou rota.")
    if any(decimal(row["comprimento_assumido_m"]) <= 0 for row in cables):
        errors.append("Cabo com comprimento não positivo.")
    if not close(decimal(next(row for row in cables if row["cabo"] == "FV-S1")["queda_pct"]), dc_drop_pct):
        errors.append("Queda de FV-S1 divergente.")
    if not close(decimal(next(row for row in cables if row["cabo"] == "FV-S2")["queda_pct"]), dc_drop_pct):
        errors.append("Queda de FV-S2 divergente.")
    if not close(decimal(next(row for row in cables if row["cabo"] == "CA-INV")["queda_pct"]), ac_drop_pct):
        errors.append("Queda de CA-INV divergente.")

    material_items = {row["item"] for row in materials}
    checks += 5
    if material_items != REQUIRED_MATERIAL_ITEMS or len(materials) != 21:
        errors.append("lista-materiais.csv não contém exatamente os 21 itens esperados.")
    if any(decimal(row["quantidade"]) <= 0 for row in materials):
        errors.append("Material com quantidade não positiva.")
    if any(not row["referencia"] or not row["observacoes"] for row in materials):
        errors.append("Material sem referência ou observação.")
    if decimal(next(row for row in materials if row["item"] == "MOD-FV")["quantidade"]) != nmod:
        errors.append("Quantidade de módulos diverge da lista de materiais.")
    if decimal(next(row for row in materials if row["item"] == "INV-FV")["quantidade"]) != Decimal(1):
        errors.append("Quantidade de inversores deve ser um.")

    # Varre todo o envelope ambiental declarado, não apenas os extremos tabulados.
    environmental_rows = 0
    for temperature in range(-5, 71):
        temp = Decimal(temperature)
        v_open = voc_string * (Decimal(1) + beta_voc * (temp - tref))
        v_power = vmp_string * (Decimal(1) + beta_vmp * (temp - tref))
        checks += 2
        environmental_rows += 1
        if v_open >= Decimal("600"):
            errors.append(f"Voc excede 600 V a {temperature} °C.")
        if not (Decimal("90") <= v_power <= Decimal("550")):
            errors.append(f"Vmp fora da faixa a {temperature} °C.")
        for irradiance in range(100, 1101, 10):
            current = isc * (Decimal(irradiance) / Decimal(1000)) * (
                Decimal(1) + alpha_isc * (temp - tref)
            )
            checks += 1
            if current > Decimal("20"):
                errors.append(f"Isc excede o limite em {temperature} °C e {irradiance} W/m².")

    docs = {
        name: (project / name).read_text(encoding="utf-8")
        for name in (
            "README.md", "criterios-premissas.md", "memorial-descritivo.md",
            "memoria-calculo.md", "referencias-normativas.md", "inspecao-visual.md",
        )
    }
    checks += 9
    if WARNING not in docs["README.md"] or WARNING not in docs["criterios-premissas.md"]:
        errors.append("Aviso obrigatório ausente no README ou nos critérios.")
    if WARNING not in docs["memorial-descritivo.md"] or WARNING not in docs["referencias-normativas.md"]:
        errors.append("Aviso obrigatório ausente no memorial ou nas referências.")
    for heading in ("Fatos técnicos e regulatórios", "Premissas acadêmicas", "Propostas conceituais", "Limitações"):
        if heading not in docs["criterios-premissas.md"]:
            errors.append(f"Seção epistemológica ausente: {heading}.")
    if any(reference not in docs["referencias-normativas.md"] for reference in REQUIRED_REFERENCES):
        errors.append("Referências oficiais atuais incompletas.")
    if re.search(r"\]\(https?://", "\n".join(docs.values()), flags=re.IGNORECASE):
        errors.append("Documentação interna não deve conter links externos.")
    if "especificação funcional fictícia" not in docs["README.md"] or "modelo comercial homologado" not in docs["README.md"]:
        errors.append("Natureza fictícia do inversor não está clara.")

    source_dir = project / "fonte"
    for index, filename in enumerate(SHEETS, start=1):
        path = source_dir / filename
        checks += 9 + len(SHEET_TERMS[filename])
        try:
            doc = ezdxf.readfile(path)
        except Exception as exc:  # pragma: no cover - evidência de falha externa
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
        if metadata.get("PORTFOLIO_SHEET") != f"{index:02d}/06":
            errors.append(f"Metadado de prancha incorreto em {filename}.")
        if metadata.get("PORTFOLIO_EPISTEMIC_STATUS") != "ACADEMIC_CONCEPT_NOT_FOR_EXECUTION":
            errors.append(f"Status epistemológico incorreto em {filename}.")
        text = extract_text(doc)
        if WARNING not in text:
            errors.append(f"Aviso obrigatório ausente em {filename}.")
        for term in SHEET_TERMS[filename]:
            if term.casefold() not in text.casefold():
                errors.append(f"Termo obrigatório ausente em {filename}: {term}.")

    result = {
        "checks": checks,
        "errors": errors,
        "results": {
            "ac_current_a": f"{iac:.6f}",
            "annual_energy_estimate_kwh": f"{annual_energy:.6f}",
            "dc_ac_ratio": f"{ratio:.6f}",
            "dc_drop_pct": f"{dc_drop_pct:.6f}",
            "environmental_temperature_rows": environmental_rows,
            "materials": len(materials),
            "modules": len(modules),
            "protections": len(protections),
            "sheets": len(SHEETS),
            "strings": int(nstrings),
            "voc_cold_v": f"{voc_cold:.6f}",
            "vmp_hot_v": f"{vmp_hot:.6f}",
        },
        "status": "PASS" if not errors else "FAIL",
    }
    report = project / "validacao-fotovoltaico.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return parser.parse_args()


def main() -> int:
    result = validate(parse_args().root.resolve())
    print(f"VALIDACAO PROJETO 08 {result['status']} | verificacoes={result['checks']} erros={len(result['errors'])}")
    for error in result["errors"]:
        print(f"- {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
