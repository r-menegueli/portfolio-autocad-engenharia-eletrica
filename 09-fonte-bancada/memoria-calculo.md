# Memória de cálculo

Os cálculos abaixo usam os valores de [Parâmetros](parametros.csv) e são reproduzidos
pelo validador específico. Não representam ensaio de protótipo.

## Potência e corrente de entrada

Potência máxima de saída:

`Pout = 30 V × 5 A = 150 W`

Entrada do regulador, com rendimento proposto de 92%:

`Preg,in = 150 / 0,92 = 163,043 W`

Saída requerida de PS1 incluindo 8 W auxiliares:

`Pps1,out = 163,043 + 8 = 171,043 W`

Entrada real aproximada, com rendimento de PS1 igual a 90%:

`Pin = 171,043 / 0,90 = 190,048 W`

Corrente aparente no pior ponto de 90 Vca, usando fator de potência 0,90:

`Iin,90 = 190,048 / (90 × 0,90) = 2,346 A`

O fusível T4 A é apenas proposta preliminar. Corrente de partida, temperatura,
capacidade de interrupção, tempo de atuação e coordenação não foram calculados.

## Margem de PS1

`Carga PS1 = 171,043 / 252 × 100 = 67,874%`

`Margem PS1 = 32,126%`

Essa margem não substitui a curva de derating do fabricante.

## Dissipação e ventilação

`Pperdas = 190,048 - 150 = 40,048 W`

Para elevação de 15 °C, usando o balanço simplificado de ar:

`Qmin = 1,76 × 40,048 / 15 = 4,699 CFM`

O ventilador proposto fornece 20 CFM em ar livre. Com derating de 50%, a vazão
efetiva assumida é 10 CFM, relação de 2,128 sobre o mínimo simplificado. Pressão
estática, filtro, grelha, ruído, altitude, recirculação e falha do ventilador exigem
ensaio térmico.

## Barramento de 36 V

`I36 = 171,043 / 36 = 4,751 A`

Para 0,5 m de percurso de ida, cobre 2,5 mm² e resistividade 0,0175 Ω·mm²/m:

`ΔV36 = 2 × 0,5 × 4,751 × 0,0175 / 2,5 = 0,033 V`

## Saída e shunt

`ΔVcabo = 2 × 0,5 × 5 × 0,0175 / 2,5 = 0,035 V`

Para SH1 de 10 A/75 mV:

`ΔVshunt,5A = 75 mV × 5/10 = 37,5 mV`

`Pshunt,5A = 0,0375 × 5 = 0,1875 W`

Queda interna indicativa no ponto de 30 V e 5 A:

`ΔVtotal = 0,035 + 0,0375 = 0,0725 V = 0,2417%`

O sensoriamento Kelvin pode compensar parte da queda, mas estabilidade, resposta
transitória e limites de compensação não foram modelados.

## Pré-dimensionamento do buck CC/CV

O controlador candidato U1 é o LM5190. A equação do indutor no datasheet é
`L = Vout / (Delta_IL x fSW) x (1 - Vout/Vin)`. Adoto `fSW = 100 kHz` e ondulação
alvo de 30% de 5 A, ou 1,5 A pico a pico. A 36 V nominais, o maior valor de
ondulação ocorre em 18 V e exige 60 uH. O cenário paramétrico de 42 V (não especificado
por PS1) produz o máximo em 21 V e exige 70 uH. L1=75 uH produz 1,20 A (24%) em 36 V
e 1,40 A (28%) no cenário de 42 V. O pico normal calculado a 5 A é 5,70 A.

Com RCS=9,1 mOhm, o limiar típico de 60 mV do LM5190 corresponde a 6,59 A de pico.
Subtraindo metade da ondulação de 1,40 A, a corrente média equivalente de intervenção
é 5,89 A. A perda ideal de RCS é 0,228 W a 5 A e 0,316 W no limite médio equivalente;
foi proposto resistor Kelvin de pelo menos 1 W, ainda sujeito a tolerância e verificação
térmica. A equação do datasheet para RIMON resulta em 8,62 kOhm para o alvo nominal
de 5 A, usando ganho e offset típicos; o ajuste e a exatidão final não foram validados.

O LM5190 regula a partir de 0,8 V. K1 aberto interrompe a alimentação positiva da
saída, mas não garante 0 V residual nos bornes; um circuito de descarga precisa ser
definido e dimensionado. As equações e valores completos estão em
[dimensionamento do regulador](dimensionamento-regulador.csv).
O cenário de 42 V é somente análise de sensibilidade. A tolerância e os transitórios
reais de PS1, compensação das malhas, capacitâncias, perdas, térmica, EMC e layout
precisam ser definidos e verificados antes de qualquer implementação.
