# Inspeção visual — Projeto 04

Data da inspeção: 2026-09-09

Autor: Rogério Eduardo Moreira Menegueli

Revisão: 00

## Escopo e métodos

Foram inspecionadas as seis pranchas em três cadeias de visualização:

- PNG de produção gerado a 300 dpi pelo renderizador do portfólio;
- PDF A3 reaberto e rasterizado a 160 dpi pelo Poppler `pdftoppm` 26.07.0;
- SVG aberto diretamente no Google Chrome 152.0.7977.77 em viewport A3.

Também foram renderizadas e examinadas todas as seis abas de `tabelas-projeto-04.xlsx`: Resumo, Instrumentos, IO, Cabos, Materiais e Bornes.

## Resultado por prancha

| Prancha | PNG | PDF/Poppler | SVG/Chrome | Resultado |
|---|---|---|---|---|
| 01 — Fluxograma do processo | legível | legível | legível | aprovado |
| 02 — P&ID e instrumentação | legível | legível | legível | aprovado |
| 03 — Malha de controle | legível | legível | legível | aprovado após correção |
| 04 — Diagrama elétrico | legível | legível | legível | aprovado |
| 05 — Interligações dos instrumentos | legível | legível | legível | aprovado |
| 06 — Layout do sistema | legível | legível | legível | aprovado após correção |

## Correções realizadas

Na primeira inspeção, a caixa de falhas da prancha 03 interferia com o bloco de LT-101. O transmissor foi reposicionado e a nota de falhas foi compactada em uma área independente. Na prancha 06, a identificação de C-101 a C-104 colidia com o texto de nível; a identificação foi deslocada para uma faixa livre. Os DXFs e todos os derivados foram regenerados após as correções.

## Conferência final

- Molduras e carimbos completos, sem cortes.
- Títulos, autor, data, revisão e numeração 01/06 a 06/06 legíveis.
- Aviso obrigatório presente e legível em todas as pranchas.
- Símbolos, tags, notas e legendas distinguíveis na escala de folha inteira.
- Nenhum desalinhamento ou texto ilegível observado na segunda inspeção.
- Workbook sem fórmulas de erro; resumo calculado com 10 instrumentos/equipamentos, 23 pontos de I/O, 9 cabos, 17 itens de materiais e 11 grupos de bornes.

Resultado final da inspeção visual: **APROVADO**.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
