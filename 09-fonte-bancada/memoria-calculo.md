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
