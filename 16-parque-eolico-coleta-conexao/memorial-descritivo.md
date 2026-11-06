# Memorial descritivo — P16

## Objetivo e escopo

Representar a arquitetura elétrica conceitual de um parque eólico terrestre hipotético, desde os terminais de geração até um ponto de conexão ilustrativo. O estudo mostra cinco blocos de aerogerador e transformação unitária, dois circuitos coletores radiais, subestação coletora com transformação principal e interfaces funcionais de medição, controle e supervisão.

## Solução representada

Cada bloco WTG é considerado como uma unidade de 2,0 MW com conversor e transformador elevador TRG de 2,5 MVA, relação ilustrativa 0,69/34,5 kV. Os cinco blocos totalizam 10 MW instalados. O alimentador F01 reúne WTG-01 a WTG-03 e o F02 reúne WTG-04 e WTG-05; os dois circuitos chegam à barra coletora de 34,5 kV na CSE-01.

A transformação principal TR-01 é representada como 12,5 MVA, 34,5/69 kV, seguida de um bay e ponto de interconexão POI-01 em 69 kV. O desenho identifica blocos de medição, proteção, PPC e SCADA como interfaces a especificar. A localização do ponto de conexão e a propriedade de cada instalação não foram definidas.

## Critério aritmético

Para fins didáticos, a potência aparente é calculada por `S = P / FP` e a corrente trifásica por `I = P / (√3 × V × FP)`, usando FP = 0,95 e tensões nominais assumidas. Para o parque, `10 MW / 0,95 = 10,526 MVA`. Para cada unidade, `2 MW / 0,95 = 2,105 MVA`. Essas operações não incluem perdas, tolerâncias, sobrecargas, requisitos dinâmicos de reativos, temperatura, altitude ou critérios do fabricante.

## Funcionamento conceitual

Os conversores das turbinas entregariam energia à rede coletora por transformadores unitários. F01 e F02 são seccionáveis por disjuntores conceituais CB-F01 e CB-F02. A barra coletora agrega a geração para a transformação principal. O controle da usina e a medição trocam sinais com os equipamentos de geração e com a interface de conexão; os desenhos indicam a existência dessas interfaces sem fixar lógica, protocolo, ajustes ou permissivos.

## Responsabilidade e limitações

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

Os desenhos não são projeto executivo nem comprovam conexão, desempenho, segurança ou conformidade. Dependem de dados de fabricante, levantamento de campo, recurso eólico, estudos elétricos, requisitos do agente acessado, licenciamento e responsabilidade profissional. O memorial não substitui estudos de fluxo de potência, curto-circuito, estabilidade, qualidade de energia, proteção, aterramento ou análise de risco.
