# P20 — Subestação de tração ferroviária em corrente contínua

Estudo conceitual de uma subestação fixa para alimentar, por um terceiro trilho, uma linha urbana hipotética em 750 Vcc. As três pranchas cobrem a cadeia de conversão, o retorno de corrente e as funções de proteção e supervisão que ainda exigem estudo.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Unifilar CA/CC, retificador, terceiro trilho e retorno pelos trilhos | [DXF](fonte/01_unifilar_subestacao_tracao.dxf) | [PDF](exports/01_unifilar_subestacao_tracao.pdf) | [SVG](exports/01_unifilar_subestacao_tracao.svg) | [PNG](exports/01_unifilar_subestacao_tracao.png) |
| 02/03 | Zonas de alimentação, seccionamento conceitual e caminho de retorno | [DXF](fonte/02_zonas_alimentacao_retorno_tracao.dxf) | [PDF](exports/02_zonas_alimentacao_retorno_tracao.pdf) | [SVG](exports/02_zonas_alimentacao_retorno_tracao.svg) | [PNG](exports/02_zonas_alimentacao_retorno_tracao.png) |
| 03/03 | Matriz de proteção, medição e supervisão com estudos pendentes | [DXF](fonte/03_matriz_protecao_supervisao_tracao_cc.dxf) | [PDF](exports/03_matriz_protecao_supervisao_tracao_cc.pdf) | [SVG](exports/03_matriz_protecao_supervisao_tracao_cc.svg) | [PNG](exports/03_matriz_protecao_supervisao_tracao_cc.png) |

Documentos e dados: [memorial](memorial-descritivo.md), [critérios e premissas](criterios-premissas.md), [referências](referencias-normativas.md), [sensibilidade de corrente](sensibilidade-corrente.csv), [materiais](lista-materiais.csv), [sinais](lista-sinais.csv), [matriz de proteção](matriz-protecao.csv), [plano de estudos](plano-estudos.csv), [gerador](fonte/gerar_projeto_20.py), [validador](fonte/validar_projeto_20.py), [validação](validacao-projeto-20.json) e [inspeção visual](inspecao-visual.md).

## Caso-base ilustrativo

- PCC de entrada hipotético: 13,8 kV AC, 60 Hz.
- Barramento de tração adotado para o estudo: 750 Vcc.
- Potência CC de referência: 1,0 MW.
- Corrente ideal no barramento: `I = P/V = 1.333,3 A`.

O valor é uma conta ideal de sensibilidade, sem ondulação, perdas, perfil de trens, ciclos de aceleração, regeneração ou queda de tensão. Não seleciona retificador, transformador, disjuntor, cabo ou terceiro trilho.

## Como reproduzir

Na raiz do repositório, com `.venv` e as dependências de `requirements.txt`:

```powershell
.\.venv\Scripts\python.exe .\20-tracao-ferroviaria-cc-750v\fonte\gerar_projeto_20.py --root .
.\.venv\Scripts\python.exe .\scripts\renderizar.py --root . --artifact p20-01-unifilar-subestacao-tracao --artifact p20-02-zonas-alimentacao-retorno-tracao --artifact p20-03-matriz-protecao-supervisao-tracao-cc
.\.venv\Scripts\python.exe .\20-tracao-ferroviaria-cc-750v\fonte\validar_projeto_20.py --root .
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

DXF AC1027 é a fonte editável em milímetros. PDF, SVG e PNG são derivados. Não há DWG neste projeto.

## Limites

Não foram calculados curto-circuito, coordenação ou seletividade, queda de tensão, ondulação, potência de frenagem regenerativa, correntes simultâneas, retorno, tensões de toque, correntes vagantes, corrosão, aterramento, isolamento, interfaces com sinalização ou geometria do terceiro trilho. As zonas e as duas subestações da prancha 02 são esquemáticas. Não há ajustes de proteção, modelo de trens, simulação de alimentação, análise de risco, ensaio ou verificação de campo.
