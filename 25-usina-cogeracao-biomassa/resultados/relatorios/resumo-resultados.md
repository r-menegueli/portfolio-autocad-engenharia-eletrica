# Resultados — Usina de cogeração a biomassa, 25 MW

## Balanços estáticos recalculados

| Grandeza | Resultado de referência |
|---|---:|
| Potência ativa bruta | 25,000 MW |
| Potência aparente do gerador em operação | 27,778 MVA |
| Potência aparente nominal assumida | 32,000 MVA |
| Corrente do gerador em operação | 1.162,14 A |
| Corrente nominal da placa assumida | 1.338,78 A |
| Exportação líquida | 22,800 MW |
| Exportação reativa após banco | 7,043 MVAr |
| Fator de potência no POI | 0,9555 |
| Corrente no POI | 99,84 A |
| Carregamento aparente do transformador de 40 MVA | 59,66% |
| Curto equivalente em 13,8 kV, com contribuições de rede e máquina usando X'd | 13,714 kA |
| Curto equivalente no lado de 138 kV | 21,441 kA |
| Energia líquida anual a 7.200 h | 164.160 MWh |

Os balanços foram recalculados por `validacao/calculos_independentes_p25.py`; três testes independentes passaram. O curto é uma soma fasorial simplificada com resistência da rede omitida e X'd assumida; não é resultado IEC 60909 nem corrente subtransitória.

## Dinâmica

A série antiga ainda representa somente afundamento de tensão e degrau de potência de referência, em modelo pu agregado. Ela não cobre integralmente os oito cenários requeridos e não foi regenerada nesta revisão. A versão corrigida de `matlab/calculos/run_analysis.m` não foi executada no MATLAB; não atribuir os valores da tabela dinâmica antiga ao código atualizado.

Nenhum resultado é medição, certificação, ajuste de proteção ou liberação de engenharia executiva.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
