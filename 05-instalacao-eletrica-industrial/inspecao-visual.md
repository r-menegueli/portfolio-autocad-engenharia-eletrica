# Inspeção visual - Projeto 05

Estado: aprovada em 2026-09-09.

## Método

As sete pranchas foram examinadas nos PNGs de produção a 300 dpi, nos PDFs
rasterizados pelo Poppler a 150 dpi e nos SVGs abertos pelo Google Chrome headless em
janela de 1600 x 1131 px. Foram verificados conjunto da folha, moldura, carimbo, aviso
obrigatório, legenda, notas, tabelas, regiões densas, alinhamentos e legibilidade.

Os sete PDFs têm uma página e formato A3 paisagem de 1190,55 x 841,89 pt. As sete abas
do workbook — Resumo, Quadro Cargas, Circuitos, Alimentadores, Cabos, Materiais e
Auditoria — também foram renderizadas individualmente e inspecionadas. A aba Auditoria
apresenta todos os critérios como `PASS`, sem fórmulas de erro.

## Correções efetuadas

- reposicionamento de rótulos de ambientes que ficavam atrás dos quadros no layout;
- deslocamento do alimentador e do quadro QADM-05 no unifilar para recuperar folgas;
- reposicionamento do rótulo de alimentação no unifilar;
- correção da apresentação da maior corrente de fase para 86,550 A;
- redução do intervalo formatado do workbook para remover grandes áreas vazias nas
  pré-visualizações.

## Resultado

Após a regeneração, não foram observados cortes, colisões, desalinhamentos relevantes
ou textos ilegíveis. A comparação entre PNG, PDF rasterizado e SVG foi consistente. O
validador também não reportou entidades fora da moldura nem sobreposições potenciais.
Os 28 artefatos CAD do projeto (sete DXFs e 21 derivados) conservaram hashes SHA-256
idênticos em uma reconstrução completa.
