# Criterios tecnicos permanentes

## Finalidade e limite de uso

Esta infraestrutura organiza estudos academicos; ela nao fornece, por si so, um
projeto executivo. Nenhuma prancha pode sugerir aprovacao, liberacao para obra ou
responsabilidade tecnica registrada.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

O limite profissional e coerente com a
[Lei 5.194/1966](https://www.planalto.gov.br/ccivil_03/leis/l5194.htm) e com a
[Resolucao Confea 1.137/2023](https://normativos.confea.org.br/Ementas/Visualizar?id=76099),
que disciplina a ART. O aviso nao substitui uma avaliacao juridica ou tecnica.

## Registro de premissas

Antes de desenhar, cada projeto deve registrar no minimo:

- objetivo didatico e fronteira do sistema;
- tensoes, frequencia, numero de fases e esquema de aterramento adotados;
- condicoes de instalacao, temperatura, agrupamento e ambiente;
- cargas, regimes, fatores de demanda e simultaneidade, com origem dos dados;
- nivel de curto-circuito ou hipotese claramente identificada;
- criterios de queda de tensao, capacidade de conducao, protecao e seletividade;
- interfaces de comando, instrumentacao, automacao e seguranca;
- normas, edicoes, data de consulta e trechos aplicaveis;
- itens fora do escopo, incertezas e dados ainda pendentes.

Valores nao fornecidos devem ser marcados como `PREMISSA ACADEMICA`, nunca
apresentados como levantamento real.

## Verificacoes por tipo de sistema

Aplicar apenas os grupos pertinentes ao escopo, mantendo memoria de calculo ou
justificativa rastreavel:

1. **Baixa tensao:** balanco e demanda, corrente de projeto, capacidade dos
   condutores, queda de tensao, protecao contra sobrecorrente e choque, seccionamento,
   identificacao e aterramento.
2. **Media tensao:** classe de tensao, coordenacao de isolamento, curto-circuito,
   protecao, arranjos, distancias, aterramento e continuidade de servico.
3. **SPDA e surtos:** necessidade da protecao, analise de risco, classes, zonas,
   equipotencializacao e medidas contra surtos.
4. **Motores e comando:** regime, partida, corrente, torque, protecoes, intertravamentos,
   parada segura e estados de falha.
5. **Cabos e encaminhamento:** ocupacao, segregacao, raio de curvatura, dissipacao,
   suportacao e identificacao ponta a ponta.
6. **Instrumentacao:** faixa, unidade, tipo de sinal, alimentacao, blindagem,
   aterramento funcional, falha segura e referencia cruzada.
7. **Fotovoltaico e fontes:** limites CC/CA, polaridade, protecao, seccionamento,
   aterramento, sobretensao e interface com a rede, quando aplicavel.

Todo calculo deve declarar formula, unidade, entrada, resultado, arredondamento e
fonte. Coerencia dimensional e obrigatoria.

## Referencias normativas controladas

A tabela registra o estado consultado em 2026-09-05. Antes de cada projeto final,
confirmar novamente no catalogo oficial e consultar o texto integral licenciado.
"Referencia" nao significa certificacao de conformidade.

| Referencia | Aplicacao indicativa | Estado observado |
|---|---|---|
| [ABNT NBR 5410:2004 Versao Corrigida:2008](https://www.abntcatalogo.com.br/pnm.aspx?Q=bWl2M29BSEtyWlhaUWp5cXlOQlNNNGxCdmIvWDZCNmVCbkw3SzdhcGxqdz0=) | instalacoes de baixa tensao | catalogo indicava confirmacao em 2018 |
| [ABNT NBR 14039:2021](https://www.abntcatalogo.com.br/pnm.aspx?Q=MzQ5UEhnQTNmcGVEcTJqVEd1eVh5RmJiSitQby9BUUN0U1JFc0w3c2RDMD0=) | instalacoes de 1,0 kV a 36,2 kV | edicao 2021 listada |
| [ABNT NBR 5419-1:2026](https://www.abntcatalogo.com.br/pnm.aspx?Q=R0RZZDVqY2pvNE1lOTR6aU9OTnF6MmZ6RERoQnVBN2t6NlRVejg5c3U4QT0=) | principios gerais de protecao contra descargas | versao corrigida 2026 |
| [ABNT NBR 5419-2:2026](https://www.abntcatalogo.com.br/pnm.aspx?Q=REZxa2hZejlUejZ1a3RaUzdubks3ZlE3ajNIMGFPR2tRYnpuUDhNeEdUOD0=) | gerenciamento de risco | versao corrigida 2026 |
| [ABNT NBR 5419-3:2026](https://www.abntcatalogo.com.br/pnm.aspx?Q=cld2NDkxSm1oU2lyVXhXQ2ZXRXY1TE9FNGlLS3Z1cTBWT3d6eWVSb3FoUT0=) | danos fisicos e risco a vida | versao corrigida 2026 |
| [ABNT NBR 5419-4:2026](https://www.abntcatalogo.com.br/pnm.aspx?Q=anlGM2pWTXlJdnh2RkIvY1BWREVNTmFUUzB3bmZsaTRLQ1VnUWJzWkRnaz0=) | sistemas eletricos e eletronicos | versao corrigida 2026 |
| [NR-10 do MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-10-nr-10) | seguranca em instalacoes e servicos | texto de 2019 vigente ate 2027-05-31; nova redacao prevista para 2027-06-01 |
| [ABNT NBR 16752:2020](https://www.abntcatalogo.com.br/pnm.aspx?Q=WDZpNW1lb2pNdzJNOTB6RXZPTlZNTE1kQTJuaGJNSVZRMGI2cW10c3I2ND0=) | folhas e elementos de desenho tecnico | confirmada em 2025 |
| [IEC 60617:2026 DB](https://webstore.iec.ch/en/publication/2723) | simbolos eletrotecnicos | base licenciada publicada em 2026 |
| [IEC 61082-1:2014](https://webstore.iec.ch/en/publication/4469) | apresentacao de informacao eletrotecnica | estabilidade indicada ate 2029 |

A ABNT NBR 5444:1989 consta cancelada sem substituicao desde 2014. Ela nao deve
ser usada para alegar conformidade vigente. Nao armazenar copias integrais de
normas ou bibliotecas licenciadas no repositorio.

## Entregaveis de cada projeto

Cada pasta em `projetos/NN-nome-curto/` deve conter:

- `README.md` com objetivo, reproducao, unidades, criterios, arquivos e aviso;
- `memorial-descritivo.md`;
- `criterios-premissas.md`;
- `lista-materiais.csv` codificada em UTF-8;
- `fonte/` com DXF principal e script-fonte;
- `exports/` com PDF, SVG e PNG correspondentes;
- resultado de validacao automatica e registro de inspecao visual.

Campos minimos do CSV: `item`, `tag`, `descricao`, `especificacao_academica`,
`quantidade`, `unidade`, `fabricante_referencia`, `observacoes`. A indicacao de
fabricante deve ser apenas referencia comparativa e nunca publicidade ou requisito
oculto.

## Revisao e rastreabilidade

- Revisao `00` e a primeira emissao; alteracoes tecnicas incrementam a revisao.
- Toda prancha deve manter numero unico e referencia cruzada consistente.
- O commit deve conter simultaneamente fonte, derivados, documentos e manifesto.
- DXF e a fonte principal. PDF, SVG e PNG sao meios de revisao.
- DWG derivado exige conversao real por ferramenta identificada, assinatura binaria
  compativel e reabertura sem erros; renomear DXF e falha grave.
- A validacao automatica reduz erros objetivos, mas nao substitui a inspecao visual
  nem a revisao de engenharia.
