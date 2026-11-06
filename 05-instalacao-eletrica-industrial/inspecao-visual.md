# Inspeção visual — Projeto 05

Estado: revisão 05, inspeção em 2026-11-06.

## Escopo e método

As nove pranchas foram regeneradas em DXF e em PDF, SVG e PNG. Conferi o contato
atualizado das nove folhas para margens, carimbos, numeração, revisão e composição.
A P05-01 foi ampliada no PNG de produção a 300 dpi e na rasterização independente do
PDF via `pypdfium2` a 150 dpi. A leitura visual em navegador dos SVGs segue aguardando
autorização do usuário.

## Resultado da P05-01

A tabela relaciona M-501 a M-505 e TUE-501 aos circuitos C01–C06, potência aparente
instalada e coordenadas X/Y do croqui. O marcador de origem e as notas informam que as
coordenadas são derivadas da geometria em escala 1:125, não de levantamento topográfico.
Tabela, planta, dimensões, legenda, notas, aviso e carimbo estão dentro da folha; não
observei cortes ou colisões relevantes. A folha continua conceitual: pegadas, folgas,
acessos, fluxo e rotas reais não estão representados.

## Verificações

- O validador específico passou em 443 verificações, sem erros; confirmou os seis
  registros da tabela e as respectivas tags, circuitos, cargas e coordenadas.
- O AutoCAD AcCoreConsole 2027 abriu e auditou os nove DXFs; os logs registram zero
  erros encontrados e zero corrigidos.
- A similaridade PDF/PNG de P05-01 foi 0,992284. No conjunto P05, o revisor integrado
  confirmou nove folhas e similaridade mínima de 0,984155.
- A revisão integrada do portfólio confirmou 12 projetos, 114 folhas, 456 arquivos
  gráficos e 77 CSVs, com similaridade mínima geral de 0,981493. A validação estrita
  passou em 668.075 verificações, sem erros ou avisos.

Essas verificações avaliam consistência, abertura e apresentação. Não confirmam
dimensionamento, conformidade normativa, implantação real ou aptidão para execução.
O workbook foi regenerado a partir da lista de materiais revisada; os cálculos elétricos
não mudaram.
