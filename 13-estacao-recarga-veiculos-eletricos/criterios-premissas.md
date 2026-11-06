# Critérios e premissas — P13

## Dados usados no estudo

| Item | Valor de representação | Classificação |
| --- | --- | --- |
| Equipamentos AC | 4 × 11 kW de potência nominal de saída | Hipótese didática; modelo OEM não selecionado |
| Equipamentos DC | 2 × 60 kW de potência nominal de saída | Hipótese didática; modelo OEM não selecionado |
| Soma nominal de saída | 164 kW | Aritmética: 4 × 11 + 2 × 60 |
| Alimentação indicada | 380/220 V, 3F+N+PE, 60 Hz | Hipótese gráfica; não confirmada pela concessionária |
| Dimensão gráfica da vaga | Envelope de referência 2,5 × 5,0 m | Hipótese de arranjo, não levantamento nem aprovação |
| Folha CAD | A3 paisagem, milímetros, DXF AC1027 | Padrão do repositório |

## Critérios de representação

- Identificar equipamento, alimentador, sinal e interface com tags coerentes entre desenhos, CSV e documentação.
- Separar visualmente a distribuição de potência da interface de instrumentação/gestão.
- Manter posições QF-01 a QF-06 como funções sem seleção de especificação ou ajuste.
- Tratar a lógica EMS como sequência conceitual; todas as condições de aceitação e estados seguros dependem de análise posterior.
- Exibir os cenários da folha 03 como soma de potência nominal de saída. Não converter essas somas em corrente ou demanda de entrada.
- Usar 380/220 V apenas para contextualizar uma arquitetura trifásica hipotética. Não dimensionar pelo valor ilustrativo.

## Cálculos que podem ser conferidos

- Potência nominal agregada de saída: `4 × 11 kW + 2 × 60 kW = 164 kW`.
- Cenário S1: `2 × 60 kW = 120 kW`.
- Cenário S2: `2 × 60 kW + 2 × 11 kW = 142 kW`.
- Cenário S3: `1 × 60 kW + 3 × 11 kW = 93 kW`.
- Cenário S4: `2 × 60 kW + 4 × 11 kW = 164 kW`.

Esses valores são de saída nominal hipotética. Para estabelecer a potência absorvida pela rede, ainda são necessários dados de placa, eficiência, fator de potência, comportamento do carregador, limites de controle, cargas coincidentes e critérios de demanda.

## Dependências de projeto

Permanecem pendentes: levantamento e propriedade do local; rota, acessos e critérios de circulação; condições de acessibilidade e sinalização; dados de fornecimento e concessionária; demanda existente e capacidade disponível; tensão e regime de aterramento; corrente máxima e mínima de curto-circuito; equipamentos e documentação dos fabricantes; corrente de entrada e proteção requerida; instalação e comprimento dos circuitos; temperatura, agrupamento e método de instalação; cabos, terminações e seletividade; aterramento e equipotencialização; proteção contra surtos; interoperabilidade e protocolo do EMS; comportamento de perda de comunicação; prioridades e políticas de operação; requisitos de faturamento e medição; e verificações regulamentares aplicáveis.

## Limites

Nenhuma proteção, seção de condutor, eletroduto, barramento, transformador, sistema de aterramento, ajuste, acessibilidade ou capacidade de conexão foi selecionado ou calculado. A geometria não é levantamento. As referências normativas são pontos de consulta e não demonstram conformidade.
