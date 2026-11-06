# Inspeção visual - Projeto 08

Estado atual: revisão gráfica 04 em 2026-11-06. As seções anteriores registram o histórico.

As seis pranchas da revisão anterior foram examinadas nos PNGs de produção a 300 dpi, com 4960 × 3507
pixels; nos PDFs A3 de uma página, rasterizados pelo Poppler a 150 dpi em 2481 × 1754
pixels; e nos SVGs abertos pelo Google Chrome e rasterizados em 1600 × 1131 pixels.

## Primeira passagem e correções

- corrigida a legenda de cor dos módulos na prancha 01;
- deslocado o rótulo do PE na prancha 03 para eliminar interferência visual;
- desviadas as descidas de PE dos DPS na prancha 04 para não cruzar os condutores CC;
- separados QD-FV, BEP, eletrodo e interface com SPDA na prancha 05;
- ortogonalizadas as rotas CA e reposicionada a rota PE na prancha 06.

## Resultado final

A segunda passagem da revisão anterior confirmou moldura e carimbo íntegros, aviso obrigatório legível,
numeração 01/06 a 06/06, símbolos e cores consistentes, duas strings independentes,
polaridades identificadas, proteções CC/CA, DPS, seccionamento, aterramento, rotas e
tabelas sem cortes, desalinhamentos, sobreposições aparentes ou textos ilegíveis.

Na revisão 02, as sete pranchas foram geradas em DXF, PDF, SVG e PNG. As sete PNGs de
produção a 300 dpi e os sete PDFs A3 rasterizados foram inspecionados. A prancha 07
apresenta grade de HSP/PR, caso-base atual, fórmula, unidade e ausência de dados locais;
os rótulos da escala foram conferidos contra os 13 registros do CSV. A inspeção visual
adicional dos SVGs da revisão 02 em navegador aguarda autorização do usuário.

O resultado visual não transforma o estudo acadêmico em documentação executiva e não
substitui verificação de engenharia no local.

## Revisão gráfica 03 - 2026-11-06

As oito folhas foram reemitidas como `NN/08`, revisão 03. P08-08 foi examinada no PNG
de produção a 300 dpi e em PDF rasterizado independentemente pelo Poppler a 150 dpi.
Curvas, tabela, limites, notas, legenda e carimbo cabem na moldura; não identifiquei
cortes ou colisões relevantes. A prancha representa os mesmos valores que
`envelope-termico.csv`. O AcCoreConsole 2027 abriu e auditou 8/8 DXFs, e o validador
específico passou em 8.119 verificações. A inspeção visual adicional dos SVGs no
navegador aguarda autorização do usuário.

## Revisão gráfica 04 - 2026-11-06

P08-01 e P08-06 foram reemitidas com correção da legenda de cor CC e identificação
individual dos cabos/rotas do layout. A separação S1/MPPT 1 e S2/MPPT 2, os IDs e os
comprimentos assumidos foram conferidos contra `lista-cabos.csv`. Os comprimentos não
são medições; a geometria das rotas não representa um imóvel levantado. O cabo
COM-INV está marcado como opcional e sem trajeto físico definido.

As PNGs integrais de P08-01 e P08-06 foram examinadas a 300 dpi. Os PDFs de ambas são
de uma página A3 paisagem e foram rasterizados independentemente pelo Poppler a 150 dpi;
carimbos, notas, legendas, trajetos e margens permaneceram visíveis sem cortes ou
colisões gráficas relevantes. O contato das oito folhas confirma revisão 04 e
numeração `01/08` a `08/08`.

O validador específico passou em 8.131 verificações e o AcCoreConsole 2027 auditou
8/8 DXFs com `PASS`. A revisão integrada confirmou 12 projetos, 114 folhas, 456 arquivos
gráficos e 77 CSVs; P08-06 obteve similaridade PDF/PNG de 0,989889. A validação estrita
passou em 674.521 verificações, sem erros ou avisos. Os SVGs foram gerados, mas a
inspeção visual adicional no navegador aguarda autorização do usuário.
