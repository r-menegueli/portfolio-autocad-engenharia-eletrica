"""Validação focada das entregas P23-P25, compatível com checkout esparso."""

from __future__ import annotations

import argparse
import csv
from datetime import date
import json
from pathlib import Path
import re
import sys
import tomllib
import unicodedata

import ezdxf
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
KEYS = {
    "p23": "23-complexo-siderurgico-eaf",
    "p24": "24-linha-transmissao-138kv",
    "p25": "25-usina-cogeracao-biomassa",
}
NOTICE = "Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado."


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", value.replace("\\P", " ")).strip().lower()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", choices=("all", *KEYS), default="all")
    args = parser.parse_args()
    with (ROOT / "portfolio.toml").open("rb") as stream:
        config = tomllib.load(stream)
    selected = tuple(KEYS) if args.project == "all" else (args.project,)
    errors: list[str] = []
    warnings: list[str] = []
    page_w = float(config["page"]["width"])
    page_h = float(config["page"]["height"])
    expected_notice = normalized(NOTICE)

    for key in selected:
        project_id = KEYS[key]
        project = next((p for p in config["projects"] if p["id"] == project_id), None)
        if not project:
            errors.append(f"{key}: projeto ausente no portfolio.toml")
            continue
        base = ROOT / project["path"]
        for relative in project.get("required_files", []):
            if relative == "validacao/relatorio-validacao.json":
                continue  # written at the end of this validation pass
            if not (base / relative).is_file():
                errors.append(f"{key}: arquivo obrigatório ausente: {relative}")
        artifacts = [a for a in config["artifacts"] if a.get("source", "").startswith(project["path"] + "/fonte/")]
        if len(artifacts) != 10:
            errors.append(f"{key}: manifesto lista {len(artifacts)} pranchas-fonte; esperado 10")
        for art in artifacts:
            source = ROOT / art["source"]
            source_title = ""
            if not source.is_file():
                errors.append(f"{key}: DXF ausente: {art['source']}")
                continue
            try:
                doc = ezdxf.readfile(source)
                auditor = doc.audit()
                if auditor.errors:
                    errors.append(f"{key}: {art['source']} tem {len(auditor.errors)} erro(s) DXF")
                if doc.dxfversion != "AC1027":
                    errors.append(f"{key}: {art['source']} DXF {doc.dxfversion}; esperado AC1027")
                if doc.header.get("$INSUNITS") != 4:
                    errors.append(f"{key}: {art['source']} não declara milímetros")
                if doc.ezdxf_metadata().get("PORTFOLIO_PROJECT") != project_id:
                    errors.append(f"{key}: metadado de projeto incorreto em {art['source']}")
                missing_layers = set(config["layers"]["required"]) - {layer.dxf.name for layer in doc.layers}
                if missing_layers:
                    errors.append(f"{key}: layers ausentes em {art['source']}: {sorted(missing_layers)}")
                texts = []
                for entity in doc.modelspace():
                    if entity.dxftype() == "TEXT":
                        texts.append(entity.dxf.text)
                        point = entity.dxf.insert
                        if entity.dxf.layer == "02_TEXTO" and abs(point.x - 210.0) < 1.0 and abs(point.y - 277.0) < 1.0:
                            source_title = entity.dxf.text
                    elif entity.dxftype() == "MTEXT":
                        texts.append(entity.text)
                    elif entity.dxftype() == "INSERT":
                        texts.extend(attribute.dxf.text for attribute in entity.attribs)
                searchable = normalized(" ".join(texts))
                if expected_notice not in searchable:
                    errors.append(f"{key}: aviso obrigatório ausente em {art['source']}")
            except Exception as exc:  # report all failed files in one pass
                errors.append(f"{key}: falha ao ler {art['source']}: {exc}")
                continue

            for kind in ("pdf", "svg", "png"):
                output_rel = art.get(kind)
                output = ROOT / output_rel if output_rel else None
                if not output or not output.is_file():
                    errors.append(f"{key}: derivado {kind} ausente: {output_rel}")
                    continue
                if kind == "pdf":
                    try:
                        reader = PdfReader(str(output))
                        if len(reader.pages) != 1:
                            errors.append(f"{key}: {output_rel} tem {len(reader.pages)} páginas")
                        extracted = normalized(reader.pages[0].extract_text() or "")
                        expected_title = normalized(source_title)
                        if expected_title and expected_title not in extracted:
                            errors.append(f"{key}: texto pesquisável não contém o título em {output_rel}")
                        if expected_notice not in extracted:
                            errors.append(f"{key}: texto pesquisável não contém o aviso obrigatório em {output_rel}")
                        box = reader.pages[0].mediabox
                        w, h = float(box.width), float(box.height)
                        if abs(w - page_w * 72 / 25.4) > 1.0 or abs(h - page_h * 72 / 25.4) > 1.0:
                            errors.append(f"{key}: página PDF fora de A3 paisagem: {output_rel} ({w:.1f}×{h:.1f} pt)")
                    except Exception as exc:
                        errors.append(f"{key}: PDF ilegível {output_rel}: {exc}")
                elif kind == "png":
                    try:
                        with Image.open(output) as image:
                            if image.width < 4000 or image.height < 2800 or image.width <= image.height:
                                errors.append(f"{key}: PNG fora da resolução/formato A3 esperado: {output_rel} {image.size}")
                            image.verify()
                    except Exception as exc:
                        errors.append(f"{key}: PNG ilegível {output_rel}: {exc}")
                elif output.stat().st_size == 0:
                    errors.append(f"{key}: SVG vazio: {output_rel}")

        params = base / "dados" / "parametros.csv"
        if params.is_file():
            try:
                with params.open("r", encoding="utf-8-sig", newline="") as stream:
                    rows = list(csv.DictReader(stream))
                if not rows or not {"name", "value", "unit", "source"}.issubset(rows[0]):
                    errors.append(f"{key}: esquema CSV de parâmetros inválido")
                if any(not row["value"].strip() for row in rows):
                    errors.append(f"{key}: parâmetro com valor vazio")
            except Exception as exc:
                errors.append(f"{key}: falha lendo parâmetros: {exc}")

    report = {
        "data": date.today().isoformat(),
        "escopo": list(selected),
        "resultado": "aprovado" if not errors else "reprovado",
        "tipo": "validacao_estrutural_de_arquivos_e_renderizacoes",
        "erros": errors,
        "avisos": warnings,
        "observacao": "Validação estrutural focada; inclui leitura DXF/PDF/PNG e checklist de arquivos. Não certifica cálculo, norma ou projeto executivo.",
    }
    for key in selected:
        base = ROOT / KEYS[key]
        (base / "validacao").mkdir(parents=True, exist_ok=True)
        (base / "validacao" / "relatorio-validacao.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
