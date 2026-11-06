# Memorial descritivo — Controle de nível de reservatório

Autor: Rogério Eduardo Moreira Menegueli

Projeto: 04 — Controle de nível de reservatório

Revisão: 01

## Objeto

O sistema conceitual mantém o nível de TK-101 em torno de 60% por meio da bomba centrífuga P-101, acionada pelo motor M-101 e pelo inversor VFD-101. O transmissor LT-101 envia ao PLC-101 um sinal de 4–20 mA correspondente a 0–100% do nível.

## Processo e controle

A variável controlada é o nível de TK-101. A variável manipulada é a referência de frequência de VFD-101, enviada por saída analógica de 4–20 mA. A vazão de consumo na saída do reservatório é a perturbação principal; pressão da fonte e curva da bomba são perturbações secundárias. A origem e o equipamento de sucção a montante de P-101 não foram especificados e aparecem apenas como limite externo no fluxograma. HV-102 é uma válvula manual conceitual na saída; seleção, diâmetro e classe de pressão estão pendentes do projeto hidráulico.

A prancha 08 e `dados-fonte-succao.csv` registram sete grupos de dados D01–D07 necessários para estudar a fronteira de sucção, incluindo fonte e regime, geometria da fonte e da linha/acessórios, datum, curva OEM, eventual proteção, propriedades do fluido e pressão absoluta/barométrica. A prancha 09 apresenta o método paramétrico do balanço de sucção e da comparação NPSHa/NPSHr. Todos os dados permanecem pendentes; não há bomba selecionada nem resultado hidráulico.

O controlador LIC-101 é implementado no PLC-101. Em automático, a ação aumenta a frequência quando o nível fica abaixo do setpoint e reduz a frequência quando o nível sobe. O algoritmo inicial é PI, com anti-windup, transferência manual/automático sem salto e limitação de 20 a 60 Hz enquanto a bomba estiver habilitada.

## Instrumentação e proteção

LT-101 realiza a medição contínua. LSL-101, LSH-101 e LSHH-101 fornecem indicações discretas independentes nos níveis de 15%, 85% e 95%. LSHH-101 participa do bloqueio de funcionamento do VFD, independente da malha PID comum. Falha do transmissor, falha do inversor, inconsistência entre instrumentos e tempo máximo de enchimento geram alarme e transição para estado seguro conforme a filosofia documentada.

## Alimentação e interligações

O circuito de potência conceitual utiliza 220 V trifásico para VFD-101 e M-101. A instrumentação e o comando utilizam 24 Vcc. Cabos de sinal analógico são blindados e segregados dos cabos de potência. A blindagem é aterrada em um único ponto no painel, conforme revisão executiva futura.

## Escopo e limitações

Capacidades, correntes, proteções, cabos, bornes e distâncias são premissas acadêmicas. A implantação real exige levantamento de campo, cálculo hidráulico, coordenação e seletividade, curto-circuito, aterramento, EMC, análise de riscos, definição de nível de desempenho de segurança e responsabilidade técnica.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
