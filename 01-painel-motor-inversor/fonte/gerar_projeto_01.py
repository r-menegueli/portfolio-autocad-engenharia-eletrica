"""Gera as seis pranchas DXF do Projeto 01 de forma deterministica."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
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
    TEXT_STYLE,
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


PROJECT_SLUG = "01-painel-motor-inversor"
PROJECT_DATE = "2026-09-05"
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
        "01_diagrama_unifilar.dxf",
        "DIAGRAMA UNIFILAR",
        "Arquitetura geral de potência e aterramento",
        "Rede assumida: 380 V, 3 fases, 60 Hz, TN-S. Motor M1: 7,5 kW.\\P"
        "Q0, Q1, DPS1 e VFD1 exigem seleção final por estudo de aplicação.",
        "Q: manobra/proteção | VFD: inversor | X: borne | M: motor | PE: proteção",
    ),
    SheetSpec(
        2,
        "02_diagrama_potencia.dxf",
        "DIAGRAMA DE POTÊNCIA",
        "Circuito trifásico do alimentador ao motor",
        "Não manobrar o circuito entre VFD1 e M1 com o inversor em operação.\\P"
        "Blindagem de W02 terminada em 360 graus nas duas extremidades.",
        "L1/L2/L3: fases | U/V/W: saída PWM | PE: proteção | SH: blindagem",
    ),
    SheetSpec(
        3,
        "03_diagrama_comando.dxf",
        "DIAGRAMA DE COMANDO",
        "Comandos em 24 Vcc, seleção local/remoto e STO",
        "Emergência em dois canais via KSR1 e STO de VFD1; categoria de segurança\\P"
        "não declarada sem análise de risco. Rearme automático desabilitado.",
        "S: botão/seletor | H: sinalizador | KSR: relé de segurança | DI/AI/RO: I/O",
    ),
    SheetSpec(
        4,
        "04_layout_interno_painel.dxf",
        "LAYOUT INTERNO DO PAINEL",
        "Arranjo conceitual do invólucro 800 x 600 x 300 mm",
        "Dimensões do painel e folgas são premissas acadêmicas. Confirmar perdas,\\P"
        "ventilação, EMC, acessibilidade, raio de curvatura e manutenção.",
        "Tracejado: trilho DIN | Cinza: canaleta | PE: barra de proteção | SH: abraçadeira",
    ),
    SheetSpec(
        5,
        "05_diagrama_bornes.dxf",
        "DIAGRAMA DE BORNES",
        "Réguas X1, X2 e X3 com cabos e funções identificados",
        "Separar fisicamente potência, comando e sinais analógicos. Identificar todos\\P"
        "os condutores nas duas extremidades e aterrar blindagens conforme projeto.",
        "X1: entrada | X2: motor/PTC | X3: comando e sinais | SH: blindagem",
    ),
    SheetSpec(
        6,
        "06_interligacoes_campo.dxf",
        "INTERLIGAÇÕES DE CAMPO",
        "Interfaces do painel com rede, motor, emergência e automação",
        "Comprimentos são premissas para documentação e orçamento conceitual.\\P"
        "Rotas, segregação, queda de tensão e EMC dependem de levantamento em campo.",
        "W01/W02: potência | W03/W04/W05/W06: comando e instrumentação",
    ),
)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def centered_text(layout, value: str, point: tuple[float, float], height: float, layer: str) -> None:
    add_text(
        layout,
        value,
        point,
        height,
        layer=layer,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )


def equipment_box(
    layout,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    tag: str,
    description: str,
    *,
    layer: str = "04_EQUIPAMENTOS",
) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered_text(layout, tag, ((x0 + x1) / 2.0, y1 - 5.0), 2.5, layer)
    centered_text(layout, description, ((x0 + x1) / 2.0, y0 + 5.0), 1.6, "02_TEXTO")


def cable_label(layout, value: str, point: tuple[float, float]) -> None:
    centered_text(layout, value, point, 1.8, "08_CABOS")


def define_project_symbols(doc: ezdxf.document.Drawing) -> None:
    if "P01_MOTOR" not in doc.blocks:
        motor = doc.blocks.new("P01_MOTOR", base_point=(0.0, 0.0))
        motor.add_circle((0.0, 0.0), 12.0, dxfattribs={"layer": "04_EQUIPAMENTOS"})
        centered_text(motor, "M", (0.0, 2.0), 5.0, "04_EQUIPAMENTOS")
        centered_text(motor, "3~", (0.0, -5.0), 2.0, "04_EQUIPAMENTOS")

    if "P01_TERRA" not in doc.blocks:
        ground = doc.blocks.new("P01_TERRA", base_point=(0.0, 0.0))
        line(ground, (0.0, 4.0), (0.0, 0.0), "05_POTENCIA")
        line(ground, (-4.0, 0.0), (4.0, 0.0), "05_POTENCIA")
        line(ground, (-2.8, -1.7), (2.8, -1.7), "05_POTENCIA")
        line(ground, (-1.4, -3.4), (1.4, -3.4), "05_POTENCIA")

    for name, normally_closed in (("P01_CONTATO_NA", False), ("P01_CONTATO_NF", True)):
        if name in doc.blocks:
            continue
        block = doc.blocks.new(name, base_point=(0.0, 0.0))
        line(block, (-7.0, 0.0), (-2.0, 0.0), "06_COMANDO")
        line(block, (2.0, 0.0), (7.0, 0.0), "06_COMANDO")
        line(block, (-2.0, 0.0), (2.0, 3.0), "06_COMANDO")
        if normally_closed:
            line(block, (-2.0, 3.0), (2.0, -1.0), "06_COMANDO")

    if "P01_LAMPADA" not in doc.blocks:
        lamp = doc.blocks.new("P01_LAMPADA", base_point=(0.0, 0.0))
        lamp.add_circle((0.0, 0.0), 3.2, dxfattribs={"layer": "06_COMANDO"})
        line(lamp, (-2.2, -2.2), (2.2, 2.2), "06_COMANDO")
        line(lamp, (-2.2, 2.2), (2.2, -2.2), "06_COMANDO")

    if "P01_POT" not in doc.blocks:
        pot = doc.blocks.new("P01_POT", base_point=(0.0, 0.0))
        line(pot, (-8.0, 0.0), (8.0, 0.0), "07_INSTRUMENTACAO")
        line(pot, (-5.0, -2.0), (-3.0, 2.0), "07_INSTRUMENTACAO")
        line(pot, (-3.0, 2.0), (-1.0, -2.0), "07_INSTRUMENTACAO")
        line(pot, (-1.0, -2.0), (1.0, 2.0), "07_INSTRUMENTACAO")
        line(pot, (1.0, 2.0), (3.0, -2.0), "07_INSTRUMENTACAO")
        line(pot, (3.0, -2.0), (5.0, 2.0), "07_INSTRUMENTACAO")
        line(pot, (0.0, 7.0), (0.0, 2.5), "07_INSTRUMENTACAO")
        line(pot, (0.0, 2.5), (2.0, 4.5), "07_INSTRUMENTACAO")


def add_revision_table(layout) -> None:
    add_rect(layout, 230.0, 72.0, 410.0, 94.0, "01_CARIMBO")
    line(layout, (230.0, 86.0), (410.0, 86.0), "01_CARIMBO")
    for x in (248.0, 280.0, 352.0):
        line(layout, (x, 72.0), (x, 94.0), "01_CARIMBO")
    for value, x in (("REV.", 239.0), ("DATA", 264.0), ("DESCRIÇÃO", 316.0), ("RESP.", 381.0)):
        centered_text(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239.0), (PROJECT_DATE, 264.0), ("EMISSÃO INICIAL DO PROJETO 01", 316.0), ("R.E.M.M.", 381.0)):
        centered_text(layout, value, (x, 78.5), 1.7, "02_TEXTO")


def add_bottom_information(layout, spec: SheetSpec, warning: str) -> None:
    add_rect(layout, 18.0, 18.0, 224.0, 46.0, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATÓRIO", (22.0, 42.0), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22.0, 37.0), 198.0, 1.55, "13_NOTAS")

    add_rect(layout, 18.0, 50.0, 224.0, 70.0, "13_NOTAS")
    add_text(layout, "NOTAS DA PRANCHA", (22.0, 66.5), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, spec.notes, (22.0, 62.0), 198.0, 1.55, "13_NOTAS")

    add_rect(layout, 18.0, 74.0, 224.0, 94.0, "12_LEGENDA")
    add_text(layout, "LEGENDA", (22.0, 90.5), 2.1, layer="12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, spec.legend, (22.0, 86.0), 198.0, 1.55, "12_LEGENDA")


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
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230.0, 10.0), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(values)


def create_sheet(config: dict, spec: SheetSpec):
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height))
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = PROJECT_SLUG
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/06"
    define_title_block(doc)
    define_symbols(doc)
    define_project_symbols(doc)
    msp = doc.modelspace()
    add_frame(msp, geometry)
    centered_text(msp, spec.title, (210.0, 277.0), 4.2, "02_TEXTO")
    centered_text(msp, spec.subtitle, (210.0, 270.8), 2.1, "02_TEXTO")
    add_bottom_information(msp, spec, config["portfolio"]["warning"])
    add_revision_table(msp)
    add_title_block(msp, spec, config)
    return doc, msp


def draw_unifilar(layout) -> None:
    y = 191.0
    line(layout, (28.0, y), (67.0, y), "05_POTENCIA")
    equipment_box(layout, 67.0, 177.0, 101.0, 205.0, "Q0", "Seccionadora 3P 32 A")
    line(layout, (101.0, y), (116.0, y), "05_POTENCIA")
    equipment_box(layout, 116.0, 177.0, 151.0, 205.0, "Q1", "Disjuntor 3P 25 A")
    line(layout, (151.0, y), (203.0, y), "05_POTENCIA")
    equipment_box(layout, 203.0, 164.0, 267.0, 218.0, "VFD1", "11 kW / 380-480 V")
    line(layout, (267.0, y), (335.0, y), "05_POTENCIA")
    layout.add_blockref("P01_MOTOR", (351.0, y), dxfattribs={"layer": "04_EQUIPAMENTOS"})

    centered_text(layout, "REDE 3~ 380 V / 60 Hz", (46.0, 218.0), 2.2, "02_TEXTO")
    centered_text(layout, "X1", (46.0, 199.0), 2.0, "09_BORNES")
    layout.add_blockref("SIM_TERMINAL", (46.0, y), dxfattribs={"layer": "09_BORNES"})
    centered_text(layout, "X2", (295.0, 199.0), 2.0, "09_BORNES")
    layout.add_blockref("SIM_TERMINAL", (295.0, y), dxfattribs={"layer": "09_BORNES"})
    centered_text(layout, "M1", (351.0, 211.0), 2.2, "04_EQUIPAMENTOS")
    centered_text(layout, "7,5 kW / 15,5 A", (351.0, 169.0), 1.8, "02_TEXTO")
    cable_label(layout, "W01 - 4G4 mm²", (47.0, 184.0))
    cable_label(layout, "W02 - CABO VFD BLINDADO", (301.0, 181.0))

    line(layout, (170.0, y), (170.0, 157.0), "05_POTENCIA")
    equipment_box(layout, 158.0, 137.0, 182.0, 157.0, "DPS1", "Tipo 2 / 3P")
    line(layout, (170.0, 137.0), (170.0, 120.0), "05_POTENCIA")
    line(layout, (28.0, 120.0), (369.0, 120.0), "05_POTENCIA")
    layout.add_blockref("P01_TERRA", (34.0, 116.0), dxfattribs={"layer": "05_POTENCIA"})
    line(layout, (235.0, 164.0), (235.0, 120.0), "05_POTENCIA")
    line(layout, (351.0, 179.0), (351.0, 120.0), "05_POTENCIA")
    centered_text(layout, "BARRAMENTO PE", (93.0, 126.0), 2.0, "05_POTENCIA")
    centered_text(layout, "TN-S", (50.0, 108.0), 1.8, "02_TEXTO")
    centered_text(layout, "STO A/B E COMANDO 24 Vcc: VER PRANCHA 03", (273.0, 108.0), 1.8, "06_COMANDO")


def draw_power(layout) -> None:
    phases = ((224.0, "L1", "U"), (204.0, "L2", "V"), (184.0, "L3", "W"))
    for y, source_label, output_label in phases:
        line(layout, (27.0, y), (70.0, y), "05_POTENCIA")
        line(layout, (100.0, y), (117.0, y), "05_POTENCIA")
        line(layout, (147.0, y), (187.0, y), "05_POTENCIA")
        line(layout, (255.0, y), (300.0, y), "05_POTENCIA")
        motor_y = 204.0 + (y - 204.0) * 0.48
        motor_dy = motor_y - 204.0
        motor_x = 352.0 - math.sqrt(12.0**2 - motor_dy**2)
        line(layout, (304.0, y), (motor_x, motor_y), "05_POTENCIA")
        add_text(layout, source_label, (30.0, y + 2.5), 1.8, layer="02_TEXTO")
        add_text(layout, output_label, (260.0, y + 2.5), 1.8, layer="02_TEXTO")
        layout.add_blockref("SIM_TERMINAL", (302.0, y), dxfattribs={"layer": "09_BORNES"})

    equipment_box(layout, 70.0, 172.0, 100.0, 236.0, "Q0", "AC-23A / 32 A")
    equipment_box(layout, 117.0, 172.0, 147.0, 236.0, "Q1", "3P / 25 A / 10 kA")
    for y, _, _ in phases:
        line(layout, (70.0, y), (80.0, y), "05_POTENCIA")
        line(layout, (80.0, y), (92.0, y + 3.0), "05_POTENCIA")
        line(layout, (92.0, y + 3.0), (100.0, y), "05_POTENCIA")
        line(layout, (117.0, y), (127.0, y), "05_POTENCIA")
        line(layout, (127.0, y), (139.0, y + 3.0), "05_POTENCIA")
        line(layout, (139.0, y + 3.0), (147.0, y), "05_POTENCIA")
    equipment_box(layout, 187.0, 163.0, 255.0, 245.0, "VFD1", "R/S/T → U/V/W")
    centered_text(layout, "RETIFICADOR + BARRAMENTO CC + INVERSOR PWM", (221.0, 203.0), 1.7, "04_EQUIPAMENTOS")
    centered_text(layout, "X2:1...3", (302.0, 239.0), 1.8, "09_BORNES")
    layout.add_blockref("P01_MOTOR", (352.0, 204.0), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    centered_text(layout, "M1", (352.0, 224.0), 2.1, "04_EQUIPAMENTOS")

    for x in (159.0, 165.0, 171.0):
        line(layout, (x, 184.0 + (x - 159.0) / 6.0 * 40.0), (x, 157.0), "05_POTENCIA")
    equipment_box(layout, 151.0, 137.0, 179.0, 157.0, "DPS1", "T2 / 3P")
    line(layout, (165.0, 137.0), (165.0, 116.0), "05_POTENCIA")
    line(layout, (28.0, 116.0), (370.0, 116.0), "05_POTENCIA")
    layout.add_blockref("P01_TERRA", (34.0, 112.0), dxfattribs={"layer": "05_POTENCIA"})
    line(layout, (221.0, 163.0), (221.0, 116.0), "05_POTENCIA")
    line(layout, (352.0, 192.0), (352.0, 116.0), "05_POTENCIA")
    centered_text(layout, "PE", (47.0, 122.0), 1.8, "05_POTENCIA")
    cable_label(layout, "W01", (48.0, 233.0))
    cable_label(layout, "W02 - BLINDAGEM SH/PE", (284.0, 158.0))
    centered_text(layout, "Proteção térmica eletrônica: parâmetro de VFD1 = 15,5 A", (282.0, 108.0), 1.8, "13_NOTAS")


def add_contact(layout, x: float, y: float, tag: str, *, nc: bool = False, detail: str = "") -> None:
    name = "P01_CONTATO_NF" if nc else "P01_CONTATO_NA"
    layout.add_blockref(name, (x, y), dxfattribs={"layer": "06_COMANDO"})
    centered_text(layout, tag, (x, y + 6.0), 1.8, "06_COMANDO")
    if detail:
        centered_text(layout, detail, (x, y - 5.0), 1.4, "02_TEXTO")


def draw_command(layout) -> None:
    line(layout, (25.0, 107.0), (25.0, 257.0), "06_COMANDO")
    line(layout, (270.0, 107.0), (270.0, 257.0), "06_COMANDO")
    centered_text(layout, "+24 Vcc", (25.0, 263.0), 1.9, "06_COMANDO")
    centered_text(layout, "0 V", (270.0, 263.0), 1.9, "06_COMANDO")

    for y in (239.0, 219.0):
        line(layout, (25.0, y), (51.0, y), "06_COMANDO")
    add_contact(layout, 58.0, 239.0, "S0A", nc=True, detail="EMERG. CH1")
    add_contact(layout, 58.0, 219.0, "S0B", nc=True, detail="EMERG. CH2")
    line(layout, (65.0, 239.0), (128.0, 239.0), "06_COMANDO")
    line(layout, (65.0, 219.0), (128.0, 219.0), "06_COMANDO")
    equipment_box(layout, 128.0, 208.0, 201.0, 250.0, "KSR1", "Relé segurança 24 Vcc", layer="06_COMANDO")
    line(layout, (201.0, 239.0), (270.0, 239.0), "06_COMANDO")
    line(layout, (201.0, 219.0), (270.0, 219.0), "06_COMANDO")
    add_text(layout, "STO-A", (223.0, 242.0), 1.7, layer="07_INSTRUMENTACAO")
    add_text(layout, "STO-B", (223.0, 222.0), 1.7, layer="07_INSTRUMENTACAO")

    for y in (190.0, 168.0):
        line(layout, (25.0, y), (48.0, y), "06_COMANDO")
    line(layout, (25.0, 146.0), (65.0, 146.0), "06_COMANDO")
    add_contact(layout, 55.0, 190.0, "S3-L", detail="LOCAL")
    add_contact(layout, 91.0, 190.0, "S2", nc=True, detail="PARAR")
    add_contact(layout, 127.0, 190.0, "S1", detail="PARTIR")
    line(layout, (62.0, 190.0), (84.0, 190.0), "06_COMANDO")
    line(layout, (98.0, 190.0), (120.0, 190.0), "06_COMANDO")
    line(layout, (134.0, 190.0), (270.0, 190.0), "06_COMANDO")
    add_text(layout, "VFD1-DI1 RUN 3 FIOS", (171.0, 194.0), 1.7, layer="07_INSTRUMENTACAO")

    add_contact(layout, 55.0, 168.0, "S3-R", detail="REMOTO")
    add_contact(layout, 103.0, 168.0, "X3:7", detail="RUN REMOTO")
    add_contact(layout, 151.0, 168.0, "X3:8", nc=True, detail="STOP REMOTO")
    line(layout, (62.0, 168.0), (96.0, 168.0), "06_COMANDO")
    line(layout, (110.0, 168.0), (144.0, 168.0), "06_COMANDO")
    line(layout, (158.0, 168.0), (270.0, 168.0), "06_COMANDO")

    add_contact(layout, 72.0, 146.0, "S4", detail="RESET")
    line(layout, (79.0, 146.0), (270.0, 146.0), "06_COMANDO")
    add_text(layout, "VFD1-DI2 RESET", (157.0, 150.0), 1.7, layer="07_INSTRUMENTACAO")

    line(layout, (25.0, 128.0), (64.0, 128.0), "07_INSTRUMENTACAO")
    layout.add_blockref("P01_POT", (72.0, 128.0), dxfattribs={"layer": "07_INSTRUMENTACAO"})
    line(layout, (80.0, 128.0), (145.0, 128.0), "07_INSTRUMENTACAO")
    centered_text(layout, "P1 / 0-10 V LOCAL", (105.0, 134.0), 1.5, "07_INSTRUMENTACAO")
    line(layout, (25.0, 110.0), (145.0, 110.0), "07_INSTRUMENTACAO")
    centered_text(layout, "X3:10-11 / 4-20 mA REMOTO", (85.0, 116.0), 1.5, "07_INSTRUMENTACAO")
    add_rect(layout, 145.0, 104.0, 207.0, 134.0, "07_INSTRUMENTACAO")
    centered_text(layout, "S3 - FONTE DE REFERÊNCIA", (176.0, 129.0), 1.7, "07_INSTRUMENTACAO")
    centered_text(layout, "LOCAL / REMOTO", (176.0, 118.5), 1.6, "02_TEXTO")
    line(layout, (207.0, 118.5), (270.0, 118.5), "07_INSTRUMENTACAO")
    centered_text(layout, "VFD1-AI1", (238.5, 125.0), 1.6, "07_INSTRUMENTACAO")

    add_rect(layout, 292.0, 112.0, 401.0, 254.0, "12_LEGENDA")
    centered_text(layout, "SINALIZAÇÃO", (346.5, 247.0), 2.3, "12_LEGENDA")
    statuses = (("H1", "PAINEL ENERGIZADO", 224.0), ("H2", "VFD PRONTO", 196.0), ("H3", "MOTOR EM MARCHA", 168.0), ("H4", "FALHA VFD", 140.0))
    for tag, label, y in statuses:
        layout.add_blockref("P01_LAMPADA", (310.0, y), dxfattribs={"layer": "06_COMANDO"})
        add_text(layout, tag, (320.0, y + 2.0), 1.8, layer="06_COMANDO")
        add_text(layout, label, (320.0, y - 3.0), 1.55, layer="02_TEXTO")
    centered_text(layout, "H2/H3/H4 comandadas por RO/DO de VFD1", (346.5, 119.0), 1.5, "13_NOTAS")


def draw_layout(layout) -> None:
    add_rect(layout, 52.0, 105.0, 368.0, 261.0, "11_ARQUITETURA")
    centered_text(layout, "PLACA DE MONTAGEM - 800 x 600 mm", (210.0, 255.0), 2.2, "11_ARQUITETURA")

    for x0, x1 in ((62.0, 82.0), (338.0, 358.0)):
        add_rect(layout, x0, 117.0, x1, 244.0, "10_ELETROCALHAS")
        centered_text(layout, "CANALETA", ((x0 + x1) / 2.0, 180.0), 1.4, "10_ELETROCALHAS")
    for y0, y1 in ((222.0, 236.0), (174.0, 188.0), (124.0, 138.0)):
        add_rect(layout, 82.0, y0, 338.0, y1, "10_ELETROCALHAS")

    for y in (217.0, 169.0, 119.0):
        line(layout, (88.0, y), (332.0, y), "03_COTAS")

    equipment_box(layout, 92.0, 194.0, 122.0, 216.0, "Q0", "32 A")
    equipment_box(layout, 130.0, 194.0, 160.0, 216.0, "Q1", "25 A")
    equipment_box(layout, 168.0, 194.0, 198.0, 216.0, "DPS1", "T2")
    equipment_box(layout, 206.0, 194.0, 242.0, 216.0, "Q2", "2 A")
    equipment_box(layout, 250.0, 194.0, 291.0, 216.0, "PS1", "24 Vcc")
    equipment_box(layout, 299.0, 194.0, 330.0, 216.0, "KSR1", "STO", layer="06_COMANDO")

    equipment_box(layout, 125.0, 141.0, 244.0, 169.0, "VFD1", "11 kW / ventilação vertical")
    centered_text(layout, "≥100 mm LIVRE", (184.5, 179.0), 1.7, "03_COTAS")
    centered_text(layout, "≥100 mm LIVRE", (184.5, 130.0), 1.7, "03_COTAS")
    equipment_box(layout, 255.0, 145.0, 326.0, 167.0, "TB-PE", "Barra de terra", layer="05_POTENCIA")

    add_rect(layout, 92.0, 108.0, 330.0, 122.0, "09_BORNES")
    for x in range(104, 330, 14):
        line(layout, (float(x), 108.0), (float(x), 122.0), "09_BORNES")
    centered_text(layout, "X1 | X2 | X3 - RÉGUAS DE BORNES", (211.0, 115.0), 1.8, "09_BORNES")

    line(layout, (45.0, 105.0), (45.0, 261.0), "03_COTAS")
    line(layout, (41.0, 105.0), (49.0, 105.0), "03_COTAS")
    line(layout, (41.0, 261.0), (49.0, 261.0), "03_COTAS")
    centered_text(layout, "600 mm", (40.0, 183.0), 1.8, "03_COTAS")
    line(layout, (52.0, 265.0), (368.0, 265.0), "03_COTAS")
    centered_text(layout, "800 mm", (210.0, 263.0), 1.8, "03_COTAS")


def terminal_group(layout, x0: float, x1: float, y_top: float, title: str, rows: list[tuple[str, str, str]], row_h: float = 8.0) -> None:
    header_h = 12.0
    y_bottom = y_top - header_h - row_h * len(rows)
    add_rect(layout, x0, y_bottom, x1, y_top, "09_BORNES")
    line(layout, (x0, y_top - header_h), (x1, y_top - header_h), "09_BORNES")
    c1 = x0 + 17.0
    c2 = x0 + (x1 - x0) * 0.63
    line(layout, (c1, y_bottom), (c1, y_top - header_h), "09_BORNES")
    line(layout, (c2, y_bottom), (c2, y_top - header_h), "09_BORNES")
    centered_text(layout, title, ((x0 + x1) / 2.0, y_top - 6.0), 2.2, "09_BORNES")
    for index, (terminal, function, cable) in enumerate(rows):
        y1 = y_top - header_h - index * row_h
        y0 = y1 - row_h
        if index:
            line(layout, (x0, y1), (x1, y1), "09_BORNES")
        centered_text(layout, terminal, ((x0 + c1) / 2.0, (y0 + y1) / 2.0), 1.55, "09_BORNES")
        centered_text(layout, function, ((c1 + c2) / 2.0, (y0 + y1) / 2.0), 1.45, "02_TEXTO")
        centered_text(layout, cable, ((c2 + x1) / 2.0, (y0 + y1) / 2.0), 1.45, "08_CABOS")


def draw_terminals(layout) -> None:
    terminal_group(
        layout,
        18.0,
        105.0,
        257.0,
        "X1 - ENTRADA",
        [("1", "L1", "W01-1"), ("2", "L2", "W01-2"), ("3", "L3", "W01-3"), ("4", "PE", "W01-PE")],
        10.0,
    )
    terminal_group(
        layout,
        111.0,
        228.0,
        257.0,
        "X2 - MOTOR / PTC",
        [("1", "U", "W02-1"), ("2", "V", "W02-2"), ("3", "W", "W02-3"), ("4", "PE/SH", "W02-PE"), ("5", "PTC1", "W03-1"), ("6", "PTC2", "W03-2")],
        10.0,
    )
    x3_rows = [
        ("1", "+24 Vcc", "W04-1"),
        ("2", "0 V", "W04-2"),
        ("3", "E-STOP CH1", "W04-3"),
        ("4", "RET. CH1", "W04-4"),
        ("5", "E-STOP CH2", "W04-5"),
        ("6", "RET. CH2", "W04-6"),
        ("7", "RUN REMOTO", "W05-1"),
        ("8", "STOP REMOTO", "W05-2"),
        ("9", "RESET REMOTO", "W05-3"),
        ("10", "AI1 +", "W06-1"),
        ("11", "AI1 -", "W06-2"),
        ("12", "RUN NO", "W05-4"),
        ("13", "FALHA NO", "W05-5"),
        ("14", "COMUM RO", "W05-6"),
        ("15", "SHIELD", "W06-SH"),
    ]
    terminal_group(layout, 234.0, 405.0, 257.0, "X3 - COMANDO / SINAIS", x3_rows, 8.2)
    centered_text(layout, "PONTES: nenhuma ponte permanente nos canais de emergência", (123.0, 116.0), 1.6, "13_NOTAS")
    centered_text(layout, "SEGREGAÇÃO: X1/X2 potência; X3 controle e instrumentação", (123.0, 108.0), 1.6, "13_NOTAS")


def orthogonal_cable(layout, points: list[tuple[float, float]], cable: str, label_point: tuple[float, float], layer: str) -> None:
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)
    cable_label(layout, cable, label_point)


def draw_field(layout) -> None:
    equipment_box(layout, 149.0, 146.0, 272.0, 228.0, "PAINEL P01", "Q0/Q1/VFD1/KSR1/X1-X3")
    equipment_box(layout, 22.0, 184.0, 94.0, 224.0, "QDG", "Rede 380 V 3~ + PE")
    equipment_box(layout, 332.0, 184.0, 398.0, 224.0, "M1", "Motor 7,5 kW + PTC")
    equipment_box(layout, 23.0, 239.0, 105.0, 260.0, "S0", "Emergência 2 canais", layer="06_COMANDO")
    equipment_box(layout, 315.0, 239.0, 399.0, 260.0, "PLC REMOTO", "Comandos e estados", layer="07_INSTRUMENTACAO")
    equipment_box(layout, 26.0, 108.0, 105.0, 137.0, "MALHA PE", "TN-S / equipotencial")
    equipment_box(layout, 315.0, 108.0, 399.0, 137.0, "REFERÊNCIA", "4-20 mA remota", layer="07_INSTRUMENTACAO")

    orthogonal_cable(layout, [(94.0, 204.0), (149.0, 204.0)], "W01 - 4G4", (121.5, 210.0), "05_POTENCIA")
    orthogonal_cable(layout, [(272.0, 204.0), (332.0, 204.0)], "W02 - VFD", (302.0, 210.0), "05_POTENCIA")
    orthogonal_cable(layout, [(272.0, 181.0), (314.0, 181.0), (314.0, 192.0), (332.0, 192.0)], "W03 - PTC", (293.0, 176.0), "07_INSTRUMENTACAO")
    orthogonal_cable(layout, [(105.0, 249.0), (128.0, 249.0), (128.0, 218.0), (149.0, 218.0)], "W04", (126.0, 255.0), "06_COMANDO")
    orthogonal_cable(layout, [(315.0, 249.0), (292.0, 249.0), (292.0, 218.0), (272.0, 218.0)], "W05", (294.0, 255.0), "07_INSTRUMENTACAO")
    orthogonal_cable(layout, [(315.0, 122.0), (291.0, 122.0), (291.0, 158.0), (272.0, 158.0)], "W06", (294.0, 116.0), "07_INSTRUMENTACAO")
    orthogonal_cable(layout, [(105.0, 122.0), (127.0, 122.0), (127.0, 158.0), (149.0, 158.0)], "PE", (125.0, 116.0), "05_POTENCIA")

    centered_text(layout, "X1", (143.0, 205.0), 1.8, "09_BORNES")
    centered_text(layout, "X2", (278.0, 205.0), 1.8, "09_BORNES")
    centered_text(layout, "X3:3-6", (141.0, 222.0), 1.6, "09_BORNES")
    centered_text(layout, "X3:7-14", (280.0, 222.0), 1.6, "09_BORNES")
    centered_text(layout, "X3:10-11/15", (286.0, 162.0), 1.5, "09_BORNES")
    centered_text(layout, "TB-PE", (141.0, 162.0), 1.6, "09_BORNES")


DRAWERS = {
    1: draw_unifilar,
    2: draw_power,
    3: draw_command,
    4: draw_layout,
    5: draw_terminals,
    6: draw_field,
}


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    source_dir = root / PROJECT_SLUG / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for spec in SHEETS:
        doc, layout = create_sheet(config, spec)
        DRAWERS[spec.number](layout)
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
    args = parse_args()
    generate(args.root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
