# Inspeção visual - Projeto 07

Estado: revisão inicial aprovada em 2026-09-09; revisão gráfica 02 em 2026-11-05.

## Amostra examinada

Foram examinadas visualmente todas as oito pranchas em três cadeias independentes:

- oito PNGs de produção a 300 dpi, com 4.960 × 3.507 pixels;
- oito PDFs A3 paisagem reabertos pelo `pdfinfo` e rasterizados pelo Poppler a
  150 dpi, com 2.481 × 1.754 pixels;
- oito SVGs abertos pelo Google Chrome 152.0.7977.83 e rasterizados em
  1.600 × 1.131 pixels.

Em cada prancha foram conferidos moldura, carimbo, aviso obrigatório, número, revisão,
legenda, notas, hierarquia, legibilidade e correspondência entre os três formatos.
Também foram inspecionados sentido do fluxo de energia, polaridade HV, estados da
pré-carga, habilitação física, cadeias V/f e FOC, topologia CAN e segregação de rotas.

## Correções da primeira revisão

1. O conversor CC-CC foi retirado da representação em série com o barramento LV e
   passou a mostrar entradas HV e saída LV separadas.
2. A cadeia física de habilitação foi segmentada entre blocos, eliminando linhas que
   atravessavam símbolos.
3. O estágio do inversor foi redesenhado como ponte de seis chaves/PWM, com fases U,
   V e W distintas, e a realimentação da cadeia FOC foi esclarecida.
4. Os sensores foram agrupados por barramentos de aquisição, removendo o efeito de
   linhas em leque e cruzamentos ambíguos.
5. A tabela CAN foi estreitada e a observação inferior reposicionada para eliminar
   interferência com a área de diagnóstico.

Os scripts-fonte foram corrigidos e todos os DXFs e derivados foram regenerados antes
da segunda revisão.

## Resultado

As oito pranchas e os 24 derivados da revisão inicial foram aprovados. Não foram observados cortes,
desalinhamentos, textos encobertos, perda do aviso obrigatório ou divergências visuais
entre PNG, PDF e SVG. A inspeção visual complementa, mas não substitui, a validação
automática e a auditoria dos DXFs no AutoCAD.

## Revisão gráfica 02 - 2026-11-05

As oito folhas existentes foram reemitidas como `NN/09`, revisão 02. P07-09 foi
inspecionada no PNG integral de produção a 300 dpi e no PDF rasterizado pelo Poppler a
150 dpi. Também conferi a folha de contato atual das nove pranchas. Tabela, limites,
notas, aviso obrigatório, legenda e carimbo estão dentro da moldura; não identifiquei
cortes nem colisões relevantes. A inspeção visual do SVG no navegador continua pendente
da autorização do usuário.
