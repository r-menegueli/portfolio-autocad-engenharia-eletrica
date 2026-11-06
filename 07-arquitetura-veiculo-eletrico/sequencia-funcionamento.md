# Sequência de funcionamento - EV-07

## Estados propostos

1. `OFF`: contatores abertos; bateria auxiliar disponível apenas para vigília.
2. `WAKE`: chave ligada; VCU e BMS inicializam e verificam comunicação.
3. `CHECK`: BMS, HVIL, IMD, emergência e colisão precisam estar válidos.
4. `PRECHARGE`: KMN-701 e KPR-701 fecham; KMP-701 permanece aberto.
5. `READY`: quando VDC/VBAT medido atinge 90% dentro do timeout proposto, solicita-se
   o fechamento de KMP-701; retorno auxiliar, tempo máximo de atuação e critério para
   abrir KPR-701 ainda dependem do hardware a selecionar.
6. `DRIVE`: VCU libera torque se APPS/BPS forem plausíveis e o inversor estiver pronto.
7. `FAULT`: torque é zerado; contatores abrem conforme sequência definida pela análise
   de segurança real; um novo ciclo de chave é exigido.

## Temporização da pré-carga

A prancha 11 compara a curva ideal com o timeout proposto. Com R=100 ohm, C=2.200 uF
e limiar de 90%, `tau=0,22 s` e `t90=0,506569 s`, deixando `0,993431 s` de margem
aritmética até 1,5 s. Esse tempo não inclui tolerâncias, bateria, sensor, filtro,
chicote ou movimento dos contatores. O modelo não define o tempo de retorno auxiliar:
confirmar o fechamento de KMP antes de abrir KPR é uma dependência a resolver com o
fabricante. Se a razão medida não atingir o limiar antes do timeout, a proposta vai a
`FAULT`, mantém torque inibido e requer novo ciclo de chave.

## Intertravamentos

O pedido de alta tensão só é aceito se 12 V, BMS, HVIL, isolação, emergência e sinal de
colisão estiverem válidos. `READY` exige contatores sem diagnóstico de solda e
pré-carga confirmada por tensão. Pedal de acelerador inválido, freio conflitante,
timeout CAN, sobretemperatura ou limite do BMS reduz ou remove o pedido de torque.

## Desconexão de emergência

SDE-701 atua no circuito de baixa tensão e solicita desenergização de drivers de
contatores, além de informar VCU/BMS. MSD-701 é o desconector manual em série com a
bateria e destina-se apenas ao conceito de serviço. A eficácia física, categoria de
segurança, acesso de resgate e comportamento pós-colisão não foram validados.

## Rearme

Nenhuma recuperação de comunicação ou retorno de um permissivo causa `READY` ou torque
automaticamente. É necessário remover a solicitação, reconhecer a falha e executar um
novo ciclo de chave.

## Matriz de interfaces e falhas

`matriz-interfaces-falhas.csv` e a prancha P07-09 reúnem dez eventos e apontam o sinal,
a reação proposta, o estado e a pendência de validação. Onde a resposta depende de
hardware, a matriz mantém essa decisão em aberto. Em especial, contatores soldados,
perda de alimentação, latência de desligamento e retorno pós-falha exigem análise dos
circuitos e componentes selecionados; a matriz não valida uma função de segurança.
