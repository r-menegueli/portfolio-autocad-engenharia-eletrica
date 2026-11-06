# P15 — Microrrede industrial com FV, BESS e gerador

Estudo conceitual de uma microrrede CA conectada à rede, com geração fotovoltaica, armazenamento em baterias, grupo gerador, ponto de interconexão e prioridades de carga. As pranchas cobrem o unifilar, o layout esquemático e os balanços de potência para modos conectados e ilhados.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Rede, PCC, transformador, FV, BESS, GE e cargas no barramento CA | [DXF](fonte/01_unifilar_microrrede.dxf) | [PDF](exports/01_unifilar_microrrede.pdf) | [SVG](exports/01_unifilar_microrrede.svg) | [PNG](exports/01_unifilar_microrrede.png) |
| 02/03 | Implantação esquemática das fontes, quadro e grupos de cargas | [DXF](fonte/02_layout_fontes_cargas.dxf) | [PDF](exports/02_layout_fontes_cargas.pdf) | [SVG](exports/02_layout_fontes_cargas.svg) | [PNG](exports/02_layout_fontes_cargas.png) |
| 03/03 | Balanços aritméticos, transições de modo e prioridades de carga | [DXF](fonte/03_operacao_balanco_energia.dxf) | [PDF](exports/03_operacao_balanco_energia.pdf) | [SVG](exports/03_operacao_balanco_energia.svg) | [PNG](exports/03_operacao_balanco_energia.png) |

Complementam as pranchas o [memorial](memorial-descritivo.md), os [critérios e premissas](criterios-premissas.md), as [referências](referencias-normativas.md), as listas de [materiais](lista-materiais.csv) e [sinais](lista-sinais.csv), o [gerador](fonte/gerar_projeto_15.py), a [validação específica](fonte/validar_projeto_15.py) e a [inspeção visual](inspecao-visual.md).

## Hipóteses principais

- Carga total: 1.000 kW, dividida em 800 kW prioritários e 200 kW não prioritários.
- Campo FV: 600 kW AC; BESS: conversor de 500 kW e energia nominal de 1 MWh; GE: 500 kW.
- Transformador: 1.500 kVA; fatores de potência usados nos cálculos são premissas didáticas.
- A energia/potência do BESS resulta em 2 h ideais a 500 kW, sem perdas, reserva de SOC ou limites do fabricante.
- O diagrama não define proteção de interconexão, autorização de paralelismo nem capacidade efetiva de operação ilhada.

## Como reproduzir

Na raiz do repositório, com Python 3.11 ou superior e as dependências de `requirements.txt`:

```powershell
python .\15-microrrede-industrial-fv-bess-gerador\fonte\gerar_projeto_15.py --root .
python .\scripts\renderizar.py --root . --artifact p15-01-unifilar-microrrede --artifact p15-02-layout-fontes-cargas --artifact p15-03-operacao-balanco
python .\15-microrrede-industrial-fv-bess-gerador\fonte\validar_projeto_15.py --root .
python .\scripts\validar_portfolio.py --root . --strict
```

DXF AC1027 é a fonte editável. PDF, SVG e PNG são derivados; não há DWG nesta entrega.

## Limites

As pranchas não definem corrente de curto-circuito, proteção anti-ilhamento, direcionalidade, sincronismo, religamento, seletividade, aterramento, condutores, fluxo de potência, dinâmica de frequência/tensão, estabilidade, black start, autonomia, envelhecimento de bateria, combustível ou autorização da concessionária. As somas não são uma simulação de operação.
