# Regras permanentes do portfólio

Este arquivo rege todo o repositório e todos os dez projetos acadêmicos que serão
desenvolvidos nele. As instruções explícitas do usuário prevalecem; em seguida,
`portfolio.toml` é a fonte normativa para metadados, geometria, layers, artefatos e
parâmetros de validação. Não altere esses contratos silenciosamente.

## Escopo e finalidade

- O repositório fornece infraestrutura técnica, visual e documental reproduzível para
  um portfólio acadêmico de Engenharia Elétrica.
- A base comum foi concluída antes do início dos projetos. Desenvolva somente o projeto
  solicitado pelo usuário e não antecipe os demais.
- Todo desenho é acadêmico e conceitual. Não o trate como projeto executivo, documento
  de fabricação, instalação, obra, comissionamento ou segurança.
- Autor oficial: **Rogério Eduardo Moreira Menegueli**.

## Privacidade

- Use apenas o nome do autor nos artefatos e metadados do portfólio.
- Nunca inclua CPF, RG, telefone, endereço residencial ou outro dado pessoal sensível.
- Não adicione assinaturas, registros profissionais, números de conselho ou selos que
  possam sugerir responsabilidade técnica inexistente.
- Antes de versionar arquivos, verifique metadados e caminhos incorporados para evitar
  nomes de usuário locais, diretórios particulares, tokens ou outros segredos.

## Aviso obrigatório

Inclua, sem abreviar nem reformular, o texto abaixo em cada projeto, no desenho e no
`README.md` individual. Repita-o no memorial quando houver uma seção de responsabilidade
ou limitações:

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

O texto deve permanecer legível nas saídas PDF, SVG e PNG.

## Padrão da prancha

- Use exclusivamente folha **A3 em orientação paisagem**, com 420 × 297 mm.
- Trabalhe em milímetros, declare `mm` no carimbo e grave `$INSUNITS = 4` no DXF. Se um
  valor técnico usar outra unidade, indique-a junto ao valor e explique-a nas premissas.
- Configure os limites da folha entre `(0, 0)` e `(420, 297)` mm.
- Use moldura interna de `(10, 10)` a `(410, 287)` mm. A tolerância geométrica de
  validação é 0,5 mm.
- Toda prancha deve conter moldura e carimbo, título, autor, data, revisão, número da
  prancha, unidades, legenda, notas técnicas e o aviso obrigatório.
- Use data inequívoca no formato `AAAA-MM-DD`, revisão controlada (`00`, `01`, ...), e
  numeração de prancha no formato `NN/TT`.
- Não deixe conteúdo gráfico ou texto fora da moldura, exceto a própria geometria da
  folha/moldura quando tecnicamente necessária e prevista pelo template.
- Preserve margens, alinhamentos, hierarquia tipográfica e área útil estabelecidos em
  `templates/template-a3.dxf` e `docs/padrao-grafico.md`.

## Layers obrigatórios

Todo DXF de prancha deve conter, com esta grafia exata, no mínimo os layers abaixo:

1. `00_MOLDURA`
2. `01_CARIMBO`
3. `02_TEXTO`
4. `03_COTAS`
5. `04_EQUIPAMENTOS`
6. `05_POTENCIA`
7. `06_COMANDO`
8. `07_INSTRUMENTACAO`
9. `08_CABOS`
10. `09_BORNES`
11. `10_ELETROCALHAS`
12. `11_ARQUITETURA`
13. `12_LEGENDA`
14. `13_NOTAS`

- Não renomeie, traduza, reutilize ou mude a finalidade desses layers.
- Aplique cor ACI, espessura e tipo de linha definidos em `portfolio.toml`.
- Layers adicionais só são permitidos quando indispensáveis, com nome numerado,
  finalidade inequívoca e documentação no README do projeto.
- Não deixe entidades de produção no layer `0`; ele pode existir apenas por exigência
  interna do DXF e por definições de bloco.

## Símbolos, textos e representação elétrica

- Use uma biblioteca coerente de símbolos elétricos, preferencialmente alinhada às
  convenções IEC/ABNT aplicáveis ao tema, e declare a referência adotada.
- Modele símbolos como blocos reutilizáveis, com ponto de inserção, escala e atributos
  consistentes. Não misture convenções gráficas sem legenda explícita.
- Identifique equipamentos, cabos, bornes e circuitos de modo único e mantenha a mesma
  identificação no desenho, memorial e lista de materiais.
- Garanta contraste, espessuras e alturas de texto legíveis em A3 impresso e na
  renderização em tela.
- Evite colisões entre textos, cotas, símbolos, linhas e bordas. Alertas do detector de
  sobreposição exigem inspeção; não devem ser descartados automaticamente.

## Formatos e proveniência

- **DXF é a fonte principal** de cada desenho. Gere DXF verdadeiro e compatível com
  AutoCAD; a versão padrão é AC1027/AutoCAD 2013, conforme `portfolio.toml`.
- Mantenha o script-fonte que produz ou transforma cada DXF. A geração deve ser
  determinística, repetível a partir de um ambiente limpo e independente de edição
  manual não documentada.
- Gere PDF, SVG e PNG a partir do DXF principal. Esses arquivos são derivados para
  visualização e não substituem a fonte.
- O PNG de prancha deve ter, no mínimo, 2400 px de largura; use 300 dpi no fluxo padrão.
- Nunca renomeie um arquivo `.dxf` para `.dwg`, nem declare que um DXF é DWG.
- Só gere DWG por conversão real com AutoCAD, ODA File Converter ou conversor compatível.
  Registre ferramenta e versão, confirme a assinatura/formato do arquivo resultante e
  reabra/audite o DWG convertido. Sem conversor disponível e verificação bem-sucedida,
  não entregue DWG.
- Não edite apenas um derivado. Corrija o script ou o DXF fonte e regenere todas as
  visualizações para manter equivalência entre formatos.

## Convenção dos projetos

Cada projeto futuro deve ocupar `projetos/NN-slug/`, onde `NN` vai de `01` a `10` e
`slug` é curto, descritivo, minúsculo, sem espaços e sem acentos. A estrutura mínima é:

Exceções registradas: por instruções explícitas, os Projetos 01 a 10 ocupam
`01-painel-motor-inversor/`, `02-projeto-eletrico-residencial/` e
`03-painel-automacao-clp/`, `04-controle-nivel-reservatorio/` e
`05-instalacao-eletrica-industrial/`, `06-centro-controle-motores/` e
`07-arquitetura-veiculo-eletrico/`, `08-sistema-fotovoltaico/`,
`09-fonte-bancada/` e `10-rede-instrumentacao-industrial/` na raiz. Não mova nem
duplique essas pastas. A convenção
`projetos/NN-slug/` continua sendo o padrão dos próximos projetos, salvo nova
instrução explícita.

```text
projetos/NN-slug/
├── README.md
├── memorial-descritivo.md
├── criterios-premissas.md
├── lista-materiais.csv
├── fonte/
│   ├── NN-slug.dxf
│   └── gerar_NN_slug.py
└── exports/
    ├── NN-slug.pdf
    ├── NN-slug.svg
    └── NN-slug.png
```

- O `README.md` individual deve explicar objetivo, escopo, exclusões, unidades,
  normas/referências, como reproduzir, lista de artefatos e resultado da validação.
- O memorial descritivo deve registrar solução, funcionamento e interfaces sem alegar
  aptidão para execução real.
- `criterios-premissas.md` deve separar fatos, hipóteses, critérios de cálculo, limites
  e pontos que dependem de dimensionamento ou revisão profissional.
- `lista-materiais.csv` deve ser UTF-8, conter cabeçalho e usar, no mínimo, os campos
  `item,quantidade,unidade,descricao,referencia,observacoes`. Mantenha as referências
  coerentes com o desenho.
- Registre cada prancha em `portfolio.toml` como artefato quando o projeto for criado,
  sem remover os artefatos comuns existentes.
- Use apenas links locais relativos dentro da documentação. Não use `file://`, caminhos
  absolutos, letras de unidade ou links que saiam da raiz do repositório.

## Reprodutibilidade

- Python mínimo: 3.11. Instale as versões fixadas em `requirements.txt` em ambiente
  virtual local `.venv`.
- Centralize metadados e parâmetros em `portfolio.toml`; não duplique valores divergentes
  nos scripts.
- Scripts devem aceitar a raiz do repositório por argumento quando aplicável, resolver
  caminhos de forma portátil e retornar código diferente de zero ao falhar.
- Não dependa de AutoCAD para a geração básica. Quando ele não estiver disponível, use
  `ezdxf` para criar DXF real.
- Preserve UTF-8, finais de linha configurados no repositório e nomes de arquivos
  estáveis. Evite timestamps variáveis ou metadados voláteis em artefatos reproduzíveis.
- Não versione ambientes virtuais, caches, logs, backups de editores ou arquivos
  temporários do AutoCAD.

## Validação obrigatória

Execute o validador após toda alteração que afete desenhos, documentos, scripts,
configuração ou artefatos. Ele deve cobrir, no mínimo:

- abertura, auditoria e integridade dos DXFs;
- detecção de arquivos ausentes ou vazios;
- presença e grafia dos layers obrigatórios;
- presença, integridade e dimensões de PDF, SVG e PNG;
- presença do README, memorial, critérios/premissas e lista de materiais de cada projeto;
- validade e relatividade dos links locais;
- ausência de arquivos temporários;
- limites do desenho e geometria da folha;
- entidades fora da moldura;
- textos potencialmente sobrepostos;
- coerência do manifesto e dos derivados, quando aplicável;
- proibição de DWG falso ou não verificado.

Use `python scripts/validar_portfolio.py --root .` durante o trabalho e
`python scripts/validar_portfolio.py --root . --strict` antes de concluir uma entrega.
Corrija todos os erros. Em modo normal, revise cada aviso; em modo estrito, avisos também
bloqueiam a entrega. Não reduza limites ou exclua arquivos apenas para mascarar falhas.

## Inspeção visual e critérios de qualidade

- Após gerar o DXF, renderize PDF, SVG e PNG e abra os arquivos resultantes.
- Inspecione a prancha inteira e amplie carimbo, aviso, legenda, notas, cotas e regiões
  densas. Verifique cortes, clipping, margens, alinhamento, contraste, caracteres,
  espessuras, hierarquia e legibilidade.
- Compare visualmente os três derivados com o DXF. Uma execução sem exceção não é prova
  suficiente de qualidade visual.
- Corrija no arquivo-fonte ou script, regenere e reinspecione até não haver cortes,
  desalinhamentos, texto ilegível, símbolos inconsistentes ou sobreposições relevantes.
- Considere a entrega pronta somente quando a estrutura estiver completa, os DXFs
  abrirem sem erros, as renderizações forem legíveis, o validador estrito passar, o
  relatório de ferramentas estiver atualizado e o Git estiver limpo após commit local.

## Controle de mudanças

- Preserve alterações preexistentes e mantenha cada mudança dentro do escopo solicitado.
- Atualize documentação, scripts, artefatos e manifesto juntos quando uma regra comum
  mudar.
- Faça commits locais claros e verificáveis. Não publique no GitHub nem envie arquivos
  a serviços externos sem solicitação explícita.
- Antes do commit, revise `git diff`; depois dele, confirme `git status --short` vazio.
