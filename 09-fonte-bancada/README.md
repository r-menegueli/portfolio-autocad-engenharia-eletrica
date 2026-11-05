# Projeto 09 - Fonte de bancada ajustável

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 06

Formato: A3 paisagem, geometria em milímetros, revisão gráfica 01 (2026-11-05)

Estado: estudo concluído; apresentação atualizada na revisão gráfica 01

Este projeto apresenta a documentação eletromecânica acadêmica de uma fonte de
bancada ajustável. A arquitetura proposta recebe 90 a 264 Vca, 47 a 63 Hz, e fornece
saída isolada e flutuante ajustável de 0 a 30 Vcc, com limite de corrente de 0 a 5 A e
potência máxima de 150 W. A conversão combina uma fonte AC/DC isolada de 36 Vcc e um
regulador buck CC/CV.

O estudo cobre proteção de entrada, conversão, regulação, medição, comandos,
conectores, ventilação, painel frontal, organização interna e interligações. Não
define PCB, firmware, isolamento construtivo, categoria de sobretensão, coordenação
de fusíveis, compatibilidade eletromagnética, calibração, ensaios térmicos ou
homologação de componentes.

## Pranchas

1. [Diagrama de blocos](fonte/01_diagrama_blocos.dxf)
2. [Diagrama elétrico](fonte/02_diagrama_eletrico.dxf)
3. [Painel frontal](fonte/03_painel_frontal.dxf)
4. [Layout interno](fonte/04_layout_interno.dxf)
5. [Detalhes mecânicos](fonte/05_detalhes_mecanicos.dxf)
6. [Interligações](fonte/06_interligacoes.dxf)

Cada DXF tem derivados homônimos em `exports/` nos formatos PDF, SVG e PNG.

## Características declaradas

| Grandeza | Valor acadêmico |
| --- | ---: |
| entrada | 90-264 Vca, 47-63 Hz, L/N/PE |
| classe construtiva proposta | classe I, chassi metálico ligado ao PE |
| saída | 0-30 Vcc, 0-5 A, 150 W máximo |
| modo de regulação | CV/CC ajustável |
| estágio isolado PS1 | 36 Vcc, 7 A, 252 W |
| regulador REG1 | buck CC/CV, 150 W |
| saída em relação ao chassi | flutuante; negativo não ligado internamente ao PE |
| invólucro de referência | 320 × 150 × 260 mm |
| ambiente de premissa | interno, seco, 0-40 °C, até 2.000 m |

Os valores detalhados e sua classificação epistemológica estão em
[Parâmetros](parametros.csv). Nenhum componente comercial foi selecionado ou declarado
certificado.

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Referências normativas](referencias-normativas.md)
- [Lista de equipamentos](lista-equipamentos.csv)
- [Lista de proteções](lista-protecoes.csv)
- [Lista de interligações](lista-interligacoes.csv)
- [Lista de recortes](lista-recortes.csv)
- [Lista de materiais](lista-materiais.csv)
- [Resultados dos cálculos](resultados-calculo.csv)
- [Inspeção visual](inspecao-visual.md)
- [Validação específica](validacao-fonte.json)
- [Validação estrita](validacao.json)

## Reprodução

Na raiz do portfólio:

```powershell
.venv\Scripts\python.exe 09-fonte-bancada\fonte\gerar_projeto_09.py --root .
.venv\Scripts\python.exe 09-fonte-bancada\fonte\validar_projeto_09.py --root .
.venv\Scripts\python.exe scripts\renderizar.py --root . --dpi 300
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 09-fonte-bancada\validacao.json
```

O DXF AC1027 é a fonte principal. Nenhum DWG é fornecido nesta revisão.

## Resultado de qualidade

- o validador específico aprovou 18.554 verificações sem erros;
- os seis DXFs foram abertos e auditados pelo AutoCAD/AcCoreConsole 2027;
- os 18 derivados foram reconstruídos: seis PDFs, seis SVGs e seis PNGs;
- os PDFs foram reabertos e rasterizados pelo Poppler 26.07.0;
- os SVGs foram abertos pelo Google Chrome 152.0.7977.83;
- os PNGs de produção foram inspecionados em 300 dpi;
- cortes, duplicações de elementos, colisões de notas, cotas e rótulos encontrados na
  primeira inspeção foram corrigidos na fonte e a inspeção final foi aprovada;
- a validação estrita integrada aprovou 330.795 verificações, sem erros ou avisos,
  conforme [validacao.json](validacao.json).
- uma reconstrução consecutiva preservou os hashes SHA-256 dos 24 artefatos CAD e
  de visualização do projeto.

Nenhum DWG foi criado ou distribuído. O projeto continua acadêmico, conceitual, sem
certificação e sem liberação para fabricação ou uso em rede elétrica.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
