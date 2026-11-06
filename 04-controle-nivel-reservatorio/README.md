# Projeto 04 — Controle de nível de reservatório

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 09

Formato: A3 paisagem, unidades em milímetros, revisão gráfica 05 (2026-11-06)

Estado: documentação conceitual; as nove fontes DXF da revisão 05 passaram no AutoCAD
AcCoreConsole 2027 e no validador funcional. A inspeção dos SVGs no navegador aguarda
autorização.

O projeto documenta uma malha conceitual de nível para o reservatório TK-101. A variável controlada é o nível medido por LT-101; a variável manipulada é a frequência de VFD-101, que altera a vazão da bomba P-101/M-101. A vazão de saída para consumo é a principal perturbação assumida. A origem e o equipamento de sucção a montante não foram definidos e aparecem como limite externo. HV-102 é uma válvula manual conceitual na saída; os dados para sua seleção continuam pendentes.

P04-08 registra sete grupos de dados que faltam na fronteira de sucção. P04-09 mostra
como os dados entram no balanço de NPSHa e na comparação com a curva OEM de NPSHr. Todos
permanecem PENDENTE; a folha não seleciona fonte, bomba ou proteção nem calcula margem.

## Entregáveis

- `fonte/`: nove desenhos DXF R2013 e scripts reproduzíveis.
- `exports/`: versões PDF, SVG e PNG derivadas dos DXFs.
- `memorial-descritivo.md`: descrição técnica do sistema.
- `criterios-premissas.md`: premissas e limites acadêmicos.
- `filosofia-controle.md`: malha, modos, alarmes e falhas.
- `estrategia-pid.md`: estratégia PI e parâmetros iniciais.
- `sequencia-funcionamento.md`: operação esperada e intertravamentos.
- `matriz-causa-efeito.csv`: eventos e respostas documentados na prancha 07.
- `dados-fonte-succao.csv`: sete grupos PENDENTE, com fonte de evidência, orientação de unidade/referência e valor ainda vazio.
- `lista-instrumentos.csv`, `lista-io.csv`, `lista-cabos.csv`, `lista-bornes.csv` e `lista-materiais.csv`.
- `tabelas-projeto-04.xlsx`: consolidação das tabelas para consulta.
- `validacao-controle.json` e `validacao.json`: resultados das validações específica e global.
- `inspecao-visual.md`: registro dos métodos e limites da inspeção visual.

## Pranchas

1. Fluxograma do processo.
2. P&ID e instrumentação.
3. Malha de controle.
4. Diagrama elétrico.
5. Interligações dos instrumentos.
6. Layout do sistema.
7. Sequência de operação e matriz causa–efeito.
8. [Fronteira de sucção e dados da fonte](fonte/08_fronteira_succao_dados_fonte.dxf): D01–D07 para identificar a fonte, regime, fluido, pressão, geometria, curva da bomba e eventual proteção, sem selecionar uma solução.
9. [Balanço de sucção e critério de NPSH](fonte/09_balanco_succao_criterio_npsh.dxf): equação paramétrica de NPSHa, perdas da linha e comparação com NPSHr OEM; entradas e resultado continuam pendentes.

Cada prancha possui a fonte DXF correspondente em `fonte/` e derivados com o mesmo nome-base em `exports/`.

## Documentação

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Filosofia de controle](filosofia-controle.md)
- [Estratégia PI](estrategia-pid.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Matriz causa–efeito](matriz-causa-efeito.csv)
- [Dados da fonte e sucção](dados-fonte-succao.csv)
- [Referências normativas e didáticas](referencias-normativas.md)
- [Referências normativas](referencias-normativas.md)
- [Inspeção visual](inspecao-visual.md)
- [Workbook técnico](tabelas-projeto-04.xlsx)
- [Validação específica](validacao-controle.json)
- [Validação estrita](validacao.json)

## Validação e limites

- Validador funcional específico: `PASS`, 279 verificações e zero erros; D01–D07 permanecem pendentes e sem valores preenchidos.
- Revisor de planilhas do portfólio: `PASS`, dois workbooks, 13 abas e 214 fórmulas no conjunto, zero erros.
- Validador estrito do portfólio: `PASS`, 650.961 verificações, zero erros e zero avisos. O revisor integrado confirmou 12 projetos, 111 pranchas, 444 arquivos gráficos e 75 CSVs; similaridade mínima PDF/PNG de 0,981493.
- A revisão 05 reemite as nove folhas em DXF, PDF, SVG e PNG. P04-08 e P04-09 foram conferidas no PNG de produção, em PDFs rasterizados independentemente e no contato das nove folhas; as similaridades PDF/PNG foram 0,989404 e 0,989947. A inspeção dos SVGs no navegador aguarda autorização.
- Os parâmetros PI são iniciais e não representam sintonia definitiva. Divergências persistentes entre LT-101 e chaves bloqueiam o automático; a resposta pós-falta de energia exige confirmação de retenção do alarme no PLC selecionado.
- Nenhuma função recebe classificação SIL, PL ou categoria de segurança. Consulte [estrategia-pid.md](estrategia-pid.md) e [criterios-premissas.md](criterios-premissas.md).

## Como reproduzir

Na raiz do portfólio, execute:

```powershell
.venv\Scripts\python.exe 04-controle-nivel-reservatorio\fonte\gerar_projeto_04.py --root .
.venv\Scripts\python.exe 04-controle-nivel-reservatorio\fonte\validar_projeto_04.py --root .
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict
```

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
