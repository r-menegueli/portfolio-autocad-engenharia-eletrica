# Memória de cálculo - Projeto 08

Todos os resultados usam as premissas de [parametros.csv](parametros.csv) e são
reproduzidos pelo validador específico. Ponto decimal é usado nos CSVs; este documento
apresenta vírgula decimal por legibilidade.

## Potências e configuração

- potência CC: `12 × 550 = 6.600 Wp = 6,60 kWp`;
- potência CA nominal: `6.000 W`;
- relação CC/CA: `6.600 / 6.000 = 1,10`;
- configuração: `2 strings × 6 módulos em série`, sem paralelo entre MPPTs.

## String em STC

- `Vmp,string = 6 × 41,8 = 250,8 Vcc`;
- `Voc,string = 6 × 49,9 = 299,4 Vcc`;
- `Imp,string = 13,16 A`;
- `Isc,string = 13,92 A`.

## Correções ambientais acadêmicas

Para `Tmin = -5 °C`, `Tref = 25 °C` e coeficiente de Voc de `-0,28 %/°C`:

`Voc,frio = 6 × 49,9 × [1 + (-0,0028) × (-5 - 25)] = 324,5496 Vcc`.

Para temperatura máxima de célula de `70 °C` e coeficiente de Vmp de `-0,30 %/°C`:

`Vmp,quente = 6 × 41,8 × [1 + (-0,0030) × (70 - 25)] = 216,942 Vcc`.

Para irradiância de `1.100 W/m²` e coeficiente de Isc de `+0,05 %/°C`:

`Isc,corr = 13,92 × 1,10 × [1 + 0,0005 × (70 - 25)] = 15,65652 A`.

A corrente acadêmica de projeto é `1,25 × 15,65652 = 19,57065 A`. O fusível gPV
proposto é 20 A, inferior ou igual ao limite série assumido de 25 A do módulo. Esses
fatores não dispensam a aplicação integral da norma, do fabricante e das condições
reais.

## Corrente e queda de tensão CA

Para 6.000 W, 220 V e fator de potência unitário idealizado:

`Ica = 6.000 / 220 = 27,272727 A`.

Com cobre de resistividade `0,0175 ohm·mm²/m`, 15 m de ida e 10 mm²:

`ΔVca = 2 × 15 × 27,272727 × 0,0175 / 10 = 1,431818 V = 0,650826 %`.

## Queda de tensão CC

Com 20 m de ida, 6 mm² e 13,16 A:

`ΔVcc = 2 × 20 × 13,16 × 0,0175 / 6 = 1,535333 V = 0,612174 %`.

A soma indicativa dos dois trechos é `1,263001 %`. Não foram incluídos contatos,
conectores, temperatura, reatância, agrupamento ou tolerâncias do material.

## Estimativa didática e sensibilidade paramétrica de energia

O caso didático atual usa 5,2 h/dia de sol pleno e performance ratio (PR) 0,78:

`Eanual = 6,6 × 5,2 × 365 × 0,78 = 9.770,904 kWh/ano`.

Média aritmética: `814,242 kWh/mês`. Ela é apenas o ponto-base didático; não é resultado
experimental, previsão bancável ou garantia.

A prancha 07 e [sensibilidade-energia.csv](sensibilidade-energia.csv) variam HSP entre
3 e 6 h/dia e PR entre 0,70 e 0,86. Esses limites foram escolhidos apenas para mostrar
a influência matemática desses parâmetros. A grade não tem origem em base meteorológica,
localidade, distribuição estatística ou estudo de perdas. O resultado muda linearmente
com HSP e PR, mantendo 6,60 kWp constante.

Para estimar produção de um imóvel, faltam coordenadas e período, fonte meteorológica,
orientação e inclinação medidas, horizonte e sombras, modelos reais de módulos e
inversor, perdas, disponibilidade e degradação. Sem esses dados, não se deve interpretar
a grade como faixa provável ou previsão local.
