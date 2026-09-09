# Sequência de funcionamento - EV-07

## Estados propostos

1. `OFF`: contatores abertos; bateria auxiliar disponível apenas para vigília.
2. `WAKE`: chave ligada; VCU e BMS inicializam e verificam comunicação.
3. `CHECK`: BMS, HVIL, IMD, emergência e colisão precisam estar válidos.
4. `PRECHARGE`: KMN-701 e KPR-701 fecham; KMP-701 permanece aberto.
5. `READY`: após VDC/VBAT >= 90%, KMP-701 fecha e KPR-701 abre.
6. `DRIVE`: VCU libera torque se APPS/BPS forem plausíveis e o inversor estiver pronto.
7. `FAULT`: torque é zerado; contatores abrem conforme sequência definida pela análise
   de segurança real; um novo ciclo de chave é exigido.

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
