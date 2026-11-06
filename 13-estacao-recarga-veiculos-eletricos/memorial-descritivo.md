# Memorial descritivo — P13

## Objetivo

Organizar um estudo conceitual de uma estação de recarga e tornar rastreáveis as interfaces entre o local, os pontos de carga, a alimentação elétrica e a gestão de potência. O material é voltado à apresentação e ao estudo de documentação de Engenharia Elétrica.

## Configuração proposta

O arranjo mostra seis vagas e seis equipamentos identificados EVSE-01 a EVSE-06. Para o cenário didático, EVSE-01 a EVSE-04 são pontos AC com potência nominal de saída assumida de 11 kW cada, e EVSE-05 e EVSE-06 são pontos DC de 60 kW cada. A soma aritmética dessas potências de saída é 164 kW. Ela não é potência de entrada do conjunto nem demanda diversificada.

O diagrama unifilar conecta a rede de baixa tensão, a medição, o quadro geral existente, o quadro dedicado QEV-01 e seis alimentadores conceituais. Os símbolos QF-01 a QF-06 representam posições funcionais para dispositivos de proteção. Tipo, capacidade, corrente, curva, número de polos, ajustes e coordenação não foram escolhidos. A seleção depende dos dados reais de fornecimento e de cada equipamento.

O EMS-01 é representado como gestor funcional. Em uma implementação futura, poderia receber medições do ponto de entrada e estados dos EVSE, calcular uma margem operacional disponibilizada pelo responsável da instalação e solicitar limites de potência aos equipamentos. O protocolo, a integração com medidores e carregadores, a resposta a falhas de comunicação, as prioridades e as rampas ainda precisam ser definidos com os fabricantes e com a operação.

## Cenários aritméticos da folha 03

Os quatro casos ilustram combinações possíveis de potência nominal de saída: dois pontos DC somam 120 kW; dois DC e dois AC somam 142 kW; um DC e três AC somam 93 kW; os seis pontos somam 164 kW. As somas são conferíveis com a lista de equipamentos. Não representam demanda, corrente, simultaneidade real, limite de importação, eficiência, fator de potência ou capacidade de conexão.

## Referências e representação

As folhas referenciam ABNT NBR 17019:2022, IEC 60364-7-722:2018 e IEC 61851-1:2017, incluindo a corrigenda IEC 61851-1:2017/COR1:2023. O conjunto de normas aplicáveis, respectivas edições, requisitos locais e condições de uso precisam ser confirmados no desenvolvimento de qualquer projeto real. A representação é funcional e simplificada; não define instalação executiva.

## Limitações e responsabilidade

Este estudo não inclui levantamento do terreno ou da instalação existente; estudos de carga, demanda ou conexão; dimensionamento de transformador, barramentos, cabos, eletrodutos, aterramento ou proteções; avaliação de harmônicos, queda de tensão, curto-circuito, seletividade, energia reversa ou compatibilidade eletromagnética; aprovação de acessibilidade ou segurança; configuração de protocolos; ensaios; nem comissionamento.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
