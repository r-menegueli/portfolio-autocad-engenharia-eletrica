# Memória de cálculo - Projeto 05

## 1. Geometria

`30,00 m x 18,00 m = 540,00 m²`.

Produção: `24,00 m x 18,00 m = 432,00 m²`.

Apoio: `6,00 m x 18,00 m = 108,00 m²`.

## 2. Exemplo de cálculo de motor

Para M-501, com 11 kW no eixo, rendimento 0,90 e fator de potência 0,85:

`Pentrada = 11 / 0,90 = 12,222 kW`

`Sinst = 12,222 / 0,85 = 14,379 kVA`

`Ib = 14,379 x 1000 / (raiz(3) x 380) = 21,847 A`

Com fator de demanda 1,00, `Sdem = 14,379 kVA`. O circuito C01 adota, em caráter
preliminar, DJ de 32 A e condutores de 6 mm², com Iz assumida de 41 A.

## 3. Totais por quadro

| Quadro | P instalada | S instalada | P demandada | S demandada | Corrente de referência |
| --- | ---: | ---: | ---: | ---: | ---: |
| QDF-05 | 61,265 kW | 72,430 kVA | 42,459 kW | 50,242 kVA | 76,335 A |
| QDL-05 | 3,180 kW | 3,347 kVA | 3,180 kW | 3,347 kVA | 6,124 A na fase B |
| QADM-05 | 4,050 kW | 4,500 kVA | 2,430 kW | 2,700 kVA | 4,091 A por fase |
| Total | 68,495 kW | 80,277 kVA | 48,069 kW | 56,289 kVA | 85,523 A equivalente |

Os totais completos são somas das 16 linhas de [quadro-cargas.csv](quadro-cargas.csv).
A corrente equivalente total é:

`Ieq = 56,289 x 1000 / (raiz(3) x 380) = 85,523 A`.

## 4. Distribuição entre fases

QDF-05 é tratado como carga trifásica equilibrada, com 76,335 A demandados em cada
fase. As cargas monofásicas somam:

- fase A: C09 + C14 = 1,742 kVA demandados, 7,919 A;
- fase B: C10 + C12 + C15 = 2,247 kVA demandados, 10,216 A;
- fase C: C11 + C13 + C16 = 2,058 kVA demandados, 9,354 A.

Somando QDF-05, as correntes estimadas no alimentador geral são 84,253 A na fase A,
86,550 A na fase B e 85,689 A na fase C. O desequilíbrio entre maior e menor fase,
dividido pela corrente média, é aproximadamente 2,69%.

O dimensionamento do alimentador geral usa a maior fase, 86,550 A, e não apenas a
corrente equivalente média.

## 5. Alimentadores

| Alimentador | Corrente | Disjuntor | Condutores | Iz assumida | Queda |
| --- | ---: | ---: | --- | ---: | ---: |
| AL-QGBT | 86,550 A | 4P 100 A | 4 x 50 + PE 25 mm² | 134 A | 0,885% |
| AL-QDF | 76,335 A | 3P 80 A | 4 x 25 + PE 16 mm² | 89 A | 0,564% |
| AL-QDL | 6,124 A | 4P 16 A | 5 x 4 mm² | 32 A | 0,626% |
| AL-QADM | 4,091 A | 4P 16 A | 5 x 2,5 mm² | 24 A | 0,536% |

Em todos os quatro casos, a verificação acadêmica `Ib <= In <= Iz` é satisfeita.

## 6. Queda de tensão

Os circuitos finais apresentam quedas entre 0,358% e 2,297%. A soma conservadora
considera AL-QGBT, o alimentador do quadro e o circuito final:

- pior circuito de QDF-05: C08 = `0,885 + 0,564 + 1,472 = 2,921%`;
- pior circuito de QDL-05: C11 = `0,885 + 0,626 + 2,297 = 3,808%`;
- pior circuito de QADM-05: C16 = `0,885 + 0,536 + 1,674 = 3,095%`.

Todos permanecem abaixo do critério acadêmico de 4,0%. O uso da resistividade de
0,0225 ohm.mm²/m incorpora aquecimento de modo simplificado, mas não substitui cálculo
com reatância, harmônicas, método de instalação e temperatura real.

## 7. Balanço de consistência

O validador específico deve confirmar:

- 16 circuitos únicos C01-C16;
- quatro alimentadores únicos;
- 20 registros de cabos, sem circuitos órfãos;
- somas por quadro iguais às somas globais;
- fórmulas de potência, corrente e queda dentro da tolerância de arredondamento;
- proteção e ampacidade na ordem `Ib <= In <= Iz`;
- queda combinada de cada circuito menor ou igual a 4,0%;
- presença das tags críticas nas sete pranchas.

## 8. Cálculos não realizados

Faltam dados para curto-circuito, seletividade, coordenação, partida de motores,
harmônicas, fluxo de potência, fator de potência global corrigido, energia incidente,
aterramento, fotometria e dimensionamento térmico dos quadros. Esses temas devem ser
resolvidos antes de qualquer aplicação real.
