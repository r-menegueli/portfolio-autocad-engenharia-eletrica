"""Gera as seis pranchas DXF do Projeto 12 (Grupo Moto-Gerador 250 kVA com QTA e USCA) de forma deterministica."""

from __future__ import annotations

import argparse
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
    TEXT_STYLE,
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


PROJECT_SLUG = "12-grupo-gerador-qta"
PROJECT_DATE = "2026-09-25"
REVISION = "00"


@dataclass(frozen=True)
class SheetSpec:
    number: int
    filename: str
    title: str
    subtitle: str
    notes: str
    legend: str
    scale: str = "S/ESC."


SHEETS = (
    SheetSpec(
        1,
        "01_diagrama_unifilar_qta.dxf",
        "DIAGRAMA UNIFILAR GERAL - GMG E QTA",
        "Grupo moto-gerador diesel 250 kVA / 380-220 V e QTA em transicao aberta",
        "Comutacao automatica Rede/Gerador em transicao aberta (Break-Before-Make).\\P"
        "Duplo intertravamento (mecanico e eletrico) entre os contatores K1 e K2 de 400 A.\\P"
        "Alimentacao prioritaria do Quadro de Cargas Essenciais (QCE) em 380/220 V.",
        "GMG: grupo moto-gerador | QTA: quadro transf. auto. | USCA: unid. sup. CA | QCE: cargas essenciais",
    ),
    SheetSpec(
        2,
        "02_diagrama_trifilar_potencia.dxf",
        "DIAGRAMA TRIFILAR DE POTENCIA DO QTA",
        "Esquema trifilar 3F+N+PE, comutacao tetrapolar e circuitos auxiliares",
        "Manobra tetrapolar (3 fases + neutro) isolando galvanicamente as duas fontes.\\P"
        "Barramento principal em cobre eletrolitico 40x5 mm (500 A) e neutro/PE 30x5 mm.\\P"
        "Derivacao antes de K1 para carregador flutuante 12 Vcc e pre-aquecimento do motor.",
        "L1/L2/L3/N: rede | U/V/W/N: gerador | K1/K2: contatores 400A | TC: transfo. corrente 400/5A",
    ),
    SheetSpec(
        3,
        "03_diagrama_funcional_comando.dxf",
        "DIAGRAMA FUNCIONAL DE COMANDO E USCA",
        "Logica de partida, sensoriamento de tensao e intertravamento eletrico",
        "USCA alimentada em 12 Vcc pela bateria de partida com carregador inteligente.\\P"
        "Monitoramento trifasico de subtensao (<85%), sobretensao (>110%) e falta de fase.\\P"
        "Contatos auxiliares NF cruzados em serie com as bobinas de K1 e K2.",
        "USCA: controlador digital | FUEL: solenoide diesel | CRANK: motor partida | NF/NA: contatos",
    ),
    SheetSpec(
        4,
        "04_regua_bornes_interligacao.dxf",
        "REGUA DE BORNES E INTERLIGACAO DE CAMPO",
        "Mapeamento de bornes de potencia (X1..X3) e controle/supervisao (XC1/XC2)",
        "Bornes de potencia dimensionados para duplos condutores 2x120 mm2 EPR por fase.\\P"
        "Separacao fisica em eletrodutos distintos para cabos de potencia e controle.\\P"
        "Sinais de telesupervisao livres de potencial (contatos secos) para CLP/BMS.",
        "X1: entrada rede | X2: entrada GMG | X3: saida QCE | XC1: motor diesel | XC2: supervisorio",
    ),
    SheetSpec(
        5,
        "05_layout_painel_qta.dxf",
        "LAYOUT DO PAINEL DO QTA",
        "Vista externa da porta frontal e layout da placa de montagem (1800x800x400 mm)",
        "Painel autoportante em chapa de aco 14 MSG, grau de protecao IP54, cor RAL 7032.\\P"
        "Porta frontal com IHM da USCA, sinaleiros LED 22 mm, seletora e emergencia.\\P"
        "Placa de montagem com intertravamento mecanico rigido entre K1 e K2.",
        "IHM: interface USCA | H1..H6: sinaleiros LED | S0: emergencia | S1: seletora Auto-0-Man",
        "1:20",
    ),
    SheetSpec(
        6,
        "06_planta_instalacao_gmg.dxf",
        "PLANTA DE INSTALACAO E DETALHES DO GMG",
        "Arranjo fisico da sala do gerador, atenuacao acustica, escape e contencao",
        "Base de concreto isolada com 6 amortecedores elastomericos antivibratorios.\\P"
        "Cabine silenciada 75 dB(A) com venezianas de admissao e descarga atenuadas.\\P"
        "Tanque integrado de 250 L sobre bacia de contencao estanque para 297 L (110%).",
        "GMG-01: 250 kVA | ESC-01: silencioso hospitalar | TQ-01: tanque 250L | VIB: amortecedores",
        "1:50",
    ),
)


# --- Funcoes utilitarias de desenho ---

def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def centered(layout, value: str, point: tuple[float, float], height: float = 1.6, layer: str = "02_TEXTO", style: str = TEXT_STYLE) -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.MIDDLE_CENTER, style=style)


def left_text(layout, value: str, point: tuple[float, float], height: float = 1.5, layer: str = "02_TEXTO", style: str = TEXT_STYLE) -> None:
    add_text(layout, value, point, height, layer=layer, align=TextEntityAlignment.LEFT, style=style)


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


def box(layout, x0: float, y0: float, x1: float, y1: float, tag: str, detail: str = "", layer: str = "04_EQUIPAMENTOS") -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    xm = (x0 + x1) / 2
    ym = (y0 + y1) / 2
    if detail:
        centered(layout, tag, (xm, ym + 1.8), 1.45, layer, style=TITLE_STYLE)
        centered(layout, detail, (xm, ym - 2.0), 1.0, "02_TEXTO")
    else:
        centered(layout, tag, (xm, ym), 1.45, layer, style=TITLE_STYLE)


def panel_box(layout, x0: float, y0: float, x1: float, y1: float, title: str, subtitle: str = "", layer: str = "04_EQUIPAMENTOS") -> None:
    """Desenha um quadro/painel com cabecalho fixo no topo para nao sobrepor itens internos."""
    add_rect(layout, x0, y0, x1, y1, layer)
    xm = (x0 + x1) / 2
    if subtitle:
        centered(layout, title, (xm, y1 - 4.5), 1.45, layer, style=TITLE_STYLE)
        centered(layout, subtitle, (xm, y1 - 8.2), 1.05, "02_TEXTO")
        line(layout, (x0, y1 - 11.0), (x1, y1 - 11.0), layer)
    else:
        centered(layout, title, (xm, y1 - 5.0), 1.45, layer, style=TITLE_STYLE)
        line(layout, (x0, y1 - 8.5), (x1, y1 - 8.5), layer)


def ground_symbol(layout, x: float, y: float, layer: str = "05_POTENCIA") -> None:
    line(layout, (x, y), (x, y - 3.5), layer)
    line(layout, (x - 3.5, y - 3.5), (x + 3.5, y - 3.5), layer)
    line(layout, (x - 2.2, y - 5.2), (x + 2.2, y - 5.2), layer)
    line(layout, (x - 1.0, y - 6.8), (x + 1.0, y - 6.8), layer)


def generator_symbol(layout, x: float, y: float, tag: str = "GMG-01", detail: str = "250 kVA") -> None:
    r = 7.5
    layout.add_circle((x, y), r, dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "G", (x, y + 1.8), 2.5, "05_POTENCIA", style=TITLE_STYLE)
    centered(layout, "3~", (x, y - 2.5), 1.6, "05_POTENCIA")
    left_text(layout, f"{tag} - {detail}", (x + 9.5, y + 3.0), 1.35, "04_EQUIPAMENTOS", style=TITLE_STYLE)
    left_text(layout, "380/220 V - 60 Hz", (x + 9.5, y - 0.5), 1.05, "02_TEXTO")
    left_text(layout, "Diesel 1800 rpm (Standby)", (x + 9.5, y - 3.8), 1.0, "02_TEXTO")


# --- Funcoes de montagem do carimbo e template ---

def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("EMISSAO INICIAL DO PROJETO 12", 316), ("R.E.M.M.", 381)):
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
        "PRANCHA": f"{spec.number:02d}/06",
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
    metadata["PORTFOLIO_SHEET"] = f"{spec.number:02d}/06"
    define_title_block(doc)
    define_symbols(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    centered(layout, spec.title, (210, 277), 4.2, "02_TEXTO", style=TITLE_STYLE)
    centered(layout, spec.subtitle, (210, 270.8), 2.0, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


# --- Prancha 01: Diagrama Unifilar Geral do QTA ---

def draw_sheet_01(layout) -> None:
    # Coluna 1: Fonte 1 Rede Concessionaria (X = 52) e Fonte 2 GMG (X = 122)
    add_rect(layout, 28, 102, 182, 256, "11_ARQUITETURA")
    centered(layout, "QTA - QUADRO DE TRANSFERENCIA AUTOMATICA", (105, 250), 1.55, "04_EQUIPAMENTOS", style=TITLE_STYLE)

    # Fonte 1: Rede
    centered(layout, "FONTE 1: REDE", (55, 240), 1.35, "05_POTENCIA", style=TITLE_STYLE)
    centered(layout, "380/220 V - QGBT", (55, 235), 1.0, "02_TEXTO")
    line(layout, (55, 232), (55, 214), "05_POTENCIA")
    box(layout, 41, 198, 69, 214, "DJ-REDE", "400 A / 25 kA", "05_POTENCIA")
    line(layout, (55, 198), (55, 182), "05_POTENCIA")
    layout.add_circle((55, 182), 3.2, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    left_text(layout, "TC-REDE 400/5A", (60, 181), 0.95, "07_INSTRUMENTACAO")
    line(layout, (55, 178.8), (55, 162), "05_POTENCIA")
    box(layout, 41, 144, 69, 162, "K1 (REDE)", "Contator 400 A", "05_POTENCIA")
    line(layout, (55, 144), (55, 122), "05_POTENCIA")

    # Fonte 2: GMG 250 kVA
    generator_symbol(layout, 125, 234, "GMG-01", "250 kVA")
    ground_symbol(layout, 112, 226, "05_POTENCIA")
    line(layout, (117.5, 234), (112, 234), "05_POTENCIA")
    line(layout, (112, 234), (112, 226), "05_POTENCIA")
    line(layout, (125, 226.5), (125, 214), "05_POTENCIA")
    box(layout, 111, 198, 139, 214, "DJ-GER", "400 A / 16 kA", "05_POTENCIA")
    line(layout, (125, 198), (125, 182), "05_POTENCIA")
    layout.add_circle((125, 182), 3.2, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    left_text(layout, "TC-GER 400/5A", (130, 181), 0.95, "07_INSTRUMENTACAO")
    line(layout, (125, 178.8), (125, 162), "05_POTENCIA")
    box(layout, 111, 144, 139, 162, "K2 (GMG)", "Contator 400 A", "05_POTENCIA")
    line(layout, (125, 144), (125, 122), "05_POTENCIA")

    # Simbolo de Intertravamento Mecanico e Eletrico entre K1 e K2
    line(layout, (69, 153), (111, 153), "06_COMANDO")
    box(layout, 81, 148, 99, 158, "INT-MEC", "Mecan./Eletr.", "06_COMANDO")

    # Modulo USCA supervisionando K1 e K2
    box(layout, 72, 166, 108, 176, "USCA-01", "Controlador", "06_COMANDO")
    line(layout, (72, 171), (55, 171), "06_COMANDO")
    line(layout, (108, 171), (125, 171), "06_COMANDO")

    # Uniao das saidas de K1 e K2 -> Barramento Comum de Emergencia
    line(layout, (55, 122), (125, 122), "05_POTENCIA")
    centered(layout, "SAIDA COMUM COMUTADA (380/220 V)", (90, 115), 1.15, "05_POTENCIA", style=TITLE_STYLE)
    line(layout, (90, 122), (90, 106), "05_POTENCIA")

    # Quadro de Dados Tecnicos (Centro: X = 192 a 266)
    panel_box(layout, 190, 118, 266, 244, "DADOS DO SISTEMA", "", "02_TEXTO")
    specs = [
        "Potencia Standby: 250 kVA",
        "Potencia Ativa: 200 kW",
        "Tensao Nominal: 380/220 V",
        "Corrente Nominal: 379,8 A",
        "Rotacao: 1800 rpm (60 Hz)",
        "Icc Rede: 25,0 kA",
        "Icc Gerador: 1,14 kA",
        "Transicao: Aberta (BBM)",
        "Tempo Partida: <= 12 s",
        "Tanque Diesel: 250 L",
        "Autonomia 75%: 7,5 h",
        "Esquema Terra: TN-S",
    ]
    for idx, text_line in enumerate(specs):
        left_text(layout, text_line, (194, 228 - idx * 9.2), 1.05, "02_TEXTO")

    # Quadro de Cargas Essenciais - QCE (Direita: X = 274 a 402)
    add_rect(layout, 274, 102, 402, 256, "04_EQUIPAMENTOS")
    centered(layout, "QCE - QUADRO DE CARGAS ESSENCIAIS", (338, 250), 1.45, "04_EQUIPAMENTOS", style=TITLE_STYLE)

    # Ligacao da saida do QTA ao Barramento do QCE
    orthogonal(layout, [(90, 106), (292, 106), (292, 235)], "05_POTENCIA")
    left_text(layout, "BARRAMENTO PRIORITARIO Cu 40x5 mm (500 A)", (284, 239), 1.1, "05_POTENCIA", style=TITLE_STYLE)

    # DPS no barramento do QCE
    line(layout, (292, 228), (314, 228), "05_POTENCIA")
    box(layout, 314, 220, 350, 235, "DPS-QTA", "Cl. II 20/45 kA", "05_POTENCIA")
    line(layout, (350, 228), (362, 228), "05_POTENCIA")
    ground_symbol(layout, 362, 228, "05_POTENCIA")

    # 5 Circuitos Alimentadores Essenciais
    feeders = [
        (204, "DJ 63 A", "AL-01", "Iluminacao Emergencia e Rotas Fuga"),
        (182, "DJ 125 A", "AL-02", "Bombas de Incendio e Pressurizacao"),
        (160, "DJ 100 A", "AL-03", "UPS / Sala de Servidores e TI"),
        (138, "DJ 80 A", "AL-04", "Painel de Utilidades e Automacao"),
        (116, "DJ 100 A", "AL-05", "Reserva Tecnica Prioritaria"),
    ]
    for yf, dj_label, al_tag, desc in feeders:
        line(layout, (292, yf), (314, yf), "05_POTENCIA")
        box(layout, 314, yf - 6.5, 344, yf + 6.5, dj_label, "", "05_POTENCIA")
        arrow(layout, (344, yf), (362, yf), "08_CABOS")
        left_text(layout, al_tag, (365, yf + 1.2), 1.1, "04_EQUIPAMENTOS", style=TITLE_STYLE)
        left_text(layout, desc, (365, yf - 2.8), 0.9, "02_TEXTO")


# --- Prancha 02: Diagrama Trifilar de Potencia do QTA ---

def draw_sheet_02(layout) -> None:
    # 1. Coluna Rede Trifilar (Esquerda: X = 28 a 146)
    add_rect(layout, 28, 102, 146, 256, "11_ARQUITETURA")
    centered(layout, "FONTE 1: REDE (3F+N)", (87, 250), 1.45, "05_POTENCIA", style=TITLE_STYLE)

    phases_r = [("L1", 46), ("L2", 68), ("L3", 90), ("N", 112)]
    for label, x_p in phases_r:
        centered(layout, label, (x_p, 241), 1.2, "05_POTENCIA", style=TITLE_STYLE)
        line(layout, (x_p, 238), (x_p, 126), "05_POTENCIA")
        if label != "N":
            layout.add_circle((x_p, 192), 2.5, dxfattribs={"layer": "07_INSTRUMENTACAO"})

    box(layout, 38, 206, 100, 224, "DJ-REDE (3P)", "400 A / 25 kA", "05_POTENCIA")
    left_text(layout, "TC-R1..R3", (102, 191), 0.95, "07_INSTRUMENTACAO")
    box(layout, 38, 152, 122, 174, "K1 - CONTATOR REDE (4P)", "400 A - AC-3 (3F+N)", "05_POTENCIA")

    # 2. Coluna Gerador Trifilar (Centro: X = 154 a 272)
    add_rect(layout, 154, 102, 272, 256, "11_ARQUITETURA")
    centered(layout, "FONTE 2: GERADOR (3F+N)", (213, 250), 1.45, "05_POTENCIA", style=TITLE_STYLE)

    phases_g = [("U", 172), ("V", 194), ("W", 216), ("N", 238)]
    for label, x_p in phases_g:
        centered(layout, label, (x_p, 241), 1.2, "05_POTENCIA", style=TITLE_STYLE)
        line(layout, (x_p, 238), (x_p, 126), "05_POTENCIA")
        if label != "N":
            layout.add_circle((x_p, 192), 2.5, dxfattribs={"layer": "07_INSTRUMENTACAO"})

    box(layout, 164, 206, 226, 224, "DJ-GER (3P)", "400 A / 16 kA", "05_POTENCIA")
    left_text(layout, "TC-G1..G3", (228, 191), 0.95, "07_INSTRUMENTACAO")
    box(layout, 164, 152, 248, 174, "K2 - CONTATOR GMG (4P)", "400 A - AC-3 (3F+N)", "05_POTENCIA")

    # Barramento Horizontal Inferior Unificado (L1, L2, L3, N, PE)
    bus_y = [("L1", 122), ("L2", 117), ("L3", 112), ("N", 107)]
    for idx, (b_lbl, yb) in enumerate(bus_y):
        xr = phases_r[idx][1]
        xg = phases_g[idx][1]
        line(layout, (xr, 126), (xr, yb), "05_POTENCIA")
        line(layout, (xg, 126), (xg, yb), "05_POTENCIA")
        line(layout, (40, yb), (268, yb), "05_POTENCIA")
        left_text(layout, f"Barra {b_lbl}", (248, yb + 0.8), 0.85, "05_POTENCIA")

    # 3. Circuitos Auxiliares e Barramento PE (Direita: X = 280 a 402)
    panel_box(layout, 280, 102, 402, 256, "CIRCUITOS AUXILIARES E TERRA", "Derivados antes de K1 (220 Vca)", "06_COMANDO")

    box(layout, 292, 214, 390, 234, "FUSIVEIS F1..F3 (2 A)", "Sensoriamento Tensao Rede USCA", "06_COMANDO")
    box(layout, 292, 188, 390, 208, "FUSIVEIS F4..F6 (2 A)", "Sensoriamento Tensao GMG USCA", "06_COMANDO")
    box(layout, 292, 162, 390, 182, "DISJUNTOR F7 (10 A - 220V)", "Pre-aquecedor Bloco Motor (1000 W)", "05_POTENCIA")
    box(layout, 292, 136, 390, 156, "DISJUNTOR F8 (6 A - 220V)", "Carregador Flutuante 12 Vcc / 5 A", "06_COMANDO")
    box(layout, 292, 108, 390, 128, "BARRAMENTO PE (Cu 30x5mm)", "Equipotencializacao Carcaca e BEP", "05_POTENCIA")


# --- Prancha 03: Diagrama Funcional de Comando e USCA ---

def draw_sheet_03(layout) -> None:
    # 1. Entradas AC e Sensores do Motor (Esquerda: X = 28 a 148)
    panel_box(layout, 28, 102, 148, 256, "ENTRADAS AC E SENSORES", "Sinais p/ USCA-01", "07_INSTRUMENTACAO")

    inputs = [
        ("REDE V1/V2/V3/VN", "Monitor Tensao 380/220V"),
        ("GMG U/V/W/N", "Monitor Alternador 380V"),
        ("TCs REDE E GMG", "Medicao Corrente 400/5A"),
        ("DI-1: EMERGENCIA (S0)", "Contato NF Duplo Canal"),
        ("DI-2: PRESSOSTATO OLEO", "Corte se P < 1,2 bar (NF)"),
        ("DI-3: TERMOSTATO AGUA", "Corte se T > 103 C (NF)"),
        ("DI-4: BOIA COMBUSTIVEL", "Alarme Nivel < 20% (NA)"),
    ]
    for idx, (tag_in, desc_in) in enumerate(inputs):
        yi = 226 - idx * 17.5
        box(layout, 36, yi - 6.5, 136, yi + 6.5, tag_in, desc_in, "07_INSTRUMENTACAO")
        arrow(layout, (136, yi), (156, yi), "06_COMANDO")

    # 2. Controlador Microprocessado USCA (Centro: X = 156 a 272)
    panel_box(layout, 156, 102, 272, 256, "CONTROLADOR USCA-01", "Unidade de Supervisao CA", "06_COMANDO")

    usca_params = [
        "Alimentacao: 12 Vcc (8 a 35 Vcc)",
        "Subtensao Rede: < 323 V (85%)",
        "Sobretensao Rede: > 418 V (110%)",
        "Subfrequencia GMG: < 57,0 Hz",
        "Sobrefrequencia GMG: > 63,0 Hz",
        "Retardo Falha Rede: 3,0 s",
        "Tentativas Partida: 3 x 5,0 s",
        "Estabilizacao GMG: 5,0 s",
        "Tempo Morto (BBM): 1,5 s",
        "Retorno de Rede: 120 s",
        "Cooldown (Arrefec.): 180 s",
        "Comunicacao: RS-485 Modbus RTU",
    ]
    for idx, param in enumerate(usca_params):
        left_text(layout, param, (162, 232 - idx * 10.2), 1.0, "02_TEXTO")

    # 3. Saidas de Comando e Intertravamento Cruzado (Direita: X = 280 a 402)
    panel_box(layout, 280, 102, 402, 256, "SAIDAS E INTERTRAVAMENTO", "Partida 12Vcc e Comutacao 220Vca", "06_COMANDO")

    outputs = [
        (224, "DO-1: SOLENOIDE FUEL", "Valvula Combustivel 12 Vcc"),
        (202, "DO-2: MOTOR ARRANQUE", "Relé Auxiliar Partida 12 Vcc"),
        (176, "DO-3: FECHA REDE (K1)", "Em serie c/ contato NF de K2"),
        (152, "DO-4: FECHA GMG (K2)", "Em serie c/ contato NF de K1"),
        (128, "DO-5: ALARME / FALHA", "Sirene e Telesinalizacao"),
    ]
    for yo, tag_out, desc_out in outputs:
        arrow(layout, (272, yo), (288, yo), "06_COMANDO")
        box(layout, 288, yo - 8.0, 394, yo + 8.0, tag_out, desc_out, "06_COMANDO")

    left_text(layout, "Nota: K1 e K2 possuem contatos NF cruzados", (286, 111), 0.95, "02_TEXTO")
    left_text(layout, "impedindo energizacao simultanea das bobinas.", (286, 106), 0.95, "02_TEXTO")


# --- Prancha 04: Regua de Bornes e Interligacao de Campo ---

def draw_sheet_04(layout) -> None:
    # 1. Reguas de Potencia X1, X2 e X3 (Esquerda: X = 28 a 146)
    panel_box(layout, 28, 102, 146, 256, "BORNES DE POTENCIA", "Secao 2x120 mm2 EPR / Fase", "09_BORNES")

    box(layout, 36, 204, 138, 234, "REGUA X1 - ENTRADA REDE", "Bornes: R | S | T | N | PE", "09_BORNES")
    left_text(layout, "<- Cabo CAB-REDE-QTA (do QGBT)", (38, 198), 0.95, "08_CABOS")

    box(layout, 36, 158, 138, 188, "REGUA X2 - ENTRADA GMG", "Bornes: U | V | W | N | PE", "09_BORNES")
    left_text(layout, "<- Cabo CAB-GMG-QTA (do Alternador)", (38, 152), 0.95, "08_CABOS")

    box(layout, 36, 112, 138, 142, "REGUA X3 - SAIDA CARGA", "Bornes: L1 | L2 | L3 | N | PE", "09_BORNES")
    left_text(layout, "-> Cabo CAB-QTA-QCE (p/ Quadro QCE)", (38, 106), 0.95, "08_CABOS")

    # 2. Regua de Comando XC1 - Interface Motor Diesel (Centro: X = 154 a 274)
    panel_box(layout, 154, 102, 274, 256, "REGUA XC1 - MOTOR GMG", "Interligacao QTA <-> Cabine GMG", "09_BORNES")

    xc1_pins = [
        ("XC1:01", "+12 Vcc Bateria de Partida"),
        ("XC1:02", "-12 Vcc Negativo / Massa Comum"),
        ("XC1:03", "Comando Solenoide Combustivel (53)"),
        ("XC1:04", "Comando Motor de Arranque (50)"),
        ("XC1:05", "Sinal Alternador Carga Bateria (D+)"),
        ("XC1:06", "Sensor Baixa Pressao de Oleo"),
        ("XC1:07", "Sensor Alta Temperatura Agua"),
        ("XC1:08", "Sensor Nivel Combustivel Tanque"),
        ("XC1:09", "Fase 220V Pre-Aquecedor Bloco"),
        ("XC1:10", "Neutro 220V Pre-Aquecedor Bloco"),
    ]
    for idx, (pin, desc) in enumerate(xc1_pins):
        yp = 232 - idx * 12.8
        layout.add_circle((164, yp), 1.6, dxfattribs={"layer": "09_BORNES"})
        left_text(layout, f"{pin} - {desc}", (168, yp - 1.0), 0.95, "02_TEXTO")

    # 3. Regua de Comando XC2 - Supervisorio e Seguranca (Direita: X = 282 a 402)
    panel_box(layout, 282, 102, 402, 256, "REGUA XC2 - SUPERVISORIO", "Sinais Remotos e Emergencia", "09_BORNES")

    xc2_pins = [
        ("XC2:11", "Botoeira Emergencia Externa CH1"),
        ("XC2:12", "Retorno Emergencia Externa CH1"),
        ("XC2:13", "Botoeira Emergencia Externa CH2"),
        ("XC2:14", "Retorno Emergencia Externa CH2"),
        ("XC2:15", "Entrada Partida Remota (Contato NA)"),
        ("XC2:16", "Saida Status QTA em Automatico"),
        ("XC2:17", "Saida Status GMG c/ Carga (K2 ON)"),
        ("XC2:18", "Saida Alarme Falha Geral (Comum/NA)"),
    ]
    for idx, (pin, desc) in enumerate(xc2_pins):
        yp = 232 - idx * 14.5
        layout.add_circle((292, yp), 1.6, dxfattribs={"layer": "09_BORNES"})
        left_text(layout, f"{pin} - {desc}", (296, yp - 1.0), 0.95, "02_TEXTO")

    box(layout, 290, 108, 394, 122, "CABO CAB-SUP-REM (6x1,0 mm2)", "Interligacao c/ CLP / BMS Central", "08_CABOS")


# --- Prancha 05: Layout do Painel do QTA ---

def draw_sheet_05(layout) -> None:
    # 1. Vista Externa da Porta Frontal (Esquerda: X = 32 a 196)
    panel_box(layout, 32, 102, 196, 256, "VISTA FRONTAL (PORTA EXTERNA)", "Painel Autoportante IP54 - 1800x800 mm", "04_EQUIPAMENTOS")

    # Contorno da porta do painel
    add_rect(layout, 56, 110, 172, 238, "04_EQUIPAMENTOS")

    # Modulo USCA na porta
    box(layout, 82, 206, 146, 228, "IHM - USCA-01", "Display LCD e Teclas", "06_COMANDO")

    # Sinaleiros LED H1 a H6
    leds = [
        (72, 192, "H1", "Painel ON"),
        (114, 192, "H2", "Rede OK"),
        (154, 192, "H3", "GMG OK"),
        (72, 176, "H4", "K1 Rede"),
        (114, 176, "H5", "K2 GMG"),
        (154, 176, "H6", "Falha"),
    ]
    for xl, yl, h_tag, h_desc in leds:
        layout.add_circle((xl, yl), 2.5, dxfattribs={"layer": "06_COMANDO"})
        left_text(layout, f"{h_tag}:{h_desc}", (xl - 8, yl - 6.0), 0.85, "02_TEXTO")

    # Seletora S1 e Botao de Emergencia S0
    box(layout, 70, 148, 108, 162, "S1: MODO", "Man-0-Auto", "06_COMANDO")
    box(layout, 120, 148, 158, 162, "S0: EMERG.", "Cogumelo", "06_COMANDO")

    # Veneziana de ventilacao na porta
    box(layout, 84, 118, 144, 134, "GRELHA c/ FILTRO", "Ventilacao IP54", "11_ARQUITETURA")

    # 2. Vista da Placa de Montagem Interna (Direita: X = 212 a 402)
    panel_box(layout, 212, 102, 402, 256, "PLACA DE MONTAGEM INTERNA", "Chapa 14 MSG Laranja RAL 2004 - 1700x700 mm", "04_EQUIPAMENTOS")

    # Disjuntores de Entrada no topo
    box(layout, 226, 214, 298, 236, "DJ-REDE (400 A)", "Entrada Concessionaria", "05_POTENCIA")
    box(layout, 316, 214, 388, 236, "DJ-GER (400 A)", "Entrada Gerador", "05_POTENCIA")

    # TCs de Medicao
    box(layout, 234, 196, 290, 208, "TC-REDE (3x 400/5A)", "", "07_INSTRUMENTACAO")
    box(layout, 324, 196, 380, 208, "TC-GER (3x 400/5A)", "", "07_INSTRUMENTACAO")

    # Contatores K1 e K2 com Intertravamento Mecanico
    box(layout, 226, 164, 292, 190, "CONTATOR K1", "400 A - Rede", "05_POTENCIA")
    box(layout, 322, 164, 388, 190, "CONTATOR K2", "400 A - GMG", "05_POTENCIA")
    box(layout, 292, 171, 322, 183, "INT-MEC", "Trava", "06_COMANDO")

    # Trilho DIN: Fusiveis, Carregador e DPS
    box(layout, 226, 140, 276, 156, "FUSIVEIS F1..F8", "Comando e Prot.", "06_COMANDO")
    box(layout, 282, 140, 338, 156, "CARREGADOR BAT.", "12 Vcc / 5 A", "06_COMANDO")
    box(layout, 344, 140, 388, 156, "DPS CL. II", "20/45 kA", "05_POTENCIA")

    # Regua de Bornes e Barramento PE na base
    box(layout, 226, 120, 388, 134, "REGUAS DE BORNES: X1 | X2 | X3 | XC1 | XC2", "Potencia e Controle", "09_BORNES")
    box(layout, 226, 106, 388, 116, "BARRAMENTO DE COBRE PE (30x5 mm)", "Aterramento Geral do QTA", "05_POTENCIA")


# --- Prancha 06: Planta de Instalacao e Detalhes do GMG ---

def draw_sheet_06(layout) -> None:
    # 1. Planta Baixa da Sala do GMG (Esquerda: X = 28 a 250)
    panel_box(layout, 28, 102, 250, 256, "PLANTA BAIXA - SALA DO GERADOR", "Dimensoes Internas: 6,50 x 4,00 m (Escala 1:50)", "11_ARQUITETURA")

    # Paredes da sala (alvenaria acústica)
    add_rect(layout, 42, 120, 236, 232, "11_ARQUITETURA")
    add_rect(layout, 46, 124, 232, 228, "11_ARQUITETURA")

    # Veneziana de Admissao de Ar Frio (Direita) e Atenuador de Descarga (Esquerda)
    box(layout, 218, 146, 236, 206, "VENEZIANA", "Admissao Ar", "11_ARQUITETURA")
    box(layout, 42, 146, 62, 206, "ATENUADOR", "Descarga Ar", "11_ARQUITETURA")

    # Base de concreto armado com amortecedores e Bacia de Contencao
    add_rect(layout, 82, 144, 198, 208, "11_ARQUITETURA")
    centered(layout, "BACIA CONTENCAO DIESEL (297 L - 110%)", (140, 203), 0.95, "11_ARQUITETURA")

    # Cabine do GMG-01 250 kVA
    box(layout, 92, 152, 188, 196, "GMG-01 - 250 kVA / 380-220 V", "Cabine Silenciada 75 dB(A) + Tanque 250 L", "04_EQUIPAMENTOS")

    # 6 Amortecedores vibratorios
    for xv in (98, 140, 182):
        layout.add_circle((xv, 150), 2.0, dxfattribs={"layer": "04_EQUIPAMENTOS"})
        layout.add_circle((xv, 198), 2.0, dxfattribs={"layer": "04_EQUIPAMENTOS"})

    # Painel QTA-01 na parede superior e Eletrocalha
    box(layout, 114, 214, 166, 226, "PAINEL QTA-01", "1800x800x400 mm", "04_EQUIPAMENTOS")
    line(layout, (140, 196), (140, 214), "10_ELETROCALHAS")
    left_text(layout, "Eletrocalha 200x100", (143, 205), 0.9, "10_ELETROCALHAS")

    # Porta Corta-Fogo Acustica e Extintores na parte inferior
    line(layout, (90, 120), (125, 120), "06_COMANDO")
    centered(layout, "PORTA ACUSTICA P-90 (ABRE P/ FORA)", (108, 114), 0.95, "11_ARQUITETURA")
    layout.add_circle((60, 132), 3.0, dxfattribs={"layer": "06_COMANDO"})
    left_text(layout, "EXT. PQS/CO2", (65, 131), 0.9, "06_COMANDO")

    # 2. Detalhe do Escape e Requisitos Normativos (Direita: X = 258 a 402)
    panel_box(layout, 258, 102, 402, 256, "ESCAPE HOSPITALAR E REQUISITOS", "Atenuacao Acustica e Gases", "04_EQUIPAMENTOS")

    # Fluxo de escape em blocos
    box(layout, 268, 214, 392, 232, "1. JUNTA EXPANSAO FLEXIVEL INOX", "Absorcao de vibracao na saida do turbo", "04_EQUIPAMENTOS")
    arrow(layout, (330, 214), (330, 204), "05_POTENCIA")
    box(layout, 268, 184, 392, 204, "2. SILENCIOSO HOSPITALAR DN 4\"", "Atenuacao de 32 dB(A) c/ dreno condensado", "04_EQUIPAMENTOS")
    arrow(layout, (330, 184), (330, 174), "05_POTENCIA")
    box(layout, 268, 154, 392, 174, "3. TUBULACAO ISOLADA LA DE ROCHA", "Espessura 50 mm + protecao aluminio", "04_EQUIPAMENTOS")

    reqs = [
        "- Nivel sonoro externo <= 75 dB(A) a 1,5m (NBR 10151).",
        "- Vazao de ar do radiador: 5,2 m3/s (18.720 m3/h).",
        "- Autonomia do tanque 250 L: 5,7 h (100%) / 7,6 h (75%).",
        "- Aterramento da carcaca e neutro em Cu 120 mm2 ao BEP.",
    ]
    for idx, rq in enumerate(reqs):
        left_text(layout, rq, (264, 140 - idx * 8.5), 0.92, "02_TEXTO")


DRAW_MAP = {
    1: draw_sheet_01,
    2: draw_sheet_02,
    3: draw_sheet_03,
    4: draw_sheet_04,
    5: draw_sheet_05,
    6: draw_sheet_06,
}


def build_sheet(config: dict, spec: SheetSpec, output_path: Path) -> None:
    doc, layout = create_sheet(config, spec)
    DRAW_MAP[spec.number](layout)
    prepare_deterministic_write(doc)
    doc.saveas(output_path)
    print(f"Gerado: {output_path.relative_to(ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositorio")
    parser.add_argument("--sheet", type=int, help="Gera apenas a prancha especificada (1..6)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config = load_config(root)
    source_dir = root / PROJECT_SLUG / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)

    for spec in SHEETS:
        if args.sheet and spec.number != args.sheet:
            continue
        output_path = source_dir / spec.filename
        build_sheet(config, spec, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
