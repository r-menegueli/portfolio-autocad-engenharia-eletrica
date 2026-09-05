# Plano dos dez projetos acadêmicos

Autor: Rogério Eduardo Moreira Menegueli
Estado: planejamento — nenhum projeto final é produzido nesta etapa

## Propósito

Este documento organiza a evolução do portfólio em dez projetos acadêmicos de
Engenharia Elétrica, do desenho de baixa tensão à integração de sistemas
industriais. A ordem foi escolhida para reaproveitar componentes já validados e
introduzir complexidade gradualmente.

As regras permanentes estão no [AGENTS.md](../AGENTS.md), e os critérios comuns
estão descritos no [padrão gráfico](./padrao-grafico.md) e nos
[critérios técnicos](./criterios-tecnicos.md). A organização prevista para as
pastas de trabalho está resumida em [projetos/README.md](../projetos/README.md).

## Aviso obrigatório

O texto abaixo deverá constar, sem abreviações, nas notas de todas as pranchas,
no README e no memorial descritivo de cada projeto:

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

Nenhum documento deverá conter CPF, RG, telefone ou endereço residencial do
autor.

## Base comum de cada projeto

Cada projeto deverá declarar finalidade, escopo, exclusões, unidades, normas e
edições adotadas, fontes dos dados, hipóteses de cálculo e limitações. Os valores
de entrada deverão ser fictícios ou devidamente anonimizados.

Todos os projetos deverão usar folha A3 em paisagem, moldura, carimbo, autor,
data, revisão, número da prancha, legenda, notas técnicas, layers e símbolos
padronizados. O DXF verdadeiro será a fonte principal; renomear um DXF para DWG
é proibido. Um DWG só poderá ser incluído após conversão real e verificação de
abertura.

Entregáveis mínimos por projeto:

- `README.md`, com objetivo, escopo, instruções de reprodução e índice de
  pranchas;
- `memorial-descritivo.md` e `criterios-premissas.md`;
- memória de cálculo rastreável quando houver dimensionamento;
- scripts-fonte determinísticos para gerar ou atualizar os desenhos;
- uma ou mais pranchas DXF, numeradas e validadas;
- visualizações correspondentes em PDF, SVG e PNG;
- `lista-materiais.csv`, com cabeçalhos, unidades e quantidades;
- relatório de validação automática e registro de inspeção visual.

A estrutura interna e os nomes exatos deverão seguir o
[guia da pasta de projetos](../projetos/README.md). Um projeto somente avança de
rascunho para concluído quando todos os entregáveis correspondem à mesma revisão.

## Sequência recomendada

| Ordem | Código | Projeto | Competência principal | Dependência recomendada |
| ---: | :---: | --- | --- | --- |
| 1 | P01 | Instalação elétrica residencial de baixa tensão | circuitos, cargas e documentação básica | infraestrutura do portfólio |
| 2 | P02 | Iluminação de ambiente educacional e comercial | critérios luminotécnicos e comando de iluminação | P01 |
| 3 | P03 | Distribuição predial multipavimentos | demanda, alimentadores e prumada elétrica | P01 e P02 |
| 4 | P04 | Aterramento, equipotencialização e SPDA conceitual | proteção, zonas e detalhes construtivos | P03 |
| 5 | P05 | Sistema fotovoltaico conectado à rede | geração distribuída e interfaces CC/CA | P01 e P04 |
| 6 | P06 | Distribuição elétrica industrial e CCM | arquitetura de potência, cargas e encaminhamento | P03 e P04 |
| 7 | P07 | Acionamentos e comandos de motores | lógica eletromecânica, intertravamentos e partidas | P06 |
| 8 | P08 | Automação e instrumentação de processo | I/O, malhas, bornes e integração com PLC | P07 |
| 9 | P09 | Subestação acadêmica de média e baixa tensão | transformação, proteção e manobra | P06 |
| 10 | P10 | Integração elétrica de uma microindústria | coordenação multidisciplinar e consistência global | P05 a P09 |

## P01 — Instalação elétrica residencial de baixa tensão

**Objetivo.** Estabelecer a primeira referência completa do portfólio com uma
instalação residencial fictícia, simples o bastante para testar todo o fluxo de
geração, renderização e validação.

**Escopo.** Planta de pontos de utilização e iluminação, divisão de circuitos,
quadro de distribuição, diagrama unifilar, identificação de condutores e cargas,
critérios de demanda e verificação conceitual de queda de tensão. A arquitetura
será apenas uma base didática, sem representar imóvel real.

**Pranchas e dados específicos.** Planta elétrica; quadro de cargas e legenda;
diagrama unifilar do quadro; tabela de circuitos e lista de materiais.

**Marco de aceitação.** O DXF deve fixar o padrão de símbolos e layers, manter
todos os elementos dentro da moldura e gerar PDF, SVG e PNG legíveis sem ajustes
manuais.

## P02 — Iluminação de ambiente educacional e comercial

**Objetivo.** Demonstrar um estudo luminotécnico reproduzível para salas de aula,
circulação e área administrativa fictícias.

**Escopo.** Malha de cálculo, critérios de iluminância e uniformidade, seleção
conceitual de luminárias, circuitos, comandos, iluminação de emergência e quadro
de cargas parcial. Dados fotométricos deverão ter origem registrada; na ausência
de arquivo verificável, deverão ser usados parâmetros didáticos declarados.

**Pranchas e dados específicos.** Planta de iluminação normal e de emergência;
mapa de resultados; detalhes de comando; planilha ou CSV com ambientes,
quantidades, potência e resultados calculados.

**Marco de aceitação.** Resultados numéricos, legenda gráfica e identificadores
de luminárias devem ser rastreáveis entre desenho, memória e materiais.

## P03 — Distribuição predial multipavimentos

**Objetivo.** Ampliar a documentação de baixa tensão para um edifício fictício
com múltiplos pavimentos e medição centralizada.

**Escopo.** Entrada e distribuição geral conceituais, agrupamento de medidores,
quadros por pavimento, prumada, alimentadores, estimativa de demanda, queda de
tensão e reserva de capacidade. Não abrange aprovação junto a concessionária.

**Pranchas e dados específicos.** Diagrama unifilar geral; diagrama vertical da
prumada; planta da sala elétrica; quadros de demanda e alimentadores; lista de
cabos, eletrodutos e dispositivos.

**Marco de aceitação.** A numeração de quadros, circuitos e alimentadores deve
permanecer coerente em todas as pranchas e tabelas.

## P04 — Aterramento, equipotencialização e SPDA conceitual

**Objetivo.** Documentar medidas acadêmicas de proteção contra choques e
descargas atmosféricas, deixando explícitos os limites da análise.

**Escopo.** Arranjo de aterramento, barramentos de equipotencialização, condutores
de proteção, captação e descidas de SPDA, zonas de proteção e pontos de inspeção.
A análise de risco será didática, com parâmetros e norma/edição identificados.

**Pranchas e dados específicos.** Planta de cobertura; planta de aterramento;
cortes e detalhes típicos; esquema de equipotencialização; tabela de componentes
e memória conceitual de risco.

**Marco de aceitação.** Cada componente deve ter identificador, layer correto e
correspondência na legenda e na lista de materiais; conclusões não podem ser
apresentadas como autorização de execução.

## P05 — Sistema fotovoltaico conectado à rede

**Objetivo.** Apresentar o arranjo elétrico de um sistema fotovoltaico fictício
conectado à rede, com rastreabilidade entre premissas energéticas e desenho.

**Escopo.** Estimativa de geração, organização de módulos e strings, circuitos
CC e CA, inversor, seccionamento, proteções, aterramento funcional e interface
com quadro existente. Não abrange homologação nem estudo estrutural.

**Pranchas e dados específicos.** Implantação de módulos; diagramas unifilares CC
e CA; detalhes de proteção e encaminhamento; tabela de strings; balanço energético
e lista de materiais.

**Marco de aceitação.** Tensões, correntes, quantidades de módulos e referências
dos dispositivos devem coincidir entre cálculo, desenhos e CSV.

## P06 — Distribuição elétrica industrial e centro de controle de motores

**Objetivo.** Introduzir uma instalação industrial fictícia com cargas de
processo, quadros de distribuição e centro de controle de motores (CCM).

**Escopo.** Levantamento de cargas, diagrama unifilar, QGBT e CCM, alimentadores,
proteções, queda de tensão, rotas de cabos e eletrocalhas e organização física
conceitual. Curto-circuito e seletividade serão tratados no nível acadêmico
compatível com os dados disponíveis.

**Pranchas e dados específicos.** Unifilar de potência; implantação de painéis;
rota principal de eletrocalhas; tabela de cargas e alimentadores; lista de cabos,
proteções e equipamentos.

**Marco de aceitação.** Tags elétricas e dados nominais devem ter uma única fonte
estruturada e aparecer sem divergências nas pranchas e no memorial.

## P07 — Acionamentos e comandos de motores

**Objetivo.** Detalhar circuitos de potência e comando para acionamentos típicos
de motores, com ênfase em segurança lógica e leitura do esquema.

**Escopo.** Partida direta, reversão, estrela-triângulo e acionamento por inversor
de frequência; proteções, intertravamentos, sinalização e interfaces de campo.
As sequências serão simuladas ou verificadas logicamente, sem energização real.

**Pranchas e dados específicos.** Diagramas de potência e comando; sequência
funcional; diagrama de interligações; tabela de bornes e cabos; lista de materiais
por tipo de partida.

**Marco de aceitação.** Numeração de fios, contatos cruzados, bobinas, bornes e
referências de folha deve ser completa e validável.

## P08 — Automação e instrumentação de processo

**Objetivo.** Integrar sensores, atuadores, PLC e painéis em uma célula de
processo didática.

**Escopo.** Narrativa de controle, lista de entradas e saídas, arquitetura de
automação, alimentação de instrumentos, diagramas de malha, bornes, cabos e
interfaces com os acionamentos de P07. Software de PLC poderá ser representado
por pseudocódigo ou lógica documentada, sem alegação de validação funcional em
planta real.

**Pranchas e dados específicos.** Arquitetura do sistema; diagramas de malha e
interligação; cartões de I/O; detalhes de painel; lista de I/O, instrumentos,
cabos e bornes em formatos tabulares.

**Marco de aceitação.** Cada tag deve manter tipo de sinal, canal, borne, cabo e
destino coerentes em todos os artefatos.

## P09 — Subestação acadêmica de média e baixa tensão

**Objetivo.** Consolidar conceitos de transformação, medição, proteção e manobra
em uma subestação fictícia, exclusivamente acadêmica.

**Escopo.** Diagrama unifilar de média e baixa tensão, arranjo físico conceitual,
transformador, cubículos, QGBT, proteção, intertravamentos, afastamentos
indicativos e interface de aterramento. Requisitos de concessionária e segurança
deverão ser citados como dados a confirmar, nunca presumidos.

**Pranchas e dados específicos.** Unifilar geral; planta e cortes da sala;
diagrama funcional de proteção; tabela de equipamentos e ajustes conceituais;
lista de materiais.

**Marco de aceitação.** Níveis de tensão, relações de transformação, capacidades,
tags e estados de manobra devem estar consistentes; a documentação deverá reforçar
que não serve para construção, operação ou energização.

## P10 — Integração elétrica de uma microindústria

**Objetivo.** Demonstrar a governança de um conjunto multidisciplinar, integrando
as competências anteriores em um empreendimento totalmente fictício.

**Escopo.** Interface da subestação com QGBT e CCM, geração fotovoltaica,
distribuição, iluminação, aterramento, acionamentos, automação, instrumentação,
rotas de cabos e listas consolidadas. O foco será consistência de interfaces,
revisões e rastreabilidade, não detalhamento executivo.

**Pranchas e dados específicos.** Índice geral; unifilar mestre; plantas de
distribuição e rotas; matriz de interfaces; arquitetura de automação; consolidação
de cargas, cabos, painéis, instrumentos e materiais.

**Marco de aceitação.** Uma alteração controlada de tag ou carga deve propagar-se
de forma reproduzível aos desenhos e tabelas dependentes, sem links quebrados,
arquivos temporários ou divergências de revisão.

## Fases e portões de qualidade

Cada projeto seguirá estas fases:

1. **Definição:** congelar escopo, dados fictícios, unidades, normas e critérios.
2. **Modelagem:** criar dados estruturados, cálculos e biblioteca de símbolos.
3. **Geração:** produzir DXF e derivados exclusivamente por fluxo documentado.
4. **Validação:** executar verificações automáticas de arquivos, layers, limites,
   moldura, textos, links e entregáveis.
5. **Inspeção visual:** revisar PDF, SVG e PNG em escala legível, corrigindo cortes,
   desalinhamentos, colisões e hierarquia gráfica.
6. **Congelamento:** alinhar revisão, data e número de prancha, registrar o
   resultado e fazer commit local com a árvore limpa.

O projeto seguinte poderá começar antes do congelamento do anterior apenas para
pesquisa e coleta de requisitos; componentes gráficos só serão promovidos à base
comum depois de aprovados nos dois portões de qualidade.

## Evolução da biblioteca comum

- P01 estabelece folha, carimbo, textos, cotas e símbolos básicos de baixa tensão.
- P02 acrescenta luminárias, comandos e representação de resultados.
- P03 acrescenta prumadas, medição, quadros e referências entre folhas.
- P04 acrescenta símbolos de aterramento, equipotencialização e SPDA.
- P05 acrescenta símbolos e estilos para circuitos CC e geração distribuída.
- P06 acrescenta equipamentos industriais, cabos e eletrocalhas.
- P07 acrescenta contatos, bobinas, motores e referências cruzadas.
- P08 acrescenta instrumentos, sinais, bornes e cartões de I/O.
- P09 acrescenta equipamentos de média tensão e proteções.
- P10 somente integra componentes já validados; novos símbolos exigem revisão
  explícita da biblioteca e dos testes.

## Resultado desta etapa

Nesta etapa, o resultado esperado limita-se à infraestrutura, às regras, aos
templates e às ferramentas de automação. As pastas e pranchas dos dez projetos
serão criadas apenas em etapas futuras, uma por vez, conforme esta sequência.
