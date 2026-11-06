# Critérios e premissas — P17

## Escopo verificado

- Foco em arquitetura de proteção, controle, comunicação e documentação de sinais de uma subestação hipotética.
- Diagramas de A3 paisagem, em milímetros, com DXF AC1027 como fonte e três formatos derivados.
- Rede de processo separada visualmente da rede de estação.
- As funções e mensagens listadas são exemplos sem lógica de atuação aprovada.

## Hipóteses de contexto

| Item | Hipótese | Limite |
| --- | --- | --- |
| Tensão do pátio | 138 kV | Não define classe de isolamento nem equipamentos |
| Transformador | 25 MVA; 138/13,8 kV | Potência e impedância não dimensionadas |
| Barramento secundário | 13,8 kV | Arranjo de barra apenas ilustrativo |
| IEDs | Linha, transformador, barra e dois alimentadores | Fabricante, modelos e capacidades pendentes |
| Controle de bay | IED-BAY-L01 e IED-BAY-T01 | Interface final de trip e circuitos de saída não definidos |
| MUs | Interfaces de TC/TP por zona funcional | Mapeamento de canais e sample rate pendentes |
| Redes | Processo e estação em domínios separados no desenho | VLAN, switches, redundância e endereçamento pendentes |
| Eventos | Trip, falha de disjuntor e permissivo GOOSE exemplificados | Dataset e comportamento por perda não aprovados |

## Critérios de representação

SV descreve o fluxo ilustrativo de valores amostrados de cinco MUs para IEDs. GOOSE identifica mensagens de evento entre IEDs; MMS identifica supervisão/controle no contexto da rede de estação. A posição gráfica das caixas não determina uma topologia física ou uma associação obrigatória de mensagens.

ICD, SSD, SCD e CID são listados como artefatos do processo de configuração. A entrega inclui CSVs de inventário e tabelas, mas não SCL de fornecedor, arquivos de engenharia ou comprovação de validação segundo o esquema e as regras aplicáveis.

## Verificações propostas, não executadas

O plano de verificação enumera consistência de configuração, publishers/subscribers, sincronismo, comportamento em perda de mensagens, alarmes, intertravamentos, testes de lógica, FAT e SAT. Nenhum ensaio de rede ou de proteção foi realizado. Uma execução futura depende de projeto aprovado, equipamentos e ferramentas reais.

## Pontos em aberto

1. Diagramas unifilares aprovados e estudos de curto-circuito, seletividade, estabilidade e proteção.
2. Especificação de IEDs/MUs, capacidades, datasets, funções habilitadas e modelo SCL suportado.
3. Projeto físico das redes, switches, caminhos, redundância, sincronismo e análise de tráfego/latência.
4. Endereçamento, VLANs, controle de acesso, gestão de contas, hardening, logs e resposta a incidentes.
5. Lista oficial de sinais, lógica de trip/intertravamento, permissivos, falha de disjuntor e matriz aprovada.
6. Evidências de validação SCL, ensaios de interoperabilidade, FAT/SAT e comissionamento por profissionais habilitados.
