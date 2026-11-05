# Registro de inspeção visual

Data: 2026-09-06

Status: **APROVADO PARA A REVISÃO 00 DE OITO FOLHAS (2026-09-06)**

## Método

- PDF: as oito saídas finais foram rasterizadas a 150 dpi com Poppler `pdftoppm`
  26.07.0 e examinadas individualmente e em folha de contato.
- SVG: as oito saídas foram abertas no Chromium/Google Chrome headless em viewport
  1680 x 1188 px e comparadas em folha de contato.
- PNG: as oito saídas de produção, renderizadas a 300 dpi (4960 x 3507 px), foram
  comparadas com os PDFs e SVGs.

## Não conformidade e correção

Na primeira inspeção, a tabela X4 da prancha 07 invadia as linhas finais da tabela X2.
O script-fonte foi corrigido para dividir X4 em dois blocos (`X4:1-6` e `X4:7-12`),
mantendo espaçamento livre entre as réguas. DXF, PDF, SVG e PNG foram regenerados e
reinspecionados.

## Resultado final

As oito pranchas apresentam moldura completa, carimbo legível, aviso obrigatório sem
corte, títulos, legendas e notas alinhados. As regiões densas das listas de I/O e de
bornes permanecem legíveis em A3, sem colisões visuais relevantes. PDF, SVG e PNG
representam a mesma revisão 00. O detector automático não registrou sobreposições,
entidades fora da moldura, clipping ou dimensões incompatíveis.

## Complemento da revisão 02 — prancha 09

- A nova folha de sequência foi inspecionada no PNG de produção a 300 dpi e em
  rasterização independente do PDF a 150 dpi. O fluxo, a matriz causa-efeito, o aviso,
  as notas e o carimbo permanecem dentro da moldura; os textos da matriz foram
  ampliados para conferência e não apresentam cortes ou colisões visuais relevantes.
- A sequência diferencia falhas tratadas de decisões ainda pendentes, em especial a
  resposta para uma bomba em marcha diante de sensores incoerentes.
- Esta revisão não foi aberta no AutoCAD/AcCoreConsole. A inspeção visual do SVG no
  navegador segue pendente de autorização do usuário.

## Complemento da revisão 03 — prancha 10

- A prancha de verificação foi inspecionada no PNG de produção a 300 dpi e em raster
  independente do PDF a 150 dpi. A tabela mantém os 12 itens e seus estados
  `NÃO EXECUTADO`; cabeçalho, corpo, nota, aviso acadêmico e carimbo estão dentro da
  moldura, sem cortes visíveis.
- Os dois formatos conferidos mostram a mesma composição. O carimbo identifica a
  revisão 03 como “PLANO DE VERIFICAÇÃO”; a resposta para sensor incoerente com bomba
  em marcha continua explicitamente pendente.
- O AutoCAD AcCoreConsole 2027 abriu e auditou as dez fontes DXF do P03 (`PASS`, 10/10).
  Isso confirma abertura e integridade CAD, não valida cálculos, lógica de processo,
  instalação ou segurança funcional.
- A inspeção visual do SVG no navegador continua aguardando autorização do usuário.
