# Sequência de funcionamento - CCM-06

## Permissivo comum

Com QG-06 ligado, PSU-601 energiza o comando. KSR-601 somente libera os contatores e
STO A/B quando os dois canais de S0-601 estão íntegros e houve rearme manual. Abertura
da emergência desenergiza KM-601, KM-602F e KM-602R e remove torque de M-603 via STO.
O retorno do permissivo não produz partida automática.

## Bomba M-601 - partida direta

1. QF-601 e FR-601 devem estar disponíveis.
2. S-601L energiza KM-601 através de KSR-601, S0-601, S-601P e FR-601.
3. Um contato NA de KM-601 mantém o selo após o impulso de partida.
4. S-601P, FR-601, emergência ou perda de alimentação abrem o circuito da bobina.
5. Novo funcionamento exige novo comando em S-601L.

## Esteira M-602 - partida reversora

1. S-602F solicita frente se FC-602F, FR-602 e o contato NF de KM-602R permitem.
2. S-602R solicita reverso se FC-602R, FR-602 e o contato NF de KM-602F permitem.
3. Os contatores KM-602F/KM-602R têm trava mecânica IM-602 além da trava elétrica.
4. A troca de sentido exige parada, desenergização do contator ativo e novo comando.
5. Comandos simultâneos não podem fechar os dois contatores.

## Ventilador M-603 - inversor

1. QF-603 alimenta VFD-603; não existe contator de manobra na saída PWM.
2. KSR-601 entrega os dois canais STO A/B.
3. SA-603 seleciona local/remoto; DI1 e DI2 recebem partida/parada.
4. P-603 fornece referência de velocidade 0-10 V em cabo blindado.
5. RO1/RO2 sinalizam marcha e falha; uma falha exige diagnóstico e novo comando.
