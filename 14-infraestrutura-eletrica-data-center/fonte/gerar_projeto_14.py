"""Gera as tres pranchas conceituais de infraestrutura eletrica de data center."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment


DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "14-infraestrutura-eletrica-data-center"
ROOT = DEFAULT_ROOT
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from gerar_template_a3 import (  # noqa: E402
    TITLE_BLOCK_NAME,
    PROJECT_PRINT_LAYER_COLORS,
    TITLE_STYLE,
    TEXT_STYLE,
    add_frame,
    add_line,
    add_mtext,
    add_rect,
    add_text,
    configure_document,
    define_title_block,
    prepare_deterministic_write,
)
from portfolio_config import SheetGeometry, load_config  # noqa: E402


DATE = "2026-11-06"
REVISION = "00"
WARNING_FALLBACK = (
    "Projeto academico e conceitual. Nao deve ser utilizado para fabricacao, "
    "instalacao ou execucao de servicos sem revisao, dimensionamento e "
    "responsabilidade de profissional legalmente habilitado."
)


def text(layout, value: str, x: float, y: float, h: float = 1.7,
         layer: str = "02_TEXTO", *, centered: bool = False,
         bold: bool = False) -> None:
    add_text(
        layout,
        value,
        (x, y),
        h,
        layer=layer,
        align=TextEntityAlignment.MIDDLE_CENTER if centered else TextEntityAlignment.LEFT,
        style=TITLE_STYLE if bold else TEXT_STYLE,
    )


def line(layout, a: tuple[float, float], b: tuple[float, float],
         layer: str = "02_TEXTO") -> None:
    add_line(layout, a, b, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float,
        title: str, detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        detail_height: float = 1.3) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    midx = (x0 + x1) / 2
    midy = (y0 + y1) / 2
    if detail:
        if "\n" in detail:
            text(layout, title, midx, y1 - 5, 1.7, layer, centered=True, bold=True)
            add_mtext(
                layout,
                detail.replace("\n", "\\P"),
                (x0 + 2, y1 - 8),
                x1 - x0 - 4,
                detail_height,
                "02_TEXTO",
            )
        else:
            text(layout, title, midx, midy + 2, 1.7, layer, centered=True, bold=True)
            text(layout, detail, midx, midy - 2, detail_height, "02_TEXTO", centered=True)
    else:
        text(layout, title, midx, midy, 1.7, layer, centered=True, bold=True)


def arrow(layout, start: tuple[float, float], end: tuple[float, float],
          layer: str, size: float = 2.3) -> None:
    line(layout, start, end, layer)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(
            layout,
            (end[0] - ux * size + side * px * size * 0.55,
             end[1] - uy * size + side * py * size * 0.55),
            end,
            layer,
        )


def header(layout, title: str, subtitle: str) -> None:
    text(layout, title, 20, 275, 3.2, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.65, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 2.0, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.55, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66.5, 2.0, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.42, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90.5, 2.0, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.38, "12_LEGENDA")

    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for value, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, value, x, 89.5, 1.55, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.45, "02_TEXTO", centered=True)


def make_sheet(root: Path, config: dict, number: int, spec: dict, draw) -> None:
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height), layer_color_overrides=PROJECT_PRINT_LAYER_COLORS)
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = SLUG
    metadata["PORTFOLIO_REVISION"] = REVISION
    metadata["PORTFOLIO_SHEET"] = f"{number:02d}/03"
    metadata["PORTFOLIO_UNITS"] = "mm"
    define_title_block(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    header(layout, spec["title"], spec["subtitle"])
    draw(layout)
    warning = config["portfolio"].get("warning", WARNING_FALLBACK)
    footer(layout, spec, warning)
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs(
        {
            "TITULO": spec["title"],
            "AUTOR": config["portfolio"]["author"],
            "DATA": DATE,
            "REVISAO": REVISION,
            "PRANCHA": f"{number:02d}/03",
            "ARQUIVO": spec["filename"],
            "UNIDADES": "mm",
            "ESCALA": spec["scale"],
            "FOLHA": "A3",
            "STATUS": "CONCEIT.",
        }
    )
    output = root / SLUG / "fonte" / spec["filename"]
    output.parent.mkdir(parents=True, exist_ok=True)
    prepare_deterministic_write(doc)
    with output.open("wt", encoding="utf-8", newline="\n") as stream:
        doc.write(stream)


def draw_architecture(layout) -> None:
    """Two conceptual power trains, each with its own generator and UPS."""
    rows = ((197, "A"), (128, "B"))
    xboxes = ((25, 72), (84, 130), (142, 201), (213, 272), (284, 337))
    for y0, path in rows:
        specs = (
            ("ALIM. MT-" + path, "13.8 kV* / origem pendente"),
            ("TR-" + path, "2.0 MVA*"),
            ("QGBT-" + path, "ATS-" + path + " / cargas"),
            ("UPS-" + path, "5 x 250 kW* / 4 + 1"),
            ("PDU-" + path, "rota do caminho " + path),
        )
        for (x0, x1), (title, detail) in zip(xboxes, specs):
            box(layout, x0, y0, x1, y0 + 36, title, detail, detail_height=1.15)
        cy = y0 + 18
        for i in range(4):
            arrow(layout, (xboxes[i][1], cy), (xboxes[i + 1][0], cy), "05_POTENCIA", 1.7)

    box(layout, 147, 242, 198, 259, "GE-A", "2.0 MVA*", detail_height=1.05)
    arrow(layout, (172.5, 241), (172.5, 234), "05_POTENCIA", 1.5)
    box(layout, 147, 105, 198, 122, "GE-B", "2.0 MVA*", detail_height=1.05)
    arrow(layout, (172.5, 123), (172.5, 127), "05_POTENCIA", 1.5)

    # Dual-cord rack load; the two paths stay visually separate to the load.
    add_rect(layout, 350, 128, 401, 233, "04_EQUIPAMENTOS")
    text(layout, "RACKS DE TI", 375.5, 221, 1.8, "04_EQUIPAMENTOS", centered=True, bold=True)
    line(layout, (354, 216), (397, 216), "03_COTAS")
    text(layout, "ENTRADA A", 375.5, 211, 1.25, "05_POTENCIA", centered=True, bold=True)
    line(layout, (354, 151), (397, 151), "03_COTAS")
    text(layout, "ENTRADA B", 375.5, 146, 1.25, "05_POTENCIA", centered=True, bold=True)
    text(layout, "Duas fontes por carga de TI", 375.5, 183, 1.2, "02_TEXTO", centered=True)
    text(layout, "A/B: caminhos conceituais", 375.5, 177, 1.15, "02_TEXTO", centered=True)
    arrow(layout, (337, 215), (350, 215), "05_POTENCIA", 1.5)
    arrow(layout, (337, 146), (350, 146), "05_POTENCIA", 1.5)

    text(layout, "CARGA DE TI ASSUMIDA: 1.0 MW  |  INSTALACAO: 1.5 MW  |  PUE: 1.50", 26, 181, 1.5, "13_NOTAS", bold=True)
    text(layout, "* Potencias e alimentacoes sao hipoteticas; origem MT, segregacao e transferencia exigem estudo.", 26, 174, 1.3, "13_NOTAS")


def draw_layout(layout) -> None:
    """Indicative room and rack plan showing separate A/B distribution routes."""
    add_rect(layout, 24, 108, 296, 257, "11_ARQUITETURA")
    text(layout, "SALA DE TI / CORREDORES E RACKS - ESQUEMA", 29, 249, 1.75, "11_ARQUITETURA", bold=True)

    centers = (100, 169, 238)
    rack_rows = ((186, 216, "R01", "R02", "R03", 232, 226),
                 (130, 160, "R04", "R05", "R06", 176, 170))
    for y0, y1, r1, r2, r3, bus_a, bus_b in rack_rows:
        line(layout, (68, bus_a), (281, bus_a), "10_ELETROCALHAS")
        line(layout, (68, bus_b), (281, bus_b), "10_ELETROCALHAS")
        text(layout, "A", 61, bus_a, 1.3, "05_POTENCIA", centered=True, bold=True)
        text(layout, "B", 61, bus_b, 1.3, "08_CABOS", centered=True, bold=True)
        for cx, tag in zip(centers, (r1, r2, r3)):
            add_rect(layout, cx - 22, y0, cx + 22, y1, "04_EQUIPAMENTOS")
            text(layout, tag, cx, y0 + 19, 1.7, "04_EQUIPAMENTOS", centered=True, bold=True)
            text(layout, "TI A/B", cx, y0 + 11, 1.2, "02_TEXTO", centered=True)
            # Separate drops land at distinct positions on each dual-fed rack.
            line(layout, (cx - 4, bus_a), (cx - 4, y1), "05_POTENCIA")
            line(layout, (cx + 4, bus_b), (cx + 4, y1), "08_CABOS")
    text(layout, "DISTRIBUICAO A/B NO TETO - CAMINHOS VISUALMENTE SEPARADOS", 31, 116, 1.2, "13_NOTAS")

    rooms = (
        ((306, 220, 350, 249), "QMT-A", "entrada / protecao pendente"),
        ((353, 220, 397, 249), "QMT-B", "origem independente?"),
        ((306, 188, 350, 216), "TR-A", "2.0 MVA*"),
        ((353, 188, 397, 216), "TR-B", "2.0 MVA*"),
        ((306, 156, 350, 184), "QGBT-A", "ATS / cargas"),
        ((353, 156, 397, 184), "QGBT-B", "ATS / cargas"),
        ((306, 124, 350, 152), "UPS-A", "5 x 250 kW*"),
        ((353, 124, 397, 152), "UPS-B", "5 x 250 kW*"),
        ((306, 104, 397, 121), "PATIO GE", "GE-A / GE-B"),
    )
    for (x0, y0, x1, y1), title, detail in rooms:
        box(layout, x0, y0, x1, y1, title, detail, detail_height=1.05)


def draw_power_and_contingencies(layout) -> None:
    """Transparent arithmetic and limited one-train-out examples."""
    add_rect(layout, 22, 169, 196, 257, "12_LEGENDA")
    text(layout, "BALANCO DE CARGA - HIPOTESES", 27, 248, 1.8, "12_LEGENDA", bold=True)
    line(layout, (26, 242), (192, 242), "12_LEGENDA")
    load_rows = (
        ("Potencia de TI", "1,000 kW"),
        ("Climatizacao + auxiliares", "500 kW"),
        ("Potencia total prevista", "1,500 kW"),
        ("PUE adotado", "1.50"),
        ("Fator de potencia", "0.95"),
        ("S = P / FP", "1,579 kVA"),
    )
    for i, (label, value) in enumerate(load_rows):
        y = 233 - i * 10
        line(layout, (26, y - 4), (192, y - 4), "03_COTAS")
        text(layout, label, 29, y, 1.35, "02_TEXTO")
        text(layout, value, 189, y, 1.35, "02_TEXTO", centered=True, bold=(i == 2))

    add_rect(layout, 202, 169, 398, 257, "12_LEGENDA")
    text(layout, "CAPACIDADE POR CAMINHO - CALCULO DIDATICO", 207, 248, 1.8, "12_LEGENDA", bold=True)
    line(layout, (206, 242), (394, 242), "12_LEGENDA")
    headings = ((219, "EQUIP."), (270, "NOMINAL"), (333, "UTILIZAVEL*"), (383, "RESERVA*"))
    for x, label in headings:
        text(layout, label, x, 237, 1.0, "12_LEGENDA", centered=True, bold=True)
    capacity_rows = (
        ("TR-A/B", "2,000 kVA", "1,900 kW", "400 kW"),
        ("GE-A/B", "2,000 kVA", "1,800 kW", "300 kW"),
        ("UPS-A/B", "5 x 250 kW", "4 x 250 = 1,000", "0 kW"),
    )
    for i, row in enumerate(capacity_rows):
        y = 224 - i * 13
        line(layout, (206, y - 5), (394, y - 5), "03_COTAS")
        for (x, _), value in zip(headings, row):
            text(layout, value, x, y, 1.05, "02_TEXTO", centered=True)
    text(layout, "* FP TR=0.95; FP GE=0.90; UPS: um modulo reserva N+1.", 207, 181, 1.12, "13_NOTAS")
    text(layout, "Na contingencia de um caminho, a saida deve atender 1,000 kW de TI.", 207, 175, 1.05, "13_NOTAS")

    add_rect(layout, 22, 104, 207, 163, "07_INSTRUMENTACAO")
    text(layout, "SEQUENCIA OPERACIONAL PROPOSTA", 27, 154, 1.7, "07_INSTRUMENTACAO", bold=True)
    sequence = (
        ("NORMAL", "UPS online; TI dividida A/B."),
        ("FALTA REDE", "Baterias sustentam; GE parte."),
        ("CAMINHO A FORA", "B recebe 1,000 kW TI + 500 kW suporte."),
        ("MODULO UPS", "4 x 250 kW = 1,000 kW; sem reserva."),
    )
    for i, (event, response) in enumerate(sequence):
        y = 143 - i * 11
        line(layout, (26, y - 4), (203, y - 4), "03_COTAS")
        text(layout, event, 29, y, 1.15, "06_COMANDO", bold=True)
        text(layout, response, 75, y, 1.08, "02_TEXTO")

    add_rect(layout, 213, 104, 398, 163, "13_NOTAS")
    text(layout, "LIMITES DO EXERCICIO", 218, 154, 1.7, "13_NOTAS", bold=True)
    limits = (
        "A/B nao comprova independencia da rede nem separacao fisica.",
        "Sem selecao de protecoes, cabos, baterias, autonomia ou combustivel.",
        "Curto-circuito, seletividade, harmonicos e partida de GE pendentes.",
        "Nao atribui classificacao TIA Rated ou Tier ao conceito.",
    )
    for i, item in enumerate(limits):
        text(layout, "- " + item, 219, 142 - i * 11, 1.12, "02_TEXTO")


SHEETS = (
    {
        "filename": "01_arquitetura_eletrica_ab.dxf",
        "title": "ARQUITETURA ELETRICA DO DATA CENTER",
        "subtitle": "Dois caminhos A/B ate a carga de TI; origem e independencia pendentes de estudo",
        "scale": "S/ESC.",
        "notes": "13,8 kV, 2,0 MVA, 1,0 MW TI e PUE 1,50 sao hipoteses didaticas.\\P"
                "A independencia de alimentacoes, geradores e caminhos fisicos nao foi demonstrada.",
        "legend": "TR: transformador | QGBT: quadro BT | GE: gerador | ATS: transferencia | UPS: no-break | PDU: distribuicao aos racks | N+1: quatro modulos requeridos e um reserva",
        "draw": draw_architecture,
    },
    {
        "filename": "02_layout_salas_e_racks.dxf",
        "title": "LAYOUT CONCEITUAL DAS SALAS E RACKS",
        "subtitle": "Zonas eletricas e distribuicao A/B aos racks; planta sem escala nem levantamento",
        "scale": "S/ESC.",
        "notes": "A geometria de salas, acessos, compartimentacao e rotas e apenas representativa.\\P"
                "Ventilacao, seguranca, incendio e afastamentos dependem de coordenacao multidisciplinar.",
        "legend": "A/B: caminhos separados em estudo | R01-R06: racks de TI com dupla entrada | QMT: quadros MT | TR: transformador | UPS: inversor e banco de baterias",
        "draw": draw_layout,
    },
    {
        "filename": "03_balanco_potencia_contingencias.dxf",
        "title": "BALANCO DE POTENCIA E CONTINGENCIAS",
        "subtitle": "Premissas aritmeticas, N+1 modular e respostas funcionais propostas",
        "scale": "S/ESC.",
        "notes": "Conversoes kW/kVA usam fatores de potencia assumidos apenas para exemplo.\\P"
                "Autonomia, comportamento dinamico, seletividade e capacidade real nao foram validados.",
        "legend": "PUE: potencia total / TI | FP: fator de potencia | margem: capacidade nominal menos carga assumida | valores nao representam dimensionamento",
        "draw": draw_power_and_contingencies,
    },
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    warning = config["portfolio"]["warning"]
    if warning != WARNING_FALLBACK:
        # A configuracao central e a fonte do aviso obrigatorio.
        pass
    for index, spec in enumerate(SHEETS, 1):
        make_sheet(root, config, index, spec, spec["draw"])
        print(f"DXF gerado: {root / SLUG / 'fonte' / spec['filename']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
