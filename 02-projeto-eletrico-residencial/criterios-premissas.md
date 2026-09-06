# Critérios e premissas - Projeto 02

## Dados fictícios congelados na revisão 00

| Parâmetro | Valor adotado | Natureza |
| --- | ---: | --- |
| Dimensões externas | 10,00 x 7,50 m | arquitetura original fictícia |
| Área construída | 75,00 m² | cálculo geométrico |
| Sistema | 127/220 V, 60 Hz, 2F+N+PE | premissa acadêmica |
| Esquema a jusante | TN-S conceitual | premissa a confirmar |
| Quadro | QD1, 24 módulos | reserva física didática |
| Disjuntor geral | 2P, 63 A | seleção preliminar |
| DR | 2P, 63 A, 30 mA, tipo A | proteção adicional global adotada |
| DPS | tipo 2, Uc 275 V, Imax 20 kA | seleção preliminar, 2 unidades |
| Temperatura do cobre | resistividade 0,0225 ohm.mm²/m | hipótese para queda de tensão |
| Queda admissível usada | 4% por circuito, incluindo alimentador | critério acadêmico conservador |
| Demanda geral | 100% dos primeiros 1 000 VA + 35% do excedente | hipótese didática, não regra de concessionária |
| TUE na demanda | 100% de C6, C7 e C8 | hipótese conservadora |
| Eletrodo | haste cobreada de 2,40 m | detalhe indicativo, sujeito a projeto local |

## Critérios de pontos

- Iluminação LED: fator de potência 0,92 para conversão de W em VA.
- Sala/quartos/circulação: 100 VA por TUG.
- Cozinha: 600 VA para cada um dos três primeiros TUG e 100 VA para os demais.
- Banheiro e lavanderia: 600 VA por TUG considerado.
- TUEs: potência nominal fictícia informada no ponto e circuito exclusivo.
- Todo ponto utiliza condutor PE; tomadas são representadas como 2P+T.
- Pontos, potências e circuitos têm uma única fonte tabular em [lista-pontos.csv](lista-pontos.csv).

## Critérios de dimensionamento

O cálculo de corrente usa `I = S/V`. A queda de tensão monofásica/bipolar simplificada
usa `deltaV = 2 x rho x L x I / A`, sem reatância. A capacidade de condução adotada é
apenas uma verificação preliminar conservadora; método de referência, agrupamento,
temperatura, terminais e proteção precisam ser confirmados em projeto executivo.

O alimentador assumido tem 8 m, cobre 16 mm² para fases e neutro, PE 16 mm² e QG1 de
63 A. O disjuntor geral foi escolhido a partir da corrente de demanda calculada, não da
soma aritmética de correntes de todos os circuitos.

## Critérios gráficos

- Folha A3 paisagem, 420 x 297 mm, moldura em 10 mm.
- Planta arquitetônica em escala gráfica declarada 1:50; diagramas e detalhes sem escala.
- DXF AC1027 com `$INSUNITS = 4`, layers permanentes do portfólio e fontes sem dependência externa.
- PDF, SVG e PNG são derivados do mesmo DXF e não fontes independentes.
- Símbolos locais têm prefixo `P02_` e são definidos pelo gerador reproduzível.

## Declaração de não conformidade automática

A menção a normas indica referências consultadas e não certificação. Não houve acesso
integral licenciado a todos os textos nem verificação por autoridade, concessionária ou
responsável técnico. Os desenhos não devem ser lidos como atestado de conformidade.
