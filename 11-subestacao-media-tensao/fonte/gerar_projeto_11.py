"""Gera as sete pranchas DXF do Projeto 11 (Subestacao de Media Tensao 13,8 kV / 380-220 V) de forma deterministica."""

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


PROJECT_SLUG = "11-subestacao-media-tensao"
PROJECT_DATE = "2026-11-05"
REVISION = "02"


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
        "01_diagrama_unifilar_geral.dxf",
        "DIAGRAMA UNIFILAR GERAL",
        "Subestacao abrigada 500 kVA - 13,8 kV / 380-220 V e QGBT",
        "Entrada em media tensao 13,8 kV conforme criterios da concessionaria.\\P"
        "Protecao por rele digital 50/51/50N/51N e disjuntor a vacuo 17,5 kV.\\P"
        "Transformador 500 kVA a oleo mineral Dyn1 com supervisao termica e Buchholz.",
        "MT: media tensao | DJ: disjuntor | TC: transfo. corrente | TP: transfo. potencial | DPS: prot. surto",
    ),
    SheetSpec(
        2,
        "02_planta_baixa_subestacao.dxf",
        "PLANTA BAIXA DA SUBESTACAO ABRIGADA",
        "Arranjo fisico, alvenaria, acessos e afastamentos normativos NBR 14039",
        "Dimensoes civis: 6,00 x 4,00 m externo. Portas corta-fogo P-90 abrindo para fora.\\P"
        "Piso com canaletas tecnicas para cabos de MT e BT. Ventilacao natural cruzada.\\P"
        "Bacia de contencao de oleo sob o transformador com brita n. 1 e dreno sifonado.",
        "Vermelho: equipamentos MT/BT | Cinza: alvenaria/portas | Azul: canaletas | Verde: seguranca",
        "1:50",
    ),
    SheetSpec(
        3,
        "03_cortes_detalhes_eletromecanicos.dxf",
        "CORTES E DETALHES ELETROMECANICOS",
        "Elevacoes A-A e B-B, barramentos de MT e bacia de contencao",
        "Corte A-A: percurso vertical de cabos, muflas 15 kV, chave seccionadora e disjuntor.\\P"
        "Corte B-B: cubiculo do transformador, bacia de contencao e barramento flexivel de BT.\\P"
        "Afastamentos de seguranca conforme ABNT NBR 14039 e NR-10.",
        "Isoladores epoxi 17,5 kV | Muflas termocontrateis | Grelha metalica com brita | Passantes",
        "1:50",
    ),
    SheetSpec(
        4,
        "04_diagrama_funcional_protecao.dxf",
        "DIAGRAMA FUNCIONAL DE PROTECAO E COMANDO",
        "Esquema AC/DC do rele digital, logica de trip e intertravamentos",
        "Rele microprocessado de sobrecorrente alimentado em 125 Vcc com banco auxiliar.\\P"
        "Trip atuando na bobina de abertura (BA) com contato auxiliar 52a do disjuntor.\\P"
        "Intertravamento eletrico com termometro do oleo (49) e rele Buchholz (63).",
        "50/51: sobrecorrente fase | 50N/51N: sobrecorrente neutro | BA: bobina abertura | X-PROT: bornes",
    ),
    SheetSpec(
        5,
        "05_malha_aterramento.dxf",
        "MALHA DE ATERRAMENTO E EQUIPOTENCIALIZACAO",
        "Arranjo conceitual; resistividade e seguranca sem estudo",
        "Anel e grade conceituais em cobre nu 70 mm2 a 0,60 m de profundidade.\\P"
        "8 hastes 5/8 pol. x 2,40 m sao premissas, sem dimensionamento do local.\\P"
        "Resistividade e dados de falta nao medidos; resistencia, GPR, toque e passo nao determinados.",
        "Cobre nu 70 mm2 | Haste 5/8\"x2,4m | Caixa de inspecao solo | BEP: barramento equipotencializacao",
        "1:75",
    ),
    SheetSpec(
        6,
        "06_spda_geral.dxf",
        "SISTEMA DE PROTECAO CONTRA DESCARGAS ATMOSFERICAS (SPDA)",
        "Arranjo ilustrativo de captores, descidas e equipotencializacao",
        "Geometria, classe de protecao e componentes ainda nao selecionados nem verificados.\\P"
        "A folha nao declara conformidade normativa nem coordena DPS.",
        "Reticula ilustrativa | Descidas propostas | Captores esquematicos | DPS a especificar",
        "1:75",
    ),
    SheetSpec(
        7,
        "07_plano_dados_estudo_aterramento.dxf",
        "PLANO DE DADOS PARA ESTUDO DE ATERRAMENTO",
        "Subestacao 13,8 kV | entradas, analises e portoes de revisao",
        "Resistividade do solo, corrente/tempo de falta e geometria final permanecem pendentes.\\P"
        "Esta folha organiza evidencias necessarias; nao calcula nem aprova a malha.\\P"
        "O valor hipotetico de solo e a estimativa aritmetica anteriores foram retirados do desenho.",
        "ENTRADAS PENDENTES | EVIDENCIA DE CAMPO/FABRICANTE | NAO E CRITERIO DE APROVACAO",
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
        centered(layout, tag, (xm, ym + 1.8), 1.5, layer, style=TITLE_STYLE)
        centered(layout, detail, (xm, ym - 2.0), 1.05, "02_TEXTO")
    else:
        centered(layout, tag, (xm, ym), 1.5, layer, style=TITLE_STYLE)


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


def transformer_symbol(layout, x: float, y: float, tag: str = "TR-01", detail: str = "500 kVA") -> None:
    r = 5.2
    c1 = (x, y + 3.4)
    c2 = (x, y - 3.4)
    layout.add_circle(c1, r, dxfattribs={"layer": "05_POTENCIA"})
    layout.add_circle(c2, r, dxfattribs={"layer": "05_POTENCIA"})
    centered(layout, "Δ", c1, 1.9, "05_POTENCIA")
    centered(layout, "Yn", c2, 1.7, "05_POTENCIA")
    left_text(layout, f"{tag} - {detail}", (x + 7.5, y + 3.5), 1.45, "04_EQUIPAMENTOS", style=TITLE_STYLE)
    left_text(layout, "13,8 kV / 380-220 V", (x + 7.5, y - 0.2), 1.1, "02_TEXTO")
    left_text(layout, "Dyn1 - Z%=4,5% (Oleo)", (x + 7.5, y - 3.6), 1.05, "02_TEXTO")


def breaker_mv_symbol(layout, x: float, y: float, tag: str, detail: str = "") -> None:
    w = 4.2
    add_rect(layout, x - w, y - w, x + w, y + w, "05_POTENCIA")
    line(layout, (x - w, y - w), (x + w, y + w), "05_POTENCIA")
    line(layout, (x - w, y + w), (x + w, y - w), "05_POTENCIA")
    left_text(layout, tag, (x + 6.5, y + 1.5), 1.35, "04_EQUIPAMENTOS", style=TITLE_STYLE)
    if detail:
        left_text(layout, detail, (x + 6.5, y - 2.0), 1.05, "02_TEXTO")


def disconnect_switch_symbol(layout, x: float, y: float, tag: str, with_ground: bool = True) -> None:
    line(layout, (x, y + 5), (x, y + 2), "05_POTENCIA")
    layout.add_circle((x, y + 2), 0.7, dxfattribs={"layer": "05_POTENCIA"})
    layout.add_circle((x, y - 3.5), 0.7, dxfattribs={"layer": "05_POTENCIA"})
    line(layout, (x, y - 3.5), (x, y - 6.5), "05_POTENCIA")
    line(layout, (x, y - 3.5), (x + 3.0, y + 1.5), "05_POTENCIA")
    left_text(layout, tag, (x + 5.5, y + 0.5), 1.25, "04_EQUIPAMENTOS")
    if with_ground:
        line(layout, (x - 1.5, y - 3.5), (x - 5.5, y - 3.5), "06_COMANDO")
        ground_symbol(layout, x - 5.5, y - 3.5, layer="06_COMANDO")


# --- Funcoes de montagem do carimbo e template ---

def add_revision_table(layout) -> None:
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        centered(layout, value, (x, 89.5), 1.7, "01_CARIMBO")
    for value, x in ((REVISION, 239), (PROJECT_DATE, 264), ("ESTUDO DE ATERRAMENTO", 316), ("R.E.M.M.", 381)):
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
    centered(layout, spec.title, (210, 277), 4.2, "02_TEXTO", style=TITLE_STYLE)
    centered(layout, spec.subtitle, (210, 270.8), 2.0, "02_TEXTO")
    add_bottom_information(layout, spec, config["portfolio"]["warning"])
    add_revision_table(layout)
    add_title_block(layout, spec, config)
    return doc, layout


# --- Desenho da Prancha 1: Diagrama Unifilar Geral ---
def draw_sheet_01(layout) -> None:
    # 1. Chegada da concessionaria em 13,8 kV (Topo Y=262 ate 234)
    centered(layout, "RAMAL DE ENTRADA CONCESSIONARIA 13,8 kV (AEREO)", (98, 260), 2.0, "05_POTENCIA", style=TITLE_STYLE)
    line(layout, (90, 256), (90, 248), "05_POTENCIA")
    # Para-raios MT
    line(layout, (90, 252), (108, 252), "05_POTENCIA")
    box(layout, 108, 248, 128, 256, "DPS-MT", "A especificar", "05_POTENCIA")
    line(layout, (128, 252), (135, 252), "05_POTENCIA")
    ground_symbol(layout, 135, 252, "05_POTENCIA")

    # Muflas terminais e descida subterranea
    box(layout, 81, 240, 99, 248, "MUFLA-01", "3x 15 kV", "04_EQUIPAMENTOS")
    line(layout, (90, 240), (90, 232), "08_CABOS")
    left_text(layout, "Cabo MT 3x(1x50 mm2) EPR 15 kV", (94, 234.5), 1.15, "08_CABOS")

    # 2. Cubiculo 1: Medicao da Concessionaria (Y=196 a 232)
    add_rect(layout, 30, 196, 178, 232, "11_ARQUITETURA")
    left_text(layout, "CUBICULO 01 - MEDICAO DA CONCESSIONARIA", (33, 228), 1.4, "11_ARQUITETURA", style=TITLE_STYLE)
    disconnect_switch_symbol(layout, 90, 221, "SEC-01 (630 A / 17,5 kV)")
    line(layout, (90, 214.5), (90, 196), "05_POTENCIA")
    # TCs e TPs de medicao
    layout.add_circle((86, 205), 2.8, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(layout, "TC-MED", (86, 205), 0.9, "07_INSTRUMENTACAO")
    layout.add_circle((94, 205), 2.8, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(layout, "TP-MED", (94, 205), 0.9, "07_INSTRUMENTACAO")
    line(layout, (96.8, 205), (122, 205), "07_INSTRUMENTACAO")
    box(layout, 122, 199, 172, 211, "MEDIDOR DIGITAL", "FATURAMENTO", "07_INSTRUMENTACAO")

    # 3. Cubiculo 2: Protecao Geral de Media Tensao (Y=148 a 192)
    line(layout, (90, 196), (90, 192), "05_POTENCIA")
    add_rect(layout, 30, 148, 178, 192, "11_ARQUITETURA")
    left_text(layout, "CUBICULO 02 - PROTECAO PRIMARIA (DISJUNTOR A VACUO)", (33, 188), 1.4, "11_ARQUITETURA", style=TITLE_STYLE)
    line(layout, (90, 192), (90, 181.2), "05_POTENCIA")
    breaker_mv_symbol(layout, 90, 177, "DJ-MT (630 A / 16 kA)", "Disjuntor a Vacuo 17,5 kV")
    line(layout, (90, 172.8), (90, 148), "05_POTENCIA")

    # TC de protecao toroidal / classe 10B200
    layout.add_circle((90, 160), 3.0, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    centered(layout, "TC-PROT", (90, 160), 0.85, "07_INSTRUMENTACAO")
    line(layout, (93.0, 160), (120, 160), "07_INSTRUMENTACAO")
    box(layout, 120, 152, 172, 168, "RELE DIGITAL", "ANSI 50/51/50N/51N", "07_INSTRUMENTACAO")
    # Linha de comando do rele para a bobina do disjuntor
    orthogonal(layout, [(146, 168), (146, 184), (96, 184)], "06_COMANDO")
    arrow(layout, (105, 184), (95, 184), "06_COMANDO")
    left_text(layout, "Trip (BA)", (112, 185.5), 1.0, "06_COMANDO")

    # 4. Cubiculo 3: Transformador de Forca 500 kVA (Y=100 a 144) -> Tudo acima de Y=98!
    line(layout, (90, 148), (90, 130.6), "05_POTENCIA")
    add_rect(layout, 30, 100, 178, 144, "11_ARQUITETURA")
    left_text(layout, "CUBICULO 03 - TRANSFORMACAO 500 kVA", (33, 140), 1.4, "11_ARQUITETURA", style=TITLE_STYLE)

    transformer_symbol(layout, 90, 122, "TR-01", "500 kVA")

    # Conexao secundario 380/220 V indo para QGBT (Totalmente acima de Y=100)
    line(layout, (90, 113.4), (90, 105), "05_POTENCIA")
    line(layout, (90, 105), (210, 105), "05_POTENCIA")
    ground_symbol(layout, 78, 108, "05_POTENCIA")
    line(layout, (78, 108), (90, 108), "05_POTENCIA")
    left_text(layout, "Neutro aterrado (BEP)", (40, 106), 1.05, "02_TEXTO")

    # 5. QGBT - Quadro Geral de Baixa Tensao (Lado Direito: X=192 a 402, Y=100 a 260)
    add_rect(layout, 192, 100, 402, 260, "04_EQUIPAMENTOS")
    centered(layout, "QGBT - QUADRO GERAL DE BAIXA TENSAO (380/220 V - 60 Hz)", (297, 254), 1.85, "04_EQUIPAMENTOS", style=TITLE_STYLE)

    # Disjuntor Geral BT (Caixa Aberta 800 A)
    line(layout, (210, 105), (210, 114), "05_POTENCIA")
    line(layout, (210, 114), (228, 114), "05_POTENCIA")
    box(layout, 228, 108, 258, 120, "DJ-GERAL", "800 A / 50 kA", "05_POTENCIA")
    line(layout, (258, 114), (275, 114), "05_POTENCIA")

    # Barramento principal QGBT (Trifasico 1000 A)
    line(layout, (275, 108), (275, 240), "05_POTENCIA")
    left_text(layout, "BARRAMENTO PRINCIPAL 3F+N+PE Cu 1000 A", (278, 236), 1.25, "05_POTENCIA", style=TITLE_STYLE)

    # DPS Geral BT
    line(layout, (275, 226), (295, 226), "05_POTENCIA")
    box(layout, 295, 221, 326, 231, "DPS-BT", "A especificar", "05_POTENCIA")
    line(layout, (326, 226), (336, 226), "05_POTENCIA")
    ground_symbol(layout, 336, 226, "05_POTENCIA")

    # Alimentadores que saem do QGBT
    feeders = [
        ("AL-01", "QDF-05 - Forca Industrial", "DJ 100 A", 204),
        ("AL-02", "QDL-05 - Iluminacao Fabril", "DJ 32 A", 182),
        ("AL-03", "QADM-05 - Apoio Administrativo", "DJ 32 A", 160),
        ("AL-04", "CCM-06 - Centro Controle Motores", "DJ 250 A", 138),
        ("AL-05", "RESERVA TECNICA 01", "DJ 100 A", 116),
    ]
    for tag, desc, dj, y_pos in feeders:
        line(layout, (275, y_pos), (300, y_pos), "05_POTENCIA")
        box(layout, 300, y_pos - 4, 325, y_pos + 4, dj, "", "05_POTENCIA")
        line(layout, (325, y_pos), (348, y_pos), "08_CABOS")
        arrow(layout, (338, y_pos), (348, y_pos), "08_CABOS")
        left_text(layout, tag, (352, y_pos + 1.5), 1.25, "04_EQUIPAMENTOS", style=TITLE_STYLE)
        left_text(layout, desc, (352, y_pos - 2.0), 1.0, "02_TEXTO")

    # Parametros tecnicos do QGBT
    panel_box(layout, 198, 128, 268, 224, "DADOS DE CURTO", "", "12_LEGENDA")
    specs = [
        "Potencia: 500 kVA",
        "Tensao MT: 13.800 V",
        "Tensao BT: 380/220 V",
        "In primario: 20,9 A",
        "In secundario: 759,7 A",
        "Z% trafo: 4,50%",
        "Icc sim. BT: 16,88 kA",
        "Icu DJ Geral: 50 kA",
        "Esquema: TN-S",
    ]
    for idx, s in enumerate(specs):
        left_text(layout, s, (201, 209 - idx * 9.2), 1.1, "02_TEXTO")


# --- Desenho da Prancha 2: Planta Baixa da Subestacao ---
def draw_sheet_02(layout) -> None:
    # Posicionado em X de 50 a 290, Y de 116 a 256 para que cotas e portas fiquem > Y=98
    x0, y0 = 50.0, 116.0
    w, h = 240.0, 140.0
    wall = 7.0

    # Paredes externas
    add_rect(layout, x0, y0, x0 + w, y0 + h, "11_ARQUITETURA")
    add_rect(layout, x0 + wall, y0 + wall, x0 + w - wall, y0 + h - wall, "11_ARQUITETURA")

    # Divisoria interna dos compartimentos
    line(layout, (x0 + 120, y0 + wall), (x0 + 120, y0 + h - wall), "11_ARQUITETURA")
    line(layout, (x0 + wall, y0 + 70), (x0 + 120, y0 + 70), "11_ARQUITETURA")

    # Bacia do transformador: X de x0+120 ate x0+190
    line(layout, (x0 + 190, y0 + wall), (x0 + 190, y0 + h - wall), "11_ARQUITETURA")
    add_rect(layout, x0 + 125, y0 + 14, x0 + 185, y0 + 88, "04_EQUIPAMENTOS")
    for gy in range(int(y0 + 20), int(y0 + 88), 10):
        line(layout, (x0 + 125, gy), (x0 + 185, gy), "11_ARQUITETURA")
    box(layout, x0 + 135, y0 + 32, x0 + 175, y0 + 70, "TR-01", "500 kVA (Oleo)", "05_POTENCIA")

    # Cubiculo 01 - Medicao
    box(layout, x0 + 15, y0 + 82, x0 + 110, y0 + 128, "CUBICULO DE MEDICAO", "Concessionaria 13,8 kV", "04_EQUIPAMENTOS")
    # Cubiculo 02 - Protecao
    box(layout, x0 + 15, y0 + 18, x0 + 110, y0 + 62, "CUBICULO DE PROTECAO", "DJ a Vacuo 17,5 kV + Rele 50/51", "04_EQUIPAMENTOS")

    # QGBT e Servicos Auxiliares
    box(layout, x0 + 197, y0 + 20, x0 + 226, y0 + 102, "QGBT-01", "Painel 800 A BT", "05_POTENCIA")
    box(layout, x0 + 197, y0 + 108, x0 + 226, y0 + 129, "RETIF./BAT.", "125 Vcc Aux.", "04_EQUIPAMENTOS")

    # Canaletas de piso
    add_rect(layout, x0 + 45, y0 + wall, x0 + 65, y0 + h - wall, "10_ELETROCALHAS")
    left_text(layout, "CANALETA MT 400x400", (x0 + 47, y0 + 73), 0.95, "10_ELETROCALHAS", style=TITLE_STYLE)
    add_rect(layout, x0 + 120, y0 + 96, x0 + 220, y0 + 106, "10_ELETROCALHAS")
    left_text(layout, "CANALETA BT 500x400", (x0 + 130, y0 + 99.5), 0.95, "10_ELETROCALHAS", style=TITLE_STYLE)

    # Portas corta-fogo metálicas P-90 (acima de Y=104)
    line(layout, (x0 + 60, y0), (x0 + 60, y0 - 9), "11_ARQUITETURA")
    line(layout, (x0 + 80, y0), (x0 + 80, y0 - 9), "11_ARQUITETURA")
    left_text(layout, "PORTA CORTA-FOGO P-90", (x0 + 48, y0 - 12), 1.05, "11_ARQUITETURA")
    line(layout, (x0 + 140, y0), (x0 + 140, y0 - 9), "11_ARQUITETURA")
    line(layout, (x0 + 160, y0), (x0 + 160, y0 - 9), "11_ARQUITETURA")

    # Tapete de borracha isolante 20 kV
    add_rect(layout, x0 + 20, y0 + 64, x0 + 105, y0 + 69, "06_COMANDO")
    left_text(layout, "TAPETE ISOLANTE 20 kV", (x0 + 35, y0 + 65.5), 0.95, "06_COMANDO")

    # Extintores de Incendio
    layout.add_circle((x0 + wall + 4, y0 + wall + 4), 2.8, dxfattribs={"layer": "06_COMANDO"})
    centered(layout, "CO2", (x0 + wall + 4, y0 + wall + 4), 0.95, "06_COMANDO")
    layout.add_circle((x0 + wall + 12, y0 + wall + 4), 2.8, dxfattribs={"layer": "06_COMANDO"})
    centered(layout, "PQS", (x0 + wall + 12, y0 + wall + 4), 0.85, "06_COMANDO")

    # Cotas principais (Totalmente acima de Y=98)
    line(layout, (x0, y0 - 15), (x0 + w, y0 - 15), "03_COTAS")
    centered(layout, "6 000 mm (COMPRIMENTO EXTERNO)", (x0 + w / 2, y0 - 18.2), 1.3, "03_COTAS")
    line(layout, (x0 - 10, y0), (x0 - 10, y0 + h), "03_COTAS")
    centered(layout, "4 000 mm", (x0 - 18, y0 + h / 2), 1.3, "03_COTAS")

    # Painel de informacoes laterais
    panel_box(layout, 302, 100, 402, 256, "PREMISSAS NBR 14039", "", "12_LEGENDA")
    notes_p2 = [
        "1. Pe-direito livre: 3,50 m.",
        "2. Corredor de manobra >= 1,20 m.",
        "3. Abertura das portas para fora.",
        "4. Bacia com volume >= 1,2 m3",
        "   (oleo total trafo = 850 L).",
        "5. Brita n. 1 h=10 cm abafa-chama.",
        "6. Ventilacao natural cruzada:",
        "   - venezianas com tela 2 mm;",
        "   - area util calculada: 1,8 m2.",
        "7. Tapete de seguranca 20 kV.",
        "8. Iluminacao normal e emergencia.",
        "9. Placas 'ALTA TENSAO 13.800 V'.",
    ]
    for idx, nt in enumerate(notes_p2):
        left_text(layout, nt, (306, 241 - idx * 11.2), 1.12, "02_TEXTO")


# --- Desenho da Prancha 3: Cortes e Detalhes Eletromecanicos ---
def draw_sheet_03(layout) -> None:
    # Corte A-A (X: 30 a 205, Y: 100 a 256)
    add_rect(layout, 30, 100, 205, 256, "11_ARQUITETURA")
    centered(layout, "CORTE A-A: CUBICULO DE ENTRADA E PROTECAO MT", (117, 249), 1.65, "11_ARQUITETURA", style=TITLE_STYLE)

    # Piso elevado em Y=126 para deixar a canaleta inteira dentro do quadro (Y=104..126)
    line(layout, (30, 126), (205, 126), "11_ARQUITETURA")
    left_text(layout, "NIVEL PISO ACABADO (+0,00)", (34, 129), 1.05, "11_ARQUITETURA")
    add_rect(layout, 70, 104, 105, 126, "10_ELETROCALHAS")
    centered(layout, "CANALETA MT", (87.5, 114), 1.0, "10_ELETROCALHAS")

    # Cabos subindo e muflas
    line(layout, (85, 118), (85, 144), "08_CABOS")
    box(layout, 77, 144, 93, 158, "MUFLA", "15 kV", "04_EQUIPAMENTOS")

    # Barramento rigido MT sobre isoladores epoxi
    line(layout, (85, 158), (85, 218), "05_POTENCIA")
    for iy in (168, 198):
        box(layout, 100, iy - 3.5, 116, iy + 3.5, "ISOLADOR", "17,5 kV", "04_EQUIPAMENTOS")
        line(layout, (85, iy), (100, iy), "05_POTENCIA")

    # Chave seccionadora tripé
    disconnect_switch_symbol(layout, 85, 186, "SECCIONADORA (h=2,50m)")
    # Disjuntor a vacuo
    breaker_mv_symbol(layout, 85, 218, "DJ A VACUO", "Extraivel / 17,5 kV")
    # Saida superior de barramento para o trafo
    line(layout, (85, 224), (185, 224), "05_POTENCIA")
    left_text(layout, "Barramento MT Cu 25x5 mm", (105, 227), 1.1, "05_POTENCIA")

    # Tela de protecao frontal
    line(layout, (142, 126), (142, 212), "06_COMANDO")
    left_text(layout, "TELA DE PROTECAO h=2,10 m", (145, 168), 1.0, "06_COMANDO")
    left_text(layout, "COM INTERTRAVAMENTO KIRK", (145, 163), 1.0, "06_COMANDO")

    # Corte B-B (X: 220 a 402, Y: 100 a 256)
    add_rect(layout, 220, 100, 402, 256, "11_ARQUITETURA")
    centered(layout, "CORTE B-B: CUBICULO DO TRANSFORMADOR 500 kVA", (311, 249), 1.65, "11_ARQUITETURA", style=TITLE_STYLE)

    # Piso em Y=126 e bacia rebaixada ate Y=110 (dreno em Y=104, totalmente dentro do quadro!)
    line(layout, (220, 126), (245, 126), "11_ARQUITETURA")
    line(layout, (375, 126), (402, 126), "11_ARQUITETURA")
    orthogonal(layout, [(245, 126), (245, 110), (375, 110), (375, 126)], "11_ARQUITETURA")
    left_text(layout, "BACIA DE CONTENCAO 1,2 m3", (255, 113), 1.05, "11_ARQUITETURA")
    for bx in range(250, 370, 15):
        line(layout, (bx, 120), (bx + 8, 120), "11_ARQUITETURA")
    left_text(layout, "BRITA N. 1 (10 cm)", (282, 122), 0.95, "11_ARQUITETURA")

    # Transformador
    box(layout, 260, 128, 360, 198, "TRANSFORMADOR 500 kVA", "Imerso em Oleo Mineral", "05_POTENCIA")
    # Buchas de AT (primario)
    box(layout, 273, 198, 291, 214, "BUCHA AT", "15 kV", "04_EQUIPAMENTOS")
    line(layout, (282, 214), (282, 224), "05_POTENCIA")
    # Buchas de BT (secundario)
    box(layout, 328, 198, 348, 210, "BUCHAS BT", "1 kV", "04_EQUIPAMENTOS")
    orthogonal(layout, [(338, 210), (338, 232), (392, 232)], "05_POTENCIA")
    left_text(layout, "Barramento flexivel Cu BT -> QGBT", (305, 235), 1.0, "05_POTENCIA")

    # Tubo de dreno da bacia (Y=104, acima de Y=100!)
    orthogonal(layout, [(310, 110), (310, 104), (365, 104)], "11_ARQUITETURA")
    left_text(layout, "Dreno sifonado p/ caixa separadora", (314, 105.5), 0.95, "11_ARQUITETURA")


# --- Desenho da Prancha 4: Diagrama Funcional de Protecao e Comando ---
def draw_sheet_04(layout) -> None:
    # 1. Medicao AC de corrente e tensao (Esquerda: X 25 a 165, Y 100 a 256)
    add_rect(layout, 25, 100, 165, 256, "04_EQUIPAMENTOS")
    centered(layout, "MEDICAO AC E SENSORIAMENTO", (95, 249), 1.6, "04_EQUIPAMENTOS", style=TITLE_STYLE)

    # 3 Fases primarias com roteamento ortogonal limpo para os bornes X-PROT
    fases_info = [
        ("Fase A", 45, 210, 1),
        ("Fase B", 75, 194, 2),
        ("Fase C", 105, 178, 3),
    ]
    for fase, x_f, y_tc, b_num in fases_info:
        line(layout, (x_f, 238), (x_f, 150), "05_POTENCIA")
        centered(layout, fase, (x_f, 241), 1.15, "05_POTENCIA")
        layout.add_circle((x_f, y_tc), 4.0, dxfattribs={"layer": "07_INSTRUMENTACAO"})
        centered(layout, f"TC-{b_num}", (x_f, y_tc), 0.95, "07_INSTRUMENTACAO")
        line(layout, (x_f + 4.0, y_tc), (140, y_tc), "07_INSTRUMENTACAO")
        layout.add_circle((140, y_tc), 1.5, dxfattribs={"layer": "09_BORNES"})
        left_text(layout, f"X-PROT:{b_num}", (143, y_tc - 1.0), 1.0, "09_BORNES")

    # Borne de retorno comum dos TCs
    layout.add_circle((140, 162), 1.5, dxfattribs={"layer": "09_BORNES"})
    left_text(layout, "X-PROT:4 (Comum)", (143, 161), 0.95, "09_BORNES")
    line(layout, (45, 162), (138.5, 162), "07_INSTRUMENTACAO")

    # Sensor Buchholz e Termometro
    box(layout, 35, 112, 88, 138, "RELE BUCHHOLZ", "ANSI 63 (Gas)", "07_INSTRUMENTACAO")
    box(layout, 96, 112, 155, 138, "TERMOMETRO OLEO", "ANSI 49 (85/100 C)", "07_INSTRUMENTACAO")

    # 2. Rele Microprocessado e Logica de Trip (Centro: X 180 a 285, Y 100 a 256)
    add_rect(layout, 180, 100, 285, 256, "06_COMANDO")
    centered(layout, "RELE DIGITAL DE SOBRECORRENTE", (232.5, 249), 1.55, "06_COMANDO", style=TITLE_STYLE)
    panel_box(layout, 192, 132, 273, 236, "RELE 50/51/50N/51N", "Microprocessado", "06_COMANDO")

    funcs = [
        "Entradas: IA, IB, IC, IN",
        "Curva Fase: IEC Inversa",
        "Pick-up Fase (51): 26,2 A",
        "Inst. Fase (50): 600 A",
        "Curva Neutro: Muito Inv.",
        "Pick-up Terra (51N): 5,0 A",
        "Saida DO1: Trip Disjuntor",
        "Saida DO2: Alarme Termico",
        "Alimentacao: 125 Vcc Aux.",
    ]
    for idx, fn in enumerate(funcs):
        left_text(layout, fn, (196, 218 - idx * 9.0), 1.05, "02_TEXTO")

    # 3. Circuito de Disparo e Alimentacao Auxiliar (Direita: X 300 a 402, Y 100 a 256)
    add_rect(layout, 300, 100, 402, 256, "06_COMANDO")
    centered(layout, "CIRCUITO DE DISPARO DC (TRIP)", (351, 249), 1.55, "06_COMANDO", style=TITLE_STYLE)

    # Barramento DC positivo e negativo
    line(layout, (312, 235), (386, 235), "06_COMANDO")
    left_text(layout, "+125 Vcc", (388, 234), 1.1, "06_COMANDO")
    line(layout, (312, 120), (386, 120), "06_COMANDO")
    left_text(layout, "-125 Vcc", (388, 119), 1.1, "06_COMANDO")

    # Ramo 1: Contato do Rele DO1 -> Bobina de Abertura (BA) -> Contato 52a disjuntor
    line(layout, (330, 235), (330, 215), "06_COMANDO")
    box(layout, 320, 196, 340, 215, "DO1", "Trip 50/51", "06_COMANDO")
    line(layout, (330, 196), (330, 175), "06_COMANDO")
    box(layout, 320, 155, 340, 175, "BA", "Bobina MT", "06_COMANDO")
    line(layout, (330, 155), (330, 140), "06_COMANDO")
    # Contato 52a (auxiliar disjuntor)
    line(layout, (330, 140), (334, 130), "06_COMANDO")
    layout.add_circle((330, 140), 0.8, dxfattribs={"layer": "06_COMANDO"})
    layout.add_circle((330, 126), 0.8, dxfattribs={"layer": "06_COMANDO"})
    left_text(layout, "52a", (336, 133), 1.1, "06_COMANDO")
    line(layout, (330, 126), (330, 120), "06_COMANDO")

    # Ramo 2: Trip direto pelo Buchholz / Emergencia
    line(layout, (366, 235), (366, 215), "06_COMANDO")
    box(layout, 354, 196, 378, 215, "BUCHHOLZ", "Trip 63/49", "06_COMANDO")
    line(layout, (366, 196), (366, 182), "06_COMANDO")
    orthogonal(layout, [(366, 182), (330, 182)], "06_COMANDO")
    left_text(layout, "Trip paralelo", (338, 184), 0.95, "06_COMANDO")


# --- Desenho da Prancha 5: Malha de Aterramento e Equipotencializacao ---
def draw_sheet_05(layout) -> None:
    add_rect(layout, 30, 100, 260, 256, "11_ARQUITETURA")
    centered(layout, "PLANTA DA MALHA DE ATERRAMENTO (ANEL E QUADRICULAS)", (145, 249), 1.6, "12_LEGENDA", style=TITLE_STYLE)

    # Subestacao civil no centro
    add_rect(layout, 80, 135, 200, 215, "11_ARQUITETURA")
    centered(layout, "PROJECAO CIVIL DA SUBESTACAO", (160, 182), 1.25, "12_LEGENDA")

    # Anel externo de aterramento
    add_rect(layout, 60, 115, 220, 235, "05_POTENCIA")
    left_text(layout, "Cabo de Cobre Nu 70 mm2 a 0,60 m de profundidade", (62, 238), 1.1, "05_POTENCIA")

    # Quadriculado interno de equalizacao
    for qx in (100, 140, 180):
        line(layout, (qx, 115), (qx, 235), "05_POTENCIA")
    for qy in (155, 195):
        line(layout, (60, qy), (220, qy), "05_POTENCIA")

    # 8 Hastes de aterramento
    ground_rods = [
        (60, 115), (140, 115), (220, 115),
        (60, 175), (220, 175),
        (60, 235), (140, 235), (220, 235)
    ]
    for rx, ry in ground_rods:
        layout.add_circle((rx, ry), 3.5, dxfattribs={"layer": "04_EQUIPAMENTOS"})
        line(layout, (rx - 3.5, ry), (rx + 3.5, ry), "04_EQUIPAMENTOS")
        line(layout, (rx, ry - 3.5), (rx, ry + 3.5), "04_EQUIPAMENTOS")
        centered(layout, "H", (rx + 5.5, ry - 4.5), 1.0, "04_EQUIPAMENTOS")

    # Barramento de Equipotencializacao Principal (BEP)
    box(layout, 88, 139, 126, 149, "BEP", "Barra Cu 50x6 mm", "05_POTENCIA")
    orthogonal(layout, [(88, 144), (70, 144), (70, 175)], "05_POTENCIA")

    bep_links = [
        ("Neutro Trafo 70 mm2", (104, 149), (104, 168)),
        ("Massa Trafo 70 mm2", (116, 149), (116, 168)),
        ("QGBT 50 mm2", (126, 144), (162, 144)),
    ]
    for desc, p1, p2 in bep_links:
        line(layout, p1, p2, "08_CABOS")

    # Premissas e limites: nao apresentar a estimativa como dimensionamento normativo.
    panel_box(layout, 275, 100, 402, 256, "LIMITES DO ESTUDO DE ATERRAMENTO", "SEM APROVACAO DE SEGURANCA", "12_LEGENDA")
    sections = [
        (235, "DADOS DE SOLO", "Resistividade, camadas e camada superficial nao foram medidas."),
        (205, "ARRANJO ILUSTRATIVO", "Cu nu 70 mm2 e 8 hastes sao premissas, sem dimensionamento do local."),
        (175, "RESULTADO DA MALHA", "Resistencia e elevacao de potencial nao determinadas; sem valor de aprovacao."),
        (145, "POTENCIAIS", "GPR, toque, passo e transferencia ainda nao calculados."),
        (115, "PROXIMA ETAPA", "Consolidar dados de campo e de falta conforme a prancha 07."),
    ]
    for y, heading, detail in sections:
        left_text(layout, heading, (280, y), 1.1, "12_LEGENDA", style=TITLE_STYLE)
        add_mtext(layout, detail, (280, y - 5), 116, 1.0, "02_TEXTO")


# --- Desenho da Prancha 7: Dados para estudo de aterramento ---
def draw_sheet_07(layout) -> None:
    panels = [
        (18, 140, "DADOS DE SOLO", "levantamento medido", [
            "Resistividade por pontos/profundidades",
            "Camadas e espessuras do perfil",
            "Resistividade/camada superficial",
            "Umidade e condicao sazonal",
            "Relatorio, local e data do ensaio",
        ]),
        (149, 271, "FALTA E PROTECAO", "dados da rede e ajustes", [
            "Corrente de falta e cenarios",
            "Parcela que circula pela malha",
            "Tempo de eliminacao rele + DJ",
            "Aterramento do neutro da fonte",
            "Fonte e rastreio de cada valor",
        ]),
        (280, 402, "GEOMETRIA E INTERFACES", "levantamento real/as-built", [
            "Perimetro, cotas e zonas acessiveis",
            "Malha, secoes e profundidades",
            "Hastes, conexoes e condicoes",
            "BEP e massas equipotencializadas",
            "Cercas e metais que cruzam limites",
        ]),
    ]
    for x0, x1, title, subtitle, items in panels:
        panel_box(layout, x0, 184, x1, 256, title, subtitle, "12_LEGENDA")
        for index, item in enumerate(items):
            left_text(layout, item, (x0 + 4, 238 - index * 10), 1.38, "02_TEXTO")

    arrow(layout, (141, 219), (148, 219), "08_CABOS")
    arrow(layout, (272, 219), (279, 219), "08_CABOS")

    flow = [
        (18, 109, "LEVANTAR", "solo, falta e sitio"),
        (116, 207, "MODELAR", "entradas rastreaveis"),
        (214, 305, "VERIFICAR", "condutor e potenciais"),
        (312, 402, "REVISAR", "memoria e criterios"),
    ]
    for x0, x1, title, detail in flow:
        add_rect(layout, x0, 160, x1, 181, "04_EQUIPAMENTOS")
        centered(layout, title, ((x0 + x1) / 2, 173.5), 1.55, "04_EQUIPAMENTOS", style=TITLE_STYLE)
        centered(layout, detail, ((x0 + x1) / 2, 166), 1.25, "02_TEXTO")
    for x1, x2 in ((109, 116), (207, 214), (305, 312)):
        arrow(layout, (x1, 170.5), (x2, 170.5), "08_CABOS")

    add_rect(layout, 18, 101, 402, 154, "12_LEGENDA")
    centered(layout, "ENTREGAS PARA DECISAO DOCUMENTADA", (210, 149), 1.45, "12_LEGENDA", style=TITLE_STYLE)
    centered(layout, "ANALISE / ENTREGAVEL", (79, 140.5), 1.3, "12_LEGENDA", style=TITLE_STYLE)
    centered(layout, "DADO OU EVIDENCIA A ANEXAR", (239, 140.5), 1.3, "12_LEGENDA", style=TITLE_STYLE)
    centered(layout, "STATUS", (368, 140.5), 1.3, "12_LEGENDA", style=TITLE_STYLE)
    line(layout, (18, 137), (402, 137), "12_LEGENDA")
    line(layout, (143, 101), (143, 137), "12_LEGENDA")
    line(layout, (335, 101), (335, 137), "12_LEGENDA")
    deliverables = [
        ("Modelo do solo", "Perfil medido, camadas e camada superficial"),
        ("Corrente e tempo de falta", "Fonte, parcela na malha e tempo de eliminacao"),
        ("Condutor e conexoes", "Material, secao, geometria e condicoes instaladas"),
        ("GPR, toque, passo e transferencia", "Calculo rastreavel com criterios e geometria definida"),
        ("Decisao tecnica", "Memoria, limites, revisao e evidencias anexas"),
    ]
    for index, (analysis, evidence) in enumerate(deliverables):
        y = 132.5 - index * 7
        left_text(layout, analysis, (22, y), 1.3, "02_TEXTO")
        left_text(layout, evidence, (147, y), 1.3, "02_TEXTO")
        centered(layout, "PENDENTE", (368, y), 1.3, "13_NOTAS", style=TITLE_STYLE)


# --- Desenho da Prancha 6: SPDA Geral (NBR 5419) ---
def draw_sheet_06(layout) -> None:
    # 1. Planta de Cobertura com Malha de Faraday (Esquerda: X 30 a 250, Y 100 a 256)
    add_rect(layout, 30, 100, 250, 256, "11_ARQUITETURA")
    centered(layout, "COBERTURA DA SUBESTACAO E MALHA DE CAPTACAO", (140, 249), 1.6, "11_ARQUITETURA", style=TITLE_STYLE)

    # Cobertura civil (6,00 x 4,00 m)
    add_rect(layout, 60, 125, 220, 225, "11_ARQUITETURA")
    centered(layout, "LAJE DE COBERTURA / PLATIBANDA", (180, 182), 1.2, "11_ARQUITETURA")

    # Malha captora superior em cobre nu 35 mm2 (Nivel II: malha 10 x 10 m)
    add_rect(layout, 60, 125, 220, 225, "05_POTENCIA")
    line(layout, (140, 125), (140, 225), "05_POTENCIA")
    line(layout, (60, 175), (220, 175), "05_POTENCIA")
    left_text(layout, "Condutor captor: Cobre Nu 35 mm2", (65, 229), 1.1, "05_POTENCIA")

    # 4 Captores aéreos Franklin nos cantos
    captores = [(60, 125), (220, 125), (60, 225), (220, 225)]
    for cx, cy in captores:
        layout.add_circle((cx, cy), 3.0, dxfattribs={"layer": "04_EQUIPAMENTOS"})
        centered(layout, "F", (cx, cy), 1.2, "04_EQUIPAMENTOS")
        offset_y = 5.5 if cy > 175 else -6.5
        left_text(layout, "Captor h=35cm", (cx - 10, cy + offset_y), 0.9, "04_EQUIPAMENTOS")

    # 4 Descidas pelas paredes externas
    descidas = [
        ("DESC-01", (60, 175), (42, 175), (36, 178)),
        ("DESC-02", (220, 175), (238, 175), (226, 178)),
        ("DESC-03", (140, 125), (140, 108), (144, 112)),
        ("DESC-04", (140, 225), (140, 241), (144, 236)),
    ]
    for tag, p1, p2, t_pos in descidas:
        line(layout, p1, p2, "08_CABOS")
        arrow(layout, p1, p2, "08_CABOS")
        left_text(layout, tag, t_pos, 1.0, "08_CABOS")

    # 2. Detalhes Construtivos e MPS (Direita: X 265 a 402, Y 100 a 256)
    add_rect(layout, 265, 100, 402, 256, "12_LEGENDA")
    centered(layout, "DETALHES CONSTRUTIVOS E MPS", (333.5, 249), 1.45, "12_LEGENDA", style=TITLE_STYLE)

    # Detalhe descida com tubo de protecao usando panel_box (sem sobreposicao!)
    panel_box(layout, 273, 178, 395, 242, "DETALHE DA DESCIDA DO SPDA", "Protecao Mecanica e Medicao", "04_EQUIPAMENTOS")
    dt_lines = [
        "- Condutor de descida Cu nu 35 mm2.",
        "- Eletroduto galvanizado h=2,5 m na base.",
        "- Caixa de inspecao suspensa a 1,5 m.",
        "- Conector de emenda p/ ensaio continuidade.",
        "- Solda exotermica no anel de aterramento.",
    ]
    for idx, dl in enumerate(dt_lines):
        left_text(layout, dl, (276, 224 - idx * 8.5), 1.02, "02_TEXTO")

    # Medidas contra Surtos (MPS / DPS) usando panel_box
    panel_box(layout, 273, 106, 395, 170, "INTEGRACAO CONCEITUAL DE DPS", "A especificar no projeto detalhado", "04_EQUIPAMENTOS")
    mps_lines = [
        "- Classe, Uc, Up e correntes do DPS: a definir.",
        "- Equipotencializacao de massas no BEP.",
        "- Coordenar DPS, roteamento e comprimentos",
        "  com o SPDA e o projeto executivo.",
        "- Criterio de ensaio de continuidade: a definir.",
    ]
    for idx, ml in enumerate(mps_lines):
        left_text(layout, ml, (276, 152 - idx * 8.5), 1.02, "02_TEXTO")


DRAW_MAP = {
    1: draw_sheet_01,
    2: draw_sheet_02,
    3: draw_sheet_03,
    4: draw_sheet_04,
    5: draw_sheet_05,
    6: draw_sheet_06,
    7: draw_sheet_07,
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
    parser.add_argument("--sheet", type=int, help=f"Gera apenas a prancha especificada (1..{len(SHEETS)})")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config = load_config(root)
    source_dir = root / "11-subestacao-media-tensao" / "fonte"
    source_dir.mkdir(parents=True, exist_ok=True)

    for spec in SHEETS:
        if args.sheet and spec.number != args.sheet:
            continue
        output_path = source_dir / spec.filename
        build_sheet(config, spec, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
