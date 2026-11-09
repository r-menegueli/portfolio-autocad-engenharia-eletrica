# Critérios e premissas

## Base do estudo

Potência ativa bruta 25 MW, placa 32 MVA, fp de estudo 0,90, tensão 13,8 kV, rendimento elétrico 0,985. T1=40 MVA, 13,8/138 kV, uk=12% assumida. Auxiliares agregados de 2,2 MW/fp 0,90; banco 4 MVAr. Vapor útil de processo=30 MWth. Biomassa=50 t/h, PCI=7,5 MJ/kg, eficiência de caldeira=0,82 e operação=7.200 h/ano. Parâmetros H, D, X'd, AVR e droop são hipóteses ajustáveis, não dados do fabricante. As origens e limitações estão em `dados/origem-parametros.csv`.

## Balanço e curto-circuito

A potência aparente em operação é calculada com a potência ativa e reativa do gerador (27,78 MVA) e comparada à placa assumida (32 MVA). A corrente de operação usa a potência aparente calculada; a corrente de placa é mostrada separadamente. O curto equivalente transforma a impedância do transformador da base de 40 MVA para a base de 32 MVA e soma fasorialmente as contribuições da rede e do gerador usando a reatância transitória cadastrada. É uma análise conceitual, não substitui dados subtransitórios, componentes de sequência, X/R da rede, critério IEC 60909 ou estudo de proteção.

## Dados ausentes e decisões abertas

Os valores assumidos devem ser substituídos por dados de concessionária/operador, fabricante, levantamento e investigação de campo antes do projeto executivo. Não foram definidos ajustes de proteção, especificação de isolamento, coordenação, segurança funcional, aterramento final, esforços estruturais, detalhes civis ou requisitos de conexão.

## Critério de interpretação

As referências técnicas abaixo orientam o escopo e não constituem declaração de conformidade. Em caso de revisão, o responsável deve confirmar edição, emendas, regulamentos e critérios do proprietário válidos para o local e a data do projeto.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
