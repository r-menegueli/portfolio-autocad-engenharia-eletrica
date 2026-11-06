# Memória de cálculo - CCM-06

## Equações

Para cada motor trifásico, a potência ativa de entrada é `Pin = Psaida / rendimento`,
a potência aparente é `S = Pin / fp` e a corrente é
`I = S x 1000 / (raiz(3) x 380)`.

A queda resistiva conceitual é
`dV% = 100 x raiz(3) x 0,0225 x L x I / (Scondutor x 380)`.

## Cargas

| Tag | FD | P instalada | P demandada | S instalada | S demandada | Ib do ramal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| M-601 | 1,00 | 6,321839 kW | 6,321839 kW | 7,709560 kVA | 7,709560 kVA | 11,713464 A |
| M-602 | 0,80 | 3,529412 kW | 2,823529 kW | 4,411765 kVA | 3,529412 kVA | 6,702983 A |
| M-603 | 0,90 | 8,333333 kW | 7,500000 kW | 8,771930 kVA | 7,894737 kVA | 13,327569 A |
| Total | - | 18,184584 kW | 16,645368 kW | 20,893255 kVA | 19,133709 kVA | - |

A corrente dos ramais usa S instalada por carga e não deve ser somada para representar
o W600. A potência ativa demandada é 16,645368 kW. A corrente equivalente do
alimentador usa a soma de S demandada:
`19,133709 x 1000 / (raiz(3) x 380) = 29,070663 A`.

## Alimentador e proteção

W600 adota preliminarmente `4 x 10 mm² + PE 10 mm²`, 20 m, Iz assumida de 57 A e
QG-06 de 50 A. Assim, `29,071 <= 50 <= 57 A`. A queda estimada de W600 é 0,596272%.

| Circuito | Ib | In | Iz | Condutor | dV circuito | dV combinada |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| M-601/W601 | 11,713 A | 16 A | 24 A | 2,5 mm² | 1,441538% | 2,037810% |
| M-602/W602 | 6,703 A | 10 A | 24 A | 2,5 mm² | 0,687429% | 1,283701% |
| M-603/W603A | 13,328 A | 25 A | 32 A | 4 mm² | 0,512556% | 1,108828% |

O valor máximo permanece abaixo do critério interno de 4,0%. Para W603B, a seleção
final considera corrente PWM, comprimento admitido pelo fabricante, EMC, dv/dt e
eventual redução de capacidade; a tabela não atribui uma queda senoidal convencional.

## Conferências cruzadas

- três cargas únicas e três métodos distintos;
- QF-601/KM-601/FR-601 associados somente a M-601;
- QF-602/KM-602F/KM-602R/IM-602/FR-602 associados somente a M-602;
- QF-603/VFD-603/STO A/B associados somente a M-603;
- cabos W600-W608, incluindo W603A/W603B, somam 196 m assumidos;
- réguas X1-X4 possuem 37 bornes listados.
