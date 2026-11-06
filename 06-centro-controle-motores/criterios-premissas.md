# Critérios e premissas - CCM-06

## Premissas declaradas

- rede fictícia: 380/220 V, 3F+N+PE, 60 Hz, TN-S;
- corrente de curto-circuito presumida no CCM: 6 kA, sujeita a cálculo;
- barramento CCM-06: 80 A; disjuntor geral QG-06: 4P, 50 A;
- comando: 24 Vcc por PSU-601, capacidade nominal 5 A;
- fatores de demanda 1,00/0,80/0,90 da lista de cargas aplicados por carga para formar
  os totais de P e S demandadas; a simultaneidade real não foi verificada;
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
- X3:1-24 reúne W605, W606, W604 e W608; cada núcleo listado deve ter um borne
  correspondente, inclusive reservas identificadas.
- X4:1-2 são pontos internos KSR-601–STO A/B; X4:3-10 recebe os oito condutores de
  W607, incluindo DI3 para seleção local/remoto.
- A P06-05 é um arranjo funcional sem escala. Os blocos representam ocupação prevista;
  dimensões de fabricante, folgas, segregação, IP e dissipação ainda não foram aprovados.

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

## Leitura do balanço de demanda

A prancha P06-09 apresenta lado a lado potências instaladas e demandadas, usando os
fatores declarados nos CSVs. A corrente de cada ramal deriva da sua potência aparente
instalada; a corrente equivalente do W600 deriva da potência aparente demandada total.
Os valores `In = 50 A` e `Iz = 57 A` são premissas copiadas do cadastro, e a relação
aritmética `Ib <= In <= Iz` não comprova capacidade térmica nem substitui as verificações
de instalação, correção, curto-circuito e coordenação.
