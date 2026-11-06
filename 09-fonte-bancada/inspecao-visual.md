# Inspeção visual - Projeto 09

Estado histórico: aprovada em 2026-09-09 para a revisão 00. Revisões posteriores
receberam inspeções parciais descritas abaixo. Na revisão 05 (2026-11-06), P09-05 foi
inspecionada em PNG de produção e PDF rasterizado; a conferência dos SVGs no navegador
continua aguardando autorização do usuário.

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

## Revisão 03 — 2026-11-05

A folha de contato das nove pranchas foi examinada para conferir a sequência, os
carimbos `01/09` a `09/09`, as margens e a consistência do conjunto. As pranchas
06 (interligações) e 09 (descarga paramétrica) foram inspecionadas integralmente nos
PNGs de produção de 4.960 × 3.507 px a 300 dpi e nos PDFs rasterizados pelo Poppler
26.07.0 a 150 dpi, com 2.481 × 1.754 px.

- P09-06 apresenta os grupos W26-W28 e W29-W31 sem invadir a legenda, o carimbo ou
  as notas inferiores. As seções dos novos ramos permanecem explicitamente
  `A DEFINIR`.
- P09-09 distingue o nó interno REG1/COUT da porta X2 e mostra KD1/RD1 e KD2/RD2
  como propostas. As equações RC, a sequência, a pendência de valores e o bloqueio
  condicional da porta aparecem legíveis, sem cortes ou sobreposição relevante.
- As notas dizem que KD2 não deve fechar com fonte externa conectada e que a análise
  não garante 0 V. A prancha não apresenta valores calculados nem declara segurança.
- `revisar_portfolio.py` aprovou 12 projetos, 89 folhas, 356 arquivos gráficos e
  61 CSVs; similaridade mínima PDF/PNG de 0,9842. A validação estrita aprovou
  475.517 verificações, sem erros ou avisos.
- A abertura visual dos SVGs no navegador continua pendente de autorização. O
  AutoCAD/AcCoreConsole e a simulação elétrica não foram executados nesta revisão.

## Revisão 04 — 2026-11-05

A prancha 10 foi inspecionada integralmente no PNG de produção de 4.960 × 3.507 px
a 300 dpi e no PDF rasterizado pelo Poppler 26.07.0 a 150 dpi (2.481 × 1.754 px).
O primeiro arranjo dos quadros inferiores avançava sobre a área da legenda; ele foi
reposicionado antes da exportação final. Na versão atual, quadros, fórmulas, tabelas,
notas, aviso e carimbo estão separados e não apresentam cortes ou sobreposição
relevante. A tabela de cenários permanece legível em 150 dpi.

- A matriz mostra nove pares de eficiência assumidos a POUT=150 W. Os totais variam
  de 50,5 W no cenário de menor eficiência a 14,5 W no de maior eficiência; não são
  medições, previsões ou resultados térmicos do equipamento.
- A tabela divide perdas entre PS1 e REG1 e informa a margem nominal de 252 W de PS1.
  A prancha também enumera os dados de componente, gabinete e ensaio que faltam para
  estimar temperaturas.
- O validador específico do P09 passou em 18.846 verificações, sem erros. O restante
  da revisão do portfólio e a inspeção do contato atualizado estão registrados na
  auditoria consolidada. Os SVGs continuam aguardando inspeção visual no navegador.

## Revisão 05 — 2026-11-06

P09-05 foi revisada integralmente no PNG de produção de 4.960 × 3.507 px a 300 dpi e
no PDF rasterizado pelo Poppler 26.07.0 a 150 dpi (2.481 × 1.754 px). A tabela agora
separa os dez recortes frontais dos seis traseiros e informa, para cada item, centro
X/Y, dimensão e classificação `PROPOSTA`. A geometria dos dois LEDs e dos quatro furos
de fixação FAN1, ausente ou agrupada na versão anterior, aparece individualmente. A
origem inferior esquerda e a unidade milímetro estão explicadas; as notas impedem uso
para corte e fabricação sem confirmação OEM e definição das tolerâncias e processo.

Moldura, carimbo, dimensões do envelope, tabelas, nota e aviso obrigatório cabem na
folha. Não observei corte ou colisão relevante; a composição permanece legível no PDF
rasterizado. O validador específico passou em 18.916 verificações, sem erros, e o
AcCoreConsole 2027 abriu/auditou as dez fontes P09 com resultado `PASS`. A inspeção dos
contato das dez pranchas confirma sequência `01/10` a `10/10` e carimbos atualizados.
O revisor integrado aprovou 12 projetos, 114 pranchas, 456 arquivos gráficos e 77 CSVs;
a validação estrita passou em 673.894 verificações, sem erros ou avisos. A inspeção dos
SVGs no navegador ainda aguarda autorização; a simulação elétrica não foi executada.
