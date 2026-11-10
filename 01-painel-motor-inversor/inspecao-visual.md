# Registro de inspeção visual

Data: 2026-09-05

Revisão: 00

Responsável pela documentação: Rogério Eduardo Moreira Menegueli

## Método

Cada DXF foi renderizado diretamente para SVG, PDF e PNG pelo fluxo `ezdxf` e
Matplotlib. Além do PNG direto em 300 dpi, cada PDF foi rasterizado de forma
independente com Poppler 26.07.0 a 150 dpi, e cada SVG foi aberto e rasterizado no
Chrome headless. Foram examinadas a página inteira e as regiões de título, conteúdo
técnico, legenda, notas, aviso, revisão e carimbo.

## Correções realizadas

1. A representação inicial da prancha 02 não mostrava os polos internos de Q0/Q1 e
   deixava pequenas lacunas entre as fases e o símbolo de M1. O gerador foi corrigido;
   todas as linhas agora têm continuidade geométrica até os dispositivos.
2. A representação inicial da prancha 03 deixava uma lacuna antes dos contatos de
   comando. As conexões foram estendidas até os terminais dos símbolos.
3. A referência de velocidade foi detalhada em duas entradas explícitas - P1/0-10 V
   local e X3:10-11/4-20 mA remota - ligadas ao seletor de fonte S3 e a VFD1-AI1.

## Resultado por prancha

| Prancha | PNG direto | PDF rasterizado | Cortes | Sobreposições | Conectividade visual | Resultado |
|---|---|---|---|---|---|---|
| 01 - Diagrama unifilar | legível | legível | nenhum | nenhuma | contínua | PASS |
| 02 - Diagrama de potência | legível | legível | nenhum | nenhuma | contínua após correção | PASS |
| 03 - Diagrama de comando | legível | legível | nenhum | nenhuma | contínua após correção | PASS |
| 04 - Layout interno | legível | legível | nenhum | nenhuma | não aplicável | PASS |
| 05 - Diagrama de bornes | legível | legível | nenhum | nenhuma | tabelas íntegras | PASS |
| 06 - Interligações de campo | legível | legível | nenhum | nenhuma | rotas conectadas | PASS |

Os seis PDFs têm uma página, formato A3 paisagem de 1190,55 x 841,89 pontos e não são
criptografados. As seis imagens PNG têm 4960 px de largura. Aviso obrigatório, autor,
data, revisão e número da prancha permaneceram visíveis em todos os derivados.

## Abertura CAD

Cada uma das seis fontes DXF foi aberta e auditada pelo Autodesk AcCoreConsole 2027,
versão 26.0.118.0.0, em 2026-09-05. Todas retornaram `AUTOCAD_AUDIT=PASS`.

## Conclusão

Não permaneceram cortes, desalinhamentos, linhas desconectadas, textos ilegíveis ou
colisões visuais relevantes na revisão 00. A inspeção visual complementa a validação
geométrica automática e não constitui validação de engenharia para execução real.

## Revisão gráfica 02 — 2026-11-05

A revisão acrescentou a prancha 07, com a cadeia QDG–Q0–Q1–VFD1–M1 e uma matriz de
sete grupos: corrente de curto-circuito, Q0, Q1, VFD1/M1, Q2/PS1, DPS1 e cabos W01/W02.
Cada linha identifica a premissa atual, os dados reais necessários e a análise em
aberto. A razão numérica entre a capacidade presumida de Q1 e a Icc didática foi
explicitamente marcada como insuficiente para provar coordenação.

Inspecionei visualmente a composição atual das oito folhas. P01-07 foi conferida em PNG
integral a 300 dpi e em PDF rasterizado independentemente pelo Poppler a 150 dpi.
P01-08 também foi examinada nos dois formatos; a tabela, os avisos e o carimbo cabem
na folha sem cortes ou colisões relevantes. Similaridades PDF/PNG: 0,987268 em P01-07
e 0,984095 em P01-08.

A prancha 08 acrescenta um fluxo de cinco etapas e uma matriz com doze pontos, do
fechamento documental ao pacote as-built. O CSV relacionado registra os dados e as
evidências requeridas; todos os itens aparecem como `NÃO EXECUTADO`, sem resultados de
campo nem alegações de aprovação.

O Autodesk AcCoreConsole 2027 abriu e auditou os oito DXFs: `AUTOCAD_AUDIT=PASS` em
8/8. A validação estrita integrada passou por 509.704 verificações, sem erros nem
avisos; o revisor consolidado aprovou 12 projetos, 95 pranchas, 380 arquivos gráficos
e 67 CSVs. A inspeção visual dos SVGs em navegador continua pendente de autorização.

Essa revisão confirma apresentação, integridade CAD e consistência documental. Não
confirma dimensionamento, coordenação elétrica, seletividade ou conformidade normativa.

## Revisão funcional/documental 03 — 2026-11-06

A prancha 03 foi redesenhada para separar os comandos RUN, STOP e reset de falha do VFD
em LOCAL e REMOTO. S3 passou a ser descrito como seletor de três posições
LOCAL-0-REMOTO. S5 agora é o botão dedicado de rearme manual monitorado de KSR1; S4 e
X3:9 permanecem destinados ao reset de falha do inversor. O desenho não fixa bornes nem
arquitetura interna: o mapeamento de DI/STO e a quantidade de blocos de contato continuam
dependentes dos equipamentos selecionados e de suas instruções.

A prancha 08 e o CSV relacionado agora contêm treze verificações. V13 verifica a
independência entre rearme de segurança e reset do VFD, a ausência de RUN no rearme e a
exigência de novo comando deliberado. Todos os itens continuam `NÃO EXECUTADO`.

Inspecionei em tamanho integral os PNGs das pranchas 03 e 08 e rasterizações independentes
dos PDFs a 150 dpi. Não encontrei cortes ou colisões; a tabela V13 cabe na folha. A
similaridade PDF/PNG foi 0,991639 em P01-03 e 0,983640 em P01-08. O AutoCAD AcCoreConsole
2027 abriu e auditou as oito fontes DXF: `AUTOCAD_AUDIT=PASS` em 8/8.

Após regenerar o manifesto e os derivados, o validador estrito aprovou 624.834
verificações, com zero erros e avisos. Na fotografia daquela revisão, a auditoria consolidada registrou 12 projetos, 105
pranchas, 420 arquivos gráficos e 73 CSVs; esse total foi superado por snapshots
posteriores. Os resultados atuais estão no [relatório de validação](../relatorio-validacao.md).

A inspeção dos SVGs em navegador continua aguardando autorização. Esta revisão verifica
apresentação, abertura CAD e consistência documental; não valida dimensionamento,
coordenação, categoria de segurança, PL/SIL ou funcionamento de uma instalação real.

## Revisão funcional/documental 04 — 2026-11-06

A prancha 09 resume estados de habilitação, operação normal e respostas a quatro eventos.
O fluxo exige um novo comando após rearme, falha, retorno de energia ou troca de modo.
O documento identifica explicitamente como hipótese a parada controlada e o alarme após
perda de 4–20 mA. Não declara validação de campo, categoria/PL/SIL ou tempo de parada.

Conferi a prancha integral no PNG de produção a 300 dpi, no PDF rasterizado
independentemente pelo Poppler a 150 dpi e no contato das nove folhas. Não encontrei
cortes ou colisões; a similaridade PDF/PNG de P01-09 foi 0,990330. O AcCoreConsole 2027
abriu e auditou 9/9 DXFs; o validador estrito passou em 663.880 verificações, sem erros
ou avisos. A inspeção dos SVGs em navegador aguarda autorização.
