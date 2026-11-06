# Memorial descritivo — P14

## Objetivo

Apresentar a arquitetura de distribuição elétrica de um data center de TI hipotético, com caminhos A/B até as cargas, geração local, UPS modular, distribuição por PDUs e premissas quantitativas rastreáveis.

## Arquitetura conceitual

Cada caminho A e B contém uma alimentação MT representativa, transformador TR, quadro QGBT com posição de transferência, grupo gerador GE, UPS modular e PDU. Os racks R01 a R06 possuem duas entradas de alimentação, uma por caminho. A separação A/B é um objetivo de desenho; não foram demonstradas independência das fontes, rotas físicas, salas, proteção contra falhas comuns ou manutenção simultânea.

O arranjo assume 1.000 kW de carga de TI e 500 kW de climatização e auxiliares, totalizando 1.500 kW. O PUE de 1,50 e o fator de potência 0,95 são premissas didáticas. Cada caminho de UPS contém cinco módulos de 250 kW: quatro módulos entregam 1.000 kW e o quinto representa reserva N+1. Em condição normal, a carga de TI é representada dividida entre A e B; com um caminho indisponível, o caminho remanescente deve aceitar a carga integral de TI.

Cada caminho também mostra um transformador e um grupo gerador de 2.000 kVA. Para comparações aritméticas, foram assumidos FP 0,95 para transformadores e FP 0,90 para geradores. Esses resultados não selecionam equipamentos nem demonstram capacidade de partida, regime térmico, fator de carga, seletividade ou desempenho dinâmico.

## Sequência funcional representada

Em operação normal, as duas UPS mantêm suas saídas e a carga é distribuída entre os caminhos. Na perda da fonte normal, as baterias sustentam a carga sem interrupção enquanto os geradores partem e a transferência ocorre conforme lógica ainda a projetar. Com um caminho A indisponível, o caminho B é representado atendendo a 1.000 kW de TI e 500 kW de cargas de suporte. A sequência de retorno, autonomia, paralelismo, rampas e intertravamentos dependem dos fabricantes e de estudos específicos.

## Limitações e responsabilidade

O estudo não define alimentação da concessionária, transformadores, geradores, UPS, baterias, combustível, QMT, QGBT, PDUs, cabos, barramentos, aterramento, proteção, curto-circuito, seletividade, harmônicos, partida de motores, coordenação térmica, arquitetura física ou cargas reais. Não classifica o data center em qualquer nível TIA Rated ou Tier e não demonstra conformidade com ISO/IEC 22237, ANSI/TIA-942 ou normas brasileiras.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
