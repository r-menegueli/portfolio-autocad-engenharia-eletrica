# Sequência de funcionamento

## 1. Estado seguro inicial

Q0 aberto isola o circuito principal. O motor permanece sem torque. A posição de Q0
deve admitir bloqueio por procedimento de segurança; STO não substitui seccionamento
nem comprovação de ausência de tensão.

## 2. Energização

1. Confirmar emergência S0 liberada, comandos de partida inativos e área segura.
2. Fechar Q0 e Q1. DPS1 passa a proteger o barramento segundo sua condição indicada.
3. Fechar Q2. PS1 estabelece 24 Vcc e H1 indica painel energizado.
4. KSR1 verifica os dois canais de S0 e aguarda rearme manual válido.
5. Com KSR1 rearmado, STO-A e STO-B liberam a geração de torque de VFD1.
6. VFD1 conclui autoteste; H2 indica pronto se não houver falha.

Nenhuma dessas etapas deve iniciar M1 automaticamente.

## 3. Operação local

1. Posicionar S3 em LOCAL.
2. Ajustar P1, referência de 0-10 V correspondente à faixa configurada de 5-60 Hz.
3. Pressionar S1 PARTIR. VFD1 reconhece DI1 e acelera M1 pela rampa de 5 s.
4. H3 indica motor em marcha.
5. Pressionar S2 PARAR. VFD1 desacelera pela rampa de 8 s e remove o comando de marcha.

## 4. Operação remota

1. Garantir ausência de comando ativo e posicionar S3 em REMOTO.
2. O PLC fornece RUN e STOP por contatos em X3:7 e X3:8.
3. A referência de velocidade chega por W06 em 4-20 mA a X3:10-11.
4. Os contatos de saída em X3:12-14 retornam marcha e falha ao PLC.
5. A perda do sinal de 4-20 mA deve provocar ação segura parametrizada; nesta base,
   adota-se parada controlada e alarme, a confirmar no equipamento escolhido.

## 5. Parada de emergência

1. Ao atuar S0, qualquer canal abre e KSR1 desenergiza suas saídas.
2. STO-A e STO-B de VFD1 são removidos e o inversor deixa de produzir torque.
3. M1 para por inércia; não se declara tempo de parada nem categoria de parada.
4. O comando de marcha é cancelado e o evento deve ser sinalizado.
5. A liberação física de S0 não rearma o sistema. É necessário rearme manual e novo
   comando de partida após confirmação da condição segura.

## 6. Falha e rearme

Falhas do inversor removem a condição de pronto, desligam H3 e acendem H4. O operador
deve identificar e eliminar a causa. S4 ou o comando remoto em X3:9 apenas solicita o
rearme; não deve mascarar falha presente nem gerar partida automática.

## 7. Falta e retorno de energia

Na falta de rede, VFD1 e PS1 desenergizam. No retorno, o rearme automático e a retomada
automática permanecem desabilitados. O sistema volta ao estado pronto somente após as
verificações e exige novo comando de partida.

## 8. Troca local/remoto

A troca de S3 durante a marcha deve primeiro remover o comando vigente e conduzir a
uma parada controlada. O novo modo só aceita partida após detecção de estado inativo.
Essa lógica precisa ser implementada no VFD ou PLC real e verificada em ensaio.
