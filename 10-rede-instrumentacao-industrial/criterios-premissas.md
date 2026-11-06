# Critérios e premissas — P10

## Estado epistemológico

Todos os valores são premissas de um exercício fictício. As normas citadas são fontes
de consulta e não uma declaração de atendimento. Uma aplicação real exige edição
integral vigente, dados de fabricantes, análise de riscos, cálculo e responsabilidade
profissional.

## Premissas congeladas na revisão 00

- alimentação do painel: 230 Vca, monofásica, conceitual;
- fonte PS1: 24 Vcc, 10 A, 240 W, sem produto selecionado;
- carga prevista: 3,10 A e 74,4 W, já incluindo 1,05 A de reserva auxiliar;
- instrumentos analógicos: dois fios, 4–20 mA, com entradas AI propostas como isoladas;
- entradas digitais: estados 24 Vcc, sem definição final PNP/NPN ou contato seco;
- rede: Ethernet industrial acadêmica, estrela, sub-rede documental 192.168.10.0/24;
- painel PI-101: envelope conceitual 800 x 600 x 250 mm;
- ambiente interno genérico; temperatura, poluição, IP, corrosão e vibração pendentes;
- nenhuma função do projeto é classificada como SIS, SIL ou PL.

## Critérios de separação

1. Rotas de 230 Vca, 24 Vcc, sinais analógicos, sinais digitais e comunicação devem
   permanecer identificáveis e separadas conforme análise de EMC e fabricantes.
2. Cabos analógicos são pares trançados blindados. A terminação unilateral em BE-101
   é uma premissa deste exercício, não uma regra universal.
3. O fechamento da blindagem Ethernet depende do sistema de conectores, bonding e
   orientação do fabricante; não é fixado pelas pranchas.
4. PE, 0 V funcional e shield permanecem semanticamente distintos.
5. Todo cabo, borne, canal e nó recebe identificador único nas listas estruturadas.

## Critérios gráficos e documentais

- A3 paisagem, 420 x 297 mm, moldura interna de 10 mm e DXF AC1027;
- layers mínimos do portfólio presentes mesmo quando uma função não domina a prancha;
- textos, símbolos, notas, carimbo e revisão gerados pelo mesmo script;
- PDF, SVG e PNG vinculados ao mesmo nome-base e revisão;
- validação específica de escalas, tags, I/O, cabos, endereços, potência e conteúdo;
- auditoria independente pelo AutoCAD/AcCoreConsole e inspeção visual dos derivados.

## Decisões em aberto

Fabricante, modelos, ranges calibrados, materiais molhados, classe de exatidão,
isolação galvânica, tipo de entrada digital, protocolo, tempo de ciclo, VLAN,
redundância, cybersecurity, proteção contra surtos, potência real, dissipação,
conectores, prensa-cabos e método executivo de aterramento.

A matriz causa–efeito da revisão 02 é um registro conceitual desses eventos. Ela não
define limites de diagnóstico, timeout, retenção de alarme, fail state ou resposta
específica de processo sem os modelos selecionados, a estratégia do PLC e a análise
de risco da aplicação.

## Revisão 03 — pontos de escala analógica

Para as quatro faixas fictícias declaradas, a matriz apresenta os valores ideais em
4, 8, 12, 16 e 20 mA. Os pontos intermediários correspondem a 25 %, 50 % e 75 % da
faixa linear. Não há dados de exatidão, resolução ou tolerância dos instrumentos e
cartões; portanto, os valores não são limites de aceitação, calibração ou evidência
de comissionamento.

## Revisão 04 — balanço da fonte 24 Vcc

A prancha 09 representa os sete grupos da lista de alimentação. A soma declarada é
3,10 A e 74,40 W; a capacidade proposta de PS1 é 10 A e 240 W. O saldo de 6,90 A e
165,60 W é aritmético, e a reserva auxiliar de 1,05 A já pertence aos 3,10 A
previstos. Não se deduzem ramais, fusíveis ou margem térmica. Seleção de fabricante,
inrush, derating, curto-circuito, proteção, continuidade e ensaio continuam pendentes.
