# Projeto 04 — Controle de nível de reservatório

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 06

Formato: A3 paisagem, unidades em milímetros, revisão gráfica 01 (2026-11-05)
Estado: concluído e validado em 2026-09-09

Este projeto acadêmico documenta um sistema conceitual de controle de nível para o reservatório TK-101. A variável controlada é o nível medido por LT-101; a variável manipulada é a frequência de VFD-101, que altera a vazão da bomba P-101/M-101. A principal perturbação é a vazão de saída para consumo.

## Entregáveis

- `fonte/`: seis desenhos DXF R2013 e scripts reproduzíveis.
- `exports/`: versões PDF, SVG e PNG derivadas dos DXFs.
- `memorial-descritivo.md`: descrição técnica do sistema.
- `criterios-premissas.md`: premissas e limites acadêmicos.
- `filosofia-controle.md`: malha, modos, alarmes e falhas.
- `estrategia-pid.md`: estratégia PI e parâmetros iniciais.
- `sequencia-funcionamento.md`: operação esperada e intertravamentos.
- `lista-instrumentos.csv`, `lista-io.csv`, `lista-cabos.csv`, `lista-bornes.csv` e `lista-materiais.csv`: tabelas técnicas.
- `tabelas-projeto-04.xlsx`: consolidação das tabelas para consulta.
- `validacao-controle.json` e `validacao.json`: resultados das validações específica e global.
- `inspecao-visual.md`: registro da inspeção dos arquivos renderizados.

## Pranchas

1. Fluxograma do processo.
2. P&ID e instrumentação.
3. Malha de controle.
4. Diagrama elétrico.
5. Interligações dos instrumentos.
6. Layout do sistema.

Cada prancha possui a fonte DXF correspondente em `fonte/` e derivados com o mesmo
nome-base em `exports/`.

## Documentação e tabelas

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Filosofia de controle](filosofia-controle.md)
- [Estratégia PI](estrategia-pid.md)
- [Sequência de funcionamento](sequencia-funcionamento.md)
- [Referências normativas](referencias-normativas.md)
- [Inspeção visual](inspecao-visual.md)
- [Workbook técnico](tabelas-projeto-04.xlsx)
- [Validação específica](validacao-controle.json)
- [Validação estrita](validacao.json)

## Resultado da validação

- Validador específico: `PASS`, 169 verificações e zero erros.
- Validador estrito do portfólio: `PASS`, 142.949 verificações, zero erros e zero avisos.
- AutoCAD 2027/AcCoreConsole: seis DXFs abertos e auditados com `PASS`.
- Testes automatizados: 9 aprovados.
- Reprodutibilidade: hashes idênticos para seis DXFs e 18 derivados após nova geração.
- Inspeção visual: PDF, SVG, PNG e seis abas do workbook aprovados após duas correções na fonte.

## Como reproduzir

Na raiz do portfólio, execute:

```powershell
.venv\Scripts\python.exe scripts\construir.py --root . --strict
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 04-controle-nivel-reservatorio\validacao.json
```

Os parâmetros PI são valores iniciais para estudo e comissionamento; não representam sintonia definitiva. Consulte [estrategia-pid.md](estrategia-pid.md) e [criterios-premissas.md](criterios-premissas.md).

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
