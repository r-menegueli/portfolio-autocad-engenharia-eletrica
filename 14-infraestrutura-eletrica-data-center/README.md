# P14 — Infraestrutura elétrica de data center

Estudo acadêmico de uma instalação de TI com dois caminhos elétricos A/B, UPS modular, geradores, quadros e distribuição até racks de dupla alimentação. O pacote combina arquitetura unifilar, layout conceitual e balanço aritmético de potência com cenários limitados de contingência.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Alimentações, transformação, geradores, UPS, PDUs e carga de TI A/B | [DXF](fonte/01_arquitetura_eletrica_ab.dxf) | [PDF](exports/01_arquitetura_eletrica_ab.pdf) | [SVG](exports/01_arquitetura_eletrica_ab.svg) | [PNG](exports/01_arquitetura_eletrica_ab.png) |
| 02/03 | Zonas técnicas, seis racks e rotas de distribuição A/B | [DXF](fonte/02_layout_salas_e_racks.dxf) | [PDF](exports/02_layout_salas_e_racks.pdf) | [SVG](exports/02_layout_salas_e_racks.svg) | [PNG](exports/02_layout_salas_e_racks.png) |
| 03/03 | Balanço, capacidades calculadas sob hipóteses e respostas de contingência | [DXF](fonte/03_balanco_potencia_contingencias.dxf) | [PDF](exports/03_balanco_potencia_contingencias.pdf) | [SVG](exports/03_balanco_potencia_contingencias.svg) | [PNG](exports/03_balanco_potencia_contingencias.png) |

Também fazem parte da entrega o [memorial](memorial-descritivo.md), os [critérios e premissas](criterios-premissas.md), as [referências](referencias-normativas.md), as listas de [materiais](lista-materiais.csv) e [sinais](lista-sinais.csv), o [gerador](fonte/gerar_projeto_14.py), a [validação específica](fonte/validar_projeto_14.py) e o relatório de [inspeção visual](inspecao-visual.md).

## Hipóteses principais

- Carga de TI: 1.000 kW; climatização e auxiliares: 500 kW; total ilustrativo: 1.500 kW.
- PUE assumido: 1,50; fator de potência assumido: 0,95; potência aparente calculada: aproximadamente 1.579 kVA.
- Cada caminho representa um transformador e um grupo gerador de 2.000 kVA; os fatores de potência usados para comparar capacidade são hipóteses.
- Cada caminho UPS representa cinco módulos de 250 kW, quatro requeridos e um reserva (N+1), para 1.000 kW requeridos por caminho.
- As fontes MT A/B, sua independência e a separação física dos trajetos não foram confirmadas. O desenho não declara classificação TIA Rated ou Tier.

## Como reproduzir

Na raiz do repositório, com Python 3.11 ou superior e as dependências fixadas em `requirements.txt`:

```powershell
python .\14-infraestrutura-eletrica-data-center\fonte\gerar_projeto_14.py --root .
python .\scripts\renderizar.py --root . --artifact p14-01-arquitetura-eletrica-ab --artifact p14-02-layout-salas-racks --artifact p14-03-balanco-contingencias
python .\14-infraestrutura-eletrica-data-center\fonte\validar_projeto_14.py --root .
python .\scripts\validar_portfolio.py --root . --strict
```

DXF AC1027 é a fonte editável; PDF, SVG e PNG são derivados. Não há DWG nesta entrega.

## Limites

Não foram definidos local, concessionária, topologia de média tensão, transformadores reais, corrente de curto-circuito, proteções, seletividade, condutores, autonomia de baterias, combustível, cargas térmicas, sequência certificada, segurança contra incêndio ou classificação de disponibilidade. O exemplo não prova redundância real nem conformidade normativa.
