"""Gera pranchas conceituais para a instalacao eletrica de uma clinica ambulatorial."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "21-instalacao-clinica-ambulatorial"
SCRIPTS_DIR = DEFAULT_ROOT / "scripts"
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
BOX_BLOCK = "P21_CAIXA_EQUIPAMENTO"
BOX_WIDTH = 57.0
BOX_HEIGHT = 37.0


def text(layout, value: str, x: float, y: float, h: float = 1.3,
         layer: str = "02_TEXTO", *, centered: bool = False,
         bold: bool = False) -> None:
    add_text(
        layout, value, (x, y), h, layer=layer,
        align=TextEntityAlignment.MIDDLE_CENTER if centered else TextEntityAlignment.LEFT,
        style=TITLE_STYLE if bold else TEXT_STYLE,
    )


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def rect(layout, x0: float, y0: float, x1: float, y1: float, layer: str) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)


def arrow(layout, a: tuple[float, float], b: tuple[float, float], layer: str,
          size: float = 1.5) -> None:
    line(layout, a, b, layer)
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(layout, (b[0] - ux * size + side * px * size * 0.55,
                      b[1] - uy * size + side * py * size * 0.55), b, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float, title: str,
        detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        title_height: float = 1.2, detail_height: float = 0.9) -> None:
    rect(layout, x0, y0, x1, y1, layer)
    text(layout, title, (x0 + x1) / 2, (y0 + y1) / 2 + (1.4 if detail else 0),
         title_height, layer, centered=True, bold=True)
    if detail:
        text(layout, detail, (x0 + x1) / 2, (y0 + y1) / 2 - 2,
             detail_height, "02_TEXTO", centered=True)


def symbol_light(layout, x: float, y: float, tag: str, *, emergency: bool = False) -> None:
    radius = 3.0 if emergency else 2.5
    layout.add_circle((x, y), radius, dxfattribs={"layer": "04_EQUIPAMENTOS"})
    if emergency:
        layout.add_circle((x, y), radius + 1.1, dxfattribs={"layer": "04_EQUIPAMENTOS"})
    line(layout, (x - 1.5, y - 1.5), (x + 1.5, y + 1.5), "04_EQUIPAMENTOS")
    line(layout, (x - 1.5, y + 1.5), (x + 1.5, y - 1.5), "04_EQUIPAMENTOS")
    text(layout, tag, x + 3.8, y + 2.2, 0.92, "02_TEXTO")


def symbol_outlet(layout, x: float, y: float, tag: str, *, ups: bool = False) -> None:
    if ups:
        rect(layout, x - 2.2, y - 2.2, x + 2.2, y + 2.2, "07_INSTRUMENTACAO")
    else:
        layout.add_circle((x, y), 2.2, dxfattribs={"layer": "07_INSTRUMENTACAO"})
    text(layout, tag, x + 3.0, y - 1.0, 0.88, "02_TEXTO")


def make_component_block(doc) -> None:
    if BOX_BLOCK in doc.blocks:
        return
    block = doc.blocks.new(name=BOX_BLOCK)
    block.add_lwpolyline([(0, 0), (BOX_WIDTH, 0), (BOX_WIDTH, BOX_HEIGHT), (0, BOX_HEIGHT)],
                         close=True, dxfattribs={"layer": "0"})
    block.add_line((0, 27), (BOX_WIDTH, 27), dxfattribs={"layer": "0"})
    for tag, point, height in (("TAG", (2.0, 31.5), 1.12),
                               ("TITULO", (2.0, 18.3), 1.22),
                               ("DADOS", (2.0, 7.2), 0.95)):
        block.add_attdef(tag, insert=point, text="",
                         dxfattribs={"height": height, "style": TEXT_STYLE, "layer": "0"})


def header(layout, title: str, subtitle: str) -> None:
    text(layout, title, 20, 275, 2.5, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.35, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 1.8, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.45, "13_NOTAS")
    rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66, 1.6, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.15, "13_NOTAS")
    rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90, 1.6, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.1, "12_LEGENDA")
    rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for label, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, label, x, 89.5, 1.25, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.2, "02_TEXTO", centered=True)


def draw_plan(layout) -> None:
    text(layout, "PLANTA ELETRICA ESQUEMATICA | PONTOS E CIRCUITOS A VALIDAR", 24, 253,
         1.35, "05_POTENCIA", bold=True)
    x0, x1, y0, y1 = 28.0, 392.0, 112.0, 251.0
    rect(layout, x0, y0, x1, y1, "11_ARQUITETURA")
    # Paredes internas, com aberturas simples para indicar portas sem detalhamento construtivo.
    for left, right in ((28, 76), (93, 138), (178, 220), (237, 284), (284, 329), (346, 392)):
        line(layout, (left, 183), (right, 183), "11_ARQUITETURA")
    for x, gaps in ((138, ((122, 137), (211, 226))),
                    (178, ((122, 137), (211, 226))),
                    (284, ((122, 137), (211, 226)))):
        start = y0
        for low, high in gaps:
            line(layout, (x, start), (x, low), "11_ARQUITETURA")
            start = high
        line(layout, (x, start), (x, y1), "11_ARQUITETURA")
    # Corredor longitudinal.
    text(layout, "CIRC.", 158, 242, 1.0, "11_ARQUITETURA", centered=True)
    room_labels = (
        (80, 243, "RECEPCAO / ESPERA"), (80, 153, "ADMINISTRACAO"),
        (230, 243, "CONSULTORIO A"), (338, 243, "CONSULTORIO B"),
        (230, 153, "SALA DE PROCEDIMENTO*"), (338, 153, "APOIO / ESTOQUE"),
    )
    for x, y, label in room_labels:
        text(layout, label, x, y, 1.05, "11_ARQUITETURA", centered=True, bold=True)
    # Caminhos de infraestrutura em tracejado conceitual e sem dimensoes.
    line(layout, (158, 121), (158, 239), "10_ELETROCALHAS")
    for y, left, right in ((229, 80, 158), (229, 158, 230), (229, 158, 338),
                           (145, 80, 158), (145, 158, 230), (145, 158, 338)):
        line(layout, (left, y), (right, y), "10_ELETROCALHAS")
    text(layout, "QD-CL", 158, 185, 1.0, "04_EQUIPAMENTOS", centered=True, bold=True)
    rect(layout, 148, 178, 168, 193, "04_EQUIPAMENTOS")
    # Luminarias e tomadas representadas para estudo de layout, sem contagem executiva.
    for x, y, tag in ((68, 220, "L1"), (108, 220, "L2"), (208, 220, "L3"),
                      (252, 220, "L4"), (310, 220, "L5"), (357, 220, "L6"),
                      (68, 145, "L7"), (208, 145, "L8"), (252, 145, "L9"),
                      (310, 145, "L10"), (357, 145, "L11")):
        symbol_light(layout, x, y, tag)
    for x, y, tag in ((48, 196, "T1"), (118, 196, "T2"), (192, 196, "T3"),
                      (270, 196, "T4"), (297, 196, "T5"), (378, 196, "T6"),
                      (193, 127, "T7"), (270, 127, "T8"), (298, 127, "T9"),
                      (378, 127, "T10")):
        symbol_outlet(layout, x, y, tag)
    symbol_light(layout, 158, 166, "LE1", emergency=True)
    symbol_light(layout, 158, 225, "LE2", emergency=True)
    symbol_outlet(layout, 270, 208, "U1", ups=True)
    symbol_outlet(layout, 378, 208, "U2", ups=True)
    text(layout, "ARQUITETURA INDICATIVA, SEM ESCALA. CIRCUITOS, ROTAS, DEMANDA E GRUPOS MEDICOS PENDENTES DE AVALIACAO.",
         24, 105, 0.95, "13_NOTAS")


def draw_unifilar(layout) -> None:
    text(layout, "FONTES E DISTRIBUICAO | 380/220 V, 60 Hz*", 24, 253,
         1.4, "05_POTENCIA", bold=True)
    top_y = 211.0
    units = (
        (24, "PCC-01", "REDE BT", "380/220 V*"),
        (95, "MED-01", "MEDICAO", "arranjo a definir"),
        (166, "QGBT-CL", "QUADRO GERAL", "dados a calcular"),
        (337, "QD-N", "QUADRO NORMAL", "cargas gerais"),
    )
    for x, tag, title, detail in units:
        block = layout.add_blockref(BOX_BLOCK, (x, top_y), dxfattribs={"layer": "04_EQUIPAMENTOS"})
        block.add_auto_attribs({"TAG": tag, "TITULO": title, "DADOS": detail})
    arrow(layout, (81, 229.5), (95, 229.5), "05_POTENCIA", 1.0)
    arrow(layout, (152, 229.5), (166, 229.5), "05_POTENCIA", 1.0)
    arrow(layout, (223, 229.5), (337, 229.5), "05_POTENCIA", 1.4)

    # Barramento de distribuicao normal alimenta a entrada normal do QTA e a UPS.
    line(layout, (194.5, 211), (194.5, 198), "05_POTENCIA")
    line(layout, (94.5, 198), (274.5, 198), "05_POTENCIA")
    arrow(layout, (94.5, 198), (94.5, 137), "05_POTENCIA", 1.2)
    arrow(layout, (274.5, 198), (274.5, 194), "05_POTENCIA", 1.2)
    text(layout, "BARRAMENTO NORMAL (ESQUEMATICO)", 184, 201, 0.95, "05_POTENCIA", centered=True)

    # Quadros inferiores: UPS e gerador/transferencia com cargas ainda por classificar.
    ups = layout.add_blockref(BOX_BLOCK, (66, 100), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    ups.add_auto_attribs({"TAG": "UPS-CL", "TITULO": "UPS", "DADOS": "autonomia a definir"})
    qdu = layout.add_blockref(BOX_BLOCK, (337, 100), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    qdu.add_auto_attribs({"TAG": "QD-U", "TITULO": "QUADRO UPS", "DADOS": "cargas por definir"})
    ats = layout.add_blockref(BOX_BLOCK, (246, 157), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    ats.add_auto_attribs({"TAG": "QTA-CL", "TITULO": "TRANSFERENCIA", "DADOS": "logica a estudar"})
    gen = layout.add_blockref(BOX_BLOCK, (246, 100), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    gen.add_auto_attribs({"TAG": "GE-CL", "TITULO": "GERADOR", "DADOS": "potencia pendente"})
    qde = layout.add_blockref(BOX_BLOCK, (337, 157), dxfattribs={"layer": "04_EQUIPAMENTOS"})
    qde.add_auto_attribs({"TAG": "QD-E", "TITULO": "QUADRO RESERVA", "DADOS": "cargas a classificar"})

    # Saida da UPS contorna os equipamentos pela faixa livre acima do carimbo.
    line(layout, (123, 118.5), (123, 98), "05_POTENCIA")
    line(layout, (123, 98), (365, 98), "05_POTENCIA")
    arrow(layout, (365, 98), (365, 100), "05_POTENCIA", 0.9)
    # Gerador alimenta a segunda entrada da transferencia; a saida segue ao quadro QD-E.
    arrow(layout, (274.5, 137), (274.5, 157), "06_COMANDO", 1.2)
    arrow(layout, (303, 175.5), (337, 175.5), "05_POTENCIA", 1.1)
    text(layout, "ENTRADA GE", 281, 145, 0.9, "06_COMANDO")


def draw_matrix(layout) -> None:
    text(layout, "MATRIZ PRELIMINAR DE CONTINUIDADE E SEQUENCIA DE TRANSFERENCIA", 24, 253,
         1.3, "13_NOTAS", bold=True)
    columns = ((24, 105, "GRUPO DE CARGA"), (105, 151, "NORMAL"),
               (151, 203, "GERADOR"), (203, 252, "UPS"),
               (252, 396, "DECISAO / EVIDENCIA PENDENTE"))
    top, header_bottom = 246.0, 235.0
    for left, right, label in columns:
        rect(layout, left, header_bottom, right, top, "12_LEGENDA")
        text(layout, label, (left + right) / 2, 240.5, 1.05,
             "12_LEGENDA", centered=True, bold=True)
    rows = (
        ("Iluminacao geral", "SIM", "A ESTUDAR", "NAO PREV.", "levantamento, calculo luminotecnico e circuito"),
        ("Iluminacao de emergencia", "SIM", "A DEFINIR", "A DEFINIR", "projeto de incendio, autonomia e ensaios"),
        ("Tomadas de uso geral", "SIM", "A DEFINIR", "NAO PREV.", "uso previsto, demanda e protecoes"),
        ("Equipamento eletromedico", "SIM", "A DEFINIR", "A DEFINIR", "classificacao do local e manual do fabricante"),
        ("Rede, dados e controle", "SIM", "PROPOSTA", "PROPOSTA", "autonomia, segregacao e compatibilidade"),
        ("Climatizacao", "SIM", "A ESTUDAR", "NAO PREV.", "carga, partida e prioridade operacional"),
    )
    row_h = (header_bottom - 174.0) / len(rows)
    for index, values in enumerate(rows):
        y_top = header_bottom - index * row_h
        y_bottom = y_top - row_h
        for (left, right, _), value in zip(columns, values):
            rect(layout, left, y_bottom, right, y_top, "02_TEXTO")
            text(layout, value, left + 1.4, (y_top + y_bottom) / 2, 1.05, "02_TEXTO")

    text(layout, "SEQUENCIA CONCEITUAL — SEM TEMPORIZACAO OU LOGICA DE CONTROLE DEFINIDAS", 24, 163,
         1.0, "06_COMANDO", bold=True)
    steps = (
        (24, "REDE NORMAL", "QGBT energizado"),
        (99, "FALHA", "deteccao a definir"),
        (174, "PARTIDA GE", "comando e permissivos"),
        (249, "TRANSFERENCIA", "QTA apos condicao estavel"),
        (324, "RETORNO", "retransferencia a estudar"),
    )
    for x, title, detail in steps:
        rect(layout, x, 124, x + 65, 153, "06_COMANDO")
        text(layout, title, x + 32.5, 144, 1.0, "06_COMANDO", centered=True, bold=True)
        text(layout, detail, x + 32.5, 132, 0.9, "02_TEXTO", centered=True)
    for x in (89, 164, 239, 314):
        arrow(layout, (x, 138.5), (x + 9, 138.5), "06_COMANDO", 0.9)
    rect(layout, 24, 101, 396, 117, "13_NOTAS")
    text(layout, "PENDENTE: classificar ambientes e cargas com responsaveis clinico, eletrico e de incendio; definir seletividade, curto-circuito,"
         " aterramento, protecoes, autonomia, potencia do gerador/UPS, ventilacao, ensaios e aprovacoes locais.",
         27, 108.5, 0.95, "13_NOTAS")


SHEETS = (
    {
        "filename": "01_planta_eletrica_clinica.dxf",
        "title": "INSTALACAO ELETRICA DE CLINICA AMBULATORIAL",
        "subtitle": "Planta esquematica de iluminacao, tomadas, quadro e infraestrutura aparente",
        "scale": "S/ESC.",
        "notes": "Arquitetura funcional ilustrativa; nao representa programa aprovado.\\P"
                "Pontos, circuitos, acessibilidade, grupos medicos e rotas devem ser revistos no local.",
        "legend": "L: luminaria | LE: luminaria dupla de emergencia proposta | T: tomada geral | U: tomada UPS proposta | linhas verdes: rota conceitual",
        "draw": draw_plan,
    },
    {
        "filename": "02_unifilar_fontes_quadro_clinica.dxf",
        "title": "FONTES E QUADROS DA CLINICA AMBULATORIAL",
        "subtitle": "Distribuicao normal, transferencia para gerador e ramal UPS para cargas selecionadas",
        "scale": "S/ESC.",
        "notes": "Tensao de 380/220 V e topologia sao premissas de estudo.\\P"
                "Poderes de corte, secao, demanda, aterramento e ajustes nao calculados.",
        "legend": "PCC: ponto de conexao | QGBT: quadro geral | QTA: transferencia | GE: grupo gerador | UPS: fonte ininterrupta | QD: quadro de distribuicao",
        "draw": draw_unifilar,
    },
    {
        "filename": "03_matriz_continuidade_e_transferencia.dxf",
        "title": "CONTINUIDADE DE SERVICO E TRANSFERENCIA DE FONTES",
        "subtitle": "Cargas propostas, evidencias necessarias e sequencia operacional ainda nao validada",
        "scale": "S/ESC.",
        "notes": "Matriz e sequencia sao pontos de partida, sem classificacao clinica ou requisito de autonomia definido.\\P"
                "Confirmar normas, atividades assistenciais e exigencias da vigilância sanitaria local.",
        "legend": "SIM: presente no unifilar | A ESTUDAR: sem decisao | PROPOSTA: hipotese nao validada | GE: gerador | UPS: fonte ininterrupta",
        "draw": draw_matrix,
    },
)


def make_sheet(root: Path, config: dict, number: int, spec: dict) -> None:
    geometry = SheetGeometry.from_config(config)
    doc = configure_document(config, limits=(geometry.width, geometry.height), layer_color_overrides=PROJECT_PRINT_LAYER_COLORS)
    metadata = doc.ezdxf_metadata()
    metadata["PORTFOLIO_PROJECT"] = SLUG
    metadata["PORTFOLIO_REVISION"] = REVISION
    metadata["PORTFOLIO_SHEET"] = f"{number:02d}/03"
    metadata["PORTFOLIO_UNITS"] = "mm"
    define_title_block(doc)
    make_component_block(doc)
    layout = doc.modelspace()
    add_frame(layout, geometry)
    header(layout, spec["title"], spec["subtitle"])
    spec["draw"](layout)
    footer(layout, spec, config["portfolio"]["warning"])
    insert = layout.add_blockref(TITLE_BLOCK_NAME, (230, 10), dxfattribs={"layer": "01_CARIMBO"})
    insert.add_auto_attribs({
        "TITULO": spec["title"], "AUTOR": config["portfolio"]["author"],
        "DATA": DATE, "REVISAO": REVISION, "PRANCHA": f"{number:02d}/03",
        "ARQUIVO": spec["filename"], "UNIDADES": "mm", "ESCALA": spec["scale"],
        "FOLHA": "A3", "STATUS": "CONCEIT.",
    })
    output = root / SLUG / "fonte" / spec["filename"]
    output.parent.mkdir(parents=True, exist_ok=True)
    prepare_deterministic_write(doc)
    with output.open("wt", encoding="utf-8", newline="\n") as stream:
        doc.write(stream)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    for index, spec in enumerate(SHEETS, 1):
        make_sheet(root, config, index, spec)
        print(f"DXF gerado: {root / SLUG / 'fonte' / spec['filename']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
