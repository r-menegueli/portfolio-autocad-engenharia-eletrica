"""Gera as nove pranchas DXF do Projeto 05 de forma deterministica."""

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


PROJECT_SLUG = "05-instalacao-eletrica-industrial"
PROJECT_DATE = "2026-11-06"
REVISION = "05"
REVISION_DESCRIPTION = "RASTREABILIDADE DO LAYOUT"
LAYOUT_METERS_PER_MM = 0.125  # escala 1:125 em um croqui cotado em milimetros


@dataclass(frozen=True)
class SheetSpec:
    number: int
    filename: str
    title: str
    subtitle: str
    notes: str
    legend: str
    scale: str = "S/ESC."


@dataclass(frozen=True)
class Load:
    circuit: str
    board: str
    description: str
    phases: str
    installed_kva: float
    demand_factor: float
    demand_kva: float
    current_a: float
    cable_mm2: float
    breaker_a: int
    drop_pct: float


LOADS = (
    Load("C01", "QDF-05", "M-501 compressor 11 kW", "ABC", 14.379, 1.00, 14.379, 21.847, 6.0, 32, 1.046),
    Load("C02", "QDF-05", "M-502 torno 7,5 kW", "ABC", 10.027, 0.80, 8.021, 15.234, 4.0, 25, 0.937),
    Load("C03", "QDF-05", "M-503 fresadora 5,5 kW", "ABC", 7.526, 0.80, 6.021, 11.435, 4.0, 20, 0.645),
    Load("C04", "QDF-05", "M-504 exaustor 3 kW", "ABC", 4.304, 1.00, 4.304, 6.539, 2.5, 16, 0.697),
    Load("C05", "QDF-05", "M-505 esmeril 2,2 kW", "ABC", 3.194, 0.60, 1.916, 4.853, 2.5, 10, 0.358),
    Load("C06", "QDF-05", "TUE-501 solda 12 kVA", "ABC", 12.000, 0.60, 7.200, 18.232, 6.0, 32, 0.935),
    Load("C07", "QDF-05", "TI-501/503 tomadas ind.", "ABC", 10.500, 0.40, 4.200, 15.953, 4.0, 20, 1.391),
    Load("C08", "QDF-05", "TI-504/506 tomadas ind.", "ABC", 10.500, 0.40, 4.200, 15.953, 4.0, 20, 1.472),
    Load("C09", "QDL-05", "Luz galpao setor A", "A", 0.842, 1.00, 0.842, 3.828, 1.5, 10, 2.088),
    Load("C10", "QDL-05", "Luz galpao setor B", "B", 0.842, 1.00, 0.842, 3.828, 1.5, 10, 2.192),
    Load("C11", "QDL-05", "Luz galpao setor C", "C", 0.842, 1.00, 0.842, 3.828, 1.5, 10, 2.297),
    Load("C12", "QDL-05", "Luz escritorio/apoio", "B", 0.505, 1.00, 0.505, 2.297, 1.5, 10, 0.877),
    Load("C13", "QDL-05", "Luz externa", "C", 0.316, 1.00, 0.316, 1.435, 1.5, 10, 0.685),
    Load("C14", "QADM-05", "TUG escritorio", "A", 1.500, 0.60, 0.900, 6.818, 2.5, 16, 1.395),
    Load("C15", "QADM-05", "TUG manutencao", "B", 1.500, 0.60, 0.900, 6.818, 2.5, 16, 1.506),
    Load("C16", "QADM-05", "TUG servicos", "C", 1.500, 0.60, 0.900, 6.818, 2.5, 16, 1.674),
)

LAYOUT_EQUIPMENT = (
    (72, 215, "M-501", "COMPRESSOR", "C01"),
    (126, 215, "M-502", "TORNO", "C02"),
    (180, 215, "M-503", "FRESADORA", "C03"),
    (72, 158, "M-504", "EXAUSTOR", "C04"),
    (126, 158, "M-505", "ESMERIL", "C05"),
    (192, 157, "TUE-501", "SOLDA", "C06"),
)


SHEETS = (
    SheetSpec(
        1,
        "01_layout_industrial.dxf",
        "LAYOUT INDUSTRIAL",
        "Oficina metalmecanica ficticia - 30 x 18 m - area 540 m2",
        "Dimensoes, fluxos e afastamentos sao premissas academicas.\\P"
        "Confirmar levantamento, acesso, ergonomia, incendio e seguranca de maquinas.",
        "M: motor/maquina | Q: quadro | TI: tomada industrial | Linha cinza: arquitetura",
        "1:125",
    ),
    SheetSpec(
        2,
        "02_distribuicao_forca.dxf",
        "DISTRIBUICAO DE FORCA",
        "QDF-05, maquinas trifasicas, solda e tomadas industriais",
        "Circuitos C01-C08 em 380 V 3~. Protecoes e secoes sao preliminares.\\P"
        "Confirmar partida, curto-circuito, seletividade e capacidade de interrupcao.",
        "Vermelho: potencia | Laranja: cabos | QF: protecao | TI: tomada IEC 60309",
        "1:125",
    ),
    SheetSpec(
        3,
        "03_distribuicao_iluminacao.dxf",
        "DISTRIBUICAO DE ILUMINACAO",
        "Iluminacao LED por setores, circuitos C09-C13 e QDL-05",
        "Arranjo luminotecnico e potencias sao hipoteses. Confirmar iluminancia,\\P"
        "uniformidade, ofuscamento, emergencia e influencias externas.",
        "Circulo com X: luminaria | S: comando | Verde: comando | C09/C10/C11: galpao",
        "1:125",
    ),
    SheetSpec(
        4,
        "04_eletrocalhas_rotas.dxf",
        "ELETROCALHAS E ROTAS",
        "Rotas E-501/E-502/E-503, alimentadores e descidas de circuitos",
        "Ocupacao, suportacao, raio de curvatura, segregacao e EMC nao foram\\P"
        "verificados. Comprimentos sao premissas rastreadas na lista de cabos.",
        "Cinza grosso: eletrocalha | Laranja: cabo | D: descida | PE: protecao",
        "1:125",
    ),
    SheetSpec(
        5,
        "05_diagrama_unifilar.dxf",
        "DIAGRAMA UNIFILAR",
        "Entrada 380/220 V, QGBT-05, QDF-05, QDL-05 e QADM-05",
        "Esquema TN-S conceitual a jusante do ponto de entrega. DR e DPS exigem\\P"
        "coordenacao e selecao conforme rede, cargas, fabricante e estudo executivo.",
        "DJ: disjuntor | DPS: surto | DR: diferencial | N/PE: barras separadas",
    ),
    SheetSpec(
        6,
        "06_quadro_cargas.dxf",
        "QUADRO DE CARGAS",
        "16 circuitos - potencia instalada, demanda, corrente, cabo e protecao",
        "Demanda total: 56,289 kVA; corrente equivalente: 85,523 A em 380 V 3~.\\P"
        "Valores dependem das premissas e nao substituem dimensionamento executivo.",
        "Sinst: instalada | fd: demanda | Sdem: demandada | Ib: corrente | dV: queda",
    ),
    SheetSpec(
        7,
        "07_detalhes_instalacao.dxf",
        "DETALHES DE INSTALACAO",
        "Eletrocalha, tomada industrial, quadros, PE e identificacao",
        "Detalhes sao tipicos e sem validade construtiva. Fabricante, ambiente, IP,\\P"
        "fixacao, equipotencializacao e ensaios devem ser definidos por profissional.",
        "PE: protecao | N: neutro | BEP: equipotencializacao | IP: grau de protecao",
    ),
    SheetSpec(
        8,
        "08_coordenacao_protecoes.dxf",
        "COORDENACAO DAS PROTECOES",
        "Topologia, pares de disjuntores e dados para o estudo de curto-circuito",
        "Icc max/min, curvas tempo-corrente, Icu/Ics, energia passante e seletividade\\P"
        "permanecem pendentes; ratings nominais nao demonstram coordenacao real.",
        "Ik: corrente de curto | TCC: tempo-corrente | Icu/Ics: interrupcao | I2t: energia passante",
    ),
    SheetSpec(
        9,
        "09_plano_dados_coordenacao.dxf",
        "PLANO DE DADOS PARA CURTO-CIRCUITO E COORDENACAO",
        "Entradas e evidencias necessarias para revisar os seis pares da prancha 08",
        "O estudo ainda nao foi calculado. Os doze grupos de dados permanecem pendentes.\\P"
        "Icc e capacidade de interrupcao nao foram definidos; a folha orienta verificacoes e evidencias.",
        "D01-D06: entradas | D07-D08: modelo e Icc | D09-D11: verificacoes | D12: revisao | PENDENTE: sem evidencia",
    ),
)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def centered(layout, value: str, point: tuple[float, float], height: float = 1.6, layer: str = "02_TEXTO") -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER)


def orthogonal(layout, points: list[tuple[float, float]], layer: str) -> None:
    for start, end in zip(points, points[1:]):
        line(layout, start, end, layer)


def arrow(layout, start: tuple[float, float], end: tuple[float, float], layer: str) -> None:
    line(layout, start, end, layer)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    size = 2.5
    line(layout, (end[0] - ux * size + px * size * 0.55, end[1] - uy * size + py * size * 0.55), end, layer)
    line(layout, (end[0] - ux * size - px * size * 0.55, end[1] - uy * size - py * size * 0.55), end, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float, tag: str, detail: str, layer: str = "04_EQUIPAMENTOS") -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    centered(layout, tag, ((x0 + x1) / 2, y1 - 4), 1.75, layer)
    centered(layout, detail, ((x0 + x1) / 2, y0 + 4), 1.15, "02_TEXTO")


def motor(layout, x: float, y: float, tag: str, detail: str) -> None:
    layout.add_circle((x, y), 7, dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "M", (x, y + 1.2), 3.2, "05_POTENCIA")
    centered(layout, "3~", (x, y - 2.6), 1.2, "05_POTENCIA")
    centered(layout, tag, (x, y - 10.2), 1.35, "04_EQUIPAMENTOS")
    centered(layout, detail, (x, y - 13.7), 1.0, "02_TEXTO")


def luminaire(layout, x: float, y: float, tag: str) -> None:
    layout.add_circle((x, y), 3, dxfattribs={"layer": "04_EQUIPAMENTOS"})
    line(layout, (x - 2.1, y - 2.1), (x + 2.1, y + 2.1), "04_EQUIPAMENTOS")
    line(layout, (x - 2.1, y + 2.1), (x + 2.1, y - 2.1), "04_EQUIPAMENTOS")
    centered(layout, tag, (x, y - 5.4), 0.95, "02_TEXTO")


def socket(layout, x: float, y: float, tag: str) -> None:
    layout.add_circle((x, y), 3.5, dxfattribs={"layer": "04_EQUIPAMENTOS"})
    line(layout, (x - 2.2, y), (x + 2.2, y), "04_EQUIPAMENTOS")
    line(layout, (x, y), (x, y + 2.3), "04_EQUIPAMENTOS")
    centered(layout, tag, (x, y - 6), 1.0, "02_TEXTO")


def building(layout, *, labels: bool = True) -> None:
    add_rect(layout, 24, 108, 264, 252, "11_ARQUITETURA")
    line(layout, (216, 108), (216, 252), "11_ARQUITETURA")
    line(layout, (216, 180), (264, 180), "11_ARQUITETURA")
    line(layout, (216, 216), (264, 216), "11_ARQUITETURA")
    if labels:
        centered(layout, "PRODUCAO - 24 x 18 m", (120, 245), 1.55, "11_ARQUITETURA")
        centered(layout, "ESCRITORIO", (240, 248), 1.10, "11_ARQUITETURA")
        centered(layout, "MANUTENCAO", (240, 212), 1.10, "11_ARQUITETURA")
        centered(layout, "SERVICOS", (240, 177), 1.10, "11_ARQUITETURA")


def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), (REVISION_DESCRIPTION, 316), ("R.E.M.M.", 381)):
        centered(layout, value, (x, 78.5), 1.55, "02_TEXTO")


def add_bottom_information(layout, spec: SheetSpec, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    add_text(layout, "AVISO OBRIGATORIO", (22, 42), 2.2, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    add_text(layout, "NOTAS DA PRANCHA", (22, 66.5), 2.1, layer="13_NOTAS", style=TITLE_STYLE)
    add_mtext(layout, spec.notes, (22, 62), 198, 1.48, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    add_text(layout, "LEGENDA", (22, 90.5), 2.1, layer="12_LEGENDA", style=TITLE_STYLE)
    add_mtext(layout, spec.legend, (22, 86), 198, 1.48, "12_LEGENDA")


def add_title_block(layout, spec: SheetSpec, config: dict) -> None:
    values = {
        "TITULO": spec.title,
        "AUTOR": config["portfolio"]["author"],
        "DATA": PROJECT_DATE,
        "REVISAO": REVISION,
        "PRANCHA": f"{spec.number:02d}/{len(SHEETS):02d}",
        "ARQUIVO": spec.filename,
        "UNIDADES": "mm",
        "ESCALA": spec.scale,
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
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/{len(SHEETS):02d}"
    define_title_block(doc)
    define_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 4.2, "02_TEXTO")
    centered(layout, spec.subtitle, (210, 270.8), 2.0, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


def draw_layout_industrial(layout) -> None:
    building(layout)
    for x, y, tag, detail, _circuit in LAYOUT_EQUIPMENT[:5]:
        motor(layout, x, y, tag, detail)
    box(layout, 180, 143, 204, 171, "TUE-501", "SOLDA", "04_EQUIPAMENTOS")
    layout.add_circle((24, 108), 1.4, dxfattribs={"layer": "03_COTAS"})
    add_text(layout, "O=(0,0)", (29, 112), 1.0, layer="03_COTAS")
    box(layout, 222, 223, 258, 244, "QGBT-05", "GERAL", "05_POTENCIA")
    box(layout, 222, 187, 258, 208, "QDF-05", "FORCA", "05_POTENCIA")
    box(layout, 222, 151, 258, 172, "QDL-05", "LUZ", "05_POTENCIA")
    box(layout, 222, 115, 258, 136, "QADM-05", "APOIO", "05_POTENCIA")
    for x, y, tag in ((43, 126, "TI-501"), (83, 126, "TI-502"), (123, 126, "TI-503"), (43, 239, "TI-504"), (123, 239, "TI-505"), (183, 239, "TI-506")):
        socket(layout, x, y, tag)
    line(layout, (24, 103), (264, 103), "03_COTAS")
    centered(layout, "30 000 mm", (144, 100), 1.3, "03_COTAS")
    line(layout, (270, 108), (270, 252), "03_COTAS")
    centered(layout, "18 000 mm", (279, 180), 1.3, "03_COTAS")
    add_rect(layout, 288, 111, 402, 252, "12_LEGENDA")
    centered(layout, "REGISTRO DO LAYOUT", (345, 245), 1.8, "12_LEGENDA")
    centered(layout, "Oficina ficticia - dados de estudo", (345, 237), 1.15, "02_TEXTO")
    centered(layout, "EQUIPAMENTOS, CIRCUITOS E POSICAO", (345, 227), 1.15, "12_LEGENDA")
    for label, x in (("TAG", 294), ("CIRC.", 326), ("S_inst", 345), ("X (m)", 367), ("Y (m)", 387)):
        add_text(layout, label, (x, 218), 1.05, layer="02_TEXTO")
    line(layout, (294, 215), (396, 215), "12_LEGENDA")

    loads_by_circuit = {load.circuit: load for load in LOADS}
    for index, (x, y, tag, _detail, circuit) in enumerate(LAYOUT_EQUIPMENT):
        load = loads_by_circuit[circuit]
        x_m = (x - 24) * LAYOUT_METERS_PER_MM
        y_m = (y - 108) * LAYOUT_METERS_PER_MM
        values = (
            (tag, 294),
            (circuit, 326),
            (f"{load.installed_kva:.3f}".replace(".", ","), 345),
            (f"{x_m:.3f}".replace(".", ","), 367),
            (f"{y_m:.3f}".replace(".", ","), 387),
        )
        row_y = 207 - index * 8
        for value, column_x in values:
            add_text(layout, value, (column_x, row_y), 1.0, layer="02_TEXTO")
    line(layout, (294, 159), (396, 159), "12_LEGENDA")
    centered(layout, "REFERENCIA DO CROQUI", (345, 151), 1.15, "12_LEGENDA")
    for i, text in enumerate((
        "Origem O: canto interno inferior esquerdo.",
        "X/Y em metros, derivados da escala 1:125.",
        "Nao representam levantamento topografico.",
        "S_inst: potencia aparente instalada (kVA).",
        "Pegadas, folgas e acessos reais: pendentes.",
    )):
        add_text(layout, text, (294, 143 - i * 7), 1.0, layer="02_TEXTO")


def draw_force(layout) -> None:
    building(layout)
    box(layout, 222, 221, 258, 244, "QDF-05", "80 A", "05_POTENCIA")
    trunk = [(240, 221), (240, 210), (36, 210), (36, 125)]
    orthogonal(layout, trunk, "10_ELETROCALHAS")
    centered(layout, "E-501 / POTENCIA", (137, 214), 1.2, "10_ELETROCALHAS")
    points = (
        (72, 194, "M-501", "C01 / 32 A"),
        (126, 194, "M-502", "C02 / 25 A"),
        (180, 194, "M-503", "C03 / 20 A"),
        (72, 151, "M-504", "C04 / 16 A"),
        (126, 151, "M-505", "C05 / 10 A"),
    )
    for x, y, tag, detail in points:
        motor(layout, x, y, tag, detail)
        orthogonal(layout, [(x, 210), (x, y + 7)], "08_CABOS")
    box(layout, 169, 139, 202, 165, "TUE-501", "C06 / 32 A", "04_EQUIPAMENTOS")
    orthogonal(layout, [(185.5, 210), (185.5, 165)], "08_CABOS")
    for x, y, tag, circuit in ((47, 119, "TI-501/503", "C07"), (139, 119, "TI-504/506", "C08")):
        socket(layout, x, y, tag)
        orthogonal(layout, [(x, 210), (x, y + 4)], "08_CABOS")
        centered(layout, circuit, (x + 12, 130), 1.2, "08_CABOS")
    add_rect(layout, 286, 111, 402, 252, "12_LEGENDA")
    centered(layout, "CIRCUITOS DE FORCA", (344, 245), 1.8, "12_LEGENDA")
    for i, load in enumerate(LOADS[:8]):
        add_text(layout, f"{load.circuit}  {load.current_a:.2f} A  {load.cable_mm2:g} mm2  DJ {load.breaker_a} A", (292, 232 - i * 13.5), 1.25, layer="02_TEXTO")
        add_text(layout, load.description, (297, 227 - i * 13.5), 1.0, layer="02_TEXTO")
    centered(layout, "DR 30 mA nos circuitos C06-C08 (premissa)", (344, 119), 1.15, "13_NOTAS")


def draw_lighting(layout) -> None:
    building(layout)
    grid_x = (46, 78, 110, 142, 174, 206)
    grid_y = (229, 199, 169, 139)
    circuits = ("C09-A", "C10-B", "C11-C")
    for row, y in enumerate(grid_y):
        for col, x in enumerate(grid_x):
            luminaire(layout, x, y, circuits[(row * len(grid_x) + col) % 3])
    for x, y, tag in ((228, 238, "C12-B"), (252, 238, "C12-B"), (228, 202, "C12-B"), (252, 202, "C12-B")):
        luminaire(layout, x, y, tag)
    for x, y in ((30, 258), (96, 258), (162, 258), (228, 258), (270, 214), (270, 146)):
        luminaire(layout, x, y, "C13-C")
    box(layout, 222, 116, 258, 137, "QDL-05", "4P / 16 A", "05_POTENCIA")
    orthogonal(layout, [(240, 137), (240, 146), (208, 146)], "08_CABOS")
    for x, y, tag in ((28, 116, "S-501"), (212, 116, "S-502"), (260, 183, "S-503")):
        centered(layout, "S", (x, y), 2.0, "06_COMANDO")
        centered(layout, tag, (x, y - 4), 0.95, "02_TEXTO")
    add_rect(layout, 286, 111, 402, 252, "12_LEGENDA")
    centered(layout, "RESUMO DE ILUMINACAO", (344, 245), 1.8, "12_LEGENDA")
    rows = (
        "C09-A: 8 x 100 W = 800 W",
        "C10-B: 8 x 100 W = 800 W",
        "C11-C: 8 x 100 W = 800 W",
        "C12-B: 12 x 40 W = 480 W",
        "C13-C: 6 x 50 W = 300 W",
        "Total ativo: 3,180 kW",
        "Fator de potencia: 0,95",
        "Total aparente: 3,347 kVA",
        "Comando: local por setores",
        "Emergencia: estudo especifico",
    )
    for i, text in enumerate(rows):
        add_text(layout, text, (293, 232 - i * 11.5), 1.35, layer="02_TEXTO")


def draw_routes(layout) -> None:
    building(layout)
    box(layout, 222, 226, 258, 246, "QGBT-05", "ORIGEM", "05_POTENCIA")
    box(layout, 222, 190, 258, 210, "QDF-05", "AL-QDF", "05_POTENCIA")
    box(layout, 222, 154, 258, 174, "QDL-05", "AL-QDL", "05_POTENCIA")
    box(layout, 222, 118, 258, 138, "QADM-05", "AL-QADM", "05_POTENCIA")
    orthogonal(layout, [(240, 226), (240, 210)], "08_CABOS")
    orthogonal(layout, [(240, 190), (36, 190), (36, 122)], "10_ELETROCALHAS")
    orthogonal(layout, [(240, 154), (200, 154), (200, 246)], "10_ELETROCALHAS")
    orthogonal(layout, [(240, 118), (210, 118), (210, 246)], "10_ELETROCALHAS")
    centered(layout, "E-501 300 x 100 mm - FORCA", (129, 194), 1.25, "10_ELETROCALHAS")
    centered(layout, "E-502 100 x 50 mm - ILUMINACAO", (189, 207), 1.15, "10_ELETROCALHAS")
    centered(layout, "E-503 100 x 50 mm - APOIO", (222, 145), 1.15, "10_ELETROCALHAS")
    drops = ((72, 190, 160, "D-501 C01"), (126, 190, 160, "D-502 C02"), (180, 190, 160, "D-503 C03"), (72, 190, 122, "D-504 C04"), (126, 190, 122, "D-505 C05"))
    for x, y0, y1, tag in drops:
        line(layout, (x, y0), (x, y1), "08_CABOS")
        centered(layout, tag, (x + 9, y1 + 4), 1.0, "08_CABOS")
    add_rect(layout, 286, 111, 402, 252, "12_LEGENDA")
    centered(layout, "ALIMENTADORES", (344, 245), 1.8, "12_LEGENDA")
    feeder_rows = (
        "AL-QGBT: 25 m / 4x50+PE25 mm2",
        "DJ-G: 4P 100 A / dV 0,885%",
        "AL-QDF: 18 m / 4x25+PE16 mm2",
        "DJ-QDF: 3P 80 A / dV 0,562%",
        "AL-QDL: 20 m / 5x4 mm2",
        "DJ-QDL: 4P 16 A / dV 0,626%",
        "AL-QADM: 16 m / 5x2,5 mm2",
        "DJ-QADM: 4P 16 A / dV 0,536%",
        "PE acompanha todas as rotas",
        "Segregar potencia e comunicacao",
    )
    for i, text in enumerate(feeder_rows):
        add_text(layout, text, (293, 232 - i * 11.5), 1.25, layer="02_TEXTO")


def unifilar_feeder(layout, x: float, tag: str, breaker: str, cable: str, board: str, load: str) -> None:
    line(layout, (x, 224), (x, 211), "05_POTENCIA")
    box(layout, x - 18, 181, x + 18, 211, tag, breaker, "05_POTENCIA")
    line(layout, (x, 181), (x, 165), "08_CABOS")
    centered(layout, cable, (x, 158), 1.15, "08_CABOS")
    box(layout, x - 22, 116, x + 22, 151, board, load, "05_POTENCIA")


def draw_unifilar(layout) -> None:
    centered(layout, "REDE 380/220 V - 3F + N + PE - 60 Hz", (92, 264), 1.45, "05_POTENCIA")
    arrow(layout, (18, 240), (66, 240), "05_POTENCIA")
    box(layout, 66, 222, 105, 258, "DJ-G", "4P / 100 A", "05_POTENCIA")
    box(layout, 121, 222, 160, 258, "DPS-05", "TIPO 2", "05_POTENCIA")
    line(layout, (105, 240), (121, 240), "05_POTENCIA")
    line(layout, (160, 240), (181, 240), "05_POTENCIA")
    box(layout, 181, 222, 224, 258, "QGBT-05", "BARRA 125 A", "05_POTENCIA")
    line(layout, (224, 240), (396, 240), "05_POTENCIA")
    centered(layout, "BARRAMENTO 3F+N+PE", (310, 246), 1.35, "05_POTENCIA")
    unifilar_feeder(layout, 252, "QF-QDF", "3P / 80 A", "4x25 + PE16 mm2", "QDF-05", "50,242 kVA dem.")
    unifilar_feeder(layout, 322, "QF-QDL", "4P / 16 A", "5x4 mm2", "QDL-05", "3,347 kVA dem.")
    unifilar_feeder(layout, 386, "QF-QADM", "4P / 16 A", "5x2,5 mm2", "QADM-05", "2,700 kVA dem.")
    box(layout, 24, 168, 116, 211, "AL-QGBT", "4x50 + PE25 mm2", "08_CABOS")
    centered(layout, "25 m / dV = 0,885%", (70, 176), 1.25, "02_TEXTO")
    add_rect(layout, 24, 110, 209, 154, "09_BORNES")
    centered(layout, "BARRAS E PROTECAO", (116.5, 147), 1.7, "09_BORNES")
    add_text(layout, "N: isolado do PE a jusante da origem", (31, 136), 1.25, layer="02_TEXTO")
    add_text(layout, "PE: continuo, equipotencial e identificado", (31, 127), 1.25, layer="02_TEXTO")
    add_text(layout, "Icc e capacidade de interrupcao: PENDENTES de dados e calculo", (31, 118), 1.25, layer="13_NOTAS")


def draw_load_table(layout) -> None:
    x0, y_top = 18.0, 261.0
    widths = (16, 24, 92, 17, 26, 20, 27, 24, 21, 21, 23)
    headers = ("CIRC.", "QD", "DESCRICAO", "F", "Sinst", "fd", "Sdem", "Ib", "CABO", "DJ", "dV")
    row_h = 8.2
    total_w = sum(widths)
    y_bottom = y_top - row_h * (len(LOADS) + 1)
    add_rect(layout, x0, y_bottom, x0 + total_w, y_top, "12_LEGENDA")
    for i in range(1, len(LOADS) + 1):
        y = y_top - row_h * i
        line(layout, (x0, y), (x0 + total_w, y), "12_LEGENDA")
    cursor = x0
    for width in widths[:-1]:
        cursor += width
        line(layout, (cursor, y_bottom), (cursor, y_top), "12_LEGENDA")
    values = [headers]
    for load in LOADS:
        values.append((
            load.circuit,
            load.board.replace("-05", ""),
            load.description,
            load.phases,
            f"{load.installed_kva:.3f}",
            f"{load.demand_factor:.2f}",
            f"{load.demand_kva:.3f}",
            f"{load.current_a:.2f}",
            f"{load.cable_mm2:g}",
            str(load.breaker_a),
            f"{load.drop_pct:.2f}%",
        ))
    for ridx, row in enumerate(values):
        cursor = x0
        cy = y_top - row_h * ridx - row_h / 2
        for cidx, (value, width) in enumerate(zip(row, widths)):
            if cidx == 2 and ridx:
                add_text(layout, value, (cursor + 2, cy), 1.02, layer="02_TEXTO", align=TextEntityAlignment.MIDDLE_LEFT)
            else:
                centered(layout, value, (cursor + width / 2, cy), 1.08 if ridx else 1.18, "12_LEGENDA")
            cursor += width
    centered(layout, "kVA", (x0 + 16 + 24 + 92 + 17 + 13, y_top - 5.8), 0.72, "12_LEGENDA")
    add_rect(layout, 18, 102, 402, 115, "13_NOTAS")
    centered(layout, "TOTAL INSTALADO 80,277 kVA | TOTAL DEMANDADO 56,289 kVA | I MAX. FASE 86,550 A | DJ-G 100 A | AL-QGBT 4x50+PE25 mm2", (210, 108.5), 1.35, "13_NOTAS")


def draw_details(layout) -> None:
    add_rect(layout, 18, 176, 137, 258, "12_LEGENDA")
    centered(layout, "D1 - CORTE ELETROCALHA", (77.5, 251), 1.7, "12_LEGENDA")
    add_rect(layout, 35, 202, 120, 232, "10_ELETROCALHAS")
    for x in (48, 64, 80, 96, 112):
        layout.add_circle((x, 217), 3, dxfattribs={"layer": "08_CABOS"})
    centered(layout, "E-501 300 x 100 mm", (77.5, 194), 1.3, "02_TEXTO")
    centered(layout, "Ocupacao <= 40% (criterio inicial)", (77.5, 184), 1.15, "13_NOTAS")

    add_rect(layout, 147, 176, 274, 258, "12_LEGENDA")
    centered(layout, "D2 - TOMADA INDUSTRIAL", (210.5, 251), 1.7, "12_LEGENDA")
    socket(layout, 179, 218, "TI-501")
    centered(layout, "IEC 60309 / 16 A", (225, 224), 1.25, "02_TEXTO")
    centered(layout, "3P+N+PE / 380 V", (225, 215), 1.25, "02_TEXTO")
    centered(layout, "DR 30 mA - premissa", (210.5, 194), 1.2, "13_NOTAS")
    centered(layout, "IP conforme ambiente", (210.5, 184), 1.2, "13_NOTAS")

    add_rect(layout, 284, 176, 402, 258, "12_LEGENDA")
    centered(layout, "D3 - QUADRO", (343, 251), 1.7, "12_LEGENDA")
    add_rect(layout, 311, 198, 375, 236, "04_EQUIPAMENTOS")
    centered(layout, "QDF-05", (343, 228), 1.8, "04_EQUIPAMENTOS")
    centered(layout, "EIXO 1,50 m", (343, 212), 1.2, "03_COTAS")
    line(layout, (300, 198), (386, 198), "11_ARQUITETURA")
    centered(layout, "Faixa frontal >= 1,20 m", (343, 185), 1.15, "13_NOTAS")

    add_rect(layout, 18, 106, 137, 166, "12_LEGENDA")
    centered(layout, "D4 - EQUIPOTENCIALIZACAO", (77.5, 158), 1.55, "12_LEGENDA")
    line(layout, (34, 134), (121, 134), "05_POTENCIA")
    centered(layout, "BEP-05", (77.5, 141), 1.5, "05_POTENCIA")
    for x, tag in ((44, "QGBT"), (66, "QD"), (88, "ELET."), (110, "MASSAS")):
        line(layout, (x, 134), (x, 118), "05_POTENCIA")
        centered(layout, tag, (x, 112), 0.95, "02_TEXTO")

    add_rect(layout, 147, 106, 402, 166, "13_NOTAS")
    centered(layout, "D5 - IDENTIFICACAO E INSPECAO", (274.5, 158), 1.65, "13_NOTAS")
    notes = (
        "1. Identificar quadro, circuito, cabo, origem e destino nas duas extremidades.",
        "2. Manter N e PE separados; continuidade do PE deve ser ensaiada.",
        "3. Confirmar torque, aperto, isolacao, polaridade, sequencia de fases e DR.",
        "4. Definir IP, suportacao, distancias e sinalizacao conforme ambiente real.",
        "5. Bloqueio, desenergizacao e trabalho eletrico devem seguir a NR-10 vigente.",
    )
    for i, text in enumerate(notes):
        add_text(layout, text, (154, 146 - i * 8.5), 1.22, layer="02_TEXTO")


def read_protection_pairs(root: Path) -> list[dict[str, str]]:
    path = root / PROJECT_SLUG / "matriz-coordenacao-protecoes.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 6:
        raise ValueError(f"A matriz de protecoes deve conter seis pares; encontrados {len(rows)}")
    return rows


def read_coordination_inputs(root: Path) -> list[dict[str, str]]:
    path = root / PROJECT_SLUG / "dados-estudo-coordenacao.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    expected = [f"D{index:02d}" for index in range(1, 13)]
    if [row["id"] for row in rows] != expected:
        raise ValueError("O plano deve conter os registros D01 a D12 em ordem.")
    if any(row["status"] != "PENDENTE" for row in rows):
        raise ValueError("O estudo de coordenacao nao possui evidencias executadas.")
    return rows


def draw_protection_coordination(layout, rows: list[dict[str, str]]) -> None:
    centered(layout, "TOPOLOGIA DOS DISPOSITIVOS EM ESTUDO", (210, 262), 1.7, "12_LEGENDA")
    box(layout, 20, 226, 83, 256, "PONTO DE ENTREGA", "380/220 V | Icc a confirmar", "05_POTENCIA")
    arrow(layout, (83, 241), (99, 241), "05_POTENCIA")
    box(layout, 99, 226, 151, 256, "DJ-G", "4P / 100 A*", "05_POTENCIA")
    arrow(layout, (151, 241), (166, 241), "05_POTENCIA")
    box(layout, 166, 226, 219, 256, "QGBT-05", "BARRA 125 A", "05_POTENCIA")
    line(layout, (219, 241), (231, 241), "05_POTENCIA")
    line(layout, (231, 188), (231, 247), "05_POTENCIA")

    branches = (
        ("QF-QDF", "3P / 80 A*", "QDF-05", "C01-C08 | 50,242 kVA"),
        ("QF-QDL", "4P / 16 A*", "QDL-05", "C09-C13 | 3,347 kVA"),
        ("QF-QADM", "4P / 16 A*", "QADM-05", "C14-C16 | 2,700 kVA"),
    )
    centers = (242, 215, 188)
    for (device, rating, board, circuits), center_y in zip(branches, centers):
        arrow(layout, (231, center_y), (243, center_y), "05_POTENCIA")
        box(layout, 243, center_y - 11, 296, center_y + 11, device, rating, "05_POTENCIA")
        arrow(layout, (296, center_y), (310, center_y), "05_POTENCIA")
        box(layout, 310, center_y - 11, 400, center_y + 11, board, circuits, "04_EQUIPAMENTOS")

    add_rect(layout, 18, 168, 402, 174, "13_NOTAS")
    centered(
        layout,
        "* Icc e capacidade de interrupcao seguem PENDENTES; valores nominais dos dispositivos sao premissas.",
        (210, 171),
        1.22,
        "13_NOTAS",
    )

    x0, y_top, row_h = 18.0, 162.0, 8.0
    widths = (83, 96, 155, 50)
    column_keys = ("par", "verificacoes", "dados_necessarios", "status")
    headers = dict(zip(column_keys, ("PAR MONTANTE > JUSANTE", "VERIFICAR", "DADOS EXIGIDOS", "STATUS")))
    table_rows = [headers, *rows]
    y_bottom = y_top - row_h * len(table_rows)
    total_w = sum(widths)
    add_rect(layout, x0, y_bottom, x0 + total_w, y_top, "12_LEGENDA")
    for index in range(1, len(table_rows)):
        y = y_top - row_h * index
        line(layout, (x0, y), (x0 + total_w, y), "12_LEGENDA")
    cursor = x0
    for width in widths[:-1]:
        cursor += width
        line(layout, (cursor, y_bottom), (cursor, y_top), "12_LEGENDA")
    for row_index, row in enumerate(table_rows):
        cursor = x0
        center_y = y_top - row_h * row_index - row_h / 2
        for key, width in zip(column_keys, widths):
            value = row[key]
            if key == "dados_necessarios" and row_index:
                add_text(layout, value, (cursor + 2, center_y), 1.02, layer="02_TEXTO", align=TextEntityAlignment.MIDDLE_LEFT)
            else:
                centered(layout, value, (cursor + width / 2, center_y), 1.08 if row_index else 1.12, "12_LEGENDA")
            cursor += width


def draw_coordination_data_plan(layout, rows: list[dict[str, str]]) -> None:
    centered(layout, "ROTEIRO DE VERIFICACAO — SEM RESULTADOS CALCULADOS", (210, 265), 1.65, "12_LEGENDA")
    stages = (
        ("01 | D01-D06 | ENTRADAS", "REDE, TRAFO, CABOS", "FONTES E DISPOSITIVOS", "06_COMANDO"),
        ("02 | D07 | MODELO", "CENARIOS E TIPOS DE FALTA", "IMPEDANCIAS DOCUMENTADAS", "04_EQUIPAMENTOS"),
        ("03 | D08 | CALCULO", "Icc MAX / MIN POR PONTO", "BARRAS E EXTREMIDADES", "05_POTENCIA"),
        ("04 | D09-D11 | TESTES", "CAPACIDADE / SUPORTABILIDADE", "CURVAS, PARES E RETAGUARDA", "07_INSTRUMENTACAO"),
        ("05 | D12 | FECHAMENTO", "EVIDENCIAS E EXCECOES", "MODELO, AJUSTES, REVISAO", "12_LEGENDA"),
    )
    x0, stage_y0, stage_y1, stage_w, gap = 18.0, 232.0, 260.0, 70.0, 8.5
    for index, (heading, detail_1, detail_2, heading_layer) in enumerate(stages):
        left = x0 + index * (stage_w + gap)
        add_rect(layout, left, stage_y0, left + stage_w, stage_y1, "12_LEGENDA")
        centered(layout, heading, (left + stage_w / 2, 254.5), 1.02, heading_layer)
        centered(layout, detail_1, (left + stage_w / 2, 246.5), 0.94, "02_TEXTO")
        centered(layout, detail_2, (left + stage_w / 2, 239.0), 0.94, "02_TEXTO")
        if index < len(stages) - 1:
            arrow(layout, (left + stage_w, 246.0), (left + stage_w + gap, 246.0), "03_COTAS")

    column_keys = ("id", "etapa", "entrada_ou_verificacao", "evidencia", "status")
    headers = {
        "id": "ID",
        "etapa": "GRUPO",
        "entrada_ou_verificacao": "DADO OU VERIFICACAO NECESSARIA",
        "evidencia": "FONTE / REGISTRO",
        "status": "STATUS",
    }
    table_rows = [headers, *rows]
    widths = (25.0, 55.0, 190.0, 76.0, 38.0)
    x_left, y_top, row_h = 18.0, 226.0, 9.8
    y_bottom = y_top - len(table_rows) * row_h
    x_right = x_left + sum(widths)
    add_rect(layout, x_left, y_bottom, x_right, y_top, "12_LEGENDA")
    for row_index in range(1, len(table_rows)):
        y = y_top - row_h * row_index
        line(layout, (x_left, y), (x_right, y), "12_LEGENDA")
    cursor = x_left
    for width in widths[:-1]:
        cursor += width
        line(layout, (cursor, y_bottom), (cursor, y_top), "12_LEGENDA")

    group_layers = {"ENTRADA": "06_COMANDO", "CALCULO": "05_POTENCIA", "REVISAO": "12_LEGENDA"}
    for row_index, row in enumerate(table_rows):
        center_y = y_top - row_h * row_index - row_h / 2
        cursor = x_left
        for key, width in zip(column_keys, widths):
            value = row[key]
            if row_index == 0:
                centered(layout, value, (cursor + width / 2, center_y), 0.98, "12_LEGENDA")
            elif key in {"entrada_ou_verificacao", "evidencia"}:
                add_text(
                    layout,
                    value,
                    (cursor + 1.6, center_y),
                    0.98,
                    layer="02_TEXTO",
                    align=TextEntityAlignment.MIDDLE_LEFT,
                )
            elif key == "id":
                centered(layout, value, (cursor + width / 2, center_y), 1.08, group_layers[row["etapa"]])
            else:
                centered(layout, value, (cursor + width / 2, center_y), 0.98, "12_LEGENDA")
            cursor += width


DRAWERS = {
    1: draw_layout_industrial,
    2: draw_force,
    3: draw_lighting,
    4: draw_routes,
    5: draw_unifilar,
    6: draw_load_table,
    7: draw_details,
}


def generate(root: Path) -> list[Path]:
    config = load_config(root)
    source_dir = root / PROJECT_SLUG / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for spec in SHEETS:
        doc, layout = create_sheet(config, spec)
        if spec.number == 8:
            draw_protection_coordination(layout, read_protection_pairs(root))
        elif spec.number == 9:
            draw_coordination_data_plan(layout, read_coordination_inputs(root))
        else:
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
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositorio")
    return parser.parse_args()


def main() -> int:
    generate(parse_args().root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
