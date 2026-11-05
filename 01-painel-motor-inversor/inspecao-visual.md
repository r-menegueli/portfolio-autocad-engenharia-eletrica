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

As sete folhas foram inspecionadas nos PNGs de produção a 300 dpi e na composição P01;
P01-07 também foi rasterizada independentemente do PDF com Poppler a 150 dpi. A tabela,
as notas, o aviso e o carimbo permanecem dentro da folha e sem sobreposição relevante.
O revisor do portfólio atribuiu similaridade PDF/PNG de 0,987268 a P01-07.

O Autodesk AcCoreConsole 2027 abriu e auditou os sete DXFs: `AUTOCAD_AUDIT=PASS` em
7/7. A validação estrita integrada passou por 501.282 verificações, sem erros nem
avisos; o revisor consolidado aprovou 12 projetos, 94 pranchas, 376 arquivos gráficos
e 66 CSVs. A inspeção visual dos SVGs em navegador continua pendente de autorização.

Essa revisão confirma apresentação, integridade CAD e consistência documental. Não
confirma dimensionamento, coordenação elétrica, seletividade ou conformidade normativa.
