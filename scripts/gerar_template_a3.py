"""Gera o template A3 e o carimbo em DXF real, sem depender de AutoCAD."""

from __future__ import annotations

import argparse
from pathlib import Path

import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment

from portfolio_config import ROOT, SheetGeometry, load_config, required_layers


TITLE_BLOCK_NAME = "CARIMBO_A3"
TEXT_STYLE = "PORTFOLIO_TEXTO"
TITLE_STYLE = "PORTFOLIO_TITULO"

# O ezdxf normalmente grava horario e GUIDs novos a cada save. A opcao oficial
# abaixo fixa apenas esses metadados tecnicos; a data documental permanece no
# carimbo e nos metadados PORTFOLIO_* definidos pelo gerador.
ezdxf.options.write_fixed_meta_data_for_testing = True


def add_rect(layout, x0: float, y0: float, x1: float, y1: float, layer: str) -> None:
    layout.add_lwpolyline(
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        close=True,
        dxfattribs={"layer": layer},
    )


def add_line(layout, start: tuple[float, float], end: tuple[float, float], layer: str) -> None:
    layout.add_line(start, end, dxfattribs={"layer": layer})


def add_text(
    layout,
    value: str,
    point: tuple[float, float],
    height: float,
    layer: str = "02_TEXTO",
    align: TextEntityAlignment = TextEntityAlignment.LEFT,
    style: str = TEXT_STYLE,
    rotation: float = 0.0,
) -> None:
    text = layout.add_text(
        value,
        dxfattribs={
            "height": height,
            "layer": layer,
            "style": style,
            "rotation": rotation,
        },
    )
    text.set_placement(point, align=align)


def add_mtext(
    layout,
    value: str,
    point: tuple[float, float],
    width: float,
    height: float,
    layer: str,
    style: str = TEXT_STYLE,
) -> None:
    entity = layout.add_mtext(
        value,
        dxfattribs={
            "char_height": height,
            "width": width,
            "layer": layer,
            "style": style,
            "attachment_point": 1,
            "line_spacing_factor": 1.18,
        },
    )
    entity.set_location(point)


def configure_document(config: dict, *, limits: tuple[float, float]) -> ezdxf.document.Drawing:
    doc = ezdxf.new("R2013", setup=True, units=units.MM)
    doc.units = units.MM
    doc.header["$INSUNITS"] = int(config["page"]["insunits"])
    doc.header["$MEASUREMENT"] = 1
    doc.header["$LIMMIN"] = (0.0, 0.0)
    doc.header["$LIMMAX"] = limits
    doc.header["$EXTMIN"] = (0.0, 0.0, 0.0)
    doc.header["$EXTMAX"] = (limits[0], limits[1], 0.0)

    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_TEMPLATE_DATE"] = config["portfolio"]["template_date"]
    metadata["PORTFOLIO_AUTHOR"] = config["portfolio"]["author"]
    metadata["PORTFOLIO_UNITS"] = config["page"]["units"]

    for layer_name in required_layers(config):
        style = config["layer_styles"][layer_name]
        if layer_name in doc.layers:
            layer = doc.layers.get(layer_name)
        else:
            layer = doc.layers.add(layer_name)
        layer.color = int(style["color"])
        layer.dxf.lineweight = int(style["lineweight"])
        layer.dxf.linetype = style["linetype"]

    if TEXT_STYLE not in doc.styles:
        doc.styles.add(TEXT_STYLE, font="arial.ttf")
    if TITLE_STYLE not in doc.styles:
        doc.styles.add(TITLE_STYLE, font="arialbd.ttf")
    doc.styles.get(TITLE_STYLE).dxf.width = 0.92
    return doc


def define_title_block(doc: ezdxf.document.Drawing) -> None:
    block = doc.blocks.new(name=TITLE_BLOCK_NAME, base_point=(0.0, 0.0))
    add_rect(block, 0.0, 0.0, 180.0, 58.0, "01_CARIMBO")
    for y in (10.0, 21.0, 37.0):
        add_line(block, (0.0, y), (180.0, y), "01_CARIMBO")
    for x in (90.0, 120.0, 145.0, 160.0):
        add_line(block, (x, 0.0), (x, 10.0), "01_CARIMBO")
    for x in (100.0, 140.0, 158.0):
        add_line(block, (x, 10.0), (x, 21.0), "01_CARIMBO")
    add_line(block, (148.0, 37.0), (148.0, 58.0), "01_CARIMBO")

    add_text(block, "PORTFOLIO DE", (4.0, 52.5), 3.1, style=TITLE_STYLE)
    add_text(block, "ENGENHARIA ELETRICA", (4.0, 46.3), 4.2, style=TITLE_STYLE)
    add_text(block, "BASE ACADEMICA REPRODUZIVEL", (4.0, 41.1), 2.1)
    add_text(
        block,
        "A3",
        (164.0, 47.5),
        8.0,
        align=TextEntityAlignment.MIDDLE_CENTER,
        style=TITLE_STYLE,
    )
    add_text(
        block,
        "PAISAGEM",
        (164.0, 40.8),
        1.7,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )

    labels = [
        ("TITULO", (3.0, 34.4)),
        ("AUTOR", (3.0, 18.5)),
        ("DATA", (103.0, 18.5)),
        ("REV.", (143.0, 18.5)),
        ("PRANCHA", (160.5, 18.5)),
        ("ARQUIVO", (3.0, 7.5)),
        ("UNIDADES", (92.0, 7.5)),
        ("ESCALA", (122.0, 7.5)),
        ("FOLHA", (147.0, 7.5)),
        ("STATUS", (162.0, 7.5)),
    ]
    for label, point in labels:
        add_text(block, label, point, 1.35, layer="01_CARIMBO")

    attributes = [
        ("TITULO", (3.0, 25.3), 3.3, 174.0),
        ("AUTOR", (3.0, 12.7), 2.25, 94.0),
        ("DATA", (103.0, 12.7), 2.25, 34.0),
        ("REVISAO", (143.0, 12.7), 2.25, 12.0),
        ("PRANCHA", (160.5, 12.7), 2.25, 16.5),
        ("ARQUIVO", (3.0, 2.5), 1.9, 84.0),
        ("UNIDADES", (92.0, 2.5), 1.9, 24.0),
        ("ESCALA", (122.0, 2.5), 1.9, 19.0),
        ("FOLHA", (147.0, 2.5), 1.9, 10.0),
        ("STATUS", (162.0, 2.5), 1.9, 15.0),
    ]
    for tag, point, height, width in attributes:
        block.add_attdef(
            tag=tag,
            insert=point,
            height=height,
            dxfattribs={
                "layer": "02_TEXTO",
                "style": TEXT_STYLE,
                "field_length": int(width),
            },
        )


def title_values(config: dict) -> dict[str, str]:
    return {
        "TITULO": "TEMPLATE A3 - INFRAESTRUTURA DO PORTFOLIO",
        "AUTOR": config["portfolio"]["author"],
        "DATA": config["portfolio"]["template_date"],
        "REVISAO": "00",
        "PRANCHA": "00/00",
        "ARQUIVO": "template-a3.dxf",
        "UNIDADES": "mm",
        "ESCALA": "1:1",
        "FOLHA": "A3",
        "STATUS": "MODELO",
    }


def add_frame(layout, geometry: SheetGeometry) -> None:
    add_rect(
        layout,
        geometry.frame_left,
        geometry.frame_bottom,
        geometry.frame_right,
        geometry.frame_top,
        "00_MOLDURA",
    )
    # Marcas de zona permanecem dentro da moldura para facilitar referencias.
    letters = "ABCDEFGH"
    step_x = (geometry.frame_right - geometry.frame_left) / len(letters)
    for index, letter in enumerate(letters):
        center_x = geometry.frame_left + (index + 0.5) * step_x
        add_text(
            layout,
            letter,
            (center_x, geometry.frame_top - 2.5),
            1.7,
            layer="00_MOLDURA",
            align=TextEntityAlignment.MIDDLE_CENTER,
        )
        if index:
            x = geometry.frame_left + index * step_x
            add_line(layout, (x, geometry.frame_top), (x, geometry.frame_top - 3.0), "00_MOLDURA")
    numbers = "12345"
    step_y = (geometry.frame_top - geometry.frame_bottom) / len(numbers)
    for index, number in enumerate(numbers):
        center_y = geometry.frame_bottom + (index + 0.5) * step_y
        add_text(
            layout,
            number,
            (geometry.frame_left + 2.5, center_y),
            1.7,
            layer="00_MOLDURA",
            align=TextEntityAlignment.MIDDLE_CENTER,
        )


def define_symbols(doc: ezdxf.document.Drawing) -> None:
    terminal = doc.blocks.new(name="SIM_TERMINAL", base_point=(0.0, 0.0))
    terminal.add_circle((0.0, 0.0), radius=2.0, dxfattribs={"layer": "09_BORNES"})

    motor = doc.blocks.new(name="SIM_MOTOR", base_point=(0.0, 0.0))
    motor.add_circle((0.0, 0.0), radius=4.0, dxfattribs={"layer": "04_EQUIPAMENTOS"})
    add_text(
        motor,
        "M",
        (0.0, 0.0),
        3.0,
        layer="04_EQUIPAMENTOS",
        align=TextEntityAlignment.MIDDLE_CENTER,
        style=TITLE_STYLE,
    )

    ground = doc.blocks.new(name="SIM_TERRA", base_point=(0.0, 0.0))
    add_line(ground, (0.0, 3.0), (0.0, 0.0), "05_POTENCIA")
    add_line(ground, (-3.5, 0.0), (3.5, 0.0), "05_POTENCIA")
    add_line(ground, (-2.4, -1.4), (2.4, -1.4), "05_POTENCIA")
    add_line(ground, (-1.2, -2.8), (1.2, -2.8), "05_POTENCIA")

    breaker = doc.blocks.new(name="SIM_DISJUNTOR", base_point=(0.0, 0.0))
    add_line(breaker, (-5.0, 0.0), (-2.0, 0.0), "05_POTENCIA")
    add_line(breaker, (-2.0, 0.0), (2.5, 3.0), "05_POTENCIA")
    add_line(breaker, (2.0, 0.0), (5.0, 0.0), "05_POTENCIA")


def add_legend(layout) -> None:
    add_rect(layout, 18.0, 170.0, 103.0, 267.0, "12_LEGENDA")
    add_text(layout, "LEGENDA-BASE", (22.0, 260.0), 3.2, layer="12_LEGENDA", style=TITLE_STYLE)
    add_line(layout, (22.0, 256.0), (99.0, 256.0), "12_LEGENDA")

    symbols = [
        ("SIM_DISJUNTOR", (30.0, 245.0), "Disjuntor / protecao"),
        ("SIM_MOTOR", (30.0, 233.0), "Motor trifasico"),
        ("SIM_TERMINAL", (30.0, 221.0), "Borne de conexao"),
        ("SIM_TERRA", (30.0, 209.0), "Aterramento"),
    ]
    for block_name, point, label in symbols:
        layout.add_blockref(block_name, point)
        add_text(layout, label, (40.0, point[1] - 1.2), 2.1, layer="12_LEGENDA")

    add_text(layout, "CAMADAS FUNCIONAIS", (22.0, 196.0), 2.1, layer="12_LEGENDA", style=TITLE_STYLE)
    samples = [
        ("05_POTENCIA", "Potencia"),
        ("06_COMANDO", "Comando"),
        ("07_INSTRUMENTACAO", "Instrumentacao"),
        ("08_CABOS", "Cabos"),
        ("10_ELETROCALHAS", "Eletrocalhas"),
    ]
    for index, (layer, label) in enumerate(samples):
        y = 189.0 - index * 4.2
        add_line(layout, (22.0, y), (36.0, y), layer)
        add_text(layout, label, (40.0, y - 1.0), 1.8, layer="12_LEGENDA")


def add_notes(layout, warning: str) -> None:
    add_rect(layout, 18.0, 18.0, 224.0, 66.0, "13_NOTAS")
    add_text(layout, "NOTAS TECNICAS", (22.0, 60.0), 3.0, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(
        layout,
        "1. Fonte CAD: DXF R2013 (AC1027); unidades declaradas em milimetros.\\P"
        "2. O PDF, o SVG e o PNG sao derivados para revisao; o DXF e a fonte principal.\\P"
        "3. Confirmar premissas, versoes normativas e dimensionamentos antes de cada projeto.",
        (22.0, 55.0),
        198.0,
        2.1,
        "13_NOTAS",
    )
    add_rect(layout, 18.0, 70.0, 224.0, 93.0, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATORIO", (22.0, 87.5), 2.4, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22.0, 83.0), 198.0, 2.15, "13_NOTAS")


def add_revision_table(layout) -> None:
    add_rect(layout, 230.0, 72.0, 410.0, 94.0, "01_CARIMBO")
    add_line(layout, (230.0, 86.0), (410.0, 86.0), "01_CARIMBO")
    for x in (248.0, 280.0, 352.0):
        add_line(layout, (x, 72.0), (x, 94.0), "01_CARIMBO")
    headers = [
        ("REV.", (239.0, 89.5)),
        ("DATA", (264.0, 89.5)),
        ("DESCRICAO", (316.0, 89.5)),
        ("RESP.", (381.0, 89.5)),
    ]
    for value, point in headers:
        add_text(
            layout,
            value,
            point,
            1.8,
            layer="01_CARIMBO",
            align=TextEntityAlignment.MIDDLE_CENTER,
            style=TITLE_STYLE,
        )
    values = [
        ("00", (239.0, 78.5)),
        ("2026-09-05", (264.0, 78.5)),
        ("EMISSAO INICIAL DO MODELO", (316.0, 78.5)),
        ("R.E.M.M.", (381.0, 78.5)),
    ]
    for value, point in values:
        add_text(
            layout,
            value,
            point,
            1.8,
            align=TextEntityAlignment.MIDDLE_CENTER,
        )


def build_template(config: dict, output_path: Path) -> None:
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    define_title_block(doc)
    define_symbols(doc)
    msp = doc.modelspace()
    add_frame(msp, geometry)

    add_text(
        msp,
        "AREA UTIL DO DESENHO",
        (257.0, 181.0),
        5.0,
        layer="11_ARQUITETURA",
        align=TextEntityAlignment.MIDDLE_CENTER,
        style=TITLE_STYLE,
    )
    add_text(
        msp,
        "Inserir aqui o conteudo tecnico do projeto",
        (257.0, 172.0),
        2.5,
        layer="11_ARQUITETURA",
        align=TextEntityAlignment.MIDDLE_CENTER,
    )
    add_rect(msp, 111.0, 104.0, 404.0, 267.0, "11_ARQUITETURA")
    add_line(msp, (257.5, 104.0), (257.5, 267.0), "03_COTAS")
    add_line(msp, (111.0, 185.5), (404.0, 185.5), "03_COTAS")
    add_legend(msp)
    add_notes(msp, config["portfolio"]["warning"])
    add_revision_table(msp)

    insert = msp.add_blockref(TITLE_BLOCK_NAME, (230.0, 10.0), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(title_values(config))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wt", encoding="utf-8", newline="\n") as stream:
        doc.write(stream)


def build_title_block(config: dict, output_path: Path) -> None:
    doc = configure_document(config, limits=(180.0, 58.0))
    define_title_block(doc)
    msp = doc.modelspace()
    insert = msp.add_blockref(TITLE_BLOCK_NAME, (0.0, 0.0), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(title_values(config))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wt", encoding="utf-8", newline="\n") as stream:
        doc.write(stream)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositorio")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config = load_config(root)
    build_template(config, root / "templates" / "template-a3.dxf")
    build_title_block(config, root / "templates" / "carimbo-a3" / "carimbo-a3.dxf")
    print("DXFs gerados com sucesso:")
    print("- templates/template-a3.dxf")
    print("- templates/carimbo-a3/carimbo-a3.dxf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
