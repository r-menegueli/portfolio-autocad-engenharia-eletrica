# Auditoria do portfólio CAD — 2026-11-05

## Escopo e critério

Revisei os 12 estudos, seus 83 DXFs e os derivados A3 para identificar qualidade de
apresentação, clareza do conteúdo, consistência entre documentos e maturidade real.
As folhas são material acadêmico/conceitual. A análise não concede aprovação de
engenharia, conformidade normativa ou liberação para fabricação e obra.

## O que funciona bem

- A estrutura por projeto, a numeração de folhas, as listas e a separação de
  potência/comando/instrumentação tornam o conjunto navegável.
- P02 (instalação residencial) e P03 (painel com CLP) são os melhores pontos de
  entrada: associam planta/arquitetura a diagramas e tabelas rastreáveis.
- P04, P06 e P10 mostram variedade de instrumentação, acionamentos e interfaces;
  P07 amplia o portfólio para sistemas veiculares sem se passar por produto validado.
- O DXF como fonte e PDF/SVG/PNG reproduzidos a partir dele dão bons formatos de
  leitura, edição e conferência.

## Avaliação projeto a projeto

| Projeto | Bom | Simples ou fraco | Próxima substituição que mais agregaria |
| --- | --- | --- | --- |
| P01 — Painel com inversor | Separa unifilar, potência, comando, layout e campo. | O unifilar isolado é apenas uma visão geral; seleção de proteção/coordenação não está demonstrada. | Um estudo de coordenação e ligação baseado em equipamento escolhido, sem reaproveitar valores fictícios como projeto final. |
| P02 — Residencial | Conjunto mais claro para leitura rápida: plantas, circuitos, quadro de cargas e detalhes. | Continua dependente de arquitetura e cargas assumidas. | Trocar a planta-base fictícia por uma planta cotada e identificar premissas de carga por ambiente. |
| P03 — Painel com CLP | Boa cobertura de alimentação, I/O, comando, bornes, interligações e sequência causa-efeito em nove folhas. | O desenho não prova teste em CLP ou segurança funcional certificada; a resposta para sensor incoerente com bomba em marcha ainda não foi definida. | Escolher hardware, definir a ação para incoerência de sensores e validar a sequência em software de fabricante. |
| P04 — Nível | Tem processo, P&ID, malha PI, comando e interligações. | A arquitetura ainda simplifica a instrumentação e as condições de processo. | Evoluir o P&ID com dados de processo, válvulas/instrumentos selecionados e folhas de dados. |
| P05 — Instalação industrial | Traz layout, rotas, cargas e detalhes em folhas separadas. | As rotas e dimensões não vêm de levantamento real nem comprovam coordenação de campo. | Substituir o layout ilustrativo por levantamento cotado e cálculo rastreável de alimentadores. |
| P06 — CCM | Abrange partida direta, reversão, VFD, bornes e lista de cabos. | Proteções e capacidade de curto dependem de componentes ainda não selecionados. | Substituir as premissas por catálogo e estudo de coordenação do conjunto. |
| P07 — Veículo elétrico | Boa separação conceitual entre alta/baixa tensão, controle e comunicação. | A arquitetura é de alto nível; não é esquema veicular homologável nem define segurança funcional. | Desenvolver um diagrama por subsistema com interfaces, limites elétricos e requisitos de segurança definidos. |
| P08 — Fotovoltaico | Tem arranjo, circuitos CC/CA, string box e aterramento. | Não comprova produtividade, sombreamento, configuração final ou aprovação de conexão. | Substituir parâmetros genéricos por local, módulos/inversor escolhidos e cálculo de produção e proteção. |
| P09 — Fonte de bancada | Conecta diagrama funcional, frente, arranjo interno, mecânica e interligações; agora inclui topologia buck síncrona CC/CV e pré-dimensionamento rastreável. | K1 abre só o condutor positivo; sem descarga dedicada, 0 V residual nos bornes não é garantido. Malhas, compensação, escolha térmica dos MOSFETs/indutor, proteções e layout EMI seguem pendentes. | Definir e dimensionar descarga segura da saída; completar conexões por pino, redes externas, limites de falha e dissipação antes de simular ou montar. |
| P10 — Instrumentação | Boa listagem de instrumentos e arquitetura de rede. | Tags, faixas e endereços são premissas; não há validação com folhas de dados ou protocolo implantado. | Substituir premissas por instrumentos escolhidos, diagramas de loop e matriz de comunicação testada. |
| P11 — Subestação | Escopo amplo: arranjo físico, proteção, aterramento e SPDA. | A estimativa de 18,72 Ω é apenas aritmética ilustrativa. Não calcula GPR/toque/passo; SPDA e classificação também não foram verificados. | A malha de terra deve ser redesenhada após levantamento de resistividade, dados de falta e estudo de segurança. |
| P12 — GMG/QTA | Potência, bornes, painel, implantação e sequência de transferência. | Tempos e lógica são referências conceituais; intertravamento, seletores de polo e comandos precisam de confirmação por fabricante e hardware real. | Substituir as premissas por um modelo de QTA/GMG selecionado, diagrama do fabricante e teste de lógica em bancada. |

## Correções desta revisão

- Escureci e separei as cores ACI usadas nas layers de sinal, comando, potência,
  cabos, cotas e arquitetura para que permaneçam distinguíveis sobre folha branca.
- Reemiti os carimbos em revisão gráfica 01 para a revisão anterior e em revisão 02
  para as ampliações funcionais; o conjunto atual totaliza 84 folhas.
- Acrescentei P03-09 com sequência de operação e matriz causa-efeito. A prancha
  deixa explícito que a ação sobre bombas já em marcha diante de sensor incoerente
  segue como decisão pendente, sem completar essa lacuna por suposição.
- P09 recebeu as folhas 07 (topologia buck síncrona CC/CV) e 08 (ondulação e
  pré-dimensionamento), além da lista de dimensionamento e referências ao controlador
  LM5190 como candidato, sem apresentá-lo como circuito validado.
- Em P09, 42 V aparece apenas como cenário de sensibilidade e a saída regulada inicia
  em 0,8 V. K1 aberto desabilita a entrega; 0 V residual não está garantido sem
  circuito de descarga, agora registrado como pendência.
- Acrescentei a P12-07, uma sequência visual com confirmação de falha, partidas,
  espera entre tentativas, transferência aberta, retorno e arrefecimento.
- Alinhei desenhos e simulação QTA nos tempos de referência e corrigi alegações de
  transferências impossíveis, polos e estados sem correspondência.
- Removi da documentação P11 os resultados PASS e a aprovação implícita do
  aterramento/SPDA; a estimativa restante agora está marcada como não normativa.
- Identifiquei relatórios de 2026-09-10 como históricos, pois cobrem P01–P10 e 68
  folhas. Os registros não validam a revisão atual nem P11/P12.

## Limites e validação

Os DXFs e derivados PDF/SVG/PNG de P09 foram regenerados. `scripts/validar_portfolio.py
--root . --strict` aprovou 439.853 verificações, sem erros ou avisos.
`scripts/revisar_portfolio.py --root .` aprovou 12 projetos, 84 pranchas, 336 arquivos
gráficos e 56 CSVs; a similaridade mínima PDF/PNG permaneceu 0,9842. As 12 folhas de
contato foram regeneradas e revistas por composição, inclusive o contato P03 com nove
folhas. A prancha P03-09 foi inspecionada no PNG integral de produção e em PDF
rasterizado a 150 dpi; tabela, fluxo, aviso e carimbo não apresentam cortes nem
colisões relevantes. As folhas
novas P09-07 e P09-08 foram inspecionadas em PNG integral e em PDF rasterizado a 150
dpi; a composição das oito folhas P09 foi conferida no contato. O parser aceitou os
SVGs e seus viewBox; a inspeção visual no navegador dos SVGs P09-07/08 e P03-09 está
pendente da autorização do usuário. P11-01, P11-05, P11-06 e P12-07 permanecem como
inspeções integrais documentadas da revisão anterior.

A validação do AutoCAD/AcCoreConsole não foi repetida nesta revisão; abrir o DXF no
AutoCAD e reabrir o PDF no leitor final é uma etapa independente. O mesmo cuidado
vale para FreeCAD, KiCad e uma IDE de CLP: artefatos desses repositórios não foram
aprovados dentro dos aplicativos nativos.

Use esta auditoria para priorizar o próximo ciclo; não use nenhuma das folhas como
documento de execução. As melhorias mais valiosas agora são completar o circuito e
suas verificações térmicas/EMI em P09 e desenvolver o estudo de segurança da malha de
P11, ambos dependentes de dados e componentes reais.
