# P13 — Estação de recarga de veículos elétricos

Estudo conceitual de uma estação com quatro pontos AC de 11 kW e dois pontos DC de 60 kW. O pacote acompanha o arranjo da área, a arquitetura unifilar e uma proposta de gestão dinâmica de potência. As potências são dados assumidos para demonstrar a documentação; não definem entrada, demanda, proteção ou dimensionamento da instalação.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Implantação esquemática, seis vagas, áreas técnicas e indicação de rota pendente de levantamento | [DXF](fonte/01_layout_estacao_recarga.dxf) | [PDF](exports/01_layout_estacao_recarga.pdf) | [SVG](exports/01_layout_estacao_recarga.svg) | [PNG](exports/01_layout_estacao_recarga.png) |
| 02/03 | Unifilar desde a rede até os seis pontos, com fronteiras e dados pendentes | [DXF](fonte/02_diagrama_unifilar_estacao.dxf) | [PDF](exports/02_diagrama_unifilar_estacao.pdf) | [SVG](exports/02_diagrama_unifilar_estacao.svg) | [PNG](exports/02_diagrama_unifilar_estacao.png) |
| 03/03 | Entradas do gestor, sequência operacional, estados e cenários aritméticos | [DXF](fonte/03_gestao_dinamica_carga.dxf) | [PDF](exports/03_gestao_dinamica_carga.pdf) | [SVG](exports/03_gestao_dinamica_carga.svg) | [PNG](exports/03_gestao_dinamica_carga.png) |

Também fazem parte da entrega o [memorial descritivo](memorial-descritivo.md), os [critérios e premissas](criterios-premissas.md), as [referências de estudo](referencias-normativas.md), a [lista de materiais](lista-materiais.csv), a [lista de sinais](lista-sinais.csv), o [gerador de DXF](fonte/gerar_projeto_13.py), a [validação específica](fonte/validar_projeto_13.py) e o registro de [inspeção visual](inspecao-visual.md).

## Escopo e unidades

O arranjo indica seis posições, quadro dedicado QEV-01 e gestor EMS-01. A rota física dos cabos permanece pendente de levantamento. O unifilar separa a alimentação de potência das interfaces de dados. A terceira folha mostra entradas candidatas, uma sequência de alocação e quatro somas de potência nominal de saída. Todas as folhas usam unidades geométricas em milímetros e formato A3 paisagem. A tensão 380/220 V, 3F+N+PE, 60 Hz é apenas hipótese de representação.

Foram consultadas como referências de estudo a ABNT NBR 17019:2022, a IEC 60364-7-722:2018 e a IEC 61851-1:2017 com corrigenda indicada pela IEC. Consulte [referencias-normativas.md](referencias-normativas.md) para escopo e limites. Citar uma norma não demonstra atendimento a seus requisitos.

## Como reproduzir

Na raiz do repositório, com Python 3.11 ou superior e as dependências de `requirements.txt` instaladas:

```powershell
python .\13-estacao-recarga-veiculos-eletricos\fonte\gerar_projeto_13.py --root .
python .\scripts\renderizar.py --root . --artifact p13-01-layout-estacao-recarga --artifact p13-02-unifilar-estacao-recarga --artifact p13-03-gestao-dinamica-carga
python .\13-estacao-recarga-veiculos-eletricos\fonte\validar_projeto_13.py --root .
python .\scripts\validar_portfolio.py --root . --strict
```

DXF em AC1027 é a fonte editável. PDF, SVG e PNG são derivados dos DXFs pelo fluxo comum do repositório. Não há DWG nesta entrega.

## Resultado da validação

O relatório [validacao-projeto-13.json](validacao-projeto-13.json) registra a conferência aritmética e de rastreabilidade específica. A inspeção visual e o resultado do validador estrito integrado estão registrados em [inspecao-visual.md](inspecao-visual.md).

## Limites

Não foram fornecidos levantamento do local, consulta de acesso, estudo da concessionária, corrente de curto-circuito, regime de aterramento, dados de carga do edifício, especificações de carregadores, mapa de cabos, métodos de instalação, cálculo de demanda ou coordenação de proteção. As folhas não escolhem dispositivos, condutores ou capacidades de alimentação. A implantação, acessibilidade, sinalização, circulação, segurança contra impactos e interfaces de dados dependem de informações e revisões adicionais.
