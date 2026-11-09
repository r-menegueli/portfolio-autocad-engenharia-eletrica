"""Cria folhas de contato, cadernos PDF A3 e pacote-fonte dos desenhos P23-P25."""

from __future__ import annotations

from pathlib import Path
import zipfile

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfWriter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent.parent / "outputs"
PROJECTS = {
    "P23": ("23-complexo-siderurgico-eaf", "Complexo siderúrgico EAF", "P23_Complexo_Siderurgico_EAF_10_pranchas_A3.pdf"),
    "P24": ("24-linha-transmissao-138kv", "Linha de transmissão 138 kV", "P24_Linha_Transmissao_138kV_10_pranchas_A3.pdf"),
    "P25": ("25-usina-cogeracao-biomassa", "Cogeração com biomassa", "P25_Cogeracao_Biomassa_10_pranchas_A3.pdf"),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf")
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def create_contact_sheet(project_id: str, folder: Path, title: str, output: Path) -> None:
    files = sorted((folder / "exports").glob("*.png"))
    if len(files) != 10:
        raise RuntimeError(f"{project_id}: esperadas 10 folhas PNG, encontradas {len(files)}")

    columns = 2
    margin = 28
    cell_width = 860
    image_height = round(cell_width * 297 / 420)
    label_height = 44
    row_height = label_height + image_height + 26
    rows = (len(files) + columns - 1) // columns
    width = margin * 2 + columns * cell_width + (columns - 1) * margin
    height = margin + 64 + rows * row_height + margin
    canvas = Image.new("RGB", (width, height), "#f1f3f7")
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, margin), f"{project_id} — {title}", fill="#19324d", font=font(36, True))

    for index, path in enumerate(files):
        row, col = divmod(index, columns)
        x = margin + col * (cell_width + margin)
        y = margin + 64 + row * row_height
        label = path.stem.split("_", 1)[-1].replace("_", " ")
        draw.text((x, y), f"{index + 1:02d}  {label}", fill="#263b52", font=font(20, True))
        image = Image.open(path).convert("RGB")
        image.thumbnail((cell_width, image_height), Image.Resampling.LANCZOS)
        frame = Image.new("RGB", (cell_width, image_height), "white")
        frame.paste(image, ((cell_width - image.width) // 2, (image_height - image.height) // 2))
        canvas.paste(frame, (x, y + label_height))
        draw.rectangle((x, y + label_height, x + cell_width - 1, y + label_height + image_height - 1), outline="#bac5d1", width=2)

    canvas.save(output, format="PNG", optimize=True)


def create_book(project_id: str, folder: Path, title: str, output: Path) -> None:
    files = sorted((folder / "exports").glob("*.pdf"))
    if len(files) != 10:
        raise RuntimeError(f"{project_id}: esperados 10 PDFs, encontrados {len(files)}")
    writer = PdfWriter()
    for path in files:
        writer.append(path)
    writer.add_metadata({"/Title": f"{project_id} — {title} — 10 pranchas A3", "/Author": "Rogério Eduardo Moreira Menegueli"})
    with output.open("wb") as stream:
        writer.write(stream)
    writer.close()


def create_source_zip(output: Path) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
        for project_id, (folder_name, _, _) in PROJECTS.items():
            project = ROOT / folder_name
            for subdir in ("fonte", "exports"):
                for path in sorted((project / subdir).glob("*")):
                    if path.is_file() and path.suffix.lower() in {".dxf", ".pdf", ".svg", ".png"}:
                        archive.write(path, Path(project_id) / subdir / path.name)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for project_id, (folder_name, title, book_name) in PROJECTS.items():
        folder = ROOT / folder_name
        preview = OUTPUT / f"{project_id}_pranchas_previa.png"
        book = OUTPUT / book_name
        create_contact_sheet(project_id, folder, title, preview)
        create_book(project_id, folder, title, book)
        print(f"{preview.name}; {book.name}")
    package = OUTPUT / "Desenhos_P23-P25_DXF_PDF_SVG_PNG.zip"
    create_source_zip(package)
    print(f"{package.name}")


if __name__ == "__main__":
    main()
