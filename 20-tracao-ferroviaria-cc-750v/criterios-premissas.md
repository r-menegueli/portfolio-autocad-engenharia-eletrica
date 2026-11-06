# Critérios e premissas — P20

## Fatos e referências

- A IEC 62590-1:2025 lista requisitos gerais para conversores em instalações fixas que alimentam sistemas ferroviários.
- A IEC 62590-2-1:2025 é específica para retificadores não controlados para alimentação de tração CC; a IEC indica que a parte trata de interface entre rede trifásica e tração CC por conjuntos a diodos e inclui coordenação entre transformador e retificador.
- A IEC 61992 trata de aparelhagem CC para instalações fixas de tração até 3.000 Vcc; as partes 1, 2 e 6 cobrem requisitos gerais, disjuntores CC e conjuntos de aparelhagem, respectivamente.
- A IEC 63438:2024 estabelece princípios de proteção para sistemas de alimentação de tração AC e DC e princípios para verificação de projeto; não fornece os ajustes desta instalação.
- As IEC 62128-1 e IEC 62128-2 tratam, respectivamente, de proteção contra choque elétrico e de correntes vagantes em sistemas fixos de tração CC.

## Hipóteses do estudo

- Rede de entrada: 13,8 kV AC, 60 Hz.
- Rede de contato: terceiro trilho, 750 Vcc nominal assumido.
- Potência CC de referência para conta: 1,0 MW.
- Corrente ideal de referência: `I = P/V = 1.000.000/750 = 1.333,3 A`.
- Dois pontos de alimentação aparecem na prancha 02 apenas para explicar zonas; não há estudo de contingência, paralelismo ou capacidade conjunta.
- A corrente ideal não inclui perdas, ondulação, harmônicos, transitórios, frenagem regenerativa ou perfil de trens.

## Pontos a dimensionar ou verificar

- Demanda e simultaneidade dos trens, intervalos, aceleração, frenagem e energia regenerativa.
- Transformador/retificador, fator de forma, ondulação, diodos, refrigeração e potência contínua/de pico.
- Curto-circuito CC, capacidade de interrupção, recomposição da tensão, proteção, seletividade e coordenação entre alimentadores e veículo.
- Seções e isolamento do terceiro trilho, distâncias, suportes, barreiras, cruzamentos e condições ambientais.
- Retorno pelos trilhos, potenciais, tensões de toque e de passo, ligações equipotenciais e correntes vagantes/corrosão.
- Integração com proteção de via, sinalização, SCADA e operação; respostas e modos degradados.

As contas e desenhos são didáticos; não demonstram desempenho, segurança, conformidade ou aptidão executiva.
