# Critérios e premissas — P16

## Fatos do escopo

- A finalidade é demonstrar documentação elétrica conceitual de um parque eólico onshore e suas interfaces de conexão.
- A prancha de implantação é esquemática, sem escala, coordenadas, cotas ou rotas mensuradas.
- Os símbolos WTG representam blocos funcionais e não um modelo específico de aerogerador.
- Não foram fornecidos local, dados de vento, fabricante, estudo de conexão ou levantamento topográfico.

## Hipóteses de cálculo e representação

| Parâmetro | Hipótese | Uso |
| --- | ---: | --- |
| Aerogeradores | 5 × 2,0 MW | Total nominal ilustrativo de 10 MW |
| Transformador unitário TRG | 2,5 MVA; 0,69/34,5 kV | Bloco elevador conceitual por WTG |
| Fator de potência | 0,95 | Cálculo aritmético de MVA e corrente |
| Coleta | 34,5 kV | Representação dos dois alimentadores |
| TR-01 | 12,5 MVA; 34,5/69 kV | Transformação principal conceitual |
| POI-01 | 69 kV | Tensão ilustrativa do ponto de conexão |
| Alimentadores | F01 com 3 WTG; F02 com 2 WTG | Organização de unifilar e implantação |

## Verificações aritméticas reproduzíveis

- Potência ativa instalada: `5 × 2,0 = 10,0 MW`.
- Potência aparente por unidade a FP 0,95: `2,0 / 0,95 = 2,105 MVA`.
- Limite ativo equivalente de um TRG a 2,5 MVA e FP 0,95: `2,5 × 0,95 = 2,375 MW`; margem aritmética frente a 2,0 MW: `0,375 MW`.
- Potência aparente agregada da planta: `10,0 / 0,95 = 10,526 MVA`; margem nominal aritmética frente a TR-01 de 12,5 MVA: `1,974 MVA`.
- Corrente trifásica idealizada: `I = P / (√3 × V × FP)`. Resultados de referência: 35,24 A por WTG em 34,5 kV; 176,20 A para 10 MW em 34,5 kV; 88,10 A para 10 MW em 69 kV.

## O que os cálculos não verificam

As margens aparentes não confirmam seleção de transformadores. Os cálculos não incorporam potência reativa exigida, capacidade de conversor, curva P-Q, perdas, fator de disponibilidade, corrente de magnetização, harmônicos, variação de tensão, sobrecarga, temperatura, altitude, impedância, curto-circuito ou transitórios.

As correntes não selecionam cabos nem disjuntores. Não foram definidos método de instalação, resistividade térmica do solo, agrupamento, comprimento, queda de tensão, perdas, suportabilidade térmica/dinâmica a curto-circuito, aterramento, proteção, coordenação ou limites de exportação.

## Itens para projeto futuro

1. Definir sítio, coordenadas, topografia, geotecnia, restrições ambientais, servidões e acessos.
2. Obter medições e avaliação do recurso eólico, classe de turbina, curvas de potência e dados de rede dos fabricantes.
3. Definir o ponto de conexão com o agente acessado e obter requisitos de desempenho e acesso aplicáveis.
4. Elaborar estudos de fluxo de potência, curto-circuito, estabilidade, qualidade de energia, controle de tensão/reativos e proteção.
5. Dimensionar cabos, transformadores, barramentos, aterramento e proteção contra descargas atmosféricas.
6. Definir telecomunicações, PPC, SCADA, medição comercial, sincronismo, intertravamentos, segurança e interfaces de propriedade.

As referências documentais estão em [referencias-normativas.md](referencias-normativas.md); sua citação não comprova aderência do desenho.
