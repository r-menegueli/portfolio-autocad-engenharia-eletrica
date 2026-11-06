# Inspeção visual - Projeto 05

Estado: revisão 04, inspeção ampliada em 2026-11-06.

## Método

As nove pranchas foram regeneradas em DXF e em seus derivados PDF, SVG e PNG. P05-09
foi examinada integralmente no PNG de produção a 300 dpi e na rasterização independente
do PDF via `pypdfium2`; o contato das nove folhas foi conferido para verificar carimbos,
numeração, revisão, margens e composição do conjunto.

Na P05-09 conferi as cinco etapas, os doze grupos de dados, o status de cada linha, as
fontes de evidência, a legenda, as notas e o aviso obrigatório. A prancha P05-05 foi
conferida para confirmar que a corrente de curto-circuito e a capacidade de interrupção
ficaram pendentes, sem manter os antigos valores didáticos de 6 kA e Icu de 10 kA.

O AutoCAD AcCoreConsole 2027 abriu e auditou os nove DXFs em modo somente leitura. Os
nove resultados foram `0` erros e `0` correções. O validador específico, baseado em
`ezdxf`, passou em 406 verificações; a validação estrita do portfólio passou em 652.258
verificações, sem erros ou avisos. A revisão integrada confirmou 12 projetos, 111 folhas,
444 arquivos gráficos, 75 CSVs e similaridade mínima PDF/PNG de 0,981493. A similaridade
da folha P05-09 foi 0,984839.

## Resultado

O roteiro e a tabela P05-09 cabem na folha, sem cortes ou colisões visíveis. As cinco
etapas agora discriminam dados de entrada, modelo/cenários, cálculo de Icc máximo e
mínimo por ponto, verificações de capacidade/suportabilidade e curvas/pares, e fechamento
documental. Todos os doze grupos continuam `PENDENTE`; não há cálculo de curto-circuito,
seleção de capacidade de interrupção, seletividade ou retaguarda.

As nove folhas receberam revisão 04 e data 2026-11-06 nos DXFs e derivados. A inspeção
visual dos SVGs no navegador segue aguardando autorização do usuário. O workbook foi
regenerado a partir da lista de materiais revisada; os cálculos elétricos não mudaram.
