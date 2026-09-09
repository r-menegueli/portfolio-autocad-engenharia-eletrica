"""Gera as sete pranchas DXF do Projeto 06 de forma deterministica."""

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


PROJECT_SLUG = "06-centro-controle-motores"
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
        "01_diagrama_unifilar_ccm.dxf",
        "DIAGRAMA UNIFILAR DO CCM",
        "Integração de partida direta, reversão e inversor de frequência",
        "Rede assumida: 380/220 V, 3F+N+PE, 60 Hz, TN-S. Icc presumida: 6 kA.\\P"
        "Seleção final de proteção, curto-circuito e coordenação depende de estudo executivo.",
        "Q: proteção | KM: contator | FR: sobrecarga | VFD: inversor | M: motor | PE: proteção",
    ),
    SheetSpec(
        2,
        "02_partida_direta.dxf",
        "PARTIDA DIRETA - BOMBA",
        "M-601, 5,5 kW: potência e comando em 24 Vcc",
        "KSR-601 habilita o comando; S0-601 e FR-601 derrubam KM-601.\\P"
        "O selo não permite rearme automático após emergência ou falta de tensão.",
        "S: botão | KM: contator | FR: relé térmico | H: sinalizador | X: borne",
    ),
    SheetSpec(
        3,
        "03_partida_reversora.dxf",
        "PARTIDA REVERSORA - ESTEIRA",
        "M-602, 3,0 kW: reversão com intertravamentos elétrico e mecânico",
        "KM-602F e KM-602R possuem contatos NF cruzados e trava mecânica.\\P"
        "A troca de sentido exige parada; fins de curso atuam somente no sentido associado.",
        "F: frente | R: reverso | FC: fim de curso | IM: intertravamento mecânico",
    ),
    SheetSpec(
        4,
        "04_acionamento_inversor.dxf",
        "ACIONAMENTO POR INVERSOR",
        "M-603, 7,5 kW: potência, STO e interface de comando",
        "Não instalar contator de manobra entre VFD-603 e M-603. Cabo de saída blindado.\\P"
        "STO A/B é conceitual; função de segurança requer análise de risco e validação.",
        "DI: entrada digital | AI: entrada analógica | RO: relé | STO: torque seguro desligado",
    ),
    SheetSpec(
        5,
        "05_layout_ccm.dxf",
        "LAYOUT DO CCM",
        "Arranjo conceitual do invólucro 1800 x 1000 x 400 mm",
        "Confirmar ventilação, perdas, segregação, acesso, EMC e raios de curvatura.\\P"
        "Dimensões, folgas e forma de separação são premissas acadêmicas.",
        "Azul: comando | Vermelho: potência | Cinza: canaleta | PE: barra de proteção",
    ),
    SheetSpec(
        6,
        "06_diagrama_bornes.dxf",
        "DIAGRAMA DE BORNES",
        "Réguas X1 a X4: entrada, motores, comando e sinais do VFD",
        "Separar potência, comando e sinais analógicos; identificar ambas as extremidades.\\P"
        "Blindagem de W603B termina em 360 graus no CCM e no motor, conforme estudo EMC.",
        "X1: entrada | X2: motores | X3: comando | X4: VFD e segurança | SH: blindagem",
    ),
    SheetSpec(
        7,
        "07_lista_cabos.dxf",
        "LISTA DE CABOS",
        "Cabos W600 a W608 e síntese de materiais do CCM-06",
        "Comprimentos são premissas para orçamento acadêmico. Confirmar rotas e instalação.\\P"
        "Seções não substituem dimensionamento por ampacidade, queda, curto-circuito e EMC.",
        "G: inclui PE | BL: blindado | POT: potência | CMD: comando | SIG: sinal",
    ),
)


def read_rows(project: Path, filename: str) -> list[dict[str, str]]:
    with (project / filename).open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def line(layout, start: tuple[float, float], end: tuple[float, float], layer: str) -> None:
    add_line(layout, start, end, layer)


def centered(layout, value: str, point: tuple[float, float], height: float = 1.5, layer: str = "02_TEXTO") -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER)


def left(layout, value: str, point: tuple[float, float], height: float = 1.35, layer: str = "02_TEXTO") -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_LEFT)


def orthogonal(layout, points: tuple[tuple[float, float], ...], layer: str) -> None:
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float, tag: str, detail: str, layer: str = "04_EQUIPAMENTOS") -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered(layout, tag, ((x0 + x1) / 2, y1 - 4.0), 1.7, layer)
    centered(layout, detail, ((x0 + x1) / 2, y0 + 4.0), 1.15, "02_TEXTO")


def terminal(layout, point: tuple[float, float], tag: str, *, label_offset: tuple[float, float] = (0.0, 5.0)) -> None:
    layout.add_blockref("SIM_TERMINAL", point, dxfattribs={"layer": "09_BORNES"})
    centered(layout, tag, (point[0] + label_offset[0], point[1] + label_offset[1]), 1.05, "09_BORNES")


def motor(layout, point: tuple[float, float], tag: str, detail: str) -> None:
    layout.add_blockref("SIM_MOTOR", point, dxfattribs={"layer": "04_EQUIPAMENTOS", "xscale": 2.0, "yscale": 2.0})
    centered(layout, tag, (point[0], point[1] - 11.0), 1.35, "04_EQUIPAMENTOS")
    centered(layout, detail, (point[0], point[1] - 15.0), 1.05, "02_TEXTO")


def contact(layout, x: float, y: float, tag: str, normally_closed: bool = False, label_dy: float = 5.2) -> None:
    block = "P06_CONTATO_NF" if normally_closed else "P06_CONTATO_NA"
    layout.add_blockref(block, (x, y), dxfattribs={"layer": "06_COMANDO"})
    centered(layout, tag, (x, y + label_dy), 1.0, "06_COMANDO")


def coil(layout, x: float, y: float, tag: str) -> None:
    layout.add_blockref("P06_BOBINA", (x, y), dxfattribs={"layer": "06_COMANDO"})
    centered(layout, tag, (x, y + 5.2), 1.0, "06_COMANDO")


def define_project_symbols(doc: ezdxf.document.Drawing) -> None:
    for name, nc in (("P06_CONTATO_NA", False), ("P06_CONTATO_NF", True)):
        block = doc.blocks.new(name, base_point=(0.0, 0.0))
        line(block, (-6.0, 0.0), (-2.0, 0.0), "06_COMANDO")
        line(block, (2.0, 0.0), (6.0, 0.0), "06_COMANDO")
        line(block, (-2.0, 0.0), (2.0, 2.8), "06_COMANDO")
        if nc:
            line(block, (-2.0, 2.8), (2.0, -1.0), "06_COMANDO")
    coil_block = doc.blocks.new("P06_BOBINA", base_point=(0.0, 0.0))
    add_rect(coil_block, -4.0, -3.0, 4.0, 3.0, "06_COMANDO")
    overload = doc.blocks.new("P06_RELE_TERMICO", base_point=(0.0, 0.0))
    add_rect(overload, -6.0, -5.0, 6.0, 5.0, "05_POTENCIA")
    centered(overload, "I>", (0.0, 0.0), 2.0, "05_POTENCIA")
    vfd = doc.blocks.new("P06_VFD", base_point=(0.0, 0.0))
    add_rect(vfd, -15.0, -12.0, 15.0, 12.0, "04_EQUIPAMENTOS")
    centered(vfd, "~  VFD  ~", (0.0, 2.0), 2.0, "04_EQUIPAMENTOS")
    centered(vfd, "R/S/T   U/V/W", (0.0, -4.0), 1.2, "02_TEXTO")


def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("EMISSAO INICIAL DO PROJETO 06", 316), ("R.E.M.M.", 381)):
        centered(layout, value, (x, 78.5), 1.55, "02_TEXTO")


def add_bottom_information(layout, spec: SheetSpec, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATORIO", (22, 42), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    add_text(layout, "NOTAS DA PRANCHA", (22, 66.5), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, spec.notes, (22, 62), 198, 1.47, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    add_text(layout, "LEGENDA", (22, 90.5), 2.1, layer="12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, spec.legend, (22, 86), 198, 1.47, "12_LEGENDA")


def add_title_block(layout, spec: SheetSpec, config: dict) -> None:
    values = {
        "TITULO": spec.title,
        "AUTOR": config["portfolio"]["author"],
        "DATA": PROJECT_DATE,
        "REVISAO": REVISION,
        "PRANCHA": f"{spec.number:02d}/07",
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
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/07"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 4.1, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 1.95, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_unifilar(layout, loads: list[dict[str, str]], cables: list[dict[str, str]]) -> None:
    centered(layout, "REDE 380/220 V - 3F+N+PE - 60 Hz", (86, 260), 1.35, "05_POTENCIA")
    line(layout, (20, 238), (52, 238), "05_POTENCIA")
    layout.add_blockref("SIM_DISJUNTOR", (65, 238), dxfattribs={"layer": "05_POTENCIA", "xscale": 1.3, "yscale": 1.3})
    centered(layout, "QG-06", (65, 247), 1.4, "05_POTENCIA")
    centered(layout, "4P 50 A", (65, 229), 1.1, "02_TEXTO")
    line(layout, (72, 238), (396, 238), "05_POTENCIA")
    centered(layout, "BARRAMENTO CCM-06 - 80 A - 3F+N+PE", (235, 245), 1.4, "05_POTENCIA")
    terminal(layout, (34, 238), "X1:1-5", label_offset=(0, 7))
    branch_x = (105.0, 225.0, 345.0)
    tags = (("QF-601", "KM-601", "FR-601", "M-601", "DIRETA"), ("QF-602", "KM-602F/R", "FR-602", "M-602", "REVERSAO"), ("QF-603", "VFD-603", "STO A/B", "M-603", "INVERSOR"))
    for x, load, tagset in zip(branch_x, loads, tags):
        qf, drive, protection, motor_tag, method = tagset
        line(layout, (x, 238), (x, 222), "05_POTENCIA")
        layout.add_blockref("SIM_DISJUNTOR", (x, 214), dxfattribs={"layer": "05_POTENCIA", "rotation": 90})
        centered(layout, qf, (x + 12, 214), 1.25, "05_POTENCIA")
        line(layout, (x, 207), (x, 195), "05_POTENCIA")
        if motor_tag == "M-603":
            layout.add_blockref("P06_VFD", (x, 181), dxfattribs={"layer": "04_EQUIPAMENTOS"})
            centered(layout, drive, (x, 199), 1.3, "04_EQUIPAMENTOS")
            centered(layout, protection, (x, 161), 1.1, "06_COMANDO")
            line(layout, (x, 169), (x, 145), "08_CABOS")
        else:
            box(layout, x - 18, 171, x + 18, 195, drive, method, "05_POTENCIA")
            layout.add_blockref("P06_RELE_TERMICO", (x, 158), dxfattribs={"layer": "05_POTENCIA"})
            centered(layout, protection, (x + 17, 158), 1.15, "05_POTENCIA")
            line(layout, (x, 152), (x, 145), "08_CABOS")
        motor(layout, (x, 136), motor_tag, f"{load['potencia_saida_kw']} kW")
        centered(layout, f"{load['metodo_acionamento']}", (x, 108), 1.15, "02_TEXTO")
    line(layout, (27, 116), (390, 116), "05_POTENCIA")
    centered(layout, "BARRA PE-06", (57, 122), 1.25, "05_POTENCIA")
    layout.add_blockref("SIM_TERRA", (27, 112), dxfattribs={"layer": "05_POTENCIA"})
    for x in branch_x:
        line(layout, (x + 8, 132), (x + 8, 116), "05_POTENCIA")
    centered(layout, "W600 4x10+PE10 mm2 / 20 m", (134, 233), 1.1, "08_CABOS")
    centered(layout, "KSR-601: parada comum dos contatores e STO A/B", (280, 108), 1.15, "06_COMANDO")


def draw_dol(layout, loads: list[dict[str, str]], cables: list[dict[str, str]]) -> None:
    add_rect(layout, 18, 106, 192, 258, "12_LEGENDA")
    centered(layout, "POTENCIA 380 V", (105, 251), 1.7, "12_LEGENDA")
    ys = (229, 214, 199)
    for y, phase in zip(ys, ("L1", "L2", "L3")):
        left(layout, phase, (25, y + 3), 1.2, "02_TEXTO")
        line(layout, (36, y), (165, y), "05_POTENCIA")
        layout.add_blockref("SIM_DISJUNTOR", (58, y), dxfattribs={"layer": "05_POTENCIA"})
        add_rect(layout, 82, y - 4, 101, y + 4, "05_POTENCIA")
        centered(layout, "KM", (91.5, y), 1.0, "05_POTENCIA")
        add_rect(layout, 118, y - 4, 137, y + 4, "05_POTENCIA")
        centered(layout, "FR", (127.5, y), 1.0, "05_POTENCIA")
        terminal(layout, (155, y), f"X2:{ys.index(y)+1}", label_offset=(0, 6))
    centered(layout, "QF-601", (58, 240), 1.25, "05_POTENCIA")
    centered(layout, "KM-601", (91.5, 240), 1.25, "05_POTENCIA")
    centered(layout, "FR-601", (127.5, 240), 1.25, "05_POTENCIA")
    orthogonal(layout, ((165, 229), (172, 229), (172, 165.3)), "08_CABOS")
    orthogonal(layout, ((165, 214), (178, 214), (178, 168)), "08_CABOS")
    orthogonal(layout, ((165, 199), (184, 199), (184, 165.3)), "08_CABOS")
    motor(layout, (178, 160), "M-601", "5,5 kW / bomba")
    centered(layout, "W601 - 4G2,5 mm2 - 30 m", (105, 132), 1.25, "08_CABOS")
    centered(layout, "FR ajuste preliminar 12,0 A", (105, 118), 1.15, "13_NOTAS")

    add_rect(layout, 204, 106, 402, 258, "12_LEGENDA")
    centered(layout, "COMANDO 24 Vcc", (303, 251), 1.7, "12_LEGENDA")
    line(layout, (216, 236), (216, 120), "06_COMANDO")
    line(layout, (390, 236), (390, 120), "06_COMANDO")
    centered(layout, "+24 V", (216, 243), 1.15, "06_COMANDO")
    centered(layout, "0 V", (390, 243), 1.15, "06_COMANDO")
    y = 211
    line(layout, (216, y), (228, y), "06_COMANDO")
    contact(layout, 238, y, "KSR-601", True)
    line(layout, (244, y), (252, y), "06_COMANDO")
    contact(layout, 262, y, "S0-601", True)
    line(layout, (268, y), (276, y), "06_COMANDO")
    contact(layout, 286, y, "S-601P", True)
    line(layout, (292, y), (300, y), "06_COMANDO")
    contact(layout, 310, y, "FR-601", True)
    line(layout, (316, y), (327, y), "06_COMANDO")
    contact(layout, 337, y, "S-601L", label_dy=8.2)
    line(layout, (343, y), (359, y), "06_COMANDO")
    coil(layout, 369, y, "KM-601")
    line(layout, (373, y), (390, y), "06_COMANDO")
    orthogonal(layout, ((327, 211), (327, 194), (359, 194), (359, 211)), "06_COMANDO")
    contact(layout, 343, 194, "KM-601")
    y2 = 154
    line(layout, (216, y2), (342, y2), "06_COMANDO")
    contact(layout, 352, y2, "KM-601")
    line(layout, (358, y2), (366, y2), "06_COMANDO")
    coil(layout, 376, y2, "H-601")
    line(layout, (380, y2), (390, y2), "06_COMANDO")
    centered(layout, "SELO", (343, 185), 1.0, "06_COMANDO")
    left(layout, "Permissivos em série: segurança, parada e sobrecarga", (216, 126), 1.1, "13_NOTAS")


def draw_reverse(layout, loads: list[dict[str, str]], cables: list[dict[str, str]]) -> None:
    add_rect(layout, 18, 106, 197, 258, "12_LEGENDA")
    centered(layout, "POTENCIA E REVERSAO", (107.5, 251), 1.7, "12_LEGENDA")
    for y, phase in zip((242, 232, 222), ("L1", "L2", "L3")):
        left(layout, phase, (24, y + 2), 1.15)
        line(layout, (36, y), (72, y), "05_POTENCIA")
        layout.add_blockref("SIM_DISJUNTOR", (55, y), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "QF-602 3P 10 A", (55, 252), 1.2, "05_POTENCIA")
    line(layout, (72, 242), (72, 218), "05_POTENCIA")
    line(layout, (72, 218), (152, 218), "05_POTENCIA")
    line(layout, (101, 218), (101, 214), "05_POTENCIA")
    line(layout, (152, 218), (152, 214), "05_POTENCIA")
    box(layout, 80, 181, 124, 214, "KM-602F", "ORDEM L1-L2-L3", "05_POTENCIA")
    box(layout, 130, 181, 174, 214, "KM-602R", "ORDEM L3-L2-L1", "05_POTENCIA")
    line(layout, (101, 181), (101, 166), "05_POTENCIA")
    line(layout, (152, 181), (152, 166), "05_POTENCIA")
    line(layout, (101, 166), (152, 166), "05_POTENCIA")
    line(layout, (126.5, 166), (126.5, 160), "05_POTENCIA")
    line(layout, (124, 177), (130, 177), "06_COMANDO")
    centered(layout, "IM-602", (127, 173), 1.2, "06_COMANDO")
    centered(layout, "TRAVA MECANICA", (127, 169), 0.95, "06_COMANDO")
    layout.add_blockref("P06_RELE_TERMICO", (126.5, 153), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "FR-602 / 6,8 A", (160, 153), 1.1, "05_POTENCIA")
    line(layout, (126.5, 147), (126.5, 143), "05_POTENCIA")
    motor(layout, (126.5, 135), "M-602", "3,0 kW / esteira")
    centered(layout, "W602 - 4G2,5 mm2 - 25 m", (107.5, 113), 1.15, "08_CABOS")

    add_rect(layout, 207, 106, 402, 258, "12_LEGENDA")
    centered(layout, "COMANDO REVERSOR 24 Vcc", (304.5, 251), 1.7, "12_LEGENDA")
    line(layout, (218, 238), (218, 119), "06_COMANDO")
    line(layout, (391, 238), (391, 119), "06_COMANDO")
    for y, direction, start_tag, limit_tag, opposite, coil_tag in (
        (207, "FRENTE", "S-602F", "FC-602F", "KM-602R", "KM-602F"),
        (159, "REVERSO", "S-602R", "FC-602R", "KM-602F", "KM-602R"),
    ):
        line(layout, (218, y), (226, y), "06_COMANDO")
        contact(layout, 236, y, "KSR-601", True)
        contact(layout, 258, y, "S0-601", True)
        contact(layout, 280, y, "FR-602", True)
        contact(layout, 302, y, limit_tag, True)
        contact(layout, 324, y, opposite, True)
        contact(layout, 346, y, start_tag)
        coil(layout, 376, y, coil_tag)
        segments = ((242, 252), (264, 274), (286, 296), (308, 318), (330, 340), (352, 372), (380, 391))
        for x0, x1 in segments:
            line(layout, (x0, y), (x1, y), "06_COMANDO")
        centered(layout, direction, (304, y + 12), 1.05, "02_TEXTO")
        orthogonal(layout, ((340, y), (340, y - 15), (363, y - 15), (363, y)), "06_COMANDO")
        contact(layout, 351.5, y - 15, coil_tag)
    left(layout, "NF cruzado impede KM-F e KM-R simultaneos", (218, 119), 1.05, "13_NOTAS")


def draw_vfd(layout, loads: list[dict[str, str]], cables: list[dict[str, str]]) -> None:
    add_rect(layout, 18, 106, 209, 258, "12_LEGENDA")
    centered(layout, "POTENCIA 380 V", (113.5, 251), 1.7, "12_LEGENDA")
    for y, phase in zip((231, 218, 205), ("L1", "L2", "L3")):
        left(layout, phase, (25, y + 2), 1.15)
        line(layout, (38, y), (76, y), "05_POTENCIA")
        layout.add_blockref("SIM_DISJUNTOR", (58, y), dxfattribs={"layer": "05_POTENCIA"})
        line(layout, (76, y), (96, y), "05_POTENCIA")
    centered(layout, "QF-603 3P 25 A", (58, 244), 1.2, "05_POTENCIA")
    layout.add_blockref("P06_VFD", (120, 218), dxfattribs={"layer": "04_EQUIPAMENTOS", "xscale": 1.25, "yscale": 1.45})
    centered(layout, "VFD-603 / 11 kW", (120, 242), 1.35, "04_EQUIPAMENTOS")
    for y in (231, 218, 205):
        line(layout, (139, y), (171, y), "08_CABOS")
    motor(layout, (186, 218), "M-603", "7,5 kW / ventilador")
    line(layout, (120, 200), (120, 154), "05_POTENCIA")
    line(layout, (186, 210), (186, 154), "05_POTENCIA")
    line(layout, (36, 154), (194, 154), "05_POTENCIA")
    layout.add_blockref("SIM_TERRA", (36, 150), dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "PE + blindagem 360 graus", (112, 145), 1.2, "05_POTENCIA")
    centered(layout, "W603A 4G4 / 15 m", (80, 192), 1.1, "08_CABOS")
    centered(layout, "W603B 4G4 BL / 28 m", (165, 192), 1.1, "08_CABOS")
    centered(layout, "SEM CONTATOR NA SAIDA", (113.5, 119), 1.25, "13_NOTAS")

    add_rect(layout, 219, 106, 402, 258, "12_LEGENDA")
    centered(layout, "INTERFACE E SEGURANCA", (310.5, 251), 1.7, "12_LEGENDA")
    box(layout, 232, 210, 278, 238, "KSR-601", "RELE SEG.", "06_COMANDO")
    box(layout, 328, 210, 389, 238, "VFD-603", "STO A / STO B", "06_COMANDO")
    for y, channel in ((228, "STO A"), (218, "STO B")):
        line(layout, (278, y), (328, y), "06_COMANDO")
        centered(layout, channel, (303, y + 3.2), 1.0, "06_COMANDO")
    rows = (
        (194, "DI1", "S-603L START"),
        (178, "DI2", "S-603P STOP"),
        (162, "DI3", "SA-603 LOCAL/REM"),
        (146, "AI1", "P-603 0-10 V VELOC."),
        (130, "RO1", "H-603 RUN / H-604 FALHA"),
    )
    for y, io, description in rows:
        terminal(layout, (244, y), f"X4:{io}", label_offset=(0, 5))
        line(layout, (246, y), (270, y), "07_INSTRUMENTACAO" if io.startswith("AI") else "06_COMANDO")
        left(layout, description, (276, y), 1.1, "02_TEXTO")
    left(layout, "Parada comum: KSR abre contatores e STO A/B", (228, 115), 1.05, "13_NOTAS")


def draw_layout(layout, loads: list[dict[str, str]], cables: list[dict[str, str]]) -> None:
    add_rect(layout, 24, 106, 282, 260, "11_ARQUITETURA")
    centered(layout, "CCM-06 - VISTA INTERNA", (153, 253), 1.8, "11_ARQUITETURA")
    line(layout, (24, 241), (282, 241), "11_ARQUITETURA")
    centered(layout, "BARRAMENTO 80 A / PE", (153, 247), 1.2, "05_POTENCIA")
    for x in (82, 142, 202, 246):
        line(layout, (x, 106), (x, 241), "11_ARQUITETURA")
    box(layout, 31, 202, 75, 234, "QG-06", "GERAL 50 A", "05_POTENCIA")
    box(layout, 88, 187, 136, 234, "GAVETA 601", "DIRETA", "05_POTENCIA")
    box(layout, 148, 173, 196, 234, "GAVETA 602", "REVERSAO", "05_POTENCIA")
    box(layout, 208, 163, 240, 234, "VFD-603", "11 kW", "04_EQUIPAMENTOS")
    box(layout, 250, 181, 275, 234, "KSR/PSU", "24 Vcc", "06_COMANDO")
    for x in (77, 138, 198, 243):
        add_rect(layout, x, 111, x + 4, 239, "10_ELETROCALHAS")
    add_rect(layout, 31, 114, 75, 147, "09_BORNES")
    centered(layout, "X1 / X2", (53, 132), 1.4, "09_BORNES")
    add_rect(layout, 88, 114, 196, 147, "09_BORNES")
    centered(layout, "X3 / X4 - COMANDO E SINAIS", (142, 132), 1.35, "09_BORNES")
    line(layout, (31, 108), (275, 108), "05_POTENCIA")
    centered(layout, "PE-06", (54, 112), 1.2, "05_POTENCIA")
    line(layout, (24, 101), (282, 101), "03_COTAS")
    centered(layout, "1000 mm", (153, 98), 1.25, "03_COTAS")
    line(layout, (288, 106), (288, 260), "03_COTAS")
    centered(layout, "1800 mm", (296, 183), 1.25, "03_COTAS")

    add_rect(layout, 305, 106, 402, 260, "12_LEGENDA")
    centered(layout, "CRITERIOS DE ARRANJO", (353.5, 251), 1.65, "12_LEGENDA")
    notes = (
        "Invólucro: 1800 x 1000 x 400 mm",
        "Acesso frontal: >= 1,20 m",
        "Entrada de cabos: inferior",
        "Potência separada de comando",
        "VFD com ventilação dedicada",
        "Cabo VFD afastado de sinais",
        "PE contínuo e equipotencial",
        "Canaletas com reserva >= 30%",
        "Porta: botoeiras e sinalização",
        "Grau IP depende do ambiente",
        "Dissipação requer cálculo térmico",
    )
    for index, note in enumerate(notes):
        left(layout, note, (312, 237 - index * 11), 1.15, "02_TEXTO")


def table(layout, x0: float, y_top: float, widths: tuple[float, ...], headers: tuple[str, ...], rows: list[tuple[str, ...]], *, row_height: float, text_height: float = 1.0) -> None:
    total_width = sum(widths)
    y_bottom = y_top - row_height * (len(rows) + 1)
    add_rect(layout, x0, y_bottom, x0 + total_width, y_top, "12_LEGENDA")
    for index in range(1, len(rows) + 1):
        y = y_top - row_height * index
        line(layout, (x0, y), (x0 + total_width, y), "12_LEGENDA")
    cursor = x0
    for width in widths[:-1]:
        cursor += width
        line(layout, (cursor, y_bottom), (cursor, y_top), "12_LEGENDA")
    for row_index, row in enumerate([headers, *rows]):
        cursor = x0
        center_y = y_top - row_height * row_index - row_height / 2
        for col_index, (value, width) in enumerate(zip(row, widths)):
            if col_index in (1, 2) and row_index:
                left(layout, value, (cursor + 1.5, center_y), text_height, "02_TEXTO")
            else:
                centered(layout, value, (cursor + width / 2, center_y), text_height if row_index else text_height + 0.1, "12_LEGENDA")
            cursor += width


def draw_terminals(layout, loads: list[dict[str, str]], cables: list[dict[str, str]]) -> None:
    left_rows = [
        ("X1:1", "L1 entrada", "W600-1", "QG-06"), ("X1:2", "L2 entrada", "W600-2", "QG-06"),
        ("X1:3", "L3 entrada", "W600-3", "QG-06"), ("X1:4", "N entrada", "W600-4", "barra N"),
        ("X1:5", "PE entrada", "W600-PE", "PE-06"), ("X2:1-4", "M-601 U/V/W/PE", "W601", "bomba"),
        ("X2:5-8", "M-602 U/V/W/PE", "W602", "esteira"), ("X2:9-12", "M-603 U/V/W/PE", "W603B", "ventilador"),
    ]
    right_rows = [
        ("X3:1-2", "S-601L/P", "W605", "bomba"), ("X3:3-6", "S-602F/R + FC", "W606", "esteira"),
        ("X3:7-8", "S0-601 CH1/CH2", "W604", "emergência"), ("X3:9-10", "H-601/H-602", "W608", "estado"),
        ("X4:1-2", "STO A/B", "W604", "VFD-603"), ("X4:3-4", "START/STOP", "W607", "VFD-603"),
        ("X4:5-7", "AI1/COM/SH", "W607", "referência"), ("X4:8-10", "RO1 RUN/FAULT", "W608", "estado"),
    ]
    centered(layout, "POTENCIA - X1 / X2", (111, 260), 1.7, "09_BORNES")
    centered(layout, "COMANDO E SINAIS - X3 / X4", (309, 260), 1.7, "09_BORNES")
    headers = ("BORNE", "FUNCAO", "CABO", "DESTINO")
    table(layout, 18, 253, (27, 70, 38, 58), headers, left_rows, row_height=13.8, text_height=1.05)
    table(layout, 211, 253, (29, 77, 38, 47), headers, right_rows, row_height=13.8, text_height=1.05)
    add_rect(layout, 18, 110, 402, 125, "13_NOTAS")
    centered(layout, "SEGREGACAO: X1/X2 POTENCIA | X3 COMANDO 24 Vcc | X4 STO/ANALOGICO | SH EM ABRACADEIRA EMC", (210, 117.5), 1.25, "13_NOTAS")


def draw_cable_list(layout, loads: list[dict[str, str]], cables: list[dict[str, str]]) -> None:
    rows: list[tuple[str, ...]] = []
    for cable in cables:
        rows.append((
            cable["cabo"], cable["de"], cable["para"], cable["funcao"], cable["formacao"],
            cable["blindagem"], cable["comprimento_assumido_m"], cable["rota"],
        ))
    headers = ("CABO", "DE", "PARA", "FUNCAO", "FORMACAO", "BL", "m", "ROTA")
    widths = (22, 46, 49, 77, 61, 18, 20, 91)
    table(layout, 18, 261, widths, headers, rows, row_height=10.3, text_height=0.95)
    add_rect(layout, 18, 120, 402, 141, "12_LEGENDA")
    centered(layout, "SÍNTESE DE MATERIAIS", (210, 136), 1.45, "12_LEGENDA")
    centered(layout, "QG-06 50 A | QF-601/602/603 | KM-601 | KM-602F/R + IM | FR-601/602 | VFD-603 11 kW | KSR-601 | PSU-601 24 Vcc", (210, 128), 1.12, "02_TEXTO")
    add_rect(layout, 18, 105, 402, 116, "13_NOTAS")
    centered(layout, "COMPRIMENTO TOTAL ASSUMIDO: 196 m | CONFERIR LISTA-MATERIAIS.CSV PARA QUANTITATIVOS COMPLETOS", (210, 110.5), 1.15, "13_NOTAS")


DRAWERS = {
    1: draw_unifilar,
    2: draw_dol,
    3: draw_reverse,
    4: draw_vfd,
    5: draw_layout,
    6: draw_terminals,
    7: draw_cable_list,
}


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    project = root / PROJECT_SLUG
    loads = read_rows(project, "lista-cargas.csv")
    cables = read_rows(project, "lista-cabos.csv")
    source_dir = project / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for spec in SHEETS:
        doc, layout = create_sheet(config, spec)
        DRAWERS[spec.number](layout, loads, cables)
        output = source_dir / spec.filename
        prepare_deterministic_write(doc)
        with output.open("wt", encoding="utf-8", newline="\n") as stream:
            doc.write(stream)
        outputs.append(output)
        print(f"Gerado: {output.relative_to(root)}")
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositorio")
    return parser.parse_args()


def main() -> int:
    generate(parse_args().root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
