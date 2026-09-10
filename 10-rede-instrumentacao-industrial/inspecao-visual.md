# Inspeção visual — P10

## Registro da revisão 00

- Data: 2026-09-10
- Inspetor: Codex, com revisão documental para Rogério Eduardo Moreira Menegueli
- Fontes: seis DXFs AC1027
- Derivados: seis PDFs A3, seis SVGs e seis PNGs a 300 dpi
- Método: rasterização independente dos PDFs por Poppler, comparação com PNGs de
  produção, abertura dos SVGs em Chromium e inspeção visual das seis pranchas
- Estado: aprovado após correções e nova renderização

## Checklist

| Critério | Estado final |
| --- | --- |
| moldura e carimbo íntegros | aprovado |
| títulos, subtítulos e números legíveis | aprovado |
| tabelas sem cortes ou colisões | aprovado após correção |
| símbolos e ligações coerentes | aprovado |
| distinção visual de alimentação, analógico, digital e comunicação | aprovado |
| blindagem, PE, bornes e identificadores legíveis | aprovado |
| PDF, SVG e PNG coerentes | aprovado |

## Correções aplicadas

A primeira renderização revelou a tabela de endereços da prancha 04 sobre a área da
legenda e do carimbo, e a faixa de conversão da prancha 06 tocando a tabela de I/O.
Foram reposicionados o nó ENG-101, o quadro de limites, a tabela da rede e a faixa de
conversão. A comunicação passou ao layer visual laranja coerente com a legenda.

Os seis PNGs finais foram examinados a 300 dpi. Os seis PDFs foram reabertos pelo
`pdfinfo` e rasterizados a 150 dpi pelo Poppler 26.07.0; as composições corrigidas
foram comparadas com os PNGs. Os seis SVGs foram abertos em modo headless pelo Google
Chrome 152.0.7977.83. Não restaram cortes, colisões relevantes ou textos ilegíveis.
Uma nova geração seguida de nova renderização preservou os hashes SHA-256 dos 24
artefatos do projeto.
