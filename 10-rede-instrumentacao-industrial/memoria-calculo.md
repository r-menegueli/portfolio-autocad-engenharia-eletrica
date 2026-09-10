# Memória de cálculo — P10

## Escala das entradas 4–20 mA

Para uma faixa linear entre LRV e URV, a conversão usada é:

```text
EU = LRV + ((I_mA - 4) / 16) × (URV - LRV)
```

| Tag | Faixa | 4 mA | 12 mA | 20 mA |
| --- | --- | ---: | ---: | ---: |
| TT-101 | 0–150 °C | 0 °C | 75 °C | 150 °C |
| PT-102 | 0–10 bar(g) | 0 bar(g) | 5 bar(g) | 10 bar(g) |
| FT-103 | 0–60 m³/h | 0 m³/h | 30 m³/h | 60 m³/h |
| LT-104 | 0–5 m | 0 m | 2,5 m | 5 m |

O validador verifica 16.001 pontos por instrumento, de 4,000 a 20,000 mA em passos
de 0,001 mA. Diagnóstico de fio rompido e overrange não foi definido porque depende
do hardware e da filosofia de alarmes selecionados.

## Balanço preliminar de 24 Vcc

| Grupo | Corrente | Potência em 24 V |
| --- | ---: | ---: |
| PLC-101 | 0,60 A | 14,40 W |
| SW-101 | 0,35 A | 8,40 W |
| RIO-201 | 0,45 A | 10,80 W |
| RIO-202 | 0,45 A | 10,80 W |
| quatro malhas AI | 0,10 A | 2,40 W |
| dois sensores DI | 0,10 A | 2,40 W |
| reserva auxiliar | 1,05 A | 25,20 W |
| **Total previsto** | **3,10 A** | **74,40 W** |

A fonte conceitual de 10 A opera a 31 % da corrente nominal, resultando em margem
aritmética de 69 %. A seleção final precisa considerar inrush, temperatura, derating,
curto-circuito, seletividade, continuidade e disponibilidade.

## Queda de tensão e burden

Não foi calculada uma queda executiva: resistência real, temperatura, conectores e
burden do cartão AI não foram selecionados. Para cada malha real deve-se confirmar:

```text
V_fonte_mínima ≥ V_transmissor_mínima + I_máxima × R_loop + V_AI + margens
```

As formações e comprimentos conceituais constam em [lista-cabos.csv](lista-cabos.csv).
Esses dados não autorizam compra ou instalação.
