"""Gera tres pranchas conceituais de compensacao de reativos e qualidade de energia."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
SLUG = "18-compensacao-reativos-qualidade-energia"
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
    add_text(layout, value, (x, y), h, layer=layer,
             align=TextEntityAlignment.MIDDLE_CENTER if centered else TextEntityAlignment.LEFT,
             style=TITLE_STYLE if bold else TEXT_STYLE)


def line(layout, a: tuple[float, float], b: tuple[float, float], layer: str) -> None:
    add_line(layout, a, b, layer)


def box(layout, x0: float, y0: float, x1: float, y1: float, title: str,
        detail: str = "", *, layer: str = "04_EQUIPAMENTOS",
        title_height: float = 1.45, detail_height: float = 1.1) -> None:
    add_rect(layout, x0, y0, x1, y1, layer)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    text(layout, title, cx, cy + (2 if detail else 0), title_height, layer, centered=True, bold=True)
    if detail:
        text(layout, detail, cx, cy - 2, detail_height, "02_TEXTO", centered=True)


def arrow(layout, a: tuple[float, float], b: tuple[float, float], layer: str, size: float = 1.8) -> None:
    line(layout, a, b, layer)
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    for side in (-1, 1):
        line(layout, (b[0] - ux * size + side * px * size * 0.55,
                      b[1] - uy * size + side * py * size * 0.55), b, layer)


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
    text(layout, "INSTALACAO INDUSTRIAL | 600 kW* | 400 V* | FP BASE 0,80*", 24, 252, 1.5, "05_POTENCIA", bold=True)
    box(layout, 25, 213, 73, 245, "REDE MT", "13,8 kV*", detail_height=1.05)
    box(layout, 90, 213, 143, 245, "TR-01", "1,0 MVA | 13,8/0,4 kV*", detail_height=1.0)
    box(layout, 160, 213, 220, 245, "QGBT-01", "400 V*", detail_height=1.05)
    arrow(layout, (73, 229), (90, 229), "05_POTENCIA", 1.3)
    arrow(layout, (143, 229), (160, 229), "05_POTENCIA", 1.3)
    line(layout, (220, 229), (238, 229), "05_POTENCIA")
    line(layout, (238, 181), (238, 246), "05_POTENCIA")
    line(layout, (238, 246), (238, 252), "05_POTENCIA")
    line(layout, (238, 252), (361, 252), "05_POTENCIA")
    arrow(layout, (361, 252), (361, 245), "05_POTENCIA", 1.1)
    box(layout, 253, 225, 310, 248, "CARGAS LINEARES", "400 kW*", detail_height=1.05)
    box(layout, 253, 185, 310, 208, "CARGAS COM VFD", "200 kW*", detail_height=1.05)
    arrow(layout, (238, 236), (253, 236), "05_POTENCIA", 1.25)
    arrow(layout, (238, 196), (253, 196), "05_POTENCIA", 1.25)
    box(layout, 325, 211, 397, 245, "BC-01", "300 kvar | 12 x 25*", detail_height=1.0)
    text(layout, "Q1...Q12", 361, 219, 1.05, "06_COMANDO", centered=True)
    box(layout, 25, 151, 87, 180, "CT-01 / PM-01", "PCC / analisador", layer="07_INSTRUMENTACAO", title_height=1.1, detail_height=1.0)
    box(layout, 111, 151, 173, 180, "RC-01", "controle por kvar/FP", layer="07_INSTRUMENTACAO", title_height=1.25, detail_height=1.0)
    arrow(layout, (87, 165), (111, 165), "07_INSTRUMENTACAO", 1.2)
    line(layout, (173, 165), (182, 165), "06_COMANDO")
    line(layout, (182, 165), (182, 182), "06_COMANDO")
    line(layout, (182, 182), (310, 182), "06_COMANDO")
    arrow(layout, (310, 182), (325, 211), "06_COMANDO", 1.1)
    box(layout, 191, 151, 397, 180, "ESTUDO DE HARMONICOS", "medir no PCC; filtro/reator nao selecionado", layer="13_NOTAS", title_height=1.35, detail_height=1.1)
    text(layout, "* Valores didaticos; nao substituem levantamento, analise de ressonancia ou especificacao de capacitor.", 25, 108, 1.05, "13_NOTAS")


def draw_calculation(layout) -> None:
    add_rect(layout, 22, 169, 208, 257, "12_LEGENDA")
    text(layout, "CORRECAO ARITMETICA DE FP", 27, 248, 1.45, "12_LEGENDA", bold=True)
    line(layout, (26, 242), (204, 242), "12_LEGENDA")
    rows = (
        ("P ativa assumida", "600 kW"),
        ("FP inicial", "0,80 indutivo"),
        ("Q inicial", "450,0 kvar"),
        ("FP alvo de estudo", "0,95"),
        ("Q apos correcao alvo", "197,2 kvar"),
        ("Qc calculado", "252,8 kvar"),
        ("Banco representado", "300 kvar / 12 x 25"),
        ("10 estagios ativos", "250 kvar"),
    )
    for index, (label, value) in enumerate(rows):
        y = 233 - index * 8.4
        line(layout, (26, y - 3.5), (204, y - 3.5), "03_COTAS")
        text(layout, label, 29, y, 1.25, "02_TEXTO")
        text(layout, value, 199, y, 1.25, "02_TEXTO", centered=True)

    add_rect(layout, 216, 169, 398, 257, "12_LEGENDA")
    text(layout, "SENSIBILIDADE DE CORRENTE NO QGBT", 221, 248, 1.4, "12_LEGENDA", bold=True)
    line(layout, (220, 242), (394, 242), "12_LEGENDA")
    text(layout, "I = S / (raiz(3) x V)", 225, 230, 1.4, "05_POTENCIA", bold=True)
    columns = ((227, "ESTADO"), (292, "S"), (357, "I @ 400 V"), (390, "FP"))
    for x, label in columns:
        text(layout, label, x, 217, 0.98, "12_LEGENDA", centered=True, bold=True)
    scenarios = (
        ("Sem banco", "750 kVA", "1082,5 A", "0,80"),
        ("250 kvar", "632,5 kVA", "912,9 A", "0,949"),
        ("275 kvar", "625,0 kVA", "902,1 A", "0,960"),
    )
    for index, row in enumerate(scenarios):
        y = 204 - index * 15
        line(layout, (220, y - 4), (394, y - 4), "03_COTAS")
        for (x, _), value in zip(columns, row):
            text(layout, value, x, y, 1.08, "02_TEXTO", centered=True)

    add_rect(layout, 22, 104, 208, 163, "07_INSTRUMENTACAO")
    text(layout, "EQUACOES DO CASO BASE", 27, 154, 1.4, "07_INSTRUMENTACAO", bold=True)
    formulas = (
        "Q1 = P x tan(arccos(FP1)) = 450 kvar",
        "Q2 = P x tan(arccos(0,95)) = 197,2 kvar",
        "Qc = Q1 - Q2 = 252,8 kvar",
        "S2 = raiz(P^2 + (Q1 - Qc)^2)",
    )
    for index, formula in enumerate(formulas):
        text(layout, formula, 29, 139 - index * 8, 1.05, "02_TEXTO")

    add_rect(layout, 216, 104, 398, 163, "13_NOTAS")
    text(layout, "INTERPRETACAO E LIMITE", 221, 154, 1.4, "13_NOTAS", bold=True)
    notes = (
        "10 estagios deixam Q residual ~200 kvar e FP ~0,949.",
        "11 estagios elevam FP a ~0,960 no ponto de carga assumido.",
        "Carga menor exige menos estagios para evitar sobrecompensacao.",
        "Controlador, degraus e limites dependem do perfil horario medido.",
    )
    for index, item in enumerate(notes):
        text(layout, "- " + item, 222, 141 - index * 8, 0.96, "02_TEXTO")


def draw_monitoring(layout) -> None:
    add_rect(layout, 22, 169, 208, 257, "07_INSTRUMENTACAO")
    text(layout, "CADEIA DE MEDICAO E CONTROLE", 27, 248, 1.45, "07_INSTRUMENTACAO", bold=True)
    line(layout, (26, 242), (204, 242), "07_INSTRUMENTACAO")
    steps = (
        ("CT/TP", "amostras no PCC"),
        ("PM-01", "P, Q, FP, V, I"),
        ("RC-01", "alvo e banda morta"),
        ("BC-01", "degraus 25 kvar*"),
    )
    for index, (tag, detail) in enumerate(steps):
        x = 28 + index * 43
        box(layout, x, 203, x + 37, 230, tag, detail, layer="07_INSTRUMENTACAO", title_height=1.15, detail_height=0.95)
        if index < len(steps) - 1:
            arrow(layout, (x + 37, 216.5), (x + 43, 216.5), "06_COMANDO", 0.95)
    controls = (
        "Confirmar polaridade e relacao dos TCs/TPs no PCC.",
        "Definir banda, temporizacao, rodizio e limite de manobras.",
        "Alarmar FP capacitivo, perda de sinal e sobretemperatura.",
        "Bloquear ou reduzir banco perante ressonancia/condicao anormal.",
    )
    for index, item in enumerate(controls):
        text(layout, "- " + item, 28, 190 - index * 8, 1.0, "02_TEXTO")

    add_rect(layout, 216, 169, 398, 257, "12_LEGENDA")
    text(layout, "LEVANTAMENTO DE QUALIDADE DE ENERGIA", 221, 248, 1.4, "12_LEGENDA", bold=True)
    measurements = (
        "Medir tensao/corrente no PCC em operacao representativa.",
        "Registrar espectro harmonico, inter-harmonicos e THD.",
        "Registrar estados dos VFDs, carga, degraus e horario.",
        "Estimar impedancia da fonte e cenarios de curto-circuito.",
        "Avaliar ressonancia antes de definir reatores ou filtros.",
    )
    for index, item in enumerate(measurements):
        y = 230 - index * 13
        line(layout, (220, y - 4), (394, y - 4), "03_COTAS")
        text(layout, item, 224, y, 1.02, "02_TEXTO")

    add_rect(layout, 22, 104, 208, 163, "12_LEGENDA")
    text(layout, "ESTADOS DO REGULADOR", 27, 154, 1.4, "12_LEGENDA", bold=True)
    states = (("AUTO", "controla Q/FP dentro da banda"), ("MANUAL", "comando local autorizado"), ("BLOQUEIO", "alarme ou permissivo ausente"), ("MANUTENCAO", "bloqueio e descarga confirmados"))
    for index, (state, desc) in enumerate(states):
        y = 141 - index * 8
        text(layout, state, 29, y, 1.0, "06_COMANDO", bold=True)
        text(layout, desc, 77, y, 0.98, "02_TEXTO")

    add_rect(layout, 216, 104, 398, 163, "13_NOTAS")
    text(layout, "NAO SELECIONADO", 221, 154, 1.4, "13_NOTAS", bold=True)
    limits = (
        "Nenhum filtro passivo ou reator foi dimensionado.",
        "Espectro, impedancia, ressonancia e limites do PCC pendentes.",
        "Banco nao especificado para aplicacao real ou harmônicos.",
        "Protecao, ventilacao, descarga e manobra dependem de projeto.",
    )
    for index, item in enumerate(limits):
        text(layout, "- " + item, 222, 141 - index * 8, 0.95, "02_TEXTO")


SHEETS = (
    {
        "filename": "01_unifilar_compensacao_reativos.dxf",
        "title": "UNIFILAR CONCEITUAL DA COMPENSACAO DE REATIVOS",
        "subtitle": "QGBT, cargas lineares e VFD, medicao no PCC e banco automatico",
        "scale": "S/ESC.",
        "notes": "Potencia, FP, tensoes e capacidade do banco sao premissas didaticas.\\P"
                "Nao montar ou energizar banco sem estudos, protecao e especificacao de capacitor.",
        "legend": "PCC: ponto de acoplamento comum | QGBT: quadro geral | VFD: inversor | BC: banco de capacitores | RC: regulador de FP | PM: analisador",
        "draw": draw_single_line,
    },
    {
        "filename": "02_memoria_correcao_fator_potencia.dxf",
        "title": "MEMORIA ARITMETICA DE CORRECAO DO FATOR DE POTENCIA",
        "subtitle": "Caso base, degraus discretos e sensibilidade de corrente no QGBT",
        "scale": "S/ESC.",
        "notes": "Valores nominais sem perdas, desequilibrio ou distorcao harmonica.\\P"
                "Degraus e regulacao final dependem do perfil de carga medido.",
        "legend": "P: potencia ativa | Q: potencia reativa | Qc: compensacao | FP: fator de potencia | kvar: quilovolt-ampere reativo",
        "draw": draw_calculation,
    },
    {
        "filename": "03_medicao_controle_harmonicos.dxf",
        "title": "MEDICAO, CONTROLE AUTOMATICO E ESTUDO DE HARMONICOS",
        "subtitle": "Sequencia proposta, estados do regulador e dados para decidir sobre filtros",
        "scale": "S/ESC.",
        "notes": "Nenhuma medicao de campo ou analise harmonica foi realizada.\\P"
                "O desenho nao define filtro, reator, ressonancia ou limite de emissao.",
        "legend": "THD: distorcao harmonica total | PCC: ponto de acoplamento comum | degraus: grupos comutaveis de capacitores",
        "draw": draw_monitoring,
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
