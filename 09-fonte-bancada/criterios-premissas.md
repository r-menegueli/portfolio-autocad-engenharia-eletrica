# Critérios e premissas

## Fatos do artefato

- São exigidas seis pranchas A3 paisagem, DXF AC1027 como fonte e derivados PDF,
  SVG e PNG.
- A documentação deve incluir entrada e proteção, conversão, regulação, medição,
  conectores, comandos, ventilação, painel frontal e organização interna.
- O projeto é acadêmico; não existe protótipo, placa, gabinete, ensaio ou certificação.

## Premissas elétricas

- Alimentação monofásica universal: 90-264 Vca, 47-63 Hz, por L, N e PE.
- Equipamento de classe I proposto, com PE permanente no chassi e nunca seccionado.
- PS1 é uma especificação funcional fictícia: AC/DC isolada, 36 Vcc, 7 A, 252 W.
- REG1 é uma especificação funcional fictícia: buck CC/CV, 0-30 Vcc, 0-5 A,
  máximo 150 W e rendimento de cálculo de 92%.
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

- ausência de esquema eletrônico e PCB detalhados de PS1, REG1, PS2 e M1;
- ausência de análise de risco, ensaios dielétricos, corrente de toque, continuidade
  do PE, temperatura, fogo, curto-circuito, falha única, EMC e exatidão;
- ausência de materiais, tratamento superficial, tolerâncias gerais, torque, raios,
  ferramental, processo de corte e desenhos de fabricação;
- ausência de seleção comercial, certificados, datasheets e rastreabilidade de lote;
- ausência de verificação de NR-10 aplicável à atividade e de avaliação formal pela
  série IEC 61010.

## Classificação epistemológica

- `FATO`: requisito documental ou resultado observado no repositório.
- `PREMISSA`: valor adotado apenas para viabilizar cálculos acadêmicos.
- `PROPOSTA`: solução de arquitetura ainda sujeita a seleção e revisão.
- `DERIVADO`: resultado matemático reproduzível a partir das premissas.
- `PENDENTE`: decisão que exige fabricante, ensaio, análise de risco ou profissional.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
