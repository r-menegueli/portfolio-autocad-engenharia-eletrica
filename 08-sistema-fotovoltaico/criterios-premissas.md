# Critérios e premissas - Projeto 08

## Fatos técnicos e regulatórios

- Um arranjo fotovoltaico produz corrente contínua; um inversor conectado à rede
  converte essa energia em corrente alternada e deve atender aos requisitos aplicáveis
  do produto e da conexão.
- A Lei nº 14.300/2022 institui o marco legal brasileiro da micro e minigeração
  distribuída e do sistema de compensação de energia elétrica.
- A ANEEL mantém a Resolução Normativa nº 1.000/2021, alterada pela Resolução
  Normativa nº 1.059/2023, e o Módulo 3 do PRODIST como referências para conexão.
- O Inmetro indica as Portarias nº 140/2022 e nº 515/2023 para equipamentos
  fotovoltaicos abrangidos pelo regulamento.
- A edição e o estado das referências foram conferidos em fontes oficiais em
  2026-09-09; o texto integral das normas não está reproduzido neste repositório.

## Premissas acadêmicas

- arranjo de 12 módulos monofaciais de 550 Wp, sem otimizadores;
- duas strings independentes, cada uma com seis módulos em série e um MPPT exclusivo;
- inversor funcional INV-FV-801 de 6 kWca, 220 V entre fases, dois MPPT,
  faixa MPPT de 90 a 550 Vcc e tensão CC máxima de 600 V;
- orientação ao norte geográfico, inclinação de 20° e ausência de sombra relevante;
- temperatura mínima ambiente de -5 °C, temperatura máxima de célula de 70 °C e
  irradiância máxima de cálculo de 1.100 W/m²;
- 5,2 horas de sol pleno por dia e performance ratio de 0,78 exclusivamente para uma
  estimativa didática de energia;
- cabos CC de cobre fotovoltaico com 6 mm² e percurso elétrico de ida de 20 m;
- circuito CA de cobre com 10 mm² e percurso elétrico de ida de 15 m;
- instalação existente com 220 V entre fases e condutores PE e ativos separados no
  trecho representado;
- condutor de equipotencialização de 6 mm² como premissa, sujeito à revisão normativa.

## Propostas conceituais

- quatro fusíveis gPV de 20 A e 600 Vcc, um em cada polo de cada string;
- dois seccionadores sob carga de 32 A e 600 Vcc, um por MPPT;
- dois conjuntos DPS tipo 2 específicos para FV, Ucpv 600 Vcc;
- seccionador e disjuntor CA bipolares de 40 A, além de DPS tipo 2 com Uc 275 Vca;
- quadro QD-FV-801 e barramento equipotencial BEP-801 identificados;
- rotas CC e CA segregadas e cabos CC identificados nas duas extremidades.

## Critérios de verificação

- tensão de circuito aberto corrigida para frio inferior ao limite CC do inversor;
- tensão de máxima potência corrigida para célula quente dentro da faixa MPPT;
- correntes de operação e curto-circuito inferiores aos limites de cada MPPT;
- fusível gPV acima da corrente de projeto acadêmica e não superior ao fusível série
  máximo declarado para o módulo;
- relação CC/CA, quedas de tensão e estimativa de energia calculadas por fonte
  reproduzível;
- uma string por MPPT, sem paralelismo elétrico entre S1 e S2.

## Limitações e dados a confirmar

- endereço, coordenadas, distribuidora, padrão de entrada e tensão efetiva do imóvel;
- modelo comercial, registro no Inmetro, firmware e aprovação do inversor pela
  distribuidora;
- levantamento de sombras, recurso solar local, sujidade e degradação;
- capacidade estrutural, vento, fixações, impermeabilização e afastamentos do telhado;
- esquema de aterramento real, SPDA existente, análise de risco e coordenação dos DPS;
- ampacidade, método de instalação, agrupamento, temperatura, queda de tensão final,
  corrente de curto-circuito e capacidade de interrupção;
- requisitos de acesso, medição, anti-ilhamento, qualidade de energia, formulários e
  vistoria da distribuidora vigente na data da solicitação;
- ensaios, inspeção inicial, comissionamento e plano de manutenção.

Nenhuma premissa deste documento autoriza compra, instalação, conexão ou operação.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
