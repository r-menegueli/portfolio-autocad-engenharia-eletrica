# Projeto 04 — Controle de nível de reservatório

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 07

Formato: A3 paisagem, unidades em milímetros, revisão gráfica 02 (2026-11-05)

Estado: ampliação da documentação conceitual; validação funcional local aprovada.
Inspeção dos SVGs atuais no navegador e reabertura no AutoCAD ainda pendentes.

O projeto documenta uma malha conceitual de nível para o reservatório TK-101. A variável controlada é o nível medido por LT-101; a variável manipulada é a frequência de VFD-101, que altera a vazão da bomba P-101/M-101. A vazão de saída para consumo é a principal perturbação assumida.

## Entregáveis

- `fonte/`: sete desenhos DXF R2013 e scripts reproduzíveis.
- `exports/`: versões PDF, SVG e PNG derivadas dos DXFs.
- `memorial-descritivo.md`: descrição técnica do sistema.
- `criterios-premissas.md`: premissas e limites acadêmicos.
- `filosofia-controle.md`: malha, modos, alarmes e falhas.
- `estrategia-pid.md`: estratégia PI e parâmetros iniciais.
- `sequencia-funcionamento.md`: operação esperada e intertravamentos.
- `matriz-causa-efeito.csv`: eventos e respostas documentados na prancha 07.
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

Cada prancha possui a fonte DXF correspondente em `fonte/` e derivados com o mesmo nome-base em `exports/`.

## Documentação

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Filosofia de controle](filosofia-controle.md)
- [Estratégia PI](estrategia-pid.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Matriz causa–efeito](matriz-causa-efeito.csv)
- [Referências normativas](referencias-normativas.md)
- [Inspeção visual](inspecao-visual.md)
- [Workbook técnico](tabelas-projeto-04.xlsx)
- [Validação específica](validacao-controle.json)
- [Validação estrita](validacao.json)

## Validação e limites

- Validador funcional específico: `PASS`, 225 verificações e zero erros.
- Validador estrito do portfólio: `PASS`, 448.668 verificações, zero erros e zero avisos.
- Revisor consolidado: `PASS`, 12 projetos, 85 pranchas, 340 arquivos gráficos e 57 CSVs; similaridade mínima PDF/PNG de 0,984161.
- A revisão 02 foi renderizada em PNG e PDF para inspeção local. A abertura dos SVGs atuais em navegador e dos DXFs atuais no AutoCAD ainda não foi repetida.
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
