# Memória de cálculo conceitual - Projeto 07

Os valores abaixo são premissas acadêmicas, não resultados experimentais.

## Corrente estimada do barramento HV

Para potência mecânica nominal de 60 kW, rendimento assumido do inversor de 95%,
potência simultânea do CC-CC de 3 kW e tensão mínima de 320 V:

`I_HV = (60000 / 0,95 + 3000) / 320 = 206,743421 A`

O fusível F701 de 250 A é apenas uma proposta inicial. Não foram calculados capacidade
de interrupção, curva tempo-corrente, cabo, temperatura, altitude, ciclo de condução ou
coordenação com a bateria.

## Pré-carga RC

Premissas: `R = 100 Ω`, `C = 0,0022 F`, `V = 400 V`.

- constante de tempo: `tau = R × C = 0,220000 s`;
- tempo ideal até 90%: `t90 = -tau × ln(1 - 0,90) = 0,506569 s`;
- corrente inicial: `I0 = V / R = 4,000000 A`;
- potência inicial instantânea no resistor: `P0 = V² / R = 1.600,000000 W`;
- energia armazenada no elo a 400 V: `E400 = 0,5 × C × V² = 176,000000 J`;
- energia armazenada no elo a 450 V: `E450 = 222,750000 J`.

O timeout proposto de 1,5 s excede `t90` ideal, mas a aceitação depende da medição
VDC/VBAT. Resistências internas, tolerâncias, temperatura, capacitâncias adicionais e
falhas não foram incluídas. RPR-701 precisa ser especificado por energia de pulso e
repetição, não apenas pela potência instantânea calculada.

### Faixa de tensão proposta

Para um capacitor inicialmente descarregado, o modelo ideal é `VDC/VBAT = 1 - exp(-t/RC)`.
Com `R=100 ohm`, `C=2,2 mF`, limiar `0,90` e `tau=0,22 s`, o tempo até o limiar é
`t90=-RC ln(1-0,90)=0,506569 s` em qualquer tensão da faixa. A margem matemática até
o timeout de 1,5 s é 0,993431 s; ela não é uma garantia de margem operacional, pois
medição, filtragem, contatores e dispersões foram excluídos.

| VBAT assumida | VDC a 90% | I0=V/R | P0=V²/R | Energia final do capacitor | Energia dissipada por R até 90% |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 320 V | 288 V | 3,20 A | 1,024 kW | 112,64 J | 111,51 J |
| 400 V | 360 V | 4,00 A | 1,600 kW | 176,00 J | 174,24 J |
| 450 V | 405 V | 4,50 A | 2,025 kW | 222,75 J | 220,52 J |

`P0` é potência instantânea no início do pulso. A energia dissipada foi calculada
como `ER(t90)=0,5 C VBAT² [1-(1-0,90)²]` no circuito ideal. Estes cálculos mostram os
esforços que um componente selecionado precisaria suportar; não certificam o resistor,
seu ciclo de repetição, temperatura, isolamento, fusível ou estratégia de descarga.

## Energia da bateria

A energia nominal assumida de 60 kWh serve apenas para classificação da arquitetura.
Não se calcula autonomia, porque massa, ciclo de condução, perdas, regeneração,
aerodinâmica e estratégia térmica não foram definidos.
