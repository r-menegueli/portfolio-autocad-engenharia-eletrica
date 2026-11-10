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

A série atual foi regenerada pelo modelo agregado RK4 em Python: 8 cenários e 8.008 amostras. No afundamento sintético de 0,2 pu por 0,12 s, com passo de 5 ms, a corrente máxima calculada é 5.578,30 A; a potência ativa atinge 72,827 MW e −21,242 MW, e termina em −6,291 MW aos 5 s. O sinal negativo ocorre quando o ângulo do rotor fica negativo na equação assinada; não deve ser invertido ou limitado artificialmente. A sensibilidade do valor final ao passo (−6,291 MW a 5 ms; −4,864 MW a 0,625 ms) permanece significativa, e os picos excedem os valores nominais. Portanto, esta série não prova estabilidade ou suportabilidade.

O MATLAB R2026a executou os balanços estáticos e os testes MATLAB do projeto. A dinâmica MATLAB e o modelo Simulink não foram executados com sucesso; os números acima vêm somente da alternativa Python, não de Simulink.

Nenhum resultado é medição, certificação, ajuste de proteção ou liberação de engenharia executiva.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
