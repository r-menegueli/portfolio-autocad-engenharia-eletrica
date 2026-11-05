"""Renderiza os DXFs declarados em portfolio.toml para SVG, PDF e PNG."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import ezdxf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from ezdxf.addons.drawing import Frontend, RenderContext  # noqa: E402
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend  # noqa: E402
from ezdxf.addons.drawing.properties import LayoutProperties  # noqa: E402

from portfolio_config import ROOT, load_config


MM_PER_INCH = 25.4
RENDER_DPI = 300


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def artifact_bounds(artifact: dict, config: dict) -> tuple[float, float, float, float]:
    if artifact.get("require_a3", False):
        return (0.0, 0.0, float(config["page"]["width"]), float(config["page"]["height"]))
    if artifact["id"] == "carimbo-a3":
        return (0.0, 0.0, 180.0, 58.0)
    raise ValueError(f"Limites nao definidos para o artefato {artifact['id']}")


def build_manifest(root: Path, config: dict, rendered: list[dict]) -> Path:
    manifest = {
        "schema_version": 1,
        "generated_on": config["portfolio"]["template_date"],
        "source_format": "DXF",
        "dxf_writer": f"ezdxf {ezdxf.__version__}",
        "renderer": f"matplotlib {matplotlib.__version__}",
        "dpi": RENDER_DPI,
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
        default=[],
        help="ID de artefato a renderizar (pode repetir); preserva somente entradas inalteradas do manifesto",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config = load_config(root)
    artifacts = config["artifacts"]
    by_id = {artifact["id"]: artifact for artifact in artifacts}
    requested = set(args.artifact)
    unknown = requested - by_id.keys()
    if unknown:
        raise SystemExit("Artefato(s) desconhecido(s): " + ", ".join(sorted(unknown)))
    if requested and args.dpi != RENDER_DPI:
        raise SystemExit("A renderizacao parcial so aceita a resolucao oficial de 300 dpi.")
    selected = requested or set(by_id)
    rendered_by_id: dict[str, dict] = {}

    manifest_path = root / "renders" / "manifesto.json"
    previous_entries: dict[str, dict] = {}
    if manifest_path.is_file():
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        previous_entries = {entry["id"]: entry for entry in previous.get("artifacts", [])}

    for artifact in artifacts:
        if artifact["id"] in selected:
            continue
        entry = previous_entries.get(artifact["id"])
        source = root / artifact["source"]
        if not entry or entry.get("source") != artifact["source"] or entry.get("source_sha256") != sha256(source):
            raise SystemExit(f"Sem entrada de manifesto atual para {artifact['id']}; execute a renderizacao completa.")
        for kind, output_path in ((kind, root / artifact[kind]) for kind in ("svg", "pdf", "png") if kind in artifact):
            recorded = entry.get("outputs", {}).get(kind, {})
            if not output_path.is_file() or recorded.get("path") != str(output_path.relative_to(root)).replace("\\", "/") or recorded.get("sha256") != sha256(output_path):
                raise SystemExit(f"Derivado alterado para {artifact['id']} ({kind}); execute a renderizacao completa.")
        rendered_by_id[artifact["id"]] = entry

    for artifact in artifacts:
        if artifact["id"] not in selected:
            continue
        source = root / artifact["source"]
        outputs = {
            kind: root / artifact[kind]
            for kind in ("svg", "pdf", "png")
            if kind in artifact
        }
        render_document(source, outputs, artifact_bounds(artifact, config), config, args.dpi, artifact)
        rendered_by_id[artifact["id"]] = {
            "id": artifact["id"],
            "source": artifact["source"],
            "source_sha256": sha256(source),
            "outputs": {
                kind: {"path": str(path.relative_to(root)).replace("\\", "/"), "sha256": sha256(path)}
                for kind, path in sorted(outputs.items())
            },
        }
        print(f"Renderizado: {artifact['id']} -> {', '.join(sorted(outputs))}")

    rendered = [rendered_by_id[artifact["id"]] for artifact in artifacts]
    manifest = build_manifest(root, config, rendered)
    print(f"Manifesto: {manifest.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
