# Memorial descritivo — P15

## Objetivo

Documentar uma microrrede industrial CA hipotética com interface à rede, geração fotovoltaica, armazenamento em baterias, grupo gerador e cargas com prioridades distintas. O material rastreia a topologia, o conjunto de cargas e somas de potência para modos operacionais ilustrativos.

## Configuração conceitual

O unifilar conecta a rede MT ao ponto de acoplamento comum PCC-01, ao transformador TR-01 e ao QGBT-MG. No barramento CA da microrrede são representados o inversor FV-01, o conversor BESS-01 e o GE-01. A carga assumida é 1.000 kW, composta por 800 kW prioritários e 200 kW não prioritários.

O campo FV tem potência AC assumida de 600 kW. O BESS é representado com conversor de 500 kW e energia nominal de 1 MWh. O gerador fornece 500 kW na hipótese de estudo. O transformador é representado com 1.500 kVA; a conversão em potência ativa usa FP 0,95 apenas para comparação aritmética. Não foram escolhidos modelos, valores de proteção ou especificações construtivas.

## Modos representados

Em modo conectado, a carga de 1.000 kW é ilustrada com 600 kW FV e 400 kW da rede. Em ilhamento, combinações de FV, GE e BESS são somadas para atender a carga. Em um caso de indisponibilidade do GE, 300 kW de FV e 500 kW do BESS sustentam os 800 kW prioritários, com corte ilustrativo de 200 kW não prioritários. O fechamento e a abertura do PCC, o estabelecimento da referência de tensão e frequência, os ajustes e a sincronização não são definidos.

A razão 1 MWh / 500 kW resulta em duas horas ideais. Ela não é autonomia garantida: não inclui eficiência, estado de carga inicial/final, reserva operacional, potência variável, temperatura, degradação ou limites do fabricante.

## Limitações e responsabilidade

Este conceito não inclui estudo de conexão, fluxo de potência, estabilidade, frequência, tensão, curto-circuito, seletividade, proteção anti-ilhamento, sincronismo, aterramento, cabos, barramentos, harmônicos, demanda, comportamento transitório, operação paralela de geradores, segurança contra incêndio ou especificação de baterias. Não demonstra conformidade normativa nem autorização para operação conectada ou ilhada.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
