# P18 — Compensação de reativos e qualidade de energia

Estudo conceitual de uma instalação industrial de 400 V, com compensação automática de fator de potência, um caso aritmético reproduzível e um plano de medição para decidir se há necessidade de reatores ou filtros harmônicos. O escopo separa o dimensionamento preliminar de kvar da avaliação de harmônicos, que depende de medições e estudos não disponíveis.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Unifilar de cargas, medição no PCC e banco automático conceitual | [DXF](fonte/01_unifilar_compensacao_reativos.dxf) | [PDF](exports/01_unifilar_compensacao_reativos.pdf) | [SVG](exports/01_unifilar_compensacao_reativos.svg) | [PNG](exports/01_unifilar_compensacao_reativos.png) |
| 02/03 | Cálculo de kvar, degraus discretos e sensibilidade da corrente | [DXF](fonte/02_memoria_correcao_fator_potencia.dxf) | [PDF](exports/02_memoria_correcao_fator_potencia.pdf) | [SVG](exports/02_memoria_correcao_fator_potencia.svg) | [PNG](exports/02_memoria_correcao_fator_potencia.png) |
| 03/03 | Medição, sequência de controle e dados pendentes para estudo harmônico | [DXF](fonte/03_medicao_controle_harmonicos.dxf) | [PDF](exports/03_medicao_controle_harmonicos.pdf) | [SVG](exports/03_medicao_controle_harmonicos.svg) | [PNG](exports/03_medicao_controle_harmonicos.png) |

Documentos: [memorial](memorial-descritivo.md), [critérios](criterios-premissas.md), [referências](referencias-normativas.md), [curva de compensação](curva-compensacao.csv), [materiais](lista-materiais.csv), [sinais](lista-sinais.csv), [gerador](fonte/gerar_projeto_18.py), [validador](fonte/validar_projeto_18.py), [validação](validacao-projeto-18.json) e [inspeção visual](inspecao-visual.md).

## Caso-base ilustrativo

- Carga ativa hipotética de 600 kW, fator de potência inicial 0,80 indutivo, em 400 V.
- Fator de potência-alvo de estudo: 0,95.
- Compensação aritmética calculada: aproximadamente 252,8 kvar.
- Representação de um banco automático hipotético de 300 kvar, em 12 degraus de 25 kvar. No caso-base, 10 degraus (250 kvar) resultam em FP aproximado 0,949; 11 degraus (275 kvar) resultam em FP aproximado 0,960.
- Esses valores não selecionam capacitores, reatores, contatores, fusíveis ou controlador.

## Como reproduzir

```powershell
python .\18-compensacao-reativos-qualidade-energia\fonte\gerar_projeto_18.py --root .
python .\scripts\renderizar.py --root . --artifact p18-01-unifilar-compensacao-reativos --artifact p18-02-memoria-correcao-fp --artifact p18-03-medicao-controle-harmonicos
python .\18-compensacao-reativos-qualidade-energia\fonte\validar_projeto_18.py --root .
python .\scripts\validar_portfolio.py --root . --strict
```

DXF AC1027 é a fonte editável em milímetros. PDF, SVG e PNG são derivados. Não há DWG neste projeto.

## Limites

Não há medições no PCC, espectro de harmônicos, impedância de fonte, perfil horário, estudo de ressonância, cálculo de curto-circuito ou requisito de concessionária. Nenhum filtro ou reator foi escolhido. A compensação real depende da carga simultânea, da tensão efetiva, dos dados dos capacitores e de uma análise da instalação e dos efeitos harmônicos.
