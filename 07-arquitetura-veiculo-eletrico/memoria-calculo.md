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

## Energia da bateria

A energia nominal assumida de 60 kWh serve apenas para classificação da arquitetura.
Não se calcula autonomia, porque massa, ciclo de condução, perdas, regeneração,
aerodinâmica e estratégia térmica não foram definidos.
