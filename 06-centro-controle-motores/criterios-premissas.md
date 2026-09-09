# Critérios e premissas - CCM-06

## Premissas declaradas

- rede fictícia: 380/220 V, 3F+N+PE, 60 Hz, TN-S;
- corrente de curto-circuito presumida no CCM: 6 kA, sujeita a cálculo;
- barramento CCM-06: 80 A; disjuntor geral QG-06: 4P, 50 A;
- comando: 24 Vcc por PSU-601, capacidade nominal 5 A;
- simultaneidade conforme fatores de demanda da lista de cargas;
- cobre a 70 °C, resistividade conservadora de 0,0225 ohm·mm²/m para queda;
- comprimentos são hipóteses acadêmicas registradas nos CSVs.

## Critérios preliminares

- relação de proteção verificada por `Ib <= In <= Iz`;
- queda combinada adotada como limite interno de 4,0%;
- proteção de motores requer coordenação com contatores, relés e fabricante;
- QF-603 deve seguir as recomendações do fabricante do VFD-603;
- W603B é cabo para inversor, simétrico e blindado, sem dispositivo de manobra entre
  VFD e motor;
- contatores reversores têm intertravamentos elétrico e mecânico;
- qualquer partida exige comando deliberado; retorno de energia não reinicia cargas.

## Valores funcionais

- FR-601: faixa 9-13 A, ajuste inicial 12,0 A;
- FR-602: faixa 5,5-8 A, ajuste inicial 6,8 A;
- VFD-603: 11 kW para motor de 7,5 kW, seleção final dependente de corrente, regime,
  sobrecarga, temperatura, altitude e frequência de chaveamento;
- parada comum: KSR-601 retira contatores e STO A/B;
- reversão: FC-602F/FC-602R e contatos NF cruzados por sentido.

## Exclusões

Não foram definidos fabricante, forma de separação, IP, corrente real de curto-circuito,
coordenação tipo 1/2, categoria de segurança, PL/SIL, cabos conforme método real,
harmônicas, filtro EMC, reator, resistor de frenagem ou ventilação final.
