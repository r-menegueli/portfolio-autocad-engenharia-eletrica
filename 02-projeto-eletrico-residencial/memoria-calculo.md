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

## 3. Corrente superior por condutor e demanda pendente

A revisão 04 retira a conta anterior `12 595,543 VA / 220 V = 57,252 A`. Ela misturava
cargas fase-neutro de 127 V e fase-fase de 220 V em um único denominador, portanto não
representa corrente de um condutor de linha. Também não havia critério de simultaneidade
validado para a hipótese de 35%.

P02-10 calcula uma cota aritmética sem diversidade somando a magnitude `S_i/V_i` de cada
ramal em cada condutor. C6 e C7 são fase-fase, então a mesma magnitude de corrente é
contada em A e B. Os circuitos de 127 V são agrupados pela fase registrada em
`quadro-cargas.csv`:

| Condutor | Ramais fase-neutro | Soma `S/V` a 127 V | C6+C7 a 220 V | Cota superior aritmética |
| --- | --- | ---: | ---: | ---: |
| A | C1+C3+C5 | 26,651831 A | 38,636364 A | 65,288195 A |
| B | C2+C4+C8 | 28,928449 A | 38,636364 A | 67,564812 A |

`cota = soma das magnitudes dos ramais`; ela é um limite superior pela desigualdade
triangular, não corrente fasorial real nem demanda. Não há simultaneidade, fatores de
potência por aparelho, medição ou método de serviço aprovados. A antiga referência de
QG1 63 A foi retirada: os valores calculados não selecionam nem reprovam um disjuntor.
QG1, DR1, método de demanda e seção/comprimento do alimentador permanecem pendentes.

## 4. Distribuição entre fases

Circuitos a 127 V foram alocados assim:

- fase A: C1 + C3 + C5 = `3 384,7825 VA`;
- fase B: C2 + C4 + C8 = `3 673,913 VA`.

As cargas de 220 V usam ambos os condutores. Comparando somente as potências aparentes
atribuídas aos ramais de 127 V, sem considerar fatores de potência, o indicador é:

`(3 673,913 - 3 384,7825) / ((3 673,913 + 3 384,7825)/2) = 8,192%`.

Esse percentual não é o desequilíbrio de corrente do alimentador. Correntes fasoriais,
simultaneidade e alocação deverão ser revistas com cargas reais e critérios aplicáveis.

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

O cálculo anterior de queda do alimentador usando 57,252 A e 16 mm² foi retirado junto
com a corrente agregada inválida. A queda dos circuitos finais C3 e C8 permanece abaixo
de 4% no cenário didático, mas o alimentador precisa de comprimento, demanda por
condutor, seção, método de instalação e fatores de correção próprios. Rotas e quedas
reais ainda não foram medidas.

## 7. Verificações pendentes

Curto-circuito presumido, capacidade de interrupção, método de instalação, fatores de
correção, ocupação de eletrodutos, coordenação de DPS, impedância do laço, tempos de
seccionamento e resistência de aterramento exigem dados de campo e não foram calculados.
