# Inspeção visual - Projeto 09

Estado histórico: aprovada em 2026-09-09 para a revisão 00. A revisão 02 recebeu
inspeção visual parcial em 2026-11-05; o restante da conferência vetorial no navegador
aguarda autorização do usuário.

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

## Revisão 02 — 2026-11-05

O contato atualizado das oito folhas P09 foi examinado para conferir composição,
identificação `NN/08`, margens e carimbos. As folhas 07 e 08 foram inspecionadas em
PNG de 4.960 × 3.507 px a 300 dpi e em PDFs rasterizados pelo Poppler 26.07.0 a 150
dpi (2.481 × 1.754 px). Moldura, carimbo, tabelas, gráfico, notas e aviso obrigatório
estão dentro da folha, sem cortes ou colisões relevantes. Os PDFs mantêm a composição
vista nos PNGs.

- P09-07 distingue o candidato LM5190, o estágio de potência e os pinos/interface que
  ainda aguardam definição. A ligação é uma topologia conceitual; não contém circuito
  de aplicação completo nem fechamento das malhas.
- P09-08 identifica as curvas de 36 V nominal e 42 V de sensibilidade, mantém a meta
  de ondulação e classifica valores como derivados ou propostas. 42 V não é declarada
  como tolerância de PS1.
- O contato confirma que as seis folhas anteriores continuam enquadradas após a
  regeneração; sua revisão individual integral não foi repetida nesta atualização.
- Após a correção dos rótulos, as folhas 02, 03, 06 e 07 também foram revistas nos
  PNGs integrais. As chamadas da saída cabem na folha e as tabelas de interligações
  e pinos tiveram o texto ampliado sem cortes ou sobreposições observadas.
- A revisão técnica identificou que K1 abre apenas o condutor positivo: isso
  desabilita a entrega de potência, mas sem descarga dedicada não garante 0 V nos
  bornes. Os rótulos foram corrigidos; o circuito de descarga segue pendente.
- `revisar_portfolio.py` confirmou que os SVGs são XML válido, têm raiz `svg` e
  `viewBox`; a inspeção visual deles no navegador permanece pendente da autorização
  do usuário. Isto não é registrado como aprovação visual dos SVGs.

O validador estrito aprovou o portfólio inteiro. A revisão 02 ainda não teve abertura
dos DXFs no AutoCAD/AcCoreConsole nem validação da implementação em ferramenta de
simulação ou bancada.
