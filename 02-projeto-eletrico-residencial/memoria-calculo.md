# Memória de cálculo - Projeto 02

## 1. Geometria

Área externa: `10,00 m x 7,50 m = 75,00 m²`.

## 2. Potência instalada

Iluminação usa fator de potência 0,92. C1 passou a incluir a luminária L09 do closet:

- C1: `78 W / 0,92 ≈ 84,783 VA`;
- C2: `68 W / 0,92 = 73,913 VA`.

A soma das oito potências aparentes, conforme os valores tabulados e arredondados em
`quadro-cargas.csv`, é:

`84,7825 + 73,913 + 1 500 + 2 100 + 1 800 + 3 000 + 5 500 + 1 500 = 15 558,6955 VA`.

Os dados calculáveis estão em [quadro-cargas.csv](quadro-cargas.csv).

## 3. Demanda acadêmica

Grupo de iluminação e TUG, C1 a C5:

`S_geral = 84,7825 + 73,913 + 1 500 + 2 100 + 1 800 = 5 558,6955 VA`.

Hipótese didática: 100% dos primeiros 1 000 VA e 35% do excedente:

`D_geral = 1 000 + 0,35 x (5 558,6955 - 1 000) = 2 595,543425 VA`.

TUEs C6, C7 e C8 considerados a 100%:

`D_TUE = 3 000 + 5 500 + 1 500 = 10 000 VA`.

`D_total = 2 595,543425 + 10 000 = 12 595,543425 VA`.

Corrente equivalente de demanda na tensão fase-fase:

`I_dem = 12 595,543425 / 220 = 57,252 A`.

Adota-se QG1 bipolar de 63 A e alimentador de cobre de 16 mm² como seleção preliminar.

## 4. Distribuição entre fases

Circuitos a 127 V foram alocados assim:

- fase A: C1 + C3 + C5 = `3 384,7825 VA`;
- fase B: C2 + C4 + C8 = `3 673,913 VA`.

As cargas de 220 V usam ambas as fases. Comparando apenas as cargas fase-neutro, o
desequilíbrio é:

`(3 673,913 - 3 384,7825) / ((3 673,913 + 3 384,7825)/2) = 8,192%`.

Essa métrica é indicativa; a composição vetorial exata depende do sistema real da rede e
da simultaneidade. A alocação deverá ser revista com medições e critérios da concessionária.

## 5. Corrente e proteção dos circuitos

| Circ. | V | VA | I calculada | Condutor | Disjuntor |
| --- | ---: | ---: | ---: | ---: | ---: |
| C1 | 127 | 84,783 | 0,668 A | 1,5 mm² | 10 A, 1P, curva B |
| C2 | 127 | 73,913 | 0,582 A | 1,5 mm² | 10 A, 1P, curva B |
| C3 | 127 | 1 500 | 11,811 A | 4 mm² | 16 A, 1P, curva C |
| C4 | 127 | 2 100 | 16,535 A | 4 mm² | 20 A, 1P, curva C |
| C5 | 127 | 1 800 | 14,173 A | 4 mm² | 16 A, 1P, curva C |
| C6 | 220 | 3 000 | 13,636 A | 4 mm² | 20 A, 2P, curva C |
| C7 | 220 | 5 500 | 25,000 A | 6 mm² | 32 A, 2P, curva C |
| C8 | 127 | 1 500 | 11,811 A | 4 mm² | 16 A, 1P, curva C |

## 6. Queda de tensão simplificada

Com `rho = 0,0225 ohm.mm²/m`, as rotas máximas adotadas produzem:

| Circ. | L | deltaV | Percentual do circuito | Percentual combinado conservador |
| --- | ---: | ---: | ---: | ---: |
| C1 | 28 m | 0,561 V | 0,442% | 1,456% |
| C2 | 24 m | 0,419 V | 0,330% | 1,344% |
| C3 | 20 m | 2,657 V | 2,093% | 3,107% |
| C4 | 18 m | 3,349 V | 2,637% | 3,651% |
| C5 | 20 m | 3,189 V | 2,511% | 3,525% |
| C6 | 18 m | 2,761 V | 1,255% | 1,841% |
| C7 | 20 m | 3,750 V | 1,705% | 2,291% |
| C8 | 22 m | 2,923 V | 2,302% | 3,316% |

O alimentador foi estimado por `2 x 0,0225 x 8 x 57,252 / 16 = 1,288 V`, equivalente
a `0,586%` de 220 V e `1,014%` de 127 V. A soma conservadora usa o percentual
correspondente à tensão do circuito. As seções de C3 e C8 foram elevadas de 2,5 para
4 mm² durante a revisão matemática; as estimativas combinadas passaram a 3,107% e
3,316%, abaixo do critério acadêmico de 4%. Rotas e fatores de correção ainda precisam
ser confirmados em projeto executivo.

## 7. Verificações pendentes

Curto-circuito presumido, capacidade de interrupção, método de instalação, fatores de
correção, ocupação de eletrodutos, coordenação de DPS, impedância do laço, tempos de
seccionamento e resistência de aterramento exigem dados de campo e não foram calculados.
