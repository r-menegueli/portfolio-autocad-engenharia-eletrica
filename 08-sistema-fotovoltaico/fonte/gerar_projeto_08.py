"""Gera as seis pranchas DXF do Projeto 08 de forma determinística."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment


PROJECT_DIR = Path(__file__).resolve().parents[1]
ROOT = PROJECT_DIR.parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from gerar_template_a3 import (  # noqa: E402
    TITLE_BLOCK_NAME,
    TITLE_STYLE,
    add_frame,
    add_line,
    add_mtext,
    add_rect,
    add_text,
    configure_document,
    define_symbols,
    define_title_block,
    prepare_deterministic_write,
)
from portfolio_config import SheetGeometry, load_config  # noqa: E402


PROJECT_SLUG = "08-sistema-fotovoltaico"
PROJECT_DATE = "2026-09-09"
REVISION = "00"


@dataclass(frozen=True)
class SheetSpec:
    number: int
    filename: str
    title: str
    subtitle: str
    notes: str
    legend: str


SHEETS = (
    SheetSpec(
        1,
        "01_disposicao_modulos.dxf",
        "DISPOSIÇÃO DOS MÓDULOS",
        "Arranjo acadêmico de 6,60 kWp em duas strings independentes",
        "Implantação esquemática, sem levantamento de sombras ou validação estrutural.\\P"
        "Orientação, inclinação, afastamentos e acesso devem ser confirmados no local.",
        "Amarelo: módulos | Laranja: CC | Verde: PE | S1/S2: strings | MPPT: rastreamento",
    ),
    SheetSpec(
        2,
        "02_diagrama_unifilar_cc.dxf",
        "DIAGRAMA UNIFILAR CC",
        "Strings separadas, proteção, seccionamento e entradas MPPT",
        "Polos positivo e negativo não são intencionalmente aterrados neste conceito.\\P"
        "Tensões e correntes derivam de dados fictícios e exigem validação do fabricante.",
        "F: fusível gPV | DPS: proteção contra surtos | QDC: seccionador | PE: proteção",
    ),
    SheetSpec(
        3,
        "03_diagrama_unifilar_ca.dxf",
        "DIAGRAMA UNIFILAR CA",
        "Inversor 6 kWca, proteção dedicada e conexão residencial 220 V",
        "Anti-ilhamento e parâmetros de rede pertencem ao inversor homologado e à distribuidora.\\P"
        "O circuito CA, Icn, seletividade e aterramento devem ser recalculados no imóvel.",
        "QSD: seccionador | QF: disjuntor | DPS: proteção contra surtos | MED: medidor",
    ),
    SheetSpec(
        4,
        "04_string_box.dxf",
        "STRING BOX",
        "Proteções CC independentes para S1/MPPT1 e S2/MPPT2",
        "A string box não coloca S1 e S2 em paralelo; cada saída alimenta um MPPT.\\P"
        "Confirmar polaridade, Ucpv, Up, corrente, Icc, IP, temperatura e coordenação.",
        "gPV: fusível FV | DPS CC: tipo 2 FV | QDC: manobra sob carga | X: terminal",
    ),
    SheetSpec(
        5,
        "05_aterramento.dxf",
        "ATERRAMENTO E EQUIPOTENCIALIZAÇÃO",
        "Molduras, estruturas, invólucros, DPS e barramento principal",
        "A interface com eletrodo, esquema de aterramento e SPDA existentes não foi projetada.\\P"
        "Aplicar análise de risco e a série ABNT NBR 5419:2026 na revisão profissional.",
        "PE: condutor de proteção | BEP: equipotencial principal | SPDA: descargas atmosféricas",
    ),
    SheetSpec(
        6,
        "06_layout_equipamentos.dxf",
        "LAYOUT DOS EQUIPAMENTOS",
        "Telhado, parede técnica, rotas segregadas e ponto de conexão",
        "Posições e folgas são propostas, não instruções de montagem.\\P"
        "Validar acesso, ventilação, IP, raios de curvatura, estrutura e padrão da distribuidora.",
        "Laranja: CC | Vermelho: CA | Verde: PE | Cinza: arquitetura | Tracejado: folga",
    ),
)


def read_rows(project: Path, filename: str) -> list[dict[str, str]]:
    with (project / filename).open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def line(layout, start: tuple[float, float], end: tuple[float, float], layer: str) -> None:
    add_line(layout, start, end, layer)


def centered(
    layout,
    value: str,
    point: tuple[float, float],
    height: float = 1.45,
    layer: str = "02_TEXTO",
) -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER)


def left(
    layout,
    value: str,
    point: tuple[float, float],
    height: float = 1.3,
    layer: str = "02_TEXTO",
) -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_LEFT)


def orthogonal(layout, points: tuple[tuple[float, float], ...], layer: str) -> None:
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)


def arrow(
    layout,
    start: tuple[float, float],
    end: tuple[float, float],
    layer: str,
    label: str = "",
    label_offset: tuple[float, float] = (0.0, 4.0),
) -> None:
    line(layout, start, end, layer)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base = (end[0] - 4.0 * ux, end[1] - 4.0 * uy)
    layout.add_lwpolyline(
        [end, (base[0] + 1.6 * px, base[1] + 1.6 * py), (base[0] - 1.6 * px, base[1] - 1.6 * py)],
        close=True,
        dxfattribs={"layer": layer},
    )
    if label:
        centered(
            layout,
            label,
            ((start[0] + end[0]) / 2 + label_offset[0], (start[1] + end[1]) / 2 + label_offset[1]),
            1.1,
            layer,
        )


def component(
    layout,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    tag: str,
    detail: str,
    layer: str = "04_EQUIPAMENTOS",
    detail_layer: str = "02_TEXTO",
) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered(layout, tag, ((x0 + x1) / 2, y1 - 5.0), 1.55, layer)
    centered(layout, detail, ((x0 + x1) / 2, y0 + 4.0), 1.0, detail_layer)


def table(
    layout,
    x: float,
    top: float,
    widths: tuple[float, ...],
    headers: tuple[str, ...],
    rows: list[tuple[str, ...]],
    *,
    row_height: float,
    text_height: float = 0.95,
    layer: str = "12_LEGENDA",
) -> None:
    total_width = sum(widths)
    total_height = row_height * (len(rows) + 1)
    add_rect(layout, x, top - total_height, x + total_width, top, layer)
    cursor = x
    centers: list[float] = []
    for width in widths:
        centers.append(cursor + width / 2)
        cursor += width
        if cursor < x + total_width - 0.001:
            line(layout, (cursor, top - total_height), (cursor, top), layer)
    for index in range(1, len(rows) + 1):
        y = top - row_height * index
        line(layout, (x, y), (x + total_width, y), layer)
    for value, cx in zip(headers, centers):
        centered(layout, value, (cx, top - row_height / 2), text_height, layer)
    for row_index, row in enumerate(rows):
        cy = top - row_height * (row_index + 1.5)
        for value, cx in zip(row, centers):
            centered(layout, value, (cx, cy), text_height, "02_TEXTO")


def define_project_symbols(doc: ezdxf.document.Drawing) -> None:
    module = doc.blocks.new("P08_MODULO", base_point=(0.0, 0.0))
    add_rect(module, -15.0, -11.0, 15.0, 11.0, "04_EQUIPAMENTOS")
    for x in (-10.0, -5.0, 0.0, 5.0, 10.0):
        line(module, (x, -11.0), (x, 11.0), "04_EQUIPAMENTOS")
    line(module, (-15.0, 0.0), (15.0, 0.0), "04_EQUIPAMENTOS")

    fuse = doc.blocks.new("P08_FUSIVEL", base_point=(0.0, 0.0))
    line(fuse, (-6.0, 0.0), (-3.5, 0.0), "05_POTENCIA")
    add_rect(fuse, -3.5, -1.8, 3.5, 1.8, "05_POTENCIA")
    line(fuse, (-2.5, -1.1), (2.5, 1.1), "05_POTENCIA")
    line(fuse, (3.5, 0.0), (6.0, 0.0), "05_POTENCIA")

    switch = doc.blocks.new("P08_SECCIONADOR", base_point=(0.0, 0.0))
    line(switch, (-6.0, 0.0), (-2.0, 0.0), "05_POTENCIA")
    line(switch, (-2.0, 0.0), (2.8, 3.0), "05_POTENCIA")
    line(switch, (2.0, 0.0), (6.0, 0.0), "05_POTENCIA")

    dps = doc.blocks.new("P08_DPS", base_point=(0.0, 0.0))
    add_rect(dps, -5.0, -6.0, 5.0, 6.0, "05_POTENCIA")
    dps.add_lwpolyline(
        [(-2.5, 3.5), (1.2, 3.5), (-1.0, 0.4), (2.5, 0.4), (-2.0, -3.5)],
        dxfattribs={"layer": "05_POTENCIA"},
    )

    meter = doc.blocks.new("P08_MEDIDOR", base_point=(0.0, 0.0))
    meter.add_circle((0.0, 0.0), 7.0, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(meter, "kWh", (0.0, 0.0), 1.6, "07_INSTRUMENTACAO")

    north = doc.blocks.new("P08_NORTE", base_point=(0.0, 0.0))
    line(north, (0.0, -7.0), (0.0, 7.0), "03_COTAS")
    north.add_lwpolyline([(0.0, 7.0), (-2.4, 2.5), (2.4, 2.5)], close=True, dxfattribs={"layer": "03_COTAS"})
    centered(north, "N", (0.0, 11.0), 1.8, "03_COTAS")

    grid = doc.blocks.new("P08_REDE", base_point=(0.0, 0.0))
    line(grid, (0.0, -7.0), (0.0, 8.0), "11_ARQUITETURA")
    line(grid, (-7.0, 3.0), (7.0, 3.0), "11_ARQUITETURA")
    line(grid, (-5.0, -1.5), (5.0, -1.5), "11_ARQUITETURA")
    line(grid, (-6.5, -7.0), (0.0, 8.0), "11_ARQUITETURA")
    line(grid, (6.5, -7.0), (0.0, 8.0), "11_ARQUITETURA")


def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("EMISSAO INICIAL DO PROJETO 08", 316), ("R.E.M.M.", 381)):
        centered(layout, value, (x, 78.5), 1.45, "02_TEXTO")


def add_bottom_information(layout, spec: SheetSpec, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATORIO", (22, 42), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    add_text(layout, "NOTAS DA PRANCHA", (22, 66.5), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, spec.notes, (22, 62), 198, 1.42, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    add_text(layout, "LEGENDA", (22, 90.5), 2.1, layer="12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, spec.legend, (22, 86), 198, 1.42, "12_LEGENDA")


def add_title_block(layout, spec: SheetSpec, config: dict) -> None:
    values = {
        "TITULO": spec.title,
        "AUTOR": config["portfolio"]["author"],
        "DATA": PROJECT_DATE,
        "REVISAO": REVISION,
        "PRANCHA": f"{spec.number:02d}/06",
        "ARQUIVO": spec.filename,
        "UNIDADES": "mm",
        "ESCALA": "S/ESC.",
        "FOLHA": "A3",
        "STATUS": "CONCEIT.",
    }
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(values)


def create_sheet(config: dict, spec: SheetSpec):
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = PROJECT_SLUG
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/06"
    metadata["PORTFOLIO_EPISTEMIC_STATUS"] = "ACADEMIC_CONCEPT_NOT_FOR_EXECUTION"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 3.85, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 1.85, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_module_arrangement(layout, data: dict[str, list[dict[str, str]]]) -> None:
    add_rect(layout, 20, 112, 300, 254, "11_ARQUITETURA")
    line(layout, (20, 183), (300, 183), "11_ARQUITETURA")
    centered(layout, "PLANO DE COBERTURA CONCEITUAL", (160, 248), 1.4, "11_ARQUITETURA")
    layout.add_blockref("P08_NORTE", (32, 232), dxfattribs={"layer": "03_COTAS"})
    x_positions = (55, 95, 135, 175, 215, 255)
    rows = ((214, "S1", "M01"), (155, "S2", "M07"))
    for row_y, string, first in rows:
        start_number = int(first[1:])
        for index, x in enumerate(x_positions):
            layout.add_blockref("P08_MODULO", (x, row_y), dxfattribs={"layer": "04_EQUIPAMENTOS"})
            centered(layout, f"M{start_number + index:02d}", (x, row_y), 1.2, "02_TEXTO")
        centered(layout, f"{string}: 6 MÓDULOS EM SÉRIE", (155, row_y - 16), 1.25, "08_CABOS")
        line(layout, (40, row_y), (270, row_y), "08_CABOS")
        arrow(layout, (270, row_y), (295, row_y), "08_CABOS", f"{string} +/-")
    centered(layout, "NORTE | INCLINAÇÃO 20° (PREMISSAS)", (160, 120), 1.25, "03_COTAS")

    table(
        layout,
        310,
        252,
        (40, 50),
        ("DADO", "VALOR"),
        [
            ("POTÊNCIA CC", "6,60 kWp"),
            ("MÓDULOS", "12 x 550 Wp"),
            ("STRINGS", "2 x 6S"),
            ("Vmp/string", "250,8 V"),
            ("Voc/string", "299,4 V"),
            ("Imp / Isc", "13,16 / 13,92 A"),
            ("Tmin / Tcél", "-5 / 70 °C"),
            ("Irrad. máx.", "1.100 W/m²"),
        ],
        row_height=10.0,
        text_height=0.95,
    )
    add_rect(layout, 310, 112, 400, 154, "13_NOTAS")
    centered(layout, "LIMITES DA DISPOSIÇÃO", (355, 147), 1.25, "13_NOTAS")
    add_mtext(
        layout,
        "Sem levantamento de sombras, estrutura, vento, fixações, impermeabilização, acesso ou afastamentos normativos.",
        (315, 140),
        80,
        1.25,
        "13_NOTAS",
    )


def draw_dc_single_line(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "DUAS STRINGS INDEPENDENTES - SEM PARALELISMO", (205, 258), 1.45, "05_POTENCIA")
    for y, string, modules, mppt in ((226, "S1", "M01-M06", "MPPT 1"), (178, "S2", "M07-M12", "MPPT 2")):
        component(layout, 20, y - 16, 68, y + 16, string, f"{modules} | 6S", "04_EQUIPAMENTOS")
        line(layout, (68, y + 5), (250, y + 5), "05_POTENCIA")
        line(layout, (68, y - 5), (250, y - 5), "05_POTENCIA")
        centered(layout, "+", (73, y + 8), 1.1, "05_POTENCIA")
        centered(layout, "-", (73, y - 8), 1.1, "05_POTENCIA")
        for fy in (y + 5, y - 5):
            layout.add_blockref("P08_FUSIVEL", (91, fy), dxfattribs={"layer": "05_POTENCIA"})
        centered(layout, "2 x gPV 20 A", (91, y + 13), 1.0, "05_POTENCIA")
        layout.add_blockref("P08_DPS", (125, y), dxfattribs={"layer": "05_POTENCIA"})
        centered(layout, "DPS T2 FV 600 V", (125, y + 12), 1.0, "05_POTENCIA")
        line(layout, (125, y - 6), (125, 126), "06_COMANDO")
        for sy in (y + 5, y - 5):
            layout.add_blockref("P08_SECCIONADOR", (170, sy), dxfattribs={"layer": "05_POTENCIA"})
        centered(layout, "QDC 2P 32 A", (170, y + 13), 1.0, "05_POTENCIA")
        centered(layout, mppt, (236, y), 1.2, "04_EQUIPAMENTOS")
    component(layout, 250, 162, 322, 242, "INV-FV-801", "6 kWca / 2 MPPT", "04_EQUIPAMENTOS")
    arrow(layout, (322, 202), (365, 202), "05_POTENCIA", "220 Vca")
    centered(layout, "PARA PRANCHA 03", (365, 192), 1.0, "02_TEXTO")
    line(layout, (35, 126), (360, 126), "06_COMANDO")
    layout.add_blockref("SIM_TERRA", (360, 126), dxfattribs={"layer": "06_COMANDO"})
    centered(layout, "BARRAMENTO PE | DPS -> PE | POLOS CC NÃO ATERRADOS", (195, 132), 1.15, "06_COMANDO")
    table(
        layout,
        20,
        116,
        (50, 45, 45, 45),
        ("CONDIÇÃO", "TENSÃO", "LIMITE", "RESULTADO"),
        [
            ("Voc frio", "324,550 V", "< 600 V", "ATENDE PREM."),
            ("Vmp quente", "216,942 V", "90-550 V", "ATENDE PREM."),
        ],
        row_height=7.0,
        text_height=0.8,
    )


def draw_ac_single_line(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "CONEXÃO CONCEITUAL 220 V ENTRE FASES", (205, 258), 1.45, "05_POTENCIA")
    component(layout, 20, 202, 65, 240, "INV-FV-801", "6 kWca / 27,27 A", "04_EQUIPAMENTOS")
    line(layout, (65, 221), (384, 221), "05_POTENCIA")
    layout.add_blockref("P08_SECCIONADOR", (88, 221), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "QSD-CA 2P 40 A", (88, 233), 1.0, "05_POTENCIA")
    layout.add_blockref("P08_DPS", (124, 208), dxfattribs={"layer": "05_POTENCIA", "rotation": 90})
    line(layout, (124, 221), (124, 208), "05_POTENCIA")
    line(layout, (124, 203), (124, 142), "06_COMANDO")
    centered(layout, "DPS-CA T2", (124, 192), 1.0, "05_POTENCIA")
    layout.add_blockref("SIM_DISJUNTOR", (165, 221), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "QF-CA 2P 40 A", (165, 233), 1.0, "05_POTENCIA")
    component(layout, 190, 202, 238, 240, "QD-FV-801", "PROTEÇÃO CA", "04_EQUIPAMENTOS")
    layout.add_blockref("P08_MEDIDOR", (285, 221), dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(layout, "MED-801 BIDIRECIONAL", (285, 207), 1.0, "07_INSTRUMENTACAO")
    component(layout, 318, 202, 352, 240, "PCC-801", "PONTO DE CONEXÃO", "09_BORNES")
    layout.add_blockref("P08_REDE", (382, 221), dxfattribs={"layer": "11_ARQUITETURA"})
    centered(layout, "REDE", (382, 207), 1.1, "11_ARQUITETURA")

    arrow(layout, (214, 202), (214, 174), "05_POTENCIA", "CARGAS LOCAIS", (-18, 0))
    component(layout, 190, 145, 238, 174, "QDC-RES", "QUADRO EXISTENTE", "11_ARQUITETURA")
    line(layout, (25, 142), (365, 142), "06_COMANDO")
    layout.add_blockref("SIM_TERRA", (365, 142), dxfattribs={"layer": "06_COMANDO"})
    centered(layout, "PE EXISTENTE A VERIFICAR | F1/F2 E PE SEPARADOS", (195, 136), 1.1, "06_COMANDO")

    table(
        layout,
        20,
        128,
        (48, 40, 44, 48),
        ("DADO", "VALOR", "PROTEÇÃO", "OBSERVAÇÃO"),
        [
            ("Potência", "6,00 kW", "QF 40 A", "PREMISSA"),
            ("Corrente", "27,273 A", "2 polos", "fp=1 ideal"),
            ("Cabo", "10 mm²", "PE 10 mm²", "A confirmar"),
        ],
        row_height=7.2,
        text_height=0.82,
    )
    add_rect(layout, 218, 102, 400, 128, "13_NOTAS")
    centered(layout, "REQUISITOS DE CONEXÃO", (309, 122), 1.2, "13_NOTAS")
    add_mtext(
        layout,
        "Distribuidora, orçamento de conexão, medição, anti-ilhamento, qualidade de energia e vistoria permanecem obrigatórios.",
        (224, 116),
        168,
        1.18,
        "13_NOTAS",
    )


def draw_string_box(layout, data: dict[str, list[dict[str, str]]]) -> None:
    add_rect(layout, 20, 112, 282, 252, "04_EQUIPAMENTOS")
    centered(layout, "SB-FV-801 | ENTRADAS SEPARADAS | IP A SELECIONAR", (151, 246), 1.4, "04_EQUIPAMENTOS")
    for y, string, output in ((218, "S1", "MPPT1"), (166, "S2", "MPPT2")):
        centered(layout, f"X-{string} +", (31, y + 6), 1.0, "09_BORNES")
        centered(layout, f"X-{string} -", (31, y - 6), 1.0, "09_BORNES")
        for rail_y, suffix in ((y + 6, "P"), (y - 6, "N")):
            line(layout, (46, rail_y), (264, rail_y), "05_POTENCIA")
            layout.add_blockref("P08_FUSIVEL", (76, rail_y), dxfattribs={"layer": "05_POTENCIA"})
            centered(layout, f"F-{string}-{suffix}", (76, rail_y + 6), 0.9, "05_POTENCIA")
            layout.add_blockref("P08_SECCIONADOR", (190, rail_y), dxfattribs={"layer": "05_POTENCIA"})
        centered(layout, "gPV 20 A", (76, y + 14), 1.0, "05_POTENCIA")
        layout.add_blockref("P08_DPS", (126, y), dxfattribs={"layer": "05_POTENCIA"})
        centered(layout, f"DPS-CC-{1 if string == 'S1' else 2}", (126, y + 14), 1.0, "05_POTENCIA")
        if string == "S1":
            orthogonal(layout, ((126, y - 6), (126, 198), (272, 198), (272, 128)), "06_COMANDO")
        else:
            orthogonal(layout, ((126, y - 6), (126, 146), (272, 146), (272, 128)), "06_COMANDO")
        centered(layout, f"QDC-{1 if string == 'S1' else 2} 2P", (190, y + 14), 1.0, "05_POTENCIA")
        centered(layout, f"X-{output} +/-", (250, y), 1.0, "09_BORNES")
    line(layout, (42, 128), (272, 128), "06_COMANDO")
    centered(layout, "BARRA PE", (50, 134), 1.0, "06_COMANDO")
    layout.add_blockref("SIM_TERRA", (272, 128), dxfattribs={"layer": "06_COMANDO"})

    table(
        layout,
        292,
        250,
        (42, 66),
        ("ITEM", "ESPECIFICAÇÃO"),
        [
            ("F-S1-P/N", "gPV 20 A / 600 Vcc"),
            ("F-S2-P/N", "gPV 20 A / 600 Vcc"),
            ("DPS-CC-1", "Tipo 2 FV / Ucpv 600 V"),
            ("DPS-CC-2", "Tipo 2 FV / Ucpv 600 V"),
            ("QDC-1", "2P / 32 A / 600 Vcc"),
            ("QDC-2", "2P / 32 A / 600 Vcc"),
        ],
        row_height=10.0,
        text_height=0.82,
    )
    add_rect(layout, 292, 112, 400, 170, "13_NOTAS")
    centered(layout, "PONTOS DE VERIFICAÇÃO", (346, 162), 1.2, "13_NOTAS")
    add_mtext(
        layout,
        "Polaridade; Ucpv e Up; Icc; capacidade de interrupção; coordenação; grau IP; temperatura; terminais; torque; sinalização.",
        (298, 154),
        96,
        1.18,
        "13_NOTAS",
    )


def draw_grounding(layout, data: dict[str, list[dict[str, str]]]) -> None:
    centered(layout, "POLOS CC NÃO INTENCIONALMENTE ATERRADOS", (205, 258), 1.45, "05_POTENCIA")
    devices = (
        (45, "MOLDURAS", "12 MÓDULOS", "04_EQUIPAMENTOS"),
        (112, "EST-FV-801", "ESTRUTURA", "04_EQUIPAMENTOS"),
        (179, "SB-FV-801", "DPS CC", "04_EQUIPAMENTOS"),
        (246, "INV-FV-801", "CARCAÇA", "04_EQUIPAMENTOS"),
        (300, "QD-FV-801", "DPS CA", "04_EQUIPAMENTOS"),
    )
    for x, tag, detail, layer in devices:
        component(layout, x - 25, 192, x + 25, 232, tag, detail, layer)
        line(layout, (x, 192), (x, 154), "06_COMANDO")
        centered(layout, "PE", (x + 4, 174), 0.9, "06_COMANDO")
    line(layout, (25, 154), (375, 154), "06_COMANDO")
    component(layout, 250, 142, 320, 174, "BEP-801", "BARRAMENTO PRINCIPAL", "06_COMANDO")
    layout.add_blockref("SIM_TERRA", (365, 154), dxfattribs={"layer": "06_COMANDO", "xscale": 1.4, "yscale": 1.4})
    centered(layout, "ELETRODO EXISTENTE A VERIFICAR", (365, 142), 1.0, "06_COMANDO")
    line(layout, (320, 154), (365, 154), "06_COMANDO")

    add_rect(layout, 20, 105, 195, 138, "13_NOTAS")
    centered(layout, "ESCOPO CONCEITUAL DO PE", (107.5, 131), 1.2, "13_NOTAS")
    add_mtext(
        layout,
        "Equipotencializar molduras, suportes e invólucros; manter conexões dos DPS curtas; identificar e proteger os condutores.",
        (26, 124),
        163,
        1.15,
        "13_NOTAS",
    )
    add_rect(layout, 205, 105, 400, 138, "13_NOTAS")
    centered(layout, "INTERFACE COM SPDA / EDIFICAÇÃO", (302.5, 131), 1.2, "13_NOTAS")
    add_mtext(
        layout,
        "Análise de risco, distância de separação, eletrodo, esquema TN/TT, seções e coordenação de DPS não foram definidos.",
        (211, 124),
        183,
        1.15,
        "13_NOTAS",
    )
    add_rect(layout, 335, 192, 400, 232, "11_ARQUITETURA")
    centered(layout, "SPDA EXISTENTE", (367.5, 222), 1.2, "11_ARQUITETURA")
    centered(layout, "ANÁLISE NBR 5419:2026", (367.5, 201), 1.0, "11_ARQUITETURA")
    line(layout, (340, 188), (395, 188), "11_ARQUITETURA")
    centered(layout, "SEPARAÇÃO A CALCULAR", (367.5, 183), 0.9, "11_ARQUITETURA")


def draw_equipment_layout(layout, data: dict[str, list[dict[str, str]]]) -> None:
    add_rect(layout, 20, 178, 218, 252, "11_ARQUITETURA")
    centered(layout, "COBERTURA - 12 MÓDULOS", (119, 246), 1.3, "11_ARQUITETURA")
    for row, y in enumerate((218, 192)):
        for column, x in enumerate((42, 72, 102, 132, 162, 192)):
            layout.add_blockref(
                "P08_MODULO",
                (x, y),
                dxfattribs={"layer": "04_EQUIPAMENTOS", "xscale": 0.72, "yscale": 0.72},
            )
            centered(layout, f"M{row * 6 + column + 1:02d}", (x, y), 0.8, "02_TEXTO")

    add_rect(layout, 235, 112, 400, 252, "11_ARQUITETURA")
    centered(layout, "PAREDE TÉCNICA CONCEITUAL", (317.5, 246), 1.3, "11_ARQUITETURA")
    component(layout, 252, 205, 302, 235, "SB-FV-801", "CC / DPS / QDC", "04_EQUIPAMENTOS")
    component(layout, 325, 185, 385, 235, "INV-FV-801", "6 kWca / 2 MPPT", "04_EQUIPAMENTOS")
    component(layout, 252, 142, 302, 174, "QD-FV-801", "CA / DPS / QF", "04_EQUIPAMENTOS")
    layout.add_blockref("P08_MEDIDOR", (355, 156), dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(layout, "MED-801", (355, 143), 1.0, "07_INSTRUMENTACAO")
    component(layout, 325, 112, 385, 134, "PCC-801", "INSTALAÇÃO / REDE", "09_BORNES")

    orthogonal(layout, ((202, 205), (230, 205), (230, 220), (252, 220)), "08_CABOS")
    centered(layout, "R-CC-801/802", (225, 212), 0.9, "08_CABOS")
    arrow(layout, (302, 220), (325, 220), "08_CABOS", "2 MPPT")
    orthogonal(layout, ((355, 185), (355, 180), (312, 180), (312, 158), (302, 158)), "05_POTENCIA")
    centered(layout, "R-CA-801", (333, 184), 0.9, "05_POTENCIA")
    arrow(layout, (302, 158), (348, 158), "05_POTENCIA", "220 V")
    arrow(layout, (355, 149), (355, 134), "05_POTENCIA")
    line(layout, (245, 138), (392, 138), "06_COMANDO")
    centered(layout, "PE -> BEP-801", (276, 135), 0.9, "06_COMANDO")

    table(
        layout,
        20,
        166,
        (55, 63, 80),
        ("ZONA", "EQUIPAMENTO", "CRITÉRIO PENDENTE"),
        [
            ("Cobertura", "MOD-FV / EST-FV", "estrutura, sombra, acesso"),
            ("Parede", "SB-FV-801", "IP, altura, percurso CC"),
            ("Parede", "INV-FV-801", "folgas e ventilação"),
            ("Parede", "QD-FV-801", "Icn e coordenação"),
            ("Entrada", "MED / PCC", "padrão da distribuidora"),
        ],
        row_height=9.0,
        text_height=0.82,
    )
    centered(layout, "ROTAS CC E CA SEGREGADAS | POSIÇÕES NÃO EXECUTIVAS", (317, 103), 1.1, "13_NOTAS")


DRAWERS = {
    1: draw_module_arrangement,
    2: draw_dc_single_line,
    3: draw_ac_single_line,
    4: draw_string_box,
    5: draw_grounding,
    6: draw_equipment_layout,
}


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    project = root / PROJECT_SLUG
    data = {
        "parameters": read_rows(project, "parametros.csv"),
        "modules": read_rows(project, "lista-modulos.csv"),
        "protections": read_rows(project, "lista-protecoes.csv"),
        "cables": read_rows(project, "lista-cabos.csv"),
        "materials": read_rows(project, "lista-materiais.csv"),
        "calculations": read_rows(project, "resultados-calculo.csv"),
    }
    source_dir = project / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for spec in SHEETS:
        doc, layout = create_sheet(config, spec)
        DRAWERS[spec.number](layout, data)
        output = source_dir / spec.filename
        prepare_deterministic_write(doc)
        with output.open("wt", encoding="utf-8", newline="\n") as stream:
            doc.write(stream)
        outputs.append(output)
        print(f"Gerado: {output.relative_to(root)}")
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositório")
    return parser.parse_args()


def main() -> int:
    generate(parse_args().root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
