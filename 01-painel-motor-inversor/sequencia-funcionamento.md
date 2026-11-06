# Sequência de funcionamento

A representação resumida por estados está na [prancha 09](exports/09_sequencia_operacional_estados.pdf),
cuja fonte de conteúdo é [sequencia-estados.csv](sequencia-estados.csv). Ela organiza a
sequência descrita abaixo; não comprova implementação, ensaio ou resposta de segurança.

## 1. Estado seguro inicial

Q0 aberto isola o circuito principal. O motor permanece sem torque. A posição de Q0
deve admitir bloqueio por procedimento de segurança; STO não substitui seccionamento
nem comprovação de ausência de tensão.

## 2. Energização

1. Confirmar emergência S0 liberada, comandos de partida inativos e área segura.
2. Fechar Q0 e Q1. DPS1 passa a proteger o barramento segundo sua condição indicada.
3. Fechar Q2. PS1 estabelece 24 Vcc e H1 indica painel energizado.
4. KSR1 verifica os dois canais de S0 e aguarda rearme manual monitorado em S5.
5. Com KSR1 rearmado, STO-A e STO-B liberam a geração de torque de VFD1.
6. VFD1 conclui autoteste; H2 indica pronto se não houver falha.

Nenhuma dessas etapas deve iniciar M1 automaticamente.

## 3. Operação local

1. Posicionar S3 em LOCAL; a posição central 0 desabilita as fontes de comando.
2. Ajustar P1, referência de 0-10 V correspondente à faixa configurada de 5-60 Hz.
3. Pressionar S1 PARTIR. A função RUN é enviada à entrada digital configurada para
   partida no VFD1, que acelera M1 pela rampa de 5 s.
4. H3 indica motor em marcha.
5. Pressionar S2 PARAR. A função STOP é enviada à entrada digital configurada para
   parada; VFD1 desacelera pela rampa de 8 s e remove o comando de marcha.

RUN e STOP usam funções de entrada separadas. A polaridade lógica, a seleção entre
comando por nível ou pulso e os bornes concretos dependem do modelo de VFD1 e devem ser
fechados com o manual do fabricante; o diagrama é funcional, não uma ligação executiva.

## 4. Operação remota

1. Garantir ausência de comando ativo e posicionar S3 em REMOTO.
2. O PLC fornece RUN e STOP separados por contatos em X3:7 e X3:8; X3:8 é contato NF
   usado como permissivo da função de parada, conforme a lógica do VFD selecionado.
3. A referência de velocidade chega por W06 em 4-20 mA a X3:10-11.
4. Os contatos de saída em X3:12-14 retornam marcha e falha ao PLC.
5. A perda do sinal de 4-20 mA deve provocar ação segura parametrizada; nesta base,
   adota-se parada controlada e alarme, a confirmar no equipamento escolhido.

## 5. Parada de emergência

1. Ao atuar S0, qualquer canal abre e KSR1 desenergiza suas saídas.
2. STO-A e STO-B de VFD1 são removidos e o inversor deixa de produzir torque.
3. M1 para por inércia; não se declara tempo de parada nem categoria de parada.
4. O comando de marcha é cancelado e o evento deve ser sinalizado.
5. A liberação física de S0 não rearma o sistema. Depois de confirmar a condição segura,
   pressionar S5 solicita somente o rearme manual monitorado de KSR1. O rearme de S5
   não solicita RUN; um novo comando S1 ou X3:7 é necessário.

## 6. Falha e rearme

Falhas do inversor removem a condição de pronto, desligam H3 e acendem H4. O operador
deve identificar e eliminar a causa. S4 (LOCAL) ou X3:9 (REMOTO) solicita somente o
reset de falha de VFD1. Esses comandos são distintos do rearme de segurança S5/KSR1 e
não devem mascarar falha presente nem gerar partida automática.

## 7. Falta e retorno de energia

Na falta de rede, VFD1 e PS1 desenergizam. No retorno, o rearme automático e a retomada
automática permanecem desabilitados. O sistema volta ao estado pronto somente após as
verificações e exige novo comando de partida.

## 8. Troca local/remoto

A troca de S3 durante a marcha deve primeiro remover o comando vigente e conduzir a
uma parada controlada. A posição 0 desabilita os comandos. O novo modo só aceita partida
após detecção de estado inativo e novo comando de partida; essa lógica precisa ser
implementada no VFD ou PLC real e verificada em ensaio. S3 é conceitualmente de três
posições LOCAL-0-REMOTO; quantidade e arranjo dos blocos de contato permanecem pendentes.
