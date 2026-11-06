"""Valida as contas e a estrutura essencial do projeto conceitual P19."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import sys

import ezdxf

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "19-alimentacao-navios-cais-hvsc"
BOX_BLOCK = "P19_CAIXA_EQUIPAMENTO"
SCRIPTS_DIR = DEFAULT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from portfolio_config import load_config, required_layers  # noqa: E402

WARNING = (
    "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação "
    "ou execução de serviços sem revisão, dimensionamento e responsabilidade de "
    "profissional legalmente habilitado."
)
SHEETS = (
    "01_unifilar_hvsc_cais.dxf",
    "02_implantacao_eletrica_cais.dxf",
    "03_sequencia_intertravamentos_hvsc.dxf",
)
REQUIRED_FILES = (
    "README.md", "memorial-descritivo.md", "criterios-premissas.md",
    "referencias-normativas.md", "inspecao-visual.md", "calculo-correntes.csv",
    "lista-materiais.csv", "lista-sinais.csv", "matriz-interfaces.csv",
    "sequencia-conexao.csv",
    "fonte/gerar_projeto_19.py", "fonte/validar_projeto_19.py",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def check(root: Path) -> dict:
    project_dir = root / SLUG
    errors: list[str] = []
    checks = 0
    config = load_config(root)
    required = set(required_layers(config))

    for relative in REQUIRED_FILES:
        checks += 1
        if not (project_dir / relative).is_file():
            errors.append(f"Arquivo requerido ausente: {relative}")

    for relative in ("README.md", "memorial-descritivo.md"):
        checks += 1
        path = project_dir / relative
        if path.is_file() and WARNING not in path.read_text(encoding="utf-8"):
            errors.append(f"Aviso obrigatório ausente: {relative}")

    currents = read_csv(project_dir / "calculo-correntes.csv")
    checks += 1
    expected_header = {"caso", "potencia_aparente_mva", "tensao_linha_kv", "corrente_calculada_a", "base"}
    if not currents or not expected_header.issubset(currents[0]):
        errors.append("Cabeçalho ou linhas de calculo-correntes.csv inválidos.")
    else:
        expected = (133.9, 279.9, 167.3, 349.9)
        if len(currents) != 4:
            errors.append(f"Quantidade de casos de corrente divergente: {len(currents)}")
        for row, reference in zip(currents, expected):
            s_va = float(row["potencia_aparente_mva"]) * 1_000_000
            v_volt = float(row["tensao_linha_kv"]) * 1_000
            calculated = s_va / (math.sqrt(3) * v_volt)
            recorded = float(row["corrente_calculada_a"])
            checks += 1
            if not math.isclose(calculated, recorded, abs_tol=0.06):
                errors.append(f"Corrente registrada divergente: {row['caso']}")
            checks += 1
            if not math.isclose(recorded, reference, abs_tol=0.06):
                errors.append(f"Valor de referência divergente: {row['caso']}")

    materials = read_csv(project_dir / "lista-materiais.csv")
    checks += 1
    material_columns = {"item", "quantidade", "unidade", "descricao", "referencia", "observacoes"}
    if not materials or not material_columns.issubset(materials[0]):
        errors.append("Cabeçalho ou conteúdo da lista de materiais inválidos.")
    references = " ".join(row.get("referencia", "") for row in materials)
    for tag in ("PCC-01", "QMT-01", "TR-01", "Q-HVSC", "PT-01", "PA-01", "MM-01", "CS-HVSC"):
        checks += 1
        if tag not in references:
            errors.append(f"Tag não rastreada na lista de materiais: {tag}")

    signals = read_csv(project_dir / "lista-sinais.csv")
    checks += 1
    signal_columns = {"sinal", "origem", "destino", "funcao", "dado_esperado", "interface", "estado"}
    if not signals or not signal_columns.issubset(signals[0]):
        errors.append("Cabeçalho ou conteúdo da lista de sinais inválidos.")
    else:
        checks += 1
        if not any(row["sinal"] == "SAFETY_LOOP_HEALTHY" for row in signals):
            errors.append("Sinal explícito do circuito de segurança ausente.")
        checks += 1
        if not any(row["sinal"] == "COMMUNICATION_OK" for row in signals):
            errors.append("Sinal de comunicação funcional ausente.")

    interfaces = read_csv(project_dir / "matriz-interfaces.csv")
    checks += 1
    if not interfaces or not {"interface", "lado_terra", "lado_navio", "criterio_de_compatibilidade", "estado"}.issubset(interfaces[0]):
        errors.append("Cabeçalho ou conteúdo da matriz de interfaces inválidos.")
    steps = read_csv(project_dir / "sequencia-conexao.csv")
    checks += 1
    if not steps or not {"etapa", "estado", "precondicao_ou_evento", "resposta_ou_evidencia", "status"}.issubset(steps[0]):
        errors.append("Cabeçalho ou conteúdo da sequência conceitual inválidos.")

    for index, filename in enumerate(SHEETS, 1):
        path = project_dir / "fonte" / filename
        checks += 1
        if not path.is_file():
            errors.append(f"DXF ausente: {path.relative_to(root)}")
            continue
        try:
            doc = ezdxf.readfile(path)
            audit = doc.audit()
        except Exception as exc:
            errors.append(f"Falha ao abrir {filename}: {exc}")
            continue
        checks += 1
        if audit.errors:
            errors.append(f"Auditoria DXF retornou {len(audit.errors)} erro(s): {filename}")
        checks += 1
        missing = required - {layer.dxf.name for layer in doc.layers}
        if missing:
            errors.append(f"Layers ausentes em {filename}: {', '.join(sorted(missing))}")
        checks += 1
        if int(doc.header.get("$INSUNITS", 0)) != 4:
            errors.append(f"$INSUNITS diferente de mm em {filename}")
        checks += 1
        if doc.dxfversion != "AC1027":
            errors.append(f"Versão DXF diferente de AC1027 em {filename}")
        checks += 1
        if tuple(doc.header.get("$LIMMIN", ()))[:2] != (0.0, 0.0) or tuple(doc.header.get("$LIMMAX", ()))[:2] != (420.0, 297.0):
            errors.append(f"Limites A3 divergentes em {filename}")
        values: list[str] = []
        for entity in doc.modelspace().query("TEXT MTEXT ATTRIB"):
            if entity.dxftype() == "MTEXT":
                values.append(entity.plain_text())
            else:
                values.append(entity.dxf.get("text", ""))
        for insert in doc.modelspace().query("INSERT"):
            values.extend(attribute.dxf.text for attribute in insert.attribs)
        checks += 1
        if not any(WARNING in value for value in values):
            errors.append(f"Aviso obrigatório ausente em {filename}")
        checks += 1
        if not any(f"{index:02d}/03" in value for value in values):
            errors.append(f"Número de prancha {index:02d}/03 ausente em {filename}")
        if index == 1:
            checks += 1
            if BOX_BLOCK not in doc.blocks:
                errors.append(f"Bloco reutilizável de equipamento ausente em {filename}")
            elif not any(entity.dxf.name == BOX_BLOCK for entity in doc.modelspace().query("INSERT")):
                errors.append(f"Nenhuma inserção do bloco de equipamento em {filename}")

    result = {
        "project": "P19",
        "date": "2026-11-06",
        "checks": checks,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "limits": [
            "Correntes calculadas com potencia aparente e tensoes assumidas; nao selecionam componentes.",
            "Compatibilidade de navio, cabo, aterramento, protecao, intertravamentos e operacao nao verificados.",
            "Auditoria independente pelo AutoCAD e renderizacao visual devem ser registradas separadamente.",
        ],
    }
    report = project_dir / "validacao-projeto-19.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    result = check(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
