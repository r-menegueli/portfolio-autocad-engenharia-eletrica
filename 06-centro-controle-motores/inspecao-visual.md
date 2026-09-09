# Inspeção visual - Projeto 06

Estado: aprovada em 2026-09-09, revisão 00.

## Amostra examinada

As sete pranchas foram examinadas integralmente em três cadeias independentes:

- PNGs de produção a 300 dpi, com 4960 × 3507 pixels;
- PDFs vetoriais A3 paisagem, reabertos pelo `pdfinfo` e rasterizados pelo Poppler
  `pdftoppm` 26.07.0 a 150 dpi;
- SVGs abertos e capturados no Google Chrome headless em 1600 × 1131 pixels.

A inspeção cobriu moldura, carimbo, aviso obrigatório, legenda, notas, títulos,
numeração, diagramas, tabelas, identificação de equipamentos, alinhamentos, cores e
legibilidade em ampliação.

## Correções reaplicadas na fonte

Na primeira passagem foram corrigidos:

- sobreposição do texto trifásico dentro do símbolo de motor reutilizado;
- convergência dos três condutores de saída na partida direta;
- leitura ambígua do circuito de potência reversor, incluindo separação das ordens de
  fase, barramento e identificação do intertravamento mecânico;
- folgas entre motores, equipamentos e rótulos no unifilar;
- altura das linhas da lista de cabos para separar a tabela da síntese de materiais.

Os sete DXFs e todos os derivados foram regenerados após as correções. A segunda
passagem não encontrou cortes, desalinhamentos, colisões, texto ilegível ou divergência
entre DXF, PDF, SVG e PNG. Resultado final: `PASS` em 7/7 pranchas e 21/21 derivados.
