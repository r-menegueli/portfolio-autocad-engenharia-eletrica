# Registro de inspecao visual do template A3

Data da inspecao: 2026-09-05.

## Artefatos examinados

- [`../renders/template-a3.png`](../renders/template-a3.png), render direto a 300 dpi;
- [`../renders/template-a3.pdf`](../renders/template-a3.pdf), uma pagina A3 paisagem;
- rasterizacao independente do PDF a 200 dpi pelo Poppler 26.07.0;
- segunda rasterizacao diagnostica pelo PDFium 5.13.0;
- [`../templates/template-a3.svg`](../templates/template-a3.svg), estrutura XML e
  proporcao verificadas automaticamente.

## Problemas encontrados e correcoes

1. Na primeira renderizacao, entidades ACI 7 foram resolvidas como branco sobre
   fundo branco. O renderizador passou a declarar explicitamente fundo branco e cor
   padrao preta antes de desenhar cada layout.
2. Um titulo auxiliar no alto da folha teve posicionamento divergente entre o
   backend PNG/PDFium e o Poppler. Como a mesma identificacao ja consta no carimbo,
   o elemento redundante foi removido. Isso eliminou a diferenca entre os renders.
3. Cada formato agora recebe documento e figura novos, evitando caches de fonte e
   transformacao entre backends.

## Resultado final

- moldura completa, sem corte nas quatro extremidades;
- zonas A-H e 1-5 alinhadas e legiveis;
- legenda e simbolos sem colisao;
- area util e guias centralizados;
- aviso obrigatorio completo e legivel;
- notas tecnicas com espacamento regular;
- tabela de revisao alinhada;
- carimbo completo, autor/data/revisao/prancha visiveis;
- acentos do nome e do aviso renderizados corretamente;
- PNG direto e PDF rasterizado visualmente coerentes;
- nenhum texto ilegivel ou potencialmente sobreposto observado.

O PDF foi confirmado como nao criptografado, com uma pagina de
1190,55 x 841,89 pontos (A3 paisagem). A inspecao visual complementa, sem substituir,
o validador geometrico e a abertura no AutoCAD.
