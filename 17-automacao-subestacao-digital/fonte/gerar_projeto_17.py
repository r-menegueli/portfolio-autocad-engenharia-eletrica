"""Gera tres pranchas conceituais de automacao digital IEC 61850 para subestacao."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "17-automacao-subestacao-digital"
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


def text(layout, value: str, x: float, y: float, h: float = 1.6,
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


def line(layout, start: tuple[float, float], end: tuple[float, float], layer: str) -> None:
    add_line(layout, start, end, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float,
        title: str, detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        title_height: float = 1.45, detail_height: float = 1.12) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    text(layout, title, cx, cy + (2 if detail else 0), title_height, layer, centered=True, bold=True)
    if detail:
        text(layout, detail, cx, cy - 2, detail_height, "02_TEXTO", centered=True)


def arrow(layout, start: tuple[float, float], end: tuple[float, float], layer: str,
          size: float = 1.8) -> None:
    line(layout, start, end, layer)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(layout,
             (end[0] - ux * size + side * px * size * 0.55,
              end[1] - uy * size + side * py * size * 0.55),
             end, layer)


def header(layout, title: str, subtitle: str) -> None:
    text(layout, title, 20, 275, 2.8, "02_TEXTO", bold=True)
    text(layout, subtitle, 20, 269, 1.5, "02_TEXTO")
    line(layout, (20, 265), (400, 265), "03_COTAS")


def footer(layout, spec: dict, warning: str) -> None:
    add_rect(layout, 18, 18, 224, 46, "13_NOTAS")
    text(layout, "AVISO OBRIGATORIO", 22, 42, 1.9, "13_NOTAS", bold=True)
    add_mtext(layout, warning, (22, 37), 198, 1.5, "13_NOTAS")
    add_rect(layout, 18, 50, 224, 70, "13_NOTAS")
    text(layout, "NOTAS DA PRANCHA", 22, 66, 1.75, "13_NOTAS", bold=True)
    add_mtext(layout, spec["notes"], (22, 62), 198, 1.3, "13_NOTAS")
    add_rect(layout, 18, 74, 224, 94, "12_LEGENDA")
    text(layout, "LEGENDA", 22, 90, 1.75, "12_LEGENDA", bold=True)
    add_mtext(layout, spec["legend"], (22, 86), 198, 1.25, "12_LEGENDA")
    add_rect(layout, 230, 72, 410, 94, "01_CARIMBO")
    line(layout, (230, 86), (410, 86), "01_CARIMBO")
    for x in (248, 280, 352):
        line(layout, (x, 72), (x, 94), "01_CARIMBO")
    for label, x in (("REV.", 239), ("DATA", 264), ("DESCRICAO", 316), ("RESP.", 381)):
        text(layout, label, x, 89.5, 1.35, "01_CARIMBO", centered=True, bold=True)
    for value, x in ((REVISION, 239), (DATE, 264), ("EMISSAO INICIAL", 316), ("R.E.M.M.", 381)):
        text(layout, value, x, 78.5, 1.3, "02_TEXTO", centered=True)


def make_sheet(root: Path, config: dict, number: int, spec: dict) -> None:
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


def draw_single_line(layout) -> None:
    text(layout, "SUBESTACAO 138 / 13,8 kV* | DOIS CIRCUITOS DE LINHA | UM TRANSFORMADOR*", 24, 252, 1.45, "05_POTENCIA", bold=True)
    box(layout, 25, 225, 63, 247, "LINHA L01", "138 kV*", detail_height=1.0)
    box(layout, 72, 225, 112, 247, "52-L01", "DJ", detail_height=1.0)
    box(layout, 25, 177, 63, 199, "LINHA L02", "138 kV*", detail_height=1.0)
    box(layout, 72, 177, 112, 199, "52-L02", "DJ", detail_height=1.0)
    box(layout, 133, 208, 171, 252, "BARRA A", "138 kV*", detail_height=1.15)
    box(layout, 186, 208, 223, 252, "TR-01", "25 MVA | 138/13,8 kV*", detail_height=1.05)
    box(layout, 238, 176, 275, 252, "BARRA B", "13,8 kV*", detail_height=1.15)
    for y in (236, 188):
        box(layout, 301, y - 11, 344, y + 11, f"52-F0{1 if y == 236 else 2}", "DJ", detail_height=1.0)
        box(layout, 357, y - 11, 400, y + 11, f"ALIM. F0{1 if y == 236 else 2}", "13,8 kV*", title_height=1.25, detail_height=1.0)
        arrow(layout, (344, y), (357, y), "05_POTENCIA", 1.25)
    arrow(layout, (63, 236), (72, 236), "05_POTENCIA", 1.25)
    arrow(layout, (112, 236), (133, 236), "05_POTENCIA", 1.25)
    arrow(layout, (63, 188), (72, 188), "05_POTENCIA", 1.25)
    line(layout, (112, 188), (124, 188), "05_POTENCIA")
    arrow(layout, (124, 188), (133, 214), "05_POTENCIA", 1.25)
    arrow(layout, (171, 230), (186, 230), "05_POTENCIA", 1.25)
    arrow(layout, (223, 230), (238, 230), "05_POTENCIA", 1.25)
    line(layout, (275, 188), (287, 188), "05_POTENCIA")
    line(layout, (287, 188), (287, 236), "05_POTENCIA")
    arrow(layout, (287, 236), (301, 236), "05_POTENCIA", 1.25)
    arrow(layout, (287, 188), (301, 188), "05_POTENCIA", 1.25)
    text(layout, "ASSOCIACAO FUNCIONAL DOS IEDS", 25, 159, 1.45, "07_INSTRUMENTACAO", bold=True)
    ieds = (
        (25, "IED-L01 / L02", "linha"),
        (71, "IED-T01", "transformador"),
        (117, "IED-87B", "barras"),
        (163, "IED-F01 / F02", "alimentadores"),
        (209, "IED-BAY-L01 / T01", "controle de bay"),
    )
    for x0, title, detail in ieds:
        box(layout, x0, 126, x0 + 42, 150, title, detail, layer="07_INSTRUMENTACAO", title_height=0.98, detail_height=0.92)
    box(layout, 259, 126, 397, 150, "SAS IEC 61850", "rede de estacao + rede de processo", layer="07_INSTRUMENTACAO", title_height=1.4, detail_height=1.05)
    text(layout, "* Tensoes e potencia sao premissas de diagrama; nao definem especificacao de equipamentos.", 25, 108, 1.08, "13_NOTAS")


def draw_network(layout) -> None:
    add_rect(layout, 22, 168, 398, 257, "07_INSTRUMENTACAO")
    text(layout, "REDE DE PROCESSO | SV E GOOSE | VIRTUAL LAN / REDUNDANCIA A DEFINIR", 27, 247, 1.45, "07_INSTRUMENTACAO", bold=True)
    line(layout, (26, 240), (394, 240), "07_INSTRUMENTACAO")
    mus = ((28, "MU-L01"), (77, "MU-T01"), (126, "MU-B01"), (175, "MU-F01/F02"))
    for x, tag in mus:
        box(layout, x, 207, x + 41, 232, tag, "TC/TP*", layer="04_EQUIPAMENTOS", title_height=1.22, detail_height=1.0)
        arrow(layout, (x + 20.5, 207), (x + 20.5, 193), "08_CABOS", 1.2)
    line(layout, (48, 193), (246, 193), "08_CABOS")
    box(layout, 246, 180, 289, 209, "SW-PROC-01", "Ethernet", layer="07_INSTRUMENTACAO", title_height=1.15, detail_height=1.0)
    box(layout, 315, 200, 390, 232, "IEDs DE PROTECAO", "SV / GOOSE / XCBR", layer="07_INSTRUMENTACAO", title_height=1.25, detail_height=1.0)
    arrow(layout, (289, 193), (315, 216), "08_CABOS", 1.2)
    text(layout, "SV: amostras de TC/TP para funcoes de protecao; fluxo e dataset dependem do MU/IED selecionado.", 28, 177, 1.05, "13_NOTAS")

    add_rect(layout, 22, 104, 398, 161, "06_COMANDO")
    text(layout, "REDE DE ESTACAO | MMS, SUPERVISAO E INTERTRAVAMENTOS GOOSE", 27, 151, 1.4, "06_COMANDO", bold=True)
    box(layout, 28, 115, 94, 140, "HMI-01 / GW-01", "SCADA / telecontrole", layer="07_INSTRUMENTACAO", title_height=1.15, detail_height=0.98)
    box(layout, 128, 115, 183, 140, "SW-STA-01", "MMS + GOOSE", layer="07_INSTRUMENTACAO", title_height=1.2, detail_height=1.0)
    box(layout, 190, 115, 245, 140, "ENG-01 / TS-01", "SCL / tempo", layer="07_INSTRUMENTACAO", title_height=1.1, detail_height=0.98)
    box(layout, 277, 115, 391, 140, "IEDs DE BAY", "controle, relatorios e estados", layer="07_INSTRUMENTACAO", title_height=1.2, detail_height=0.98)
    arrow(layout, (94, 127), (128, 127), "08_CABOS", 1.2)
    line(layout, (183, 127), (190, 127), "08_CABOS")
    arrow(layout, (245, 127), (277, 127), "08_CABOS", 1.2)
    text(layout, "Segmentacao, sincronismo, seguranca, topologia e comportamento em falha devem ser especificados e testados.", 28, 108, 1.05, "13_NOTAS")


def draw_matrix(layout) -> None:
    add_rect(layout, 22, 169, 208, 257, "12_LEGENDA")
    text(layout, "MATRIZ CONCEITUAL DE GOOSE", 27, 248, 1.45, "12_LEGENDA", bold=True)
    line(layout, (26, 242), (204, 242), "12_LEGENDA")
    columns = ((29, "ID"), (78, "PUBLICADOR"), (130, "ASSINANTE"), (195, "ACAO"))
    for x, label in columns:
        text(layout, label, x, 235, 1.02, "12_LEGENDA", centered=True, bold=True)
    rows = (
        ("G-TR-L01", "IED-L01", "IED-BAY-L01", "TRIP*"),
        ("G-BF-F01", "IED-F01", "IED-87B", "FALHA DJ*"),
        ("G-ILK-L02", "IED-87B", "IED-L02", "PERMISSIVO*"),
        ("G-BF-F02", "IED-F02", "IED-87B", "FALHA DJ*"),
        ("G-TR-T01", "IED-T01", "IED-BAY-T01", "TRIP*"),
    )
    for index, row in enumerate(rows):
        y = 224 - index * 12
        line(layout, (26, y - 4), (204, y - 4), "03_COTAS")
        for (x, _), value in zip(columns, row):
            text(layout, value, x, y, 0.98, "02_TEXTO", centered=True)
    text(layout, "* Intencao funcional ilustrativa; nao fixa logica, tempos, ajustes ou cablagem de trip.", 27, 173, 0.98, "13_NOTAS")

    add_rect(layout, 216, 169, 398, 257, "12_LEGENDA")
    text(layout, "VERIFICACOES DE ENGENHARIA E TESTE", 221, 248, 1.45, "12_LEGENDA", bold=True)
    checks = (
        "Revisar datasets, nomes, assinaturas e subscricoes GOOSE.",
        "Validar SCL e consistencia entre SSD, SCD e CID do fabricante.",
        "Testar perda de SV/GOOSE, qualidade, estado seguro e alarmes.",
        "Confirmar sincronismo, redundancia e comportamento de switches.",
        "Executar FAT/SAT com matriz aprovada e protecao coordenada.",
    )
    for index, item in enumerate(checks):
        y = 230 - index * 13
        line(layout, (220, y - 4), (394, y - 4), "03_COTAS")
        text(layout, item, 224, y, 1.05, "02_TEXTO")

    add_rect(layout, 22, 104, 208, 163, "07_INSTRUMENTACAO")
    text(layout, "FLUXO DE CONFIGURACAO SCL", 27, 154, 1.4, "07_INSTRUMENTACAO", bold=True)
    sequence = (("ICD", "capacidade IED"), ("SSD", "requisitos do sistema"), ("SCD", "integracao da estacao"), ("CID", "arquivo do IED"))
    for index, (tag, desc) in enumerate(sequence):
        x = 28 + index * 44
        box(layout, x, 119, x + 38, 143, tag, desc, layer="07_INSTRUMENTACAO", title_height=1.2, detail_height=0.85)
        if index < len(sequence) - 1:
            arrow(layout, (x + 38, 131), (x + 44, 131), "06_COMANDO", 1.0)

    add_rect(layout, 216, 104, 398, 163, "13_NOTAS")
    text(layout, "LIMITES DO ESTUDO", 221, 154, 1.4, "13_NOTAS", bold=True)
    limits = (
        "Sem arquivos SCL validos de fabricante ou IED selecionado.",
        "Sem ajustes, estudos de protecao ou analise de tempo real.",
        "Sem definicao de PRP/HSR, VLANs, PTP ou requisitos de ciberseguranca.",
        "Sem FAT/SAT real; plano e sinais sao itens para futura engenharia.",
    )
    for index, item in enumerate(limits):
        text(layout, "- " + item, 222, 141 - index * 8, 0.92, "02_TEXTO")


SHEETS = (
    {
        "filename": "01_unifilar_sas_ied.dxf",
        "title": "DIAGRAMA FUNCIONAL DA AUTOMACAO DA SUBESTACAO",
        "subtitle": "Baia eletrica conceitual, IEDs de protecao e interface do sistema SAS",
        "scale": "S/ESC.",
        "notes": "Tensoes, arranjo e equipamento sao hipoteses de estudo.\\P"
                "As protecoes e associacoes IED nao constituem filosofia ou ajuste aprovado.",
        "legend": "SAS: sistema de automacao | IED: dispositivo eletronico inteligente | DJ: disjuntor | TR: transformador | tag 52: identificacao funcional ilustrativa",
        "draw": draw_single_line,
    },
    {
        "filename": "02_rede_iec61850.dxf",
        "title": "ARQUITETURA DAS REDES IEC 61850",
        "subtitle": "Rede de processo, rede de estacao, interfaces MU/IED e servicos de supervisao",
        "scale": "S/ESC.",
        "notes": "SV, GOOSE e MMS sao fluxos conceituais; datasets e engenharia de comunicacao pendentes.\\P"
                "Desenho nao comprova interoperabilidade, latencia, redundancia ou ciberseguranca.",
        "legend": "MU: merging unit | SV: sampled values | GOOSE: eventos entre IEDs | MMS: supervisao/controle | SCL: linguagem de configuracao IEC 61850",
        "draw": draw_network,
    },
    {
        "filename": "03_matriz_goose_testes.dxf",
        "title": "MATRIZ DE SINAIS E PLANO DE VERIFICACAO",
        "subtitle": "Trocas GOOSE de exemplo, ciclo SCL e verificacoes FAT/SAT propostas",
        "scale": "S/ESC.",
        "notes": "Matriz funcional e plano de teste sao exemplos para revisao de engenharia.\\P"
                "Nao operar equipamento real com os sinais, permissivos ou eventos ilustrados.",
        "legend": "FAT: teste de aceitacao em fabrica | SAT: teste de aceitacao em campo | SSD/SCD/CID/ICD: arquivos de engenharia IEC 61850",
        "draw": draw_matrix,
    },
)


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
