# Sequência de funcionamento

## Inicialização

1. Q0 energiza o painel e PSU1 estabelece 24 Vcc.
2. CLP1 verifica KSR1, KDRY, RT1, RT2 e coerência dos sensores.
3. Não há partida automática após energização enquanto houver falha latente ou demanda
   não reconhecida; a condição pronta é indicada por H1.

## Modo automático

1. Com S1 em AUTO e os permissivos válidos, a ativação de LSH memoriza demanda.
2. A bomba indicada por `titular_proxima` recebe ordem de partida.
3. O retorno do respectivo contator deve ocorrer em até 2 s.
4. Se LSHH permanecer ativo por 10 s, a bomba reserva também parte, se disponível.
5. LSL encerra a demanda e para as bombas.
6. Após ciclo concluído sem falha, `titular_proxima` alterna entre M1 e M2.

## Modo manual

S2/S3 comandam partida/parada de M1 e S4/S5 comandam M2. A seleção MANUAL não contorna
S0/KSR1, KDRY, RT1/RT2, falta de 24 Vcc ou bloqueio de falha. A função manual destina-se
a ensaio e manutenção controlada, não a burlar proteções.

## Falhas e degradação

- **Emergência:** KSR1 abre as cadeias físicas de KM1/KM2; alarme é memorizado.
- **Funcionamento a seco:** LSL-LL desenergiza KDRY e bloqueia as duas bobinas.
- **Sobrecarga:** RT1 ou RT2 remove a bomba afetada e solicita a reserva em automático.
- **Falha de partida:** ausência do retorno KM em 2 s bloqueia a bomba e tenta a reserva.
- **Partida indevida:** retorno KM sem comando gera falha e exige intervenção.
- **Sensor incoerente:** combinações impossíveis de nível impedem nova partida automática.
- **Tempo excedido:** demanda acima de 30 min para as bombas e gera alarme retentivo.
- **Falha total:** se nenhuma bomba estiver disponível durante demanda, H5 e BZ1 atuam.

## Rearme e alarme

S6 reconhece/silencia BZ1 quando mantido por pelo menos 0,5 s. O rearme só remove falhas
quando emergência foi liberada, nível de captação recuperou, RTs foram rearmados e os
retornos dos contatores coincidem com os comandos. H5 permanece aceso enquanto existir
falha ativa ou memorizada.
