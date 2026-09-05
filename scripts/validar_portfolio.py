"""Validador somente leitura da infraestrutura e dos futuros projetos do portfolio."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import fnmatch
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Iterable, Iterator
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import ezdxf
from ezdxf import bbox
from markdown_it import MarkdownIt
from PIL import Image
from pypdf import PdfReader

from portfolio_config import ROOT, SheetGeometry, load_config, required_layers


TEXT_TYPES = {"TEXT", "MTEXT", "ATTRIB", "ATTDEF"}
GRAPHIC_SVG_TAGS = {
    "circle",
    "ellipse",
    "image",
    "line",
    "path",
    "polygon",
    "polyline",
    "rect",
    "text",
    "use",
}


@dataclass(order=True, frozen=True)
class Diagnostic:
    severity: str
    code: str
    path: str
    message: str
    entity: str = ""


class Validator:
    def __init__(self, root: Path, *, strict: bool = False) -> None:
        self.root = root.resolve()
        self.strict = strict
        self.config = load_config(self.root)
        self.geometry = SheetGeometry.from_config(self.config)
        self.diagnostics: list[Diagnostic] = []
        self.check_count = 0

    def relative(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    def add(
        self,
        severity: str,
        code: str,
        path: Path | str,
        message: str,
        entity: str = "",
    ) -> None:
        normalized = severity.upper()
        if self.strict and normalized == "WARNING":
            normalized = "ERROR"
            message = f"[strict] {message}"
        self.diagnostics.append(
            Diagnostic(normalized, code, self.relative(Path(path)), message, entity)
        )

    def checked(self, amount: int = 1) -> None:
        self.check_count += amount

    def run(self) -> None:
        self.check_structure()
        self.check_empty_files()
        self.check_temporary_files()
        self.check_markdown_links()
        self.check_project_contracts()
        self.check_artifacts()
        self.check_manifest()
        self.check_dwg_files()

    def walk_files(self) -> Iterator[Path]:
        excluded = set(self.config["validation"]["excluded_directories"])
        for path in sorted(self.root.rglob("*"), key=lambda item: item.as_posix().lower()):
            try:
                relative_parts = path.relative_to(self.root).parts
            except ValueError:
                continue
            if any(part in excluded for part in relative_parts):
                continue
            if path.is_file():
                yield path

    def check_structure(self) -> None:
        required_paths = [
            "AGENTS.md",
            "README.md",
            "LICENSE",
            ".gitignore",
            ".gitattributes",
            "portfolio.toml",
            "requirements.txt",
            "relatorio-ferramentas.md",
            "docs/padrao-grafico.md",
            "docs/criterios-tecnicos.md",
            "docs/plano-projetos.md",
            "templates/template-a3.dxf",
            "templates/template-a3.svg",
            "templates/carimbo-a3/README.md",
            "scripts/gerar_template_a3.py",
            "scripts/renderizar.py",
            "scripts/validar_portfolio.py",
        ]
        for item in required_paths:
            self.checked()
            path = self.root / item
            if not path.is_file():
                self.add("ERROR", "STRUCTURE_MISSING", path, "Arquivo obrigatorio ausente.")

    def check_empty_files(self) -> None:
        for path in self.walk_files():
            self.checked()
            if path.stat().st_size == 0:
                self.add("ERROR", "FILE_EMPTY", path, "Arquivo com zero byte.")

    def check_temporary_files(self) -> None:
        patterns = self.config["validation"]["temporary_patterns"]
        for path in self.walk_files():
            self.checked()
            if any(fnmatch.fnmatch(path.name, pattern) for pattern in patterns):
                self.add("ERROR", "TEMPORARY_FILE", path, "Arquivo temporario nao permitido.")

    def markdown_links(self, path: Path) -> Iterable[str]:
        parser = MarkdownIt()
        tokens = parser.parse(path.read_text(encoding="utf-8"))
        for token in tokens:
            children = token.children or []
            for child in children:
                if child.type == "link_open":
                    href = child.attrGet("href")
                    if href:
                        yield href
                elif child.type == "image":
                    src = child.attrGet("src")
                    if src:
                        yield src

    def check_real_case(self, path: Path) -> bool:
        try:
            relative = path.resolve().relative_to(self.root)
        except ValueError:
            return False
        cursor = self.root
        for part in relative.parts:
            try:
                names = {entry.name for entry in cursor.iterdir()}
            except OSError:
                return False
            if part not in names:
                return False
            cursor /= part
        return True

    def check_markdown_links(self) -> None:
        drive_pattern = re.compile(r"^[A-Za-z]:[\\/]")
        for markdown in (path for path in self.walk_files() if path.suffix.lower() == ".md"):
            for raw_link in self.markdown_links(markdown):
                self.checked()
                parsed = urlsplit(raw_link)
                if parsed.scheme in {"http", "https", "mailto"}:
                    continue
                if parsed.scheme == "file":
                    self.add("ERROR", "LINK_FILE_URI", markdown, f"URI file:// proibida: {raw_link}")
                    continue
                link_path = unquote(parsed.path)
                if not link_path:
                    continue
                if link_path.startswith(("/", "\\")) or drive_pattern.match(link_path):
                    self.add("ERROR", "LINK_ABSOLUTE", markdown, f"Link local deve ser relativo: {raw_link}")
                    continue
                candidate = (markdown.parent / link_path).resolve()
                if not candidate.is_relative_to(self.root):
                    self.add("ERROR", "LINK_ESCAPES_ROOT", markdown, f"Link sai do repositorio: {raw_link}")
                elif not candidate.exists():
                    self.add("ERROR", "LINK_BROKEN", markdown, f"Destino inexistente: {raw_link}")
                elif not self.check_real_case(candidate):
                    self.add(
                        "WARNING",
                        "LINK_CASE",
                        markdown,
                        f"Capitalizacao do link difere do arquivo real: {raw_link}",
                    )

    def check_project_contracts(self) -> None:
        projects_root = self.root / "projetos"
        self.checked()
        if not projects_root.is_dir():
            self.add("ERROR", "PROJECTS_DIR_MISSING", projects_root, "Diretorio de projetos ausente.")
            return
        project_dirs = sorted(path for path in projects_root.iterdir() if path.is_dir())
        for project in project_dirs:
            required = [
                "README.md",
                "memorial-descritivo.md",
                "criterios-premissas.md",
                "lista-materiais.csv",
            ]
            for name in required:
                self.checked()
                if not (project / name).is_file():
                    self.add(
                        "ERROR",
                        "PROJECT_FILE_MISSING",
                        project / name,
                        "Arquivo obrigatorio do projeto ausente.",
                    )
            for directory in ("fonte", "exports"):
                self.checked()
                if not (project / directory).is_dir():
                    self.add(
                        "ERROR",
                        "PROJECT_DIR_MISSING",
                        project / directory,
                        "Diretorio obrigatorio do projeto ausente.",
                    )
            readme = project / "README.md"
            if readme.is_file():
                text = normalize_text(readme.read_text(encoding="utf-8"))
                warning = normalize_text(self.config["portfolio"]["warning"])
                self.checked()
                if warning not in text:
                    self.add("ERROR", "NOTICE_MISSING", readme, "Aviso obrigatorio ausente.")

    def check_artifacts(self) -> None:
        for artifact in self.config["artifacts"]:
            source = self.root / artifact["source"]
            self.check_dxf(source, artifact)
            for kind in ("svg", "pdf", "png"):
                if kind not in artifact:
                    continue
                path = self.root / artifact[kind]
                self.checked()
                if not path.is_file():
                    self.add("ERROR", "DERIVATIVE_MISSING", path, f"Artefato {kind.upper()} ausente.")
                    continue
                if path.stat().st_size < int(self.config["validation"]["minimum_file_size"]):
                    self.add("ERROR", "DERIVATIVE_EMPTY", path, "Artefato vazio ou truncado.")
                    continue
                if kind == "svg":
                    self.check_svg(path, require_a3=bool(artifact.get("require_a3")))
                elif kind == "pdf":
                    self.check_pdf(path, require_a3=bool(artifact.get("require_a3")))
                elif kind == "png":
                    self.check_png(path, require_a3=bool(artifact.get("require_a3")))

    def check_dxf(self, path: Path, artifact: dict) -> None:
        self.checked()
        if not path.is_file():
            self.add("ERROR", "DXF_MISSING", path, "Fonte DXF ausente.")
            return
        if path.stat().st_size < int(self.config["validation"]["minimum_file_size"]):
            self.add("ERROR", "DXF_EMPTY", path, "DXF vazio ou truncado.")
            return
        try:
            doc = ezdxf.readfile(path)
        except Exception as exc:  # ezdxf expõe varias excecoes de estrutura/IO
            self.add("ERROR", "DXF_READ", path, f"Falha ao abrir DXF: {exc}")
            return

        auditor = doc.audit()
        self.checked(4)
        if auditor.errors:
            self.add("ERROR", "DXF_AUDIT", path, f"Auditoria encontrou {len(auditor.errors)} erro(s).")
        if auditor.fixes:
            self.add(
                "WARNING",
                "DXF_AUTO_FIX",
                path,
                f"Auditoria aplicou {len(auditor.fixes)} correcao(oes) em memoria.",
            )
        if doc.dxfversion != self.config["portfolio"]["dxf_version"]:
            self.add(
                "ERROR",
                "DXF_VERSION",
                path,
                f"Esperado {self.config['portfolio']['dxf_version']}; encontrado {doc.dxfversion}.",
            )
        if int(doc.header.get("$INSUNITS", 0)) != int(self.config["page"]["insunits"]):
            self.add("ERROR", "DXF_UNITS", path, "Unidade DXF nao declarada como milimetros.")

        names = {layer.dxf.name for layer in doc.layers}
        missing = sorted(set(required_layers(self.config)) - names)
        if missing:
            self.add("ERROR", "DXF_LAYERS", path, "Layers obrigatorios ausentes: " + ", ".join(missing))

        modelspace = doc.modelspace()
        if len(modelspace) == 0:
            self.add("ERROR", "DXF_SEMANTIC_EMPTY", path, "Modelspace sem entidades graficas.")
            return

        try:
            extents = bbox.extents(modelspace, fast=False)
        except Exception as exc:
            self.add("ERROR", "DXF_BBOX", path, f"Nao foi possivel calcular limites: {exc}")
            return
        if not extents.has_data:
            self.add("ERROR", "DXF_NO_EXTENTS", path, "DXF sem limites geometricos calculaveis.")
            return
        coordinates = (*extents.extmin, *extents.extmax)
        if not all(math.isfinite(float(value)) for value in coordinates):
            self.add("ERROR", "DXF_NONFINITE", path, "DXF contem limites NaN ou infinitos.")

        unsupported = sorted({entity.dxftype() for entity in modelspace if entity.dxftype() in {"RAY", "XLINE", "UNDERLAY", "3DSOLID", "BODY", "REGION"}})
        if unsupported:
            self.add(
                "WARNING",
                "DXF_UNBOUNDED_ENTITY",
                path,
                "Entidades com bbox potencialmente imprecisa: " + ", ".join(unsupported),
            )

        if artifact.get("require_notice"):
            self.check_dxf_notice(path, modelspace)
        if artifact.get("require_a3"):
            self.check_a3_geometry(path, doc, modelspace)
            self.check_text_overlaps(path, modelspace)

    def check_dxf_notice(self, path: Path, modelspace) -> None:
        text = " ".join(extract_text(entity) for entity in expanded_entities(modelspace))
        self.checked()
        if normalize_text(self.config["portfolio"]["warning"]) not in normalize_text(text):
            self.add("ERROR", "DXF_NOTICE_MISSING", path, "Aviso obrigatorio nao localizado no DXF.")

    def check_a3_geometry(self, path: Path, doc, modelspace) -> None:
        geometry = self.geometry
        tolerance = geometry.tolerance
        self.checked(3)
        limmin = doc.header.get("$LIMMIN")
        limmax = doc.header.get("$LIMMAX")
        if limmin is None or limmax is None:
            self.add("ERROR", "DXF_LIMITS_MISSING", path, "$LIMMIN/$LIMMAX ausentes.")
        else:
            expected = (0.0, 0.0, geometry.width, geometry.height)
            found = (float(limmin[0]), float(limmin[1]), float(limmax[0]), float(limmax[1]))
            if any(abs(actual - wanted) > tolerance for actual, wanted in zip(found, expected)):
                self.add("ERROR", "DXF_LIMITS", path, f"Limites declarados {found}; esperado {expected}.")

        frame = self.find_frame(modelspace)
        if frame is None:
            self.add("ERROR", "DXF_FRAME", path, "Moldura A3 retangular nao identificada.")
            return

        for entity in modelspace:
            try:
                entity_box = bbox.extents([entity], fast=False)
            except Exception:
                self.add(
                    "WARNING",
                    "DXF_ENTITY_BBOX",
                    path,
                    "Entidade sem bbox calculavel.",
                    entity.dxf.get("handle", ""),
                )
                continue
            if not entity_box.has_data:
                continue
            minimum = entity_box.extmin
            maximum = entity_box.extmax
            handle = entity.dxf.get("handle", "")
            if (
                minimum.x < -tolerance
                or minimum.y < -tolerance
                or maximum.x > geometry.width + tolerance
                or maximum.y > geometry.height + tolerance
            ):
                self.add(
                    "ERROR",
                    "DXF_OUTSIDE_SHEET",
                    path,
                    f"Entidade {entity.dxftype()} fora da folha: {format_box(entity_box)}.",
                    handle,
                )
            if entity.dxf.get("layer", "0") == "00_MOLDURA":
                continue
            if (
                minimum.x < geometry.frame_left - tolerance
                or minimum.y < geometry.frame_bottom - tolerance
                or maximum.x > geometry.frame_right + tolerance
                or maximum.y > geometry.frame_top + tolerance
            ):
                self.add(
                    "ERROR",
                    "DXF_OUTSIDE_FRAME",
                    path,
                    f"Entidade {entity.dxftype()} fora da moldura: {format_box(entity_box)}.",
                    handle,
                )

    def find_frame(self, modelspace):
        geometry = self.geometry
        tolerance = geometry.tolerance
        for entity in modelspace.query('LWPOLYLINE[layer=="00_MOLDURA"]'):
            if not entity.closed:
                continue
            entity_box = bbox.extents([entity], fast=False)
            if not entity_box.has_data:
                continue
            values = (
                entity_box.extmin.x,
                entity_box.extmin.y,
                entity_box.extmax.x,
                entity_box.extmax.y,
            )
            expected = (
                geometry.frame_left,
                geometry.frame_bottom,
                geometry.frame_right,
                geometry.frame_top,
            )
            if all(abs(actual - wanted) <= tolerance for actual, wanted in zip(values, expected)):
                return entity
        return None

    def check_text_overlaps(self, path: Path, modelspace) -> None:
        boxes: list[tuple[object, object, str]] = []
        for entity in expanded_entities(modelspace):
            if entity.dxftype() not in TEXT_TYPES:
                continue
            try:
                text_box = bbox.extents([entity], fast=False)
            except Exception:
                continue
            if not text_box.has_data:
                continue
            width = text_box.extmax.x - text_box.extmin.x
            height = text_box.extmax.y - text_box.extmin.y
            if width <= 0.0 or height <= 0.0:
                continue
            boxes.append((entity, text_box, normalize_text(extract_text(entity))))

        warning_threshold = float(self.config["validation"]["text_overlap_warning_ratio"])
        error_threshold = float(self.config["validation"]["text_overlap_error_ratio"])
        for index, (first, first_box, first_text) in enumerate(boxes):
            for second, second_box, second_text in boxes[index + 1 :]:
                self.checked()
                ratio = overlap_ratio(first_box, second_box, shrink=0.10)
                if ratio <= warning_threshold:
                    continue
                first_handle = first.dxf.get("handle", "virtual")
                second_handle = second.dxf.get("handle", "virtual")
                pair = f"{first_handle}/{second_handle}"
                duplicate = bool(first_text and first_text == second_text)
                if duplicate or ratio >= error_threshold:
                    self.add(
                        "ERROR",
                        "TEXT_OVERLAP",
                        path,
                        f"Textos potencialmente sobrepostos ({ratio:.0%} da menor caixa).",
                        pair,
                    )
                else:
                    self.add(
                        "WARNING",
                        "TEXT_OVERLAP",
                        path,
                        f"Possivel sobreposicao de textos ({ratio:.0%} da menor caixa).",
                        pair,
                    )

    def check_svg(self, path: Path, *, require_a3: bool) -> None:
        self.checked(2)
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except (ET.ParseError, OSError) as exc:
            self.add("ERROR", "SVG_PARSE", path, f"SVG invalido: {exc}")
            return
        if root.tag.split("}")[-1] != "svg":
            self.add("ERROR", "SVG_ROOT", path, "Elemento raiz nao e <svg>.")
            return
        view_box = root.attrib.get("viewBox", "").replace(",", " ").split()
        if len(view_box) != 4:
            self.add("ERROR", "SVG_VIEWBOX", path, "viewBox ausente ou invalido.")
        else:
            try:
                values = [float(value) for value in view_box]
                ratio = values[2] / values[3]
                if not all(math.isfinite(value) for value in values) or values[2] <= 0 or values[3] <= 0:
                    raise ValueError
                if require_a3:
                    self.check_aspect_ratio(path, ratio, "SVG_ASPECT")
            except (ValueError, ZeroDivisionError):
                self.add("ERROR", "SVG_VIEWBOX", path, "viewBox nao finito ou sem area.")
        graphics = sum(1 for element in root.iter() if element.tag.split("}")[-1] in GRAPHIC_SVG_TAGS)
        if graphics == 0:
            self.add("ERROR", "SVG_EMPTY", path, "SVG sem elementos graficos.")

    def check_pdf(self, path: Path, *, require_a3: bool) -> None:
        self.checked(2)
        try:
            reader = PdfReader(path)
        except Exception as exc:
            self.add("ERROR", "PDF_PARSE", path, f"PDF invalido: {exc}")
            return
        if reader.is_encrypted:
            self.add("ERROR", "PDF_ENCRYPTED", path, "PDF nao pode estar criptografado.")
            return
        if not reader.pages:
            self.add("ERROR", "PDF_EMPTY", path, "PDF sem paginas.")
            return
        if require_a3:
            page = reader.pages[0]
            width_mm = float(page.mediabox.width) * 25.4 / 72.0
            height_mm = float(page.mediabox.height) * 25.4 / 72.0
            tolerance = 2.0
            if abs(width_mm - self.geometry.width) > tolerance or abs(height_mm - self.geometry.height) > tolerance:
                self.add(
                    "ERROR",
                    "PDF_PAGE_SIZE",
                    path,
                    f"Pagina {width_mm:.2f} x {height_mm:.2f} mm; esperado A3 paisagem.",
                )

    def check_png(self, path: Path, *, require_a3: bool) -> None:
        self.checked(3)
        try:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                width, height = image.size
                extrema = image.convert("RGB").getextrema()
        except Exception as exc:
            self.add("ERROR", "PNG_PARSE", path, f"PNG invalido: {exc}")
            return
        if width < int(self.config["validation"]["minimum_png_width"]):
            self.add("ERROR", "PNG_RESOLUTION", path, f"Largura insuficiente: {width} px.")
        if require_a3:
            self.check_aspect_ratio(path, width / height, "PNG_ASPECT")
        if all(low == high for low, high in extrema):
            self.add("ERROR", "PNG_UNIFORM", path, "PNG uniforme, sem desenho visivel.")

    def check_aspect_ratio(self, path: Path, ratio: float, code: str) -> None:
        expected = self.geometry.width / self.geometry.height
        tolerance = float(self.config["validation"]["aspect_ratio_tolerance"])
        if abs(ratio - expected) / expected > tolerance:
            self.add("ERROR", code, path, f"Proporcao {ratio:.5f}; esperado {expected:.5f}.")

    def check_manifest(self) -> None:
        path = self.root / "renders" / "manifesto.json"
        self.checked()
        if not path.is_file():
            self.add("ERROR", "MANIFEST_MISSING", path, "Manifesto de renderizacao ausente.")
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.add("ERROR", "MANIFEST_PARSE", path, f"Manifesto invalido: {exc}")
            return
        entries = {entry.get("id"): entry for entry in data.get("artifacts", [])}
        for artifact in self.config["artifacts"]:
            self.checked()
            entry = entries.get(artifact["id"])
            if not entry:
                self.add("ERROR", "MANIFEST_ENTRY", path, f"Entrada ausente: {artifact['id']}")
                continue
            source = self.root / artifact["source"]
            if source.is_file() and entry.get("source_sha256") != sha256(source):
                self.add("ERROR", "MANIFEST_STALE", path, f"Fonte alterada apos render: {artifact['id']}")
            for kind in ("svg", "pdf", "png"):
                if kind not in artifact:
                    continue
                output = self.root / artifact[kind]
                recorded = entry.get("outputs", {}).get(kind, {})
                if output.is_file() and recorded.get("sha256") != sha256(output):
                    self.add("ERROR", "MANIFEST_HASH", path, f"Hash divergente: {artifact['id']} {kind}")

    def check_dwg_files(self) -> None:
        for path in (item for item in self.walk_files() if item.suffix.lower() == ".dwg"):
            self.checked()
            signature = path.read_bytes()[:6]
            if not re.fullmatch(rb"AC10\d{2}", signature):
                self.add(
                    "ERROR",
                    "DWG_SIGNATURE",
                    path,
                    "Arquivo .dwg sem assinatura binaria Autodesk; possivel renomeacao indevida.",
                )
            evidence = path.with_suffix(path.suffix + ".validacao.json")
            if not evidence.is_file():
                self.add(
                    "ERROR",
                    "DWG_EVIDENCE",
                    path,
                    "DWG sem registro de conversao e reabertura verificada.",
                )

    def result(self) -> dict:
        diagnostics = sorted(self.diagnostics)
        errors = sum(item.severity == "ERROR" for item in diagnostics)
        warnings = sum(item.severity == "WARNING" for item in diagnostics)
        return {
            "status": "PASS" if errors == 0 else "FAIL",
            "strict": self.strict,
            "checks": self.check_count,
            "errors": errors,
            "warnings": warnings,
            "diagnostics": [asdict(item) for item in diagnostics],
        }


def expanded_entities(layout) -> Iterator:
    for entity in layout:
        if entity.dxftype() == "INSERT":
            for attrib in entity.attribs:
                yield attrib
            try:
                for virtual in entity.virtual_entities():
                    if virtual.dxftype() == "INSERT":
                        yield from expanded_entities([virtual])
                    else:
                        yield virtual
            except (ezdxf.DXFError, AttributeError):
                continue
        else:
            yield entity


def extract_text(entity) -> str:
    entity_type = entity.dxftype()
    if entity_type == "MTEXT":
        return entity.plain_text()
    if entity_type in {"TEXT", "ATTRIB", "ATTDEF"}:
        return entity.dxf.get("text", "")
    return ""


def normalize_text(value: str) -> str:
    return " ".join(value.replace("\u00a0", " ").split()).casefold()


def overlap_ratio(first, second, *, shrink: float) -> float:
    def shrunken(box):
        width = box.extmax.x - box.extmin.x
        height = box.extmax.y - box.extmin.y
        pad_x = width * shrink / 2.0
        pad_y = height * shrink / 2.0
        return (
            box.extmin.x + pad_x,
            box.extmin.y + pad_y,
            box.extmax.x - pad_x,
            box.extmax.y - pad_y,
        )

    ax0, ay0, ax1, ay1 = shrunken(first)
    bx0, by0, bx1, by1 = shrunken(second)
    width = min(ax1, bx1) - max(ax0, bx0)
    height = min(ay1, by1) - max(ay0, by0)
    if width <= 0.0 or height <= 0.0:
        return 0.0
    overlap = width * height
    first_area = max((ax1 - ax0) * (ay1 - ay0), 1e-9)
    second_area = max((bx1 - bx0) * (by1 - by0), 1e-9)
    return overlap / min(first_area, second_area)


def format_box(box) -> str:
    return (
        f"({box.extmin.x:.2f}, {box.extmin.y:.2f})-"
        f"({box.extmax.x:.2f}, {box.extmax.y:.2f}) mm"
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def print_human(result: dict) -> None:
    print(
        f"VALIDACAO {result['status']} | verificacoes={result['checks']} "
        f"erros={result['errors']} avisos={result['warnings']} strict={result['strict']}"
    )
    for item in result["diagnostics"]:
        entity = f" entidade={item['entity']}" if item["entity"] else ""
        print(f"[{item['severity']}] {item['code']} {item['path']}{entity}: {item['message']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositorio")
    parser.add_argument("--strict", action="store_true", help="Converte avisos em erros")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    parser.add_argument("--report", type=Path, help="Grava copia JSON do resultado")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = Validator(args.root, strict=args.strict)
    try:
        validator.run()
    except Exception as exc:
        print(f"ERRO INTERNO DO VALIDADOR: {exc}", file=sys.stderr)
        return 2
    result = validator.result()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
