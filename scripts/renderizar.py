"""Renderiza os DXFs declarados em portfolio.toml para SVG, PDF e PNG."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
import math
import os
from pathlib import Path
import tempfile

import ezdxf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from ezdxf.addons.drawing import Frontend, RenderContext  # noqa: E402
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend  # noqa: E402
from ezdxf.addons.drawing.properties import LayoutProperties  # noqa: E402
from pypdf import PdfReader, PdfWriter  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

from portfolio_config import ROOT, load_config


MM_PER_INCH = 25.4
MM_TO_POINTS = 72.0 / MM_PER_INCH
RENDER_DPI = 300
SEARCHABLE_FONT = "PortfolioDejaVuSans"


def _register_searchable_font() -> None:
    if SEARCHABLE_FONT in pdfmetrics.getRegisteredFontNames():
        return
    font_path = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSans.ttf"
    pdfmetrics.registerFont(TTFont(SEARCHABLE_FONT, str(font_path)))


def _text_entity_data(entity) -> tuple[str, tuple[float, float], float, float] | None:
    kind = entity.dxftype()
    if kind not in {"TEXT", "ATTRIB", "ATTDEF", "MTEXT"}:
        return None
    if kind == "MTEXT":
        value = entity.plain_text()
        height = float(entity.dxf.char_height)
        direction = entity.dxf.get("text_direction", (1.0, 0.0, 0.0))
        rotation = math.degrees(math.atan2(direction[1], direction[0]))
    else:
        value = str(entity.dxf.text)
        height = float(entity.dxf.get("height", 1.5))
        rotation = float(entity.dxf.get("rotation", 0.0))
    if kind in {"TEXT", "ATTRIB", "ATTDEF"} and entity.dxf.get("halign", 0):
        point = entity.dxf.get("align_point", entity.dxf.insert)
    else:
        point = entity.dxf.insert
    value = " ".join(str(value).replace("\x00", "").split())
    if not value:
        return None
    return value, (float(point.x), float(point.y)), height, rotation


def _iter_layout_text(layout, depth: int = 0):
    """Yield visible DXF text, expanding nested inserts into sheet coordinates."""
    if depth > 8:
        return
    for entity in layout:
        data = _text_entity_data(entity)
        if data is not None:
            yield data
        if entity.dxftype() != "INSERT":
            continue
        for attrib in entity.attribs:
            data = _text_entity_data(attrib)
            if data is not None:
                yield data
        try:
            virtual = entity.virtual_entities()
            for child in virtual:
                data = _text_entity_data(child)
                if data is not None:
                    yield data
                elif child.dxftype() == "INSERT":
                    yield from _iter_layout_text((child,), depth + 1)
        except (AttributeError, ezdxf.DXFError):
            # Unsupported proxy/insert graphics remain visible in the source PDF;
            # they simply have no corresponding searchable text object.
            continue


def _add_searchable_text_layer(source: Path, pdf_path: Path) -> None:
    """Overlay invisible Unicode text at DXF coordinates for PDF search/copy."""
    _register_searchable_font()
    doc = ezdxf.readfile(source)
    width_pt = 420.0 * MM_TO_POINTS
    height_pt = 297.0 * MM_TO_POINTS
    buffer = BytesIO()
    overlay = canvas.Canvas(buffer, pagesize=(width_pt, height_pt), pageCompression=1)
    for value, (x, y), height_mm, rotation in _iter_layout_text(doc.modelspace()):
        overlay.saveState()
        overlay.translate(x * MM_TO_POINTS, y * MM_TO_POINTS)
        overlay.rotate(rotation)
        text = overlay.beginText(0, 0)
        text.setFont(SEARCHABLE_FONT, max(1.0, height_mm * MM_TO_POINTS))
        text.setTextRenderMode(3)  # invisible text: visual CAD paths remain unchanged
        text.textOut(value)
        overlay.drawText(text)
        overlay.restoreState()
    overlay.save()
    buffer.seek(0)

    original = PdfReader(str(pdf_path))
    if len(original.pages) != 1:
        raise RuntimeError(f"Era esperada uma página para {pdf_path}")
    page = original.pages[0]
    page.merge_page(PdfReader(buffer).pages[0])
    writer = PdfWriter()
    writer.add_page(page)
    metadata = original.metadata
    if metadata:
        writer.add_metadata({key: str(value) for key, value in metadata.items() if value is not None})
    with tempfile.NamedTemporaryFile(prefix=f"{pdf_path.stem}-", suffix=".pdf", dir=pdf_path.parent, delete=False) as stream:
        temp_path = Path(stream.name)
    try:
        with temp_path.open("wb") as stream:
            writer.write(stream)
        os.replace(temp_path, pdf_path)
    finally:
        temp_path.unlink(missing_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_artifact(root: Path, artifact: dict) -> dict:
    source = root / artifact["source"]
    outputs = {
        kind: root / artifact[kind]
        for kind in ("svg", "pdf", "png")
        if kind in artifact
    }
    return {
        "id": artifact["id"],
        "source": artifact["source"],
        "source_sha256": sha256(source),
        "outputs": {
            kind: {"path": str(path.relative_to(root)).replace("\\", "/"), "sha256": sha256(path)}
            for kind, path in sorted(outputs.items())
        },
    }


def output_metadata(kind: str, config: dict, artifact: dict) -> dict:
    title = artifact.get("title", "Template A3 - Portfolio AutoCAD de Engenharia Eletrica")
    common = {
        "Title": title,
        "Author": config["portfolio"]["author"],
        "Creator": f"ezdxf {ezdxf.__version__} + matplotlib {matplotlib.__version__}",
    }
    if kind == "pdf":
        fixed = datetime(2026, 9, 5, 12, tzinfo=timezone.utc)
        return {
            **common,
            "Subject": "Template academico A3 paisagem",
            "Keywords": "Engenharia Eletrica, DXF, AutoCAD, A3",
            "CreationDate": fixed,
            "ModDate": fixed,
        }
    if kind == "svg":
        return {
            "Title": common["Title"],
            "Creator": [common["Author"], common["Creator"]],
            "Date": config["portfolio"]["template_date"],
            "Description": "Visualizacao derivada do DXF principal.",
        }
    return {
        "Title": common["Title"],
        "Author": common["Author"],
        "Software": common["Creator"],
        "Description": "Visualizacao derivada do DXF principal.",
    }


def render_document(
    source: Path,
    outputs: dict[str, Path],
    bounds: tuple[float, float, float, float],
    config: dict,
    dpi: int,
    artifact: dict,
) -> None:
    doc = ezdxf.readfile(source)
    audit = doc.audit()
    if audit.errors:
        raise RuntimeError(f"DXF com erros de auditoria: {source} ({len(audit.errors)})")

    x0, y0, x1, y1 = bounds
    width_mm = x1 - x0
    height_mm = y1 - y0
    matplotlib.rcParams["svg.hashsalt"] = "portfolio-autocad-eletrica-a3-v1"
    for kind, output_path in outputs.items():
        # Cada backend recebe uma figura nova. Reutilizar a mesma figura entre SVG,
        # PDF e PNG pode conservar caches de transformacao dependentes do backend.
        # O documento tambem e reaberto porque o frontend do ezdxf mantem caches de
        # resolucao de texto que dependem do primeiro backend utilizado.
        render_doc = ezdxf.readfile(source)
        modelspace = render_doc.modelspace()
        fig = plt.figure(
            figsize=(width_mm / MM_PER_INCH, height_mm / MM_PER_INCH),
            dpi=dpi,
            facecolor="white",
        )
        ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
        ax.set_facecolor("white")
        ax.set_axis_off()
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)

        context = RenderContext(render_doc)
        context.set_current_layout(modelspace)
        layout_properties = LayoutProperties.from_layout(modelspace)
        layout_properties.set_colors("#ffffff", "#000000")
        backend = MatplotlibBackend(ax, adjust_figure=False)
        backend.set_background("#ffffff")
        Frontend(context, backend).draw_layout(
            modelspace,
            finalize=False,
            layout_properties=layout_properties,
        )

        # O backend pode ajustar os limites; restaurar a folha garante A3 exato.
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_kwargs = {
            "format": kind,
            "facecolor": "white",
            "edgecolor": "none",
            "transparent": False,
            "metadata": output_metadata(kind, config, artifact),
        }
        if kind == "png":
            save_kwargs["dpi"] = dpi
        fig.savefig(output_path, **save_kwargs)
        plt.close(fig)
        if kind == "svg":
            # Matplotlib usa o separador nativo da plataforma; normalizar evita
            # hashes diferentes entre Windows e ambientes Unix.
            svg_text = output_path.read_text(encoding="utf-8")
            output_path.write_text(svg_text, encoding="utf-8", newline="\n")
    if "pdf" in outputs:
        _add_searchable_text_layer(source, outputs["pdf"])


def artifact_bounds(artifact: dict, config: dict) -> tuple[float, float, float, float]:
    if artifact.get("require_a3", False):
        return (0.0, 0.0, float(config["page"]["width"]), float(config["page"]["height"]))
    if artifact["id"] == "carimbo-a3":
        return (0.0, 0.0, 180.0, 58.0)
    raise ValueError(f"Limites nao definidos para o artefato {artifact['id']}")


def build_manifest(root: Path, config: dict, rendered: list[dict], dpi: int) -> Path:
    manifest = {
        "schema_version": 1,
        "generated_on": config["portfolio"]["template_date"],
        "source_format": "DXF",
        "dxf_writer": f"ezdxf {ezdxf.__version__}",
        "renderer": f"matplotlib {matplotlib.__version__}",
        "dpi": dpi,
        "artifacts": rendered,
    }
    path = root / "renders" / "manifesto.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositorio")
    parser.add_argument("--dpi", type=int, default=RENDER_DPI, help="Resolucao do PNG")
    parser.add_argument(
        "--artifact",
        action="append",
        dest="artifacts",
        help="ID de um artefato para renderizar; pode ser informado mais de uma vez",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config = load_config(root)
    available = {artifact["id"] for artifact in config["artifacts"]}
    requested = set(args.artifacts or [])
    unknown = sorted(requested - available)
    if unknown:
        raise SystemExit("Artefato(s) desconhecido(s): " + ", ".join(unknown))

    selected = [
        artifact
        for artifact in config["artifacts"]
        if not requested or artifact["id"] in requested
    ]
    for artifact in selected:
        source = root / artifact["source"]
        outputs = {
            kind: root / artifact[kind]
            for kind in ("svg", "pdf", "png")
            if kind in artifact
        }
        render_document(source, outputs, artifact_bounds(artifact, config), config, args.dpi, artifact)
        print(f"Renderizado: {artifact['id']} -> {', '.join(sorted(outputs))}")

    # Rebuild complete manifest hashes so selective rendering preserves records for
    # every other artifact while still updating the files just rendered.
    rendered = [manifest_artifact(root, artifact) for artifact in config["artifacts"]]
    manifest = build_manifest(root, config, rendered, args.dpi)
    print(f"Manifesto: {manifest.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
