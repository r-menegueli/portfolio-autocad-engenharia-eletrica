# Auditoria do portfólio CAD — 2026-11-05

## Escopo e critério

Revisei os 12 estudos, seus 81 DXFs e os derivados A3 para identificar qualidade de
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
| P03 — Painel com CLP | Boa cobertura de alimentação, I/O, comando, bornes e interligações. | O desenho não prova teste em CLP ou segurança funcional certificada. | Gerar esquema a partir de hardware e módulos definidos e validar em software do fabricante. |
| P04 — Nível | Tem processo, P&ID, malha PI, comando e interligações. | A arquitetura ainda simplifica a instrumentação e as condições de processo. | Evoluir o P&ID com dados de processo, válvulas/instrumentos selecionados e folhas de dados. |
| P05 — Instalação industrial | Traz layout, rotas, cargas e detalhes em folhas separadas. | As rotas e dimensões não vêm de levantamento real nem comprovam coordenação de campo. | Substituir o layout ilustrativo por levantamento cotado e cálculo rastreável de alimentadores. |
| P06 — CCM | Abrange partida direta, reversão, VFD, bornes e lista de cabos. | Proteções e capacidade de curto dependem de componentes ainda não selecionados. | Substituir as premissas por catálogo e estudo de coordenação do conjunto. |
| P07 — Veículo elétrico | Boa separação conceitual entre alta/baixa tensão, controle e comunicação. | A arquitetura é de alto nível; não é esquema veicular homologável nem define segurança funcional. | Desenvolver um diagrama por subsistema com interfaces, limites elétricos e requisitos de segurança definidos. |
| P08 — Fotovoltaico | Tem arranjo, circuitos CC/CA, string box e aterramento. | Não comprova produtividade, sombreamento, configuração final ou aprovação de conexão. | Substituir parâmetros genéricos por local, módulos/inversor escolhidos e cálculo de produção e proteção. |
| P09 — Fonte de bancada | Conecta diagrama funcional, frente, arranjo interno, mecânica e interligações. | A folha elétrica usa módulos em bloco; o circuito CC/CV e as proteções não estão detalhados componente a componente. | É a substituição técnica prioritária: redesenhar a folha elétrica somente após fechar a topologia, componentes, dissipação e limites de falha. |
| P10 — Instrumentação | Boa listagem de instrumentos e arquitetura de rede. | Tags, faixas e endereços são premissas; não há validação com folhas de dados ou protocolo implantado. | Substituir premissas por instrumentos escolhidos, diagramas de loop e matriz de comunicação testada. |
| P11 — Subestação | Escopo amplo: arranjo físico, proteção, aterramento e SPDA. | A estimativa de 18,72 Ω é apenas aritmética ilustrativa. Não calcula GPR/toque/passo; SPDA e classificação também não foram verificados. | A malha de terra deve ser redesenhada após levantamento de resistividade, dados de falta e estudo de segurança. |
| P12 — GMG/QTA | Potência, bornes, painel, implantação e sequência de transferência. | Tempos e lógica são referências conceituais; intertravamento, seletores de polo e comandos precisam de confirmação por fabricante e hardware real. | Substituir as premissas por um modelo de QTA/GMG selecionado, diagrama do fabricante e teste de lógica em bancada. |

## Correções desta revisão

- Escureci e separei as cores ACI usadas nas layers de sinal, comando, potência,
  cabos, cotas e arquitetura para que permaneçam distinguíveis sobre folha branca.
- Reemiti os carimbos em revisão gráfica 01 e reconstruí o conjunto para 81 folhas.
- Acrescentei a P12-07, uma sequência visual com confirmação de falha, partidas,
  espera entre tentativas, transferência aberta, retorno e arrefecimento.
- Alinhei desenhos e simulação QTA nos tempos de referência e corrigi alegações de
  transferências impossíveis, polos e estados sem correspondência.
- Removi da documentação P11 os resultados PASS e a aprovação implícita do
  aterramento/SPDA; a estimativa restante agora está marcada como não normativa.
- Identifiquei relatórios de 2026-09-10 como históricos, pois cobrem P01–P10 e 68
  folhas. Os registros não validam a revisão atual nem P11/P12.

## Limites e validação

O comando `scripts/construir.py --root . --strict` reconstruiu os DXFs e os derivados
PDF/SVG/PNG. Em seguida, `scripts/validar_portfolio.py --root . --strict` aprovou
423.833 verificações, sem erros ou avisos. `scripts/revisar_portfolio.py --root .`
aprovou 12 projetos, 81 pranchas, 324 arquivos gráficos e 54 CSVs; a similaridade
mínima entre PDFs e PNGs foi 0,9842. As 12 folhas de contato foram geradas; o conjunto
foi revisto por composição e as folhas técnicas P11-01, P11-05, P11-06 e P12-07 foram
inspecionadas em resolução integral.

A validação do AutoCAD/AcCoreConsole não foi repetida nesta revisão; abrir o DXF no
AutoCAD e reabrir o PDF no leitor final é uma etapa independente. O mesmo cuidado
vale para FreeCAD, KiCad e uma IDE de CLP: artefatos desses repositórios não foram
aprovados dentro dos aplicativos nativos.

Use esta auditoria para priorizar o próximo ciclo; não use nenhuma das folhas como
documento de execução. As melhorias mais valiosas agora são o circuito detalhado de
P09 e o estudo de segurança completo da malha de P11, ambos dependentes de dados e
componentes reais.
