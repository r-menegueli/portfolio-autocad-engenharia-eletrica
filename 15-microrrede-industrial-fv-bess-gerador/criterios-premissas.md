# Critérios e premissas — P15

## Hipóteses quantitativas

| Item | Valor ilustrativo | Classificação |
| --- | ---: | --- |
| Carga total | 1.000 kW | Hipótese |
| Carga prioritária | 800 kW | Hipótese |
| Carga não prioritária | 200 kW | Hipótese |
| Inversor FV | 600 kW AC | Potência nominal assumida |
| Conversor BESS | 500 kW | Potência nominal assumida |
| Energia nominal do BESS | 1.000 kWh | Hipótese; não é energia útil garantida |
| Grupo gerador | 500 kW | Hipótese |
| Transformador | 1.500 kVA | Hipótese |
| FP usado na comparação TR | 0,95 | Premissa didática |

## Balanços verificáveis

- Cargas: `800 kW prioritários + 200 kW não prioritários = 1.000 kW`.
- Modo conectado: `600 kW FV + 400 kW rede = 1.000 kW`.
- Ilha, FV alta: `600 kW FV + 400 kW GE + 0 kW BESS = 1.000 kW`.
- Ilha, FV baixa: `200 kW FV + 500 kW GE + 300 kW BESS = 1.000 kW`.
- Ilha, sem FV: `0 kW FV + 500 kW GE + 500 kW BESS = 1.000 kW`.
- GE indisponível: `300 kW FV + 500 kW BESS = 800 kW prioritários`; os 200 kW restantes são cortados no exemplo.
- Duração energética ideal: `1.000 kWh / 500 kW = 2 h`, sem perdas ou reserva.
- Capacidade ativa comparativa do TR: `1.500 kVA × 0,95 = 1.425 kW`; margem aritmética sobre 1.000 kW: `425 kW`.

Esses balanços não avaliam limites de importação/exportação, potência reativa, rampas, qualidade de energia, reserva dinâmica, potência útil, estado de carga ou autonomia real.

## Critérios de representação

- Diferenciar interface de rede, barra interna e fontes FV, BESS e GE.
- Indicar cargas prioritárias e não prioritárias para que o corte do exemplo seja explícito.
- Tratar os estados conectada, ilhamento, ilhada e ressincronização como funções a projetar, sem inserir ajustes ou comandos executivos.
- Não chamar o desenho de instalação aprovada ou de microrrede certificada.

## Dados ainda necessários

Dados da concessionária, tensão e aterramento; demanda e curvas de carga; irradiância e perfil FV; características e controles dos inversores; impedâncias e curto-circuito; proteção de interface e anti-ilhamento; controle formador de rede; capacidade de partida do GE; bateria, SOC e energia útil; transições de modo; estabilidade e sincronização; estratégias de carga prioritária; aterramento, cabos, barramentos, instalação física, incêndio, ventilação, operação e manutenção.
