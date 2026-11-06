# Inspeção visual — Projeto 04

Data: 2026-11-06

Revisão gráfica vigente: 05

Escopo vigente: nove pranchas A3, fontes DXF AC1027 e derivados PDF, SVG e PNG.

## Revisão gráfica 05

- O AutoCAD AcCoreConsole 2027 abriu e auditou as nove fontes DXF. O validador funcional passou em 279 verificações, sem erros.
- Conferi P04-08 e P04-09 nos PNGs de produção a 300 dpi, em PDFs rasterizados independentemente pelo Poppler a 150 dpi e no contato atualizado das nove folhas. A tabela D01–D07 cabe; equação, notas, entradas, carimbo e aviso não apresentam cortes ou colisões visíveis.
- O revisor integrado confirmou similaridade PDF/PNG de 0,989404 para P04-08 e 0,989947 para P04-09. No conjunto, confirmou 12 projetos, 111 pranchas, 444 arquivos gráficos e 75 CSVs; a similaridade mínima foi 0,981493.
- O CSV registra D01–D07 como `PENDENTE`, com `valor_registrado` vazio. D03 pede geometria da fonte se a velocidade superficial for relevante, acessórios, unidades e datum; D06 e D07 registram propriedades do fluido e pressão absoluta/barométrica.
- P04-09 documenta o método NPSHa/NPSHr e a necessidade de margem aplicável; não contém dados numéricos, seleção de bomba ou aprovação hidráulica.
- A inspeção visual dos SVGs no navegador aguarda autorização do usuário.

## Revisão gráfica 04 — histórico

- O AcCoreConsole 2027 abriu e auditou as oito fontes DXF. O validador funcional passou em 259 verificações, sem erros.
- Conferi P04-08 no PNG de produção a 300 dpi, em PDF rasterizado independentemente pelo Poppler a 150 dpi e no contato das oito folhas. A fronteira fonte–bomba–TK-101, os cinco grupos D01–D05, os status PENDENTE, o aviso de risco, a V01 e o carimbo cabem sem cortes ou colisões visíveis.
- O revisor integrado confirmou similaridade PDF/PNG de 0,99014 para P04-08 e 0,981493 como mínimo global. A revisão estrita passou em 646.736 verificações, sem erros ou avisos.
- O CSV contém os mesmos cinco grupos, com coluna separada para unidade/referência, evidência solicitada e `valor_registrado` vazio. D02–D04 pedem unidades e D03 pede datum; ainda não há fonte, bomba ou proteção especificadas.
- A inspeção visual dos SVGs no navegador aguarda autorização do usuário.

## Revisão gráfica 03 — registro histórico

- Na revisão 03, o AcCoreConsole 2027 abriu e auditou as sete fontes DXF então vigentes. O validador funcional passou em 228 verificações, sem erros.
- Examinei P04-01 em PNG integral e PDF rasterizado pelo Poppler a 150 dpi. A linha entra de uma origem externa não especificada, há apenas um equipamento TK-101 e HV-102 está identificada como válvula manual. Legenda, notas e carimbo cabem na folha.
- Examinei P04-02 no PNG integral. Instrumentos, tags, níveis e sinais estão identificados; a folha continua conceitual, sem fabricantes, conexão hidráulica definida nem dados executivos.
- Examinei P04-07 em PDF rasterizado a 150 dpi e no contato atualizado das sete folhas. Aumentei o texto da matriz causa–efeito de 1,1 mm para 1,35 mm e os cabeçalhos de 1,2 mm para 1,4 mm. Os nove eventos e as cinco etapas seguem sem cortes ou sobreposição.
- Revisei o contato das sete folhas da revisão 03. P04-03 a P04-06 têm composição clara no conjunto; dimensões, relações de campo e conexões seguem como premissas.
- O revisor integrado compara PDFs e PNGs e aceita os SVGs estruturalmente. A inspeção dos SVGs no navegador aguarda autorização do usuário.
- A planilha técnica preservou suas seis abas; HV-102 aparece no cadastro de materiais e o resumo calcula 18 itens. O revisor de workbooks não encontrou erros de fórmula.

## Avaliação por prancha

| Prancha | Evidência local | Observação técnica e de apresentação |
| --- | --- | --- |
| 01 — Fluxograma | PNG integral e PDF a 150 dpi | A origem está delimitada sem inventar outro TK-101. Fonte e condições de sucção, vazão, carga e tubulação não foram especificadas. HV-102 está na saída e foi adicionada ao cadastro de materiais. |
| 02 — P&ID | PNG integral e contato | Tags e sinais são legíveis. A arquitetura usa uma bomba e instrumentos genéricos; faltam seleção, dados de processo e conexões de campo. |
| 03 — Malha de controle | Contato atualizado | O sentido da malha, PV, SP e MV são claros. Os valores PI são iniciais e não foram sintonizados por ensaio. |
| 04 — Diagrama elétrico | Contato atualizado | Separa potência, comando e STO conceitualmente. Proteções, contatos e bornes dependem do VFD, PLC e relé a selecionar. Não há estudo de curto-circuito ou coordenação executiva. |
| 05 — Interligações | Contato atualizado | Separa sinais analógicos e discretos. Bitolas, comprimentos, polaridade e terminação aguardam especificação dos componentes e levantamento. |
| 06 — Layout | Contato atualizado | O espaço de 12 m × 7 m é indicativo. Não foi feito levantamento do local; acesso, NPSH, drenagem e rotas continuam a verificar. |
| 07 — Sequência e causa–efeito | PDF a 150 dpi e contato | A tipografia da matriz foi aumentada e as nove linhas cabem. As ações para LA-L/LA-H e a retenção de alarmes após falta de energia continuam pendentes de definição. |
| 08 — Fronteira de sucção | PNG integral, PDF a 150 dpi e contato da revisão 05 | Os sete grupos D01–D07 estão legíveis e permanecem PENDENTE. A folha solicita unidade, referência e evidência, sem registrar valores nem dimensionar a hidráulica. |
| 09 — Balanço de sucção e critério de NPSH | PNG integral, PDF a 150 dpi e contato da revisão 05 | O balanço distingue pressão absoluta, pressão de vapor, elevação, velocidade superficial e perdas; NPSHr vem da curva OEM e a margem depende da aplicação. Não há cálculo ou resultado aprovado. |

## Limites da revisão

Esta inspeção verifica apresentação e coerência documental. Não comprova desempenho hidráulico, sintonia PI, seleção de materiais, conformidade normativa, segurança funcional ou aptidão para fabricação e instalação. Nenhum ensaio físico, de PLC ou de segurança foi executado.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
