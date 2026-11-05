# Critérios e premissas

## Fatos do artefato

- São exigidas dez pranchas A3 paisagem, DXF AC1027 como fonte e derivados PDF,
  SVG e PNG.
- A documentação deve incluir entrada e proteção, conversão, regulação, medição,
  conectores, comandos, ventilação, painel frontal e organização interna.
- O projeto é acadêmico; não existe protótipo, placa, gabinete, ensaio ou certificação.

## Premissas elétricas

- Alimentação monofásica universal: 90-264 Vca, 47-63 Hz, por L, N e PE.
- Equipamento de classe I proposto, com PE permanente no chassi e nunca seccionado.
- PS1 é uma especificação funcional fictícia: AC/DC isolada, 36 Vcc, 7 A, 252 W.
- REG1 é um estágio proposto de buck síncrono CC/CV. U1 LM5190 é candidato de
  arquitetura documentado pela TI, com 36 Vcc nominais na entrada, 0,8-30 Vcc
  regulados, até 5 A e 150 W máximos. K1 aberto desabilita a entrega de potência;
  sem circuito de descarga dimensionado e validado, a tensão residual nos bornes não
  é garantida.
- O controlador LM5190 requer entrada de 5-80 V e não regula abaixo de 0,8 V. K1
  interrompe o condutor positivo, mas não curto-circuita nem descarrega a saída. A
  faixa publicada não substitui a validação de tolerância, transitórios, MOSFETs e
  térmica.
- A revisão 03 separa a capacitância interna da porta X2 e registra equações RC
  ideais em `dimensionamento-descarga.csv`. C_INT_MAX, C_EXT_MAX, tensões máximas
  iniciais, V_SAFE, T_REQ e ratings dos componentes continuam pendentes; 30 V é só o
  limite nominal de ajuste proposto, não o máximo em falha ou transitório.
- A revisão 04 varre POUT=150 W em nove pares de eficiência assumidos (ηPS1 de 88%,
  92% e 96%; ηREG1 de 85%, 90% e 95%). São cenários de sensibilidade sem origem em
  fabricante ou medição; a faixa não afirma o desempenho real do conjunto.
- A potência dissipada em cada conversor é obtida por balanço ideal de potência. O
  resultado agregado não distribui perdas entre semicondutores, indutor, shunt e
  passivos e não permite estimar temperatura de junção. Rθ, limites térmicos, fluxo de
  ar e derating dependem dos componentes e do gabinete finais.
- KD1/RD1 e KD2/RD2 são blocos conceituais. O ramo KD2 exige porta isolada de toda
  fonte externa e um permissivo/intertravamento validado; não deve fechar se houver
  alimentação ou retorno de energia em X2. Não há alegação de tensão zero ou tempo de
  descarga garantido. Verificar energia e potência de pulso, repetição, temperatura,
  tolerâncias, estados de falha e comportamento dos contatos antes de qualquer seleção.
- O pré-dimensionamento acadêmico assume fSW=100 kHz, L1=75 uH, RCS=9,1 mOhm e
  RIMON=8,62 kOhm. O cenário de 42 V é apenas uma sensibilidade paramétrica; PS1
  continua sem uma curva real de tolerância.
- A saída CC é flutuante; o borne negativo não é ligado internamente ao PE. Há borne
  verde separado para referência voluntária ao chassi.
- O limite eletrônico de corrente é função de regulação, não dispositivo de segurança
  certificado. F2 de 7,5 A protege preliminarmente o barramento de 36 Vcc.
- O medidor M1 usa shunt SH1 de 10 A/75 mV e linhas Kelvin separadas.
- PS2 converte 36 Vcc para 12 Vcc/1 A para medição, relé, LEDs e ventilação.

## Premissas térmicas e mecânicas

- Uso interno e seco, 0-40 °C, altitude até 2.000 m e grau de poluição 2 como base
  de análise; nenhuma categoria de sobretensão ou grau IP foi certificado.
- Gabinete de referência: 320 mm de largura, 150 mm de altura, 260 mm de profundidade,
  painel frontal metálico de 3 mm.
- Ventilador de 80 mm, 12 Vcc e 20 CFM em ar livre. Adota-se 50% de vazão efetiva e
  elevação de temperatura-alvo de 15 °C.
- Fluxo de ar proposto da lateral frontal para exaustão traseira, sem recirculação
  direta. Entradas devem manter área livre mínima equivalente à do ventilador.
- TH1 liga a ventilação a 40 °C; TS1 remove a habilitação da saída a 75 °C. Pontos de
  montagem, histerese e contatos exigem ensaio em protótipo.
- A zona de rede deve permanecer coberta e segregada. Distâncias de escoamento,
  isolação, inflamabilidade e acesso a partes vivas não foram dimensionados.

## Critérios preliminares

- F1: fusível retardado T4 A/250 Vca na fase, com capacidade de interrupção a
  selecionar para a instalação prevista.
- S1: chave bipolar 10 A/250 Vca, desligando L e N sem interromper PE.
- FL1: filtro EMI bipolar 10 A/250 Vca; MOV1: varistor classe 275 Vca, coordenado com
  F1 somente após ensaios e dados do fabricante.
- Condutores L/N internos: 0,75 mm², 600 V, 105 °C; PE: 1,5 mm² verde-amarelo;
  barramentos de 36 V e saída: 2,5 mm²; sinais e Kelvin: 0,5 mm².
- Queda interna de saída é avaliada em volts e a 30 V; em baixas tensões, o percentual
  não representa o comportamento da malha de sensoriamento remoto.

## Limites que impedem fabricação

- ausência de esquema completo com passivos dimensionados, compensação validada e PCB
  detalhados de PS1, REG1, PS2 e M1;
- ausência de análise de risco, ensaios dielétricos, corrente de toque, continuidade
  do PE, temperatura, fogo, curto-circuito, falha única, EMC e exatidão;
- ausência de materiais, tratamento superficial, tolerâncias gerais, torque, raios,
  ferramental, processo de corte e desenhos de fabricação;
- ausência de seleção dos MOSFETs, indutor, capacitores e redes de compensação,
  certificados e rastreabilidade de lote; U1 permanece candidato, não aprovação final;
- ausência de verificação de NR-10 aplicável à atividade e de avaliação formal pela
  série IEC 61010.

## Classificação epistemológica

- `FATO`: requisito documental ou resultado observado no repositório.
- `PREMISSA`: valor adotado apenas para viabilizar cálculos acadêmicos.
- `PROPOSTA`: solução de arquitetura ainda sujeita a seleção e revisão.
- `DERIVADO`: resultado matemático reproduzível a partir das premissas.
- `PENDENTE`: decisão que exige fabricante, ensaio, análise de risco ou profissional.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
