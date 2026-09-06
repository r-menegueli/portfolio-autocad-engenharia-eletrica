# Registro de inspeção visual

Data: 2026-09-06

Status: **APROVADO**

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
