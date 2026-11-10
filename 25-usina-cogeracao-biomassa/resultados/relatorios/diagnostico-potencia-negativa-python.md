# Diagnóstico do resultado de potência ativa negativa — P25

## Execução e ponto nominal

Este arquivo foi gerado pelo modelo agregado RK4 em Python. Não é saída MATLAB/Simulink.
No ponto inicial, Pe = 25.000 MW e o resíduo da equação de balanço do rotor é 0.000e+00 pu.
A potência usa `Pe = Efd·Vgrid/Xd'·sin(δ)`, com sinal definido pelo ângulo do rotor. Não foi aplicada inversão nem saturação artificial de Pe.

## Sensibilidade do cenário de afundamento

| dt (s) | Pe final em 5 s (MW) | Pe mínima (MW) | t da mínima (s) | Pe máxima (MW) | t da máxima (s) | I máxima (A) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.005 | -6.291 | -21.242 | 1.3550 | 72.827 | 1.1650 | 5578.3 |
| 0.0025 | -5.755 | -20.350 | 1.3575 | 72.799 | 1.1650 | 5604.6 |
| 0.00125 | -5.424 | -19.852 | 1.3588 | 72.706 | 1.1613 | 5617.3 |
| 0.000625 | -4.864 | -19.133 | 1.3606 | 71.421 | 1.1613 | 5634.8 |

O cenário nominal inicial mantém exportação positiva. Após a falta sintética de 0,2 pu por 0,12 s, δ cruza zero durante a oscilação e Pe fica temporariamente negativo. Isso é reversão de potência ativa prevista pela equação assinada do modelo; os picos calculados também ultrapassam 25 MW e 32 MVA, mostrando que o equivalente não inclui limites de corrente/estabilidade utilizáveis para liberar equipamento.

A comparação entre passos e horizontes está no JSON ao lado. A variação numérica não foi ocultada: a curva de 5 s permanece sensível ao passo devido a descontinuidades e limitadores do modelo reduzido. Em horizonte maior, a comparação serve apenas para conferir a tendência deste sistema matemático; não valida a usina real.

## Conclusão técnica

O valor negativo não deve ser corrigido invertendo o sinal ou cortando a curva. É um resultado transitório do modelo, enquanto a magnitude de pico e a sensibilidade numérica deixam a resposta inadequada para concluir estabilidade, suportabilidade à falta ou comportamento de uma unidade comercial. O modelo Simulink ainda precisa de execução real e revisão técnica independente.

Reprodução: `python 25-usina-cogeracao-biomassa/validacao/diagnostico_potencia_negativa_p25.py`.
