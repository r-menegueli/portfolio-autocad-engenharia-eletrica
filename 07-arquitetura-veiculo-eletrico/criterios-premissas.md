# Critérios, premissas e limites - Projeto 07

## Fatos técnicos de referência

- Um inversor de tração possui barramento CC capacitivo e converte energia elétrica
  entre o barramento CC e o motor CA trifásico.
- A pré-carga limita a corrente de energização do capacitor do barramento antes do
  fechamento do caminho principal.
- O controle V/f é escalar; o FOC usa um modelo e transformações de coordenadas para
  desacoplar as componentes de fluxo e torque.
- A rede CAN de alta velocidade adota barramento linear com terminação nas extremidades.
- Um sistema HV veicular real exige engenharia de segurança elétrica, funcional,
  térmica, mecânica e de compatibilidade eletromagnética além deste desenho.

Esses itens descrevem princípios gerais. Não constituem comprovação de conformidade do
EV-07 nem resultados experimentais do TCC.

## Premissas acadêmicas numéricas

- bateria BAT-HV-701: 400 Vcc nominais, faixa operacional proposta de 320 a 450 Vcc e
  energia nominal assumida de 60 kWh;
- motor IM-701: 60 kW nominais assumidos, trifásico, de indução;
- inversor INV-701: classe conceitual de 75 kVA e rendimento assumido de 95% no ponto
  usado apenas para estimar a corrente do barramento;
- capacitor equivalente do elo CC: 2.200 µF;
- resistor de pré-carga RPR-701: 100 Ω, sujeito a validação de pulso, temperatura e
  repetição;
- limiar proposto para transição: VDC/VBAT >= 90% em até 1,5 s;
- conversor DCDC-701: 400/14 Vcc, 3 kW; bateria BAT-LV-701: 12 V, 40 Ah;
- fusível principal F701: 250 A apenas como coordenação inicial; cabos HV de 70 mm²
  apenas como hipótese geométrica e de lista.

## Propostas conceituais

- arquitetura com dois contatores principais, KMN-701 e KMP-701, e ramo de pré-carga
  KPR-701 + RPR-701 em paralelo com o contator positivo;
- HVIL-701, IMD-701, SDE-701 e sinal de colisão como permissivos independentes para a
  solicitação de alta tensão;
- CAN-PT a 500 kbit/s, com VCU-701 e BMS-701 nas extremidades e duas terminações de
  120 Ω; identificadores e períodos da matriz são exemplos;
- V/f para estudo de controle escalar e FOC sensorizado para estudo de controle
  vetorial; a seleção não é feita automaticamente por este modelo.

## Critérios de projeto

- o barramento HV é representado como sistema isolado; o chassi não conduz corrente
  normal de tração;
- carcaças e blindagens recebem ligação equipotencial ao chassi, sujeita a estudo EMC;
- a perda de qualquer permissivo abre contatores e bloqueia novo torque;
- o contator de pré-carga nunca permanece fechado no estado de tração;
- a transição para `READY` exige confirmação de tensão, não apenas temporização;
- falha ou timeout mantém os contatores principais abertos e exige novo ciclo de chave;
- comandos CAN não substituem caminhos físicos de desligamento exigidos pela análise de
  segurança de um veículo real.

## Limitações

Não foram modelados arco, resistência interna da bateria, indutâncias parasitas,
temperatura, envelhecimento, curto-circuito, isolamento, crashworthiness, regeneração,
limites de aderência, observador FOC, saturação magnética ou identificação de parâmetros.
As seções de cabos, proteções e componentes não podem ser usadas para fabricação.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
