# Critérios técnicos e premissas

## Dados assumidos

| Tema | Premissa acadêmica |
|---|---|
| Rede | 220 V, 3 fases, 60 Hz, TN-S, corrente de curto-circuito não informada |
| Bombas | M1 e M2, 3 kW cada, 220 V trifásico, corrente nominal estimada 10,8 A |
| Partida | Direta por contator; verificar impacto hidráulico e elétrico no caso real |
| Comando | 24 Vcc PELV conceitual, fonte 10 A, saídas digitais PNP |
| CLP | Genérico, 16 DI e 16 DO, memória retentiva para alternância |
| Painel | Invólucro conceitual 800 x 600 x 300 mm; IP e material não definidos |
| Ambiente | Interno, sem atmosfera explosiva; temperatura/altitude não levantadas |
| Processo | Sentido (enchimento ou esgotamento), tanques de origem/destino e função/localização dos quatro sensores ainda pendentes; P03-11 compara as duas lógicas sem selecionar uma |

## Critérios de operação

- Emergência, RT1/RT2 e KDRY são permissivos prioritários às ordens do CLP.
- A alternância muda somente ao fim de um ciclo automático concluído em LSL.
- Falha de partida é ausência de retorno KM em até 2 s após comando.
- LSHH solicita a segunda bomba após 10 s se a demanda persiste e ambas estão aptas.
- Funcionamento contínuo acima de 30 min gera alarme de tempo excedido e bloqueio.
- Rearme exige causa removida; o reconhecimento silencia o alarme sonoro, mas não
  elimina o registro de falha.
- Combinações impossíveis dos níveis (por exemplo LSHH sem LSH) geram falha de sensor.
- A V01 deve confirmar se as bombas enchem ou esvaziam o reservatório. A sequência
  atualmente desenhada (LSH inicia, LSL encerra e LSHH solicita reserva) pode agravar
  uma condição de nível alto se aplicada a enchimento; não implementar antes de aprovar
  o processo e identificar tanques e sensores, inclusive a origem de LSL-LL. P03-11
  mostra o contraste didático LSL-inicia/LSH-encerra para enchimento e LSH-inicia/
  LSL-encerra para esgotamento; ação de LSHH, bomba reserva e resposta a falha não
  ficam aprovadas por essa comparação.
- Falha de sensor incoerente bloqueia novas partidas automáticas; a resposta para bomba
  já em marcha é uma decisão de processo pendente e não deve ser inferida desta prancha.
- A prancha 09 e `matriz-causa-efeito.csv` resumem a sequência e os eventos tratados;
  tempos de 2 s, 10 s, 30 min e 0,5 s permanecem premissas acadêmicas.

## Orçamento da fonte 24 Vcc

| Carga | Corrente de projeto |
|---|---:|
| CLP e módulos | 1,20 A |
| Sensores e seletores | 0,50 A |
| Relés de interface e segurança | 0,80 A |
| Contatores por relés de interface | 0,50 A |
| Sinalização e buzzer | 1,00 A |
| Reserva documentada | 2,00 A |
| Total considerado | 6,00 A |

A fonte de 10 A apresenta margem conceitual de 4 A. O valor final depende de folhas de
dados, simultaneidade, corrente de energização, temperatura e capacidade dos módulos.

## Pontos que exigem revisão profissional

- tensão e regime reais, dados de placa, curvas das bombas e processo hidráulico;
- correntes de curto-circuito, capacidade de interrupção e coordenação/seletividade;
- seção e método de instalação dos cabos, queda de tensão e proteção contra choque;
- análise de risco, arquitetura de segurança, categoria/PL/SIL e tempo de parada;
- classificação do invólucro, dissipação, EMC, segregação, ventilação e acesso;
- tipo, posição, lógica e modo de falha dos sensores de nível;
- programa final do CLP, testes de causa e efeito, FAT, SAT e comissionamento.

## Convenções

Os desenhos usam símbolos próprios coerentes e identificação funcional baseada em
convenções IEC. O alinhamento é informativo; não se afirma conformidade integral com
normas cujo conteúdo completo não integrou esta elaboração. DXF AC1027 em milímetros é
a fonte; PDF, SVG e PNG são derivados.
