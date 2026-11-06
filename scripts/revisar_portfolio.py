"""Auditoria consolidada e geracao de folhas de contato do portfolio.

Este script complementa ``validar_portfolio.py`` com verificacoes cruzadas de
inventario, carimbo, tabelas CSV e equivalencia visual entre PDF e PNG. As
saidas de apoio sao gravadas em ``work/`` e, portanto, nao sao versionadas.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

import ezdxf
import numpy as np
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader

from portfolio_config import load_config, required_layers


A3_RATIO = 420.0 / 297.0
CPF_PATTERN = re.compile(r"(?<!\d)\d{3}[.]\d{3}[.]\d{3}-\d{2}(?!\d)")
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+55\s*)?\(?\d{2}\)?\s*9?\d{4}[-\s]\d{4}(?!\d)")


def relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def dxf_texts(document: ezdxf.document.Drawing) -> list[str]:
    values: list[str] = []
    for entity in document.modelspace().query("TEXT MTEXT INSERT"):
        if entity.dxftype() == "MTEXT":
            value = entity.plain_text()
        elif entity.dxftype() == "INSERT":
            values.extend(attribute.dxf.text for attribute in entity.attribs)
            continue
        else:
            value = str(entity.dxf.get("text", ""))
        values.append(value.replace("\\P", "\n"))
    return values


def check_csv(path: Path) -> tuple[int, int, list[str]]:
    issues: list[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.reader(stream))
    if len(rows) < 2:
        return len(rows), 0, ["tabela sem linhas de dados"]
    header = [cell.strip() for cell in rows[0]]
    if any(not cell for cell in header):
        issues.append("cabecalho vazio")
    duplicates = [name for name, count in Counter(header).items() if count > 1]
    if duplicates:
        issues.append("cabecalhos duplicados: " + ", ".join(sorted(duplicates)))
    for number, row in enumerate(rows[1:], 2):
        if len(row) != len(header):
            issues.append(f"linha {number} possui {len(row)} colunas; esperado {len(header)}")
        if not any(cell.strip() for cell in row):
            issues.append(f"linha {number} vazia")
    return len(rows) - 1, len(header), issues


def pdf_preview_and_similarity(pdf_path: Path, png_path: Path, preview_path: Path) -> float:
    pdf = pdfium.PdfDocument(pdf_path)
    if len(pdf) != 1:
        raise ValueError(f"PDF possui {len(pdf)} paginas; esperado 1")
    page = pdf[0]
    rendered = page.render(scale=1.5).to_pil().convert("RGB")
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    rendered.save(preview_path, optimize=True)

    comparison_size = (840, 594)
    pdf_array = np.asarray(rendered.resize(comparison_size).convert("L"), dtype=np.float32)
    with Image.open(png_path) as source:
        png_array = np.asarray(
            source.convert("L").resize(comparison_size), dtype=np.float32
        )
    mae = float(np.mean(np.abs(pdf_array - png_array)))
    return max(0.0, 1.0 - mae / 255.0)


def contact_sheet(images: list[tuple[Path, str]], output: Path, title: str) -> None:
    columns = 2
    tile_width, image_height, label_height = 1040, 735, 54
    margin, header = 28, 74
    rows = (len(images) + columns - 1) // columns
    canvas = Image.new(
        "RGB",
        (
            columns * tile_width + (columns + 1) * margin,
            header + rows * (image_height + label_height + margin),
        ),
        "white",
    )
    draw = ImageDraw.Draw(canvas)
    font_path = Path("C:/Windows/Fonts/arial.ttf")
    bold_path = Path("C:/Windows/Fonts/arialbd.ttf")
    font = ImageFont.truetype(str(font_path), 25) if font_path.exists() else ImageFont.load_default()
    bold = ImageFont.truetype(str(bold_path), 34) if bold_path.exists() else font
    draw.text((margin, 18), title, fill="black", font=bold)

    for index, (path, label) in enumerate(images):
        row, column = divmod(index, columns)
        x = margin + column * (tile_width + margin)
        y = header + row * (image_height + label_height + margin)
        with Image.open(path) as source:
            page = source.convert("RGB")
            page.thumbnail((tile_width, image_height), Image.Resampling.LANCZOS)
            px = x + (tile_width - page.width) // 2
            py = y + (image_height - page.height) // 2
            canvas.paste(page, (px, py))
        draw.rectangle((x, y, x + tile_width, y + image_height), outline="#777777", width=2)
        draw.text((x, y + image_height + 9), label, fill="black", font=font)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, default=Path("work/revisao-portfolio"))
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    config = load_config(root)
    author = config["portfolio"]["author"]
    notice = config["portfolio"]["warning"]
    layers = set(required_layers(config))

    errors: list[str] = []
    records: list[dict[str, object]] = []
    visual_records: list[dict[str, object]] = []
    project_contacts: list[tuple[Path, str]] = []
    sheet_artifacts = [artifact for artifact in config["artifacts"] if artifact["kind"] == "sheet"]
    project_artifacts = [artifact for artifact in sheet_artifacts if artifact["id"].startswith("p")]

    expected_total = sum(int(project["sheet_count"]) for project in config["projects"])
    if len(project_artifacts) != expected_total:
        errors.append(
            f"portfolio.toml declara {expected_total} pranchas, mas possui "
            f"{len(project_artifacts)} artefatos de projeto"
        )

    for project_number, project in enumerate(config["projects"], 1):
        project_path = root / project["path"]
        prefix = f"p{project_number:02d}-"
        artifacts = [item for item in project_artifacts if item["id"].startswith(prefix)]
        if len(artifacts) != int(project["sheet_count"]):
            errors.append(
                f"{project['id']}: {len(artifacts)} artefatos; esperado {project['sheet_count']}"
            )
        contact_images: list[tuple[Path, str]] = []

        for sheet_number, artifact in enumerate(artifacts, 1):
            paths = {key: root / artifact[key] for key in ("source", "pdf", "svg", "png")}
            stems = {path.stem for path in paths.values()}
            if len(stems) != 1:
                errors.append(f"{artifact['id']}: nomes-base divergentes: {sorted(stems)}")
            for kind, path in paths.items():
                if not path.is_file() or path.stat().st_size == 0:
                    errors.append(f"{artifact['id']}: {kind} ausente ou vazio ({relative(root, path)})")

            if errors and any(artifact["id"] in item for item in errors[-4:]):
                continue

            try:
                document = ezdxf.readfile(paths["source"])
                texts = dxf_texts(document)
                combined = "\n".join(texts)
                missing_layers = sorted(layers - {layer.dxf.name for layer in document.layers})
                if document.dxfversion != config["portfolio"]["dxf_version"]:
                    errors.append(f"{artifact['id']}: versao DXF {document.dxfversion}")
                if int(document.header.get("$INSUNITS", -1)) != int(config["page"]["insunits"]):
                    errors.append(f"{artifact['id']}: $INSUNITS diferente de milimetros")
                if missing_layers:
                    errors.append(f"{artifact['id']}: layers ausentes: {', '.join(missing_layers)}")
                if author not in combined:
                    errors.append(f"{artifact['id']}: autor ausente do carimbo")
                if notice not in combined.replace("\n", " "):
                    errors.append(f"{artifact['id']}: aviso academico ausente")
                expected_sheet = f"{sheet_number:02d}/{len(artifacts):02d}"
                if expected_sheet not in combined:
                    errors.append(f"{artifact['id']}: identificador {expected_sheet} ausente")
            except Exception as exc:  # noqa: BLE001 - auditoria precisa relatar o arquivo
                errors.append(f"{artifact['id']}: falha ao ler DXF: {exc}")

            try:
                reader = PdfReader(paths["pdf"])
                if reader.is_encrypted or len(reader.pages) != 1:
                    errors.append(f"{artifact['id']}: PDF criptografado ou com numero de paginas invalido")
                else:
                    box = reader.pages[0].mediabox
                    width_mm = float(box.width) * 25.4 / 72.0
                    height_mm = float(box.height) * 25.4 / 72.0
                    if abs(width_mm - 420.0) > 0.6 or abs(height_mm - 297.0) > 0.6:
                        errors.append(
                            f"{artifact['id']}: PDF {width_mm:.2f} x {height_mm:.2f} mm"
                        )
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{artifact['id']}: falha ao ler PDF: {exc}")

            try:
                svg_root = ElementTree.parse(paths["svg"]).getroot()
                if svg_root.tag.split("}")[-1] != "svg" or not svg_root.get("viewBox"):
                    errors.append(f"{artifact['id']}: SVG sem raiz/viewBox valido")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{artifact['id']}: falha ao ler SVG: {exc}")

            try:
                with Image.open(paths["png"]) as png:
                    png.verify()
                with Image.open(paths["png"]) as png:
                    width, height = png.size
                if width < int(config["validation"]["minimum_png_width"]):
                    errors.append(f"{artifact['id']}: PNG com largura insuficiente ({width})")
                if abs(width / height - A3_RATIO) > 0.02:
                    errors.append(f"{artifact['id']}: proporcao PNG invalida ({width}x{height})")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{artifact['id']}: falha ao ler PNG: {exc}")

            preview_path = output / "pdf" / f"{artifact['id']}.png"
            try:
                similarity = pdf_preview_and_similarity(paths["pdf"], paths["png"], preview_path)
                if similarity < 0.90:
                    errors.append(f"{artifact['id']}: similaridade PDF/PNG baixa ({similarity:.4f})")
            except Exception as exc:  # noqa: BLE001
                similarity = 0.0
                errors.append(f"{artifact['id']}: falha na comparacao PDF/PNG: {exc}")

            for kind, path in paths.items():
                records.append(
                    {
                        "project": project["id"],
                        "sheet": sheet_number,
                        "artifact": artifact["id"],
                        "kind": kind,
                        "path": relative(root, path),
                        "bytes": path.stat().st_size,
                    }
                )
            visual_records.append(
                {
                    "project": project["id"],
                    "artifact": artifact["id"],
                    "pdf_png_similarity": round(similarity, 6),
                    "pdf_preview": relative(root, preview_path),
                }
            )
            contact_images.append((paths["png"], f"{sheet_number:02d} — {artifact['title']}"))

        for csv_path in sorted(project_path.glob("*.csv")):
            try:
                rows, columns, issues = check_csv(csv_path)
            except Exception as exc:  # noqa: BLE001
                rows, columns, issues = 0, 0, [str(exc)]
            records.append(
                {
                    "project": project["id"],
                    "sheet": "",
                    "artifact": "",
                    "kind": "csv",
                    "path": relative(root, csv_path),
                    "bytes": csv_path.stat().st_size,
                    "rows": rows,
                    "columns": columns,
                }
            )
            errors.extend(f"{relative(root, csv_path)}: {issue}" for issue in issues)

        contact_path = output / "contatos" / f"{project['id']}.png"
        contact_sheet(contact_images, contact_path, f"Revisao visual — {project['id']}")
        project_contacts.append((contact_path, project["id"]))

    for path in root.rglob("*"):
        if not path.is_file() or any(part in {".git", ".venv", "node_modules", "work"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".csv", ".toml", ".py", ".mjs"}:
            continue
        try:
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        if CPF_PATTERN.search(content):
            errors.append(f"{relative(root, path)}: possivel CPF encontrado")
        if PHONE_PATTERN.search(content):
            errors.append(f"{relative(root, path)}: possivel telefone encontrado")

    contact_sheet(
        project_contacts,
        output / "contatos" / "portfolio-completo.png",
        f"Portfolio completo — {len(project_contacts)} projetos",
    )

    with (output / "inventario.csv").open("w", encoding="utf-8", newline="") as stream:
        fieldnames = ["project", "sheet", "artifact", "kind", "path", "bytes", "rows", "columns"]
        writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    report = {
        "schema_version": 1,
        "status": "PASS" if not errors else "FAIL",
        "projects": len(config["projects"]),
        "project_sheets": len(project_artifacts),
        "artifact_files_checked": len(project_artifacts) * 4,
        "csv_files_checked": sum(1 for record in records if record["kind"] == "csv"),
        "pdf_png_similarity_min": min(
            (item["pdf_png_similarity"] for item in visual_records), default=0.0
        ),
        "errors": errors,
        "visual_records": visual_records,
    }
    (output / "resultado.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(
        f"REVISAO {'PASS' if not errors else 'FAIL'} | projetos={report['projects']} "
        f"pranchas={report['project_sheets']} arquivos={report['artifact_files_checked']} "
        f"csv={report['csv_files_checked']} similaridade_min={report['pdf_png_similarity_min']:.4f} "
        f"erros={len(errors)}"
    )
    for error in errors:
        print(f"ERRO {error}")
    print(f"RESULTADO={relative(root, output / 'resultado.json')}")
    print(f"CONTATOS={relative(root, output / 'contatos')}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
