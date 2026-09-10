# Inspeção visual - Projeto 09

Estado: aprovada em 2026-09-09 para a revisão 00.

## Amostra e ferramentas

Foram examinadas as seis pranchas completas nos PNGs de produção de 4.960 × 3.507 px
a 300 dpi. Os seis PDFs A3 de uma página foram reabertos e rasterizados a 150 dpi
pelo Poppler `pdftoppm` 26.07.0, resultando em imagens de 2.481 × 1.754 px. Os seis
SVGs foram abertos pelo Google Chrome 152.0.7977.83 em modo headless e comparados com
os demais derivados.

A revisão cobriu moldura, carimbo, aviso obrigatório, zonas primária e secundária,
PE, barramentos de potência, comando, medição, painel, cotas, ventilação, rotas,
tabelas, alinhamentos, contraste e legibilidade.

## Correções aplicadas

- prancha 01: a indicação de PE e saída flutuante foi integrada ao quadro de limites,
  removendo o cruzamento entre linha, símbolo e texto;
- prancha 03: controles, LEDs e bornes duplicados pelo gerador foram removidos; cotas
  e nota de origem dos recortes receberam folga adicional;
- prancha 04: as cotas foram reposicionadas, as setas de ar receberam a cor da legenda
  e o rótulo da zona primária foi separado e movido para uma faixa livre;
- prancha 05: a cota do painel frontal e a tabela de recortes foram afastadas dos
  títulos e da nota inferior;
- prancha 06: a tabela de interligações foi compactada para não colidir com a nota
  referente à lista W01-W25.

Após cada correção, os DXFs e os 18 derivados foram regenerados a partir do script.
Uma reconstrução consecutiva manteve hashes SHA-256 idênticos para os seis DXFs e
os 18 derivados.

## Resultado final

As seis pranchas preservam a folha A3 completa, sem cortes da moldura ou do carimbo.
Textos, tags, cotas, tabelas e avisos permanecem legíveis nos três formatos. Não foram
observadas sobreposições relevantes, elementos fora da moldura, páginas vazias ou
divergências visuais entre PDF, SVG e PNG. Resultado: **APROVADO**.

As imagens temporárias usadas na comparação não integram o repositório; os arquivos
oficiais permanecem em `exports/`.
