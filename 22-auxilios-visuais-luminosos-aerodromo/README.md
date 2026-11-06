# P22 — Auxílios visuais luminosos de aeródromo

Estudo conceitual de uma pista e uma pista de táxi fictícias, com arranjo de pontos luminosos, circuitos série com CCR e matriz de controle/ensaios. As folhas organizam interfaces de projeto, sem especificar geometria operacional ou declarar aprovação aeroportuária.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Arranjo indicativo de pista, cabeceiras, aproximação e pista de táxi | [DXF](fonte/01_layout_luminoso_pista_taxi.dxf) | [PDF](exports/01_layout_luminoso_pista_taxi.pdf) | [SVG](exports/01_layout_luminoso_pista_taxi.svg) | [PNG](exports/01_layout_luminoso_pista_taxi.png) |
| 02/03 | Unifilar de alimentação, CCR, circuitos série e transformadores de isolamento | [DXF](fonte/02_unifilar_circuitos_serie_ccr.dxf) | [PDF](exports/02_unifilar_circuitos_serie_ccr.pdf) | [SVG](exports/02_unifilar_circuitos_serie_ccr.svg) | [PNG](exports/02_unifilar_circuitos_serie_ccr.png) |
| 03/03 | Controle, monitoramento, alarmes e evidências de aceitação | [DXF](fonte/03_controle_monitoracao_e_ensaios.dxf) | [PDF](exports/03_controle_monitoracao_e_ensaios.pdf) | [SVG](exports/03_controle_monitoracao_e_ensaios.svg) | [PNG](exports/03_controle_monitoracao_e_ensaios.png) |

Documentos e dados: [memorial](memorial-descritivo.md), [critérios e premissas](criterios-premissas.md), [referências](referencias-normativas.md), [materiais](lista-materiais.csv), [sinais](lista-sinais.csv), [circuitos](circuitos.csv), [plano de estudos](plano-estudos.csv), [gerador](fonte/gerar_projeto_22.py), [validador](fonte/validar_projeto_22.py), [resultado da validação](validacao-projeto-22.json) e [inspeção visual](inspecao-visual.md).

## Premissas

- Pista, taxiway, posições e quantidades são cenários fictícios, qualitativos e sem escala.
- Nenhuma categoria operacional, procedimento de aproximação, intensidade, cor, espaçamento ou nível de serviço foi selecionado.
- CCR, transformadores de isolamento, controle e circuitos são topologias indicativas; correntes, tensões, capacidades e redundância estão pendentes.
- RBAC 154 Emenda 09 é a referência brasileira consultada em 2026-11-06. FAA AC 150/5340-30J e AC 150/5345-10H aparecem apenas como referências técnicas suplementares; não substituem regras brasileiras.

## Reprodução

Na raiz do repositório, com `.venv` e dependências de `requirements.txt`:

```powershell
.\.venv\Scripts\python.exe .\22-auxilios-visuais-luminosos-aerodromo\fonte\gerar_projeto_22.py --root .
.\.venv\Scripts\python.exe .\scripts\renderizar.py --root . --artifact p22-01-layout-pista-taxi --artifact p22-02-circuitos-serie-ccr --artifact p22-03-controle-ensaios-aerodromo
.\.venv\Scripts\python.exe .\22-auxilios-visuais-luminosos-aerodromo\fonte\validar_projeto_22.py --root .
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

DXF AC1027 é a fonte editável em milímetros. PDF, SVG e PNG são derivados. Não há DWG neste projeto.

## Limites

Não foram definidos levantamento aeroportuário, geometria, classes de pista, pontos de projeto, desempenho fotométrico, cores, intensidade, posições, espaçamento, circuitos e suas capacidades, proteção, aterramento, redundância, comutação, integração com torre/serviço de tráfego, procedimentos ou ensaios. O estudo não constitui projeto aprovado ou liberado para operação.
