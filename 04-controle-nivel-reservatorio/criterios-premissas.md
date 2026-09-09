# Critérios e premissas

Autor: Rogério Eduardo Moreira Menegueli

Revisão: 00

## Premissas de processo

- Reservatório TK-101 com capacidade nominal fictícia de 10 m³.
- Faixa normal de operação entre 30% e 80%; setpoint inicial em 60%.
- LSL-101 em 15%, LSH-101 em 85% e LSHH-101 em 95%.
- Uma bomba P-101 com motor M-101 de 4 kW, 220 V trifásico.
- VFD-101 com faixa comandada de 20 a 60 Hz e rampa máxima proposta de 1 Hz/s.
- Vazão de consumo variável como perturbação dominante.

## Premissas de automação

- PLC-101 genérico com entradas e saídas em 24 Vcc.
- LT-101 e referência do VFD em 4–20 mA.
- Realimentação de velocidade do VFD em 4–20 mA.
- Sinais discretos de campo do tipo contato seco ou 24 Vcc, sujeitos à definição do fabricante.
- PI inicial: Kc = 0,8 % saída/% PV; Ti = 120 s; Td = 0 s.
- Anti-windup e transferência sem salto entre manual e automático.
- LSHH-101 bloqueia o acionamento fora da rotina PID ordinária; nenhuma categoria PL ou SIL é reivindicada.

## Premissas elétricas

- Potência em 220 V trifásico e comando/instrumentação em 24 Vcc.
- Segregação física entre potência, sinais analógicos e sinais discretos.
- Blindagens aterradas em um único ponto no painel, a confirmar no projeto executivo.
- Bitolas e proteções indicadas são preliminares e dependem de dimensionamento completo.

## Critérios gráficos

- Folha A3 paisagem, unidades em milímetros e DXF R2013 como fonte principal.
- Layers, moldura, carimbo, legenda, notas e aviso conforme [AGENTS.md](../AGENTS.md).
- PDF, SVG e PNG são derivados dos DXFs e devem ser inspecionados visualmente.

## Limites

Não há levantamento de campo, cálculo hidráulico definitivo, seleção comercial, estudo de curto-circuito, coordenação de proteções, estudo EMC, análise de risco formal ou validação funcional. Todos esses itens são obrigatórios antes de aplicação real.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
