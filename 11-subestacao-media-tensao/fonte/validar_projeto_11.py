"""Valida calculos, referencias e DXFs do Projeto 11 (Subestacao de Media Tensao)."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import ezdxf


PROJECT_SLUG = "11-subestacao-media-tensao"
SHEETS = (
    "01_diagrama_unifilar_geral.dxf",
    "02_planta_baixa_subestacao.dxf",
    "03_cortes_detalhes_eletromecanicos.dxf",
    "04_diagrama_funcional_protecao.dxf",
    "05_malha_aterramento.dxf",
    "06_spda_geral.dxf",
    "07_plano_dados_estudo_aterramento.dxf",
    "08_matriz_analise_malha_aterramento.dxf",
)
REQUIRED_TAGS = {
    "TR-01",
    "DJ-MT",
    "SEC-01",
    "RELE DIGITAL",
    "QGBT",
    "DJ-GERAL",
    "DPS-BT",
    "BEP",
    "BUCHHOLZ",
    "500 kVA",
    "13,8 kV",
    "GPR",
}
REQUIRED_GROUNDING_INPUTS = {
    "perfil_resistividade_solo",
    "estratos_solo",
    "resistividade_superficial",
    "espessura_superficial",
    "condicao_sazonal",
    "corrente_falta_solo",
    "fracao_corrente_malha",
    "tempo_eliminacao",
    "contribuicao_remota",
    "aterramento_neutro_fonte",
    "geometria_patio",
    "limite_acessivel_malha",
    "material_secao_condutor",
    "profundidade_condutor",
    "espacamento_condutores",
    "hastes_quantidade_comprimento",
    "conexoes_malha",
    "interfaces_bep",
    "interfaces_cercas",
    "interfaces_metalicas_remotas",
    "zonas_pessoas_acesso",
    "criterios_metodo_revisao",
}
REQUIRED_SHEET_07_TERMS = (
    "PLANO DE DADOS PARA ESTUDO DE ATERRAMENTO",
    "DADOS DE SOLO",
    "FALTA E PROTECAO",
    "GEOMETRIA E INTERFACES",
    "LEVANTAR",
    "MODELAR",
    "VERIFICAR",
    "REVISAR",
    "GPR, toque, passo e transferencia",
    "PENDENTE",
)
REQUIRED_SHEET_08_TERMS = (
    "MATRIZ DE ANALISE DA MALHA DE ATERRAMENTO",
    "MODELO DE SOLO",
    "CENARIO DE FALTA",
    "GEOMETRIA / EXPOSICAO",
    "MODELO RASTREAVEL POR CENARIO",
    "VERIFICACOES, RESULTADOS REQUERIDOS E EVIDENCIAS",
    "Condutor / conexoes",
    "Resposta da malha",
    "Integridade e solicitacao termica",
    "Resistencia/impedancia e GPR por cenario",
    "Perfil de superficie, toque e passo",
    "Potencial em interfaces alem da malha",
    "Antes de comparar",
    "I_f = corrente de falta",
    "S_g = fracao da corrente para a malha",
    "PENDENTE",
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    project_dir = root / PROJECT_SLUG
    source_dir = project_dir / "fonte"

    errors: list[str] = []
    all_texts: list[str] = []
    sheet_texts: dict[str, str] = {}

    for index, filename in enumerate(SHEETS, start=1):
        dxf_path = source_dir / filename
        if not dxf_path.exists():
            errors.append(f"DXF ausente: {filename}")
            continue
        doc = ezdxf.readfile(dxf_path)
        audit = doc.audit()
        if audit.errors:
            errors.append(f"Erros de auditoria em {filename}: {len(audit.errors)}")
        text = extract_text(doc)
        all_texts.append(text)
        expected_sheet = f"{index:02d}/{len(SHEETS):02d}"
        if expected_sheet not in text:
            errors.append(f"Numeracao de prancha {expected_sheet} nao encontrada em {filename}")
        sheet_texts[filename] = text

    combined_text = " ".join(all_texts)
    for tag in sorted(REQUIRED_TAGS):
        if tag not in combined_text:
            errors.append(f"Tag obrigatoria nao encontrada nas pranchas: {tag}")

    sheet_07_text = sheet_texts.get("07_plano_dados_estudo_aterramento.dxf", "")
    for term in REQUIRED_SHEET_07_TERMS:
        if term not in sheet_07_text:
            errors.append(f"Termo obrigatorio ausente na prancha 07: {term}")
    sheet_08_text = sheet_texts.get("08_matriz_analise_malha_aterramento.dxf", "")
    for term in REQUIRED_SHEET_08_TERMS:
        if term not in sheet_08_text:
            errors.append(f"Termo obrigatorio ausente na prancha 08: {term}")
    sheet_02_text = sheet_texts.get("02_planta_baixa_subestacao.dxf", "")
    for term in (
        "ARRANJO CONCEITUAL DA SUBESTACAO ABRIGADA",
        "sem escala valida",
        "PREMISSAS E PENDENCIAS DE ARRANJO",
        "A planta nao demonstra conformidade ou liberacao executiva.",
        "S/ESC.",
    ):
        if term.casefold() not in sheet_02_text.casefold():
            errors.append(f"Termo de escala/limite conceitual ausente na prancha 02: {term}")
    if "afastamentos normativos NBR 14039" in sheet_02_text:
        errors.append("A prancha 02 nao pode sugerir afastamentos normativos validados.")
    sheet_05_text = sheet_texts.get("05_malha_aterramento.dxf", "")
    if "18,72" in sheet_05_text or "250 ohm.m" in sheet_05_text.lower():
        errors.append("A prancha 05 ainda apresenta valor aritmetico/solo hipotetico como entrada ativa.")

    materials = read_rows(project_dir / "lista-materiais.csv")
    cables = read_rows(project_dir / "lista-cabos.csv")
    grounding_inputs = read_rows(project_dir / "dados-estudo-aterramento.csv")
    if len(materials) < 15:
        errors.append("Lista de materiais possui menos de 15 itens.")
    if len(cables) < 10:
        errors.append("Lista de cabos possui menos de 10 itens.")
    input_tags = {row["parametro"] for row in grounding_inputs}
    if len(grounding_inputs) != len(REQUIRED_GROUNDING_INPUTS) or input_tags != REQUIRED_GROUNDING_INPUTS:
        errors.append("dados-estudo-aterramento.csv deve conter exatamente os 22 dados requeridos sem duplicatas.")
    if any(row["valor"] != "A DEFINIR" or row["status"] != "PENDENTE" for row in grounding_inputs):
        errors.append("Nenhum dado de levantamento de aterramento pode ser inferido sem evidencia de campo.")

    report = {
        "project": PROJECT_SLUG,
        "sheets_checked": len(SHEETS),
        "materials_count": len(materials),
        "cables_count": len(cables),
        "grounding_inputs_count": len(grounding_inputs),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }
    (project_dir / "validacao.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if errors:
        for err in errors:
            print(f"[ERRO] {err}")
        return 1
    print(f"Validacao Projeto 11: PASS ({len(SHEETS)} pranchas, {len(materials)} materiais, {len(cables)} cabos, {len(grounding_inputs)} dados pendentes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
