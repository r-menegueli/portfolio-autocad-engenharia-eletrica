# Filosofia de controle

## Definições da malha LIC-101

| Elemento | Definição |
|---|---|
| Variável controlada | Nível de TK-101, em % |
| Variável manipulada | Frequência de VFD-101, em Hz |
| Medição | LT-101, 4–20 mA = 0–100% |
| Elemento final | VFD-101 + M-101 + P-101 |
| Perturbação principal | Vazão de saída/consumo |
| Setpoint inicial | 60% |

## Modos

Em automático, LIC-101 calcula a referência do VFD. Se PV ficar abaixo de SP, a frequência aumenta; se PV subir acima de SP, a frequência diminui. Em manual, o operador ajusta a referência dentro dos mesmos limites e intertravamentos. A troca entre modos deve ocorrer sem salto de saída, com rastreamento e anti-windup.

## Permissivos e intertravamentos

- Partida permitida somente com emergência liberada, relé KSR-101 pronto, VFD pronto, ausência de LSHH-101 e medição LT-101 válida.
- LSHH-101 em 95% remove o permissivo e solicita parada do VFD independentemente da rotina PID comum.
- Falha de VFD ou tempo máximo de enchimento excedido bloqueia a partida e memoriza alarme.
- Rearme somente após remoção da causa e comando consciente do operador.

## Alarmes

- LA-L-101: nível baixo em 15%.
- LA-H-101: nível alto em 85%.
- LA-HH-101: nível alto-alto em 95%, com bloqueio.
- YA-101: falha de VFD.
- UA-101: sinal LT-101 fora de faixa ou diagnóstico inválido.
- TA-101: tempo máximo de enchimento, premissa inicial de 60 min.

## Falhas

Sinal LT-101 abaixo de 3,6 mA ou acima de 21 mA desabilita o PI, solicita parada da bomba e gera alarme. Operação manual excepcional exige procedimento aprovado e observação local. Divergência persistente entre LT-101 e chaves de nível gera diagnóstico e bloqueio do automático. Perda de alimentação resulta em saída desenergizada e necessidade de rearme.

Nenhuma função aqui recebe classificação SIL, PL ou categoria de segurança. Essa classificação depende de análise formal de risco e projeto executivo.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
