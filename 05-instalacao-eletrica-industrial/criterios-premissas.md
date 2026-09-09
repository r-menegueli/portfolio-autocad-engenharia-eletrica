# Critérios e premissas - Projeto 05

## Dados declarados

| Item | Valor adotado | Natureza |
| --- | ---: | --- |
| Edificação | 30,00 x 18,00 m | fictícia |
| Área total | 540,00 m² | calculada |
| Produção | 432,00 m² | fictícia |
| Apoio | 108,00 m² | fictícia |
| Pé-direito | 6,00 m | hipótese |
| Sistema | 380/220 V, 3F+N+PE, 60 Hz | hipótese |
| Aterramento | TN-S a jusante da origem | hipótese |
| Condutores | cobre | hipótese |
| Resistividade para queda | 0,0225 ohm.mm²/m | critério conservador |
| Queda combinada máxima | 4,0% | critério acadêmico |
| Corrente de curto-circuito | 6 kA presumidos | dado a confirmar |

## Critérios de cálculo

- Motor trifásico: `Pentrada = Psaída / rendimento`;
- potência aparente: `S = Pentrada / fator de potência`;
- corrente trifásica: `I = 1000 S / (raiz(3) x 380)`;
- corrente monofásica: `I = 1000 S / 220`;
- potência demandada: potência instalada multiplicada pelo fator de demanda;
- queda trifásica: `100 x raiz(3) x rho x L x I / (Scond x V)`;
- queda monofásica: `100 x 2 x rho x L x I / (Scond x V)`.

As correntes dos circuitos finais usam a potência instalada, enquanto os alimentadores
usam a potência demandada e, quando aplicável, a fase mais carregada. Para a proteção
dos condutores aplica-se o teste acadêmico `Ib <= In <= Iz`.

## Ampacidades assumidas

| Seção Cu | Iz assumida |
| ---: | ---: |
| 1,5 mm² | 17,5 A |
| 2,5 mm² | 24 A |
| 4 mm² | 32 A |
| 6 mm² | 41 A |
| 25 mm² | 89 A |
| 50 mm² | 134 A |

Esses valores são premissas didáticas. Método de instalação, temperatura, agrupamento,
número de condutores carregados, isolação, terminais, harmônicas e fabricante podem
alterá-los. Nenhuma seção está liberada para compra ou instalação.

## Demanda adotada

- compressor e exaustor: 100%;
- torno e fresadora: 80%;
- esmeril e solda: 60%;
- cada grupo de tomadas industriais: 40%;
- iluminação: 100%;
- tomadas monofásicas auxiliares: 60%.

Os fatores são didáticos e não substituem histórico de processo, medição, ciclo de
trabalho, requisitos da concessionária ou análise de expansão.

## Proteções e coordenação

- DJ-G: 4P, 100 A, capacidade de interrupção mínima assumida de 10 kA;
- QF-QDF: 3P, 80 A; QF-QDL e QF-QADM: 4P, 16 A;
- circuitos de motores: proteção ajustável e método de partida a selecionar;
- tomadas industriais e auxiliares: DR 30 mA como premissa;
- DPS tipo 2: quantidade e configuração conceituais.

Não foram calculados curto-circuito, energia incidente, seletividade, retaguarda,
coordenação de DPS, partida de motores, harmônicas, correção de fator de potência,
temperatura dos quadros nem esforços eletrodinâmicos.

## Limites do modelo

O projeto não cobre obras civis, arquitetura executiva, SPDA, subestação, grupo gerador,
fotometria, iluminação de emergência, combate a incêndio, automação, segurança de
máquinas, aterramento detalhado, classificação de áreas ou prontuário NR-10. Todas as
dimensões de montagem e graus IP dependem de levantamento e seleção real.
