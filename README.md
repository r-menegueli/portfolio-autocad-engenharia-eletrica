# Portfólio AutoCAD de Engenharia Elétrica

Infraestrutura técnica, visual e documental reproduzível para dez projetos acadêmicos
de Engenharia Elétrica.

**Autor:** Rogério Eduardo Moreira Menegueli

**Estado atual:** base comum do portfólio; os dez projetos finais ainda não fazem parte
desta etapa.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## O que esta base estabelece

- prancha A3 paisagem de 420 × 297 mm, em milímetros;
- moldura, carimbo, legenda, notas técnicas e identificação da prancha;
- 14 layers funcionais padronizados;
- DXF AC1027 (AutoCAD 2013) como fonte principal;
- PDF, SVG e PNG como formatos de visualização;
- geração e renderização reproduzíveis em Python;
- validação automática da estrutura, documentos e artefatos;
- convenção documental comum aos dez projetos futuros.

As regras normativas estão em [AGENTS.md](AGENTS.md), e os parâmetros processáveis
ficam centralizados em [portfolio.toml](portfolio.toml).

## Documentação

- [Padrão gráfico](docs/padrao-grafico.md): folha, moldura, carimbo, tipografia, layers e
  representação visual.
- [Critérios técnicos](docs/criterios-tecnicos.md): premissas, rastreabilidade, segurança
  e qualidade técnica.
- [Plano dos projetos](docs/plano-projetos.md): escopo proposto para os dez trabalhos,
  sem produzir os projetos finais nesta etapa.
- [Relatório de ferramentas](relatorio-ferramentas.md): versões detectadas, limitações e
  formatos efetivamente disponíveis no ambiente.
- [Inspeção visual](docs/inspecao-visual.md): defeitos encontrados, correções e
  conferência final do template renderizado.
- [Licença](LICENSE): condições de uso do conteúdo acadêmico.

Consulte o relatório de ferramentas antes de assumir que AutoCAD, LibreCAD, ODA File
Converter, Inkscape ou qualquer conversor está disponível.

## Estrutura

```text
portfolio-autocad-engenharia-eletrica/
├── AGENTS.md
├── README.md
├── LICENSE
├── portfolio.toml
├── requirements.txt
├── relatorio-ferramentas.md
├── docs/
│   ├── padrao-grafico.md
│   ├── criterios-tecnicos.md
│   └── plano-projetos.md
├── templates/
│   ├── template-a3.dxf
│   ├── template-a3.svg
│   └── carimbo-a3/
│       ├── carimbo-a3.dxf
│       └── carimbo-a3.svg
├── scripts/
│   ├── construir.py
│   ├── gerar_template_a3.py
│   ├── renderizar.py
│   ├── validar_portfolio.py
│   ├── autocad_console.ps1
│   └── portfolio_config.py
├── renders/
│   ├── template-a3.pdf
│   ├── template-a3.png
│   └── manifesto.json
└── projetos/                    # reservado aos dez projetos futuros
```

O diretório `projetos/` fica reservado para `01-...` até `10-...`. Cada projeto futuro
terá README, memorial descritivo, critérios e premissas, lista de materiais CSV, fonte
DXF e script em `fonte/`, além de PDF, SVG e PNG em `exports/`.

## Preparação do ambiente

Requer Python 3.11 ou superior. No PowerShell, a partir da raiz do repositório:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

Se o launcher `py` não estiver disponível, use um executável Python 3.11+ encontrado no
sistema para criar `.venv`. As dependências têm versões fixadas em
[requirements.txt](requirements.txt).

## Geração, renderização e validação

Gerar novamente o template e o carimbo em DXF verdadeiro:

```powershell
.\.venv\Scripts\python.exe .\scripts\gerar_template_a3.py --root .
```

Renderizar os artefatos declarados em `portfolio.toml` para visualização:

```powershell
.\.venv\Scripts\python.exe .\scripts\renderizar.py --root . --dpi 300
```

Executar a validação normal:

```powershell
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root .
```

Executar a validação estrita, na qual avisos também causam falha:

```powershell
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

Gerar uma saída JSON para análise automatizada:

```powershell
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --format json --report .\work\validacao.json
```

Executar a cadeia completa — geração, renderização e validação:

```powershell
.\.venv\Scripts\python.exe .\scripts\construir.py --root . --strict
```

Os comandos acima descrevem o fluxo esperado; não constituem, por si só, afirmação de
que uma execução ainda não registrada foi aprovada. Consulte a saída mais recente do
validador e faça também a inspeção visual.

Quando o AutoCAD estiver instalado, auditar a abertura pelo console headless:

```powershell
.\scripts\autocad_console.ps1 -Action Audit -InputPath .\templates\template-a3.dxf
```

Uma conversão DWG opcional exige saída nova e gera evidencia JSON ao lado do
arquivo. Use `work/` para um teste que não sera versionado:

```powershell
.\scripts\autocad_console.ps1 -Action Convert `
  -InputPath .\templates\template-a3.dxf `
  -OutputDwg .\work\template-a3-verificacao.dwg
```

O script executa `SAVEAS`, verifica a assinatura binaria e reabre o resultado no
AcCoreConsole. A disponibilidade observada esta documentada no
[relatorio de ferramentas](relatorio-ferramentas.md).

## Artefatos-base

- [Template A3 em DXF](templates/template-a3.dxf), fonte principal editável.
- [Template A3 em SVG](templates/template-a3.svg), visualização vetorial.
- [Template A3 em PDF](renders/template-a3.pdf), visualização para impressão.
- [Template A3 em PNG](renders/template-a3.png), visualização raster.
- [Carimbo A3 em DXF](templates/carimbo-a3/carimbo-a3.dxf) e
  [carimbo A3 em SVG](templates/carimbo-a3/carimbo-a3.svg).
- [Manifesto dos renders](renders/manifesto.json), com rastreabilidade dos derivados.

Após qualquer mudança no template, regenere todos os derivados e abra o PNG, o PDF e o
SVG. Confira especialmente bordas, carimbo, aviso, legenda, notas, alinhamentos e
legibilidade. A validação automática complementa essa inspeção, mas não a substitui.

## Formatos

| Formato | Papel no fluxo | Condição |
|---|---|---|
| DXF | fonte principal do desenho | AC1027/R2013 real, auditável e compatível com AutoCAD |
| SVG | visualização vetorial | derivado do DXF |
| PDF | visualização e impressão | derivado do DXF em A3 paisagem |
| PNG | inspeção visual raster | derivado do DXF, 300 dpi no fluxo padrão |
| DWG | saída opcional | somente conversão real e verificada |

Nunca renomeie DXF para DWG. Um DWG só pode ser produzido quando houver AutoCAD, ODA
File Converter ou outra ferramenta apropriada, seguido de verificação de formato e
reabertura/auditoria. Sem essa cadeia, o portfólio entrega DXF, PDF, SVG e PNG.

## O que o validador verifica

O script [validar_portfolio.py](scripts/validar_portfolio.py) verifica integridade e
auditoria de DXF, arquivos vazios, estrutura obrigatória, layers, PDFs, SVGs, PNGs,
READMEs, links relativos, arquivos temporários, limites de folha, elementos fora da
moldura e textos potencialmente sobrepostos. Também confere o manifesto e rejeita DWG
incompatível com a política do repositório.

O código de saída é `0` apenas quando o status é `PASS`; falhas de validação retornam
`1`, e erro interno retorna `2`. Use `--strict` como critério de entrega e trate cada
aviso como item de revisão visual ou técnica.

## Como iniciar um projeto futuro

1. Escolha o item correspondente em [docs/plano-projetos.md](docs/plano-projetos.md).
2. Crie `projetos/NN-slug/` com `README.md`, `memorial-descritivo.md`,
   `criterios-premissas.md`, `lista-materiais.csv`, `fonte/` e `exports/`.
3. Use [templates/template-a3.dxf](templates/template-a3.dxf) e preserve todos os layers
   obrigatórios.
4. Mantenha o DXF e o script reproduzível em `fonte/`; exporte PDF, SVG e PNG para
   `exports/`.
5. Inclua o aviso obrigatório no desenho e no README individual, registre premissas e
   mantenha a lista de materiais coerente com as referências da prancha.
6. Registre o artefato em `portfolio.toml`, gere os derivados, execute a validação
   estrita e faça inspeção visual antes do commit.

Não use os materiais como documentação executiva. Qualquer aplicação real exige revisão,
dimensionamento, conformidade normativa e responsabilidade de profissional legalmente
habilitado.
