# Padrao grafico do portfolio

Este documento define a linguagem visual comum aos 22 estudos do portfólio. O
arquivo [`portfolio.toml`](../portfolio.toml) e a fonte de verdade legivel por
maquina; divergencias entre este texto e a configuracao devem ser corrigidas antes
de uma nova prancha.

## Folha e coordenadas

- Formato: A3, orientacao paisagem, 420 x 297 mm.
- Sistema de coordenadas: origem `(0, 0)` no canto inferior esquerdo da folha.
- Unidade do modelspace: milimetro; `$INSUNITS = 4` e `$MEASUREMENT = 1`.
- Moldura: `(10, 10)` a `(410, 287)` mm.
- Coordenadas, cotas e escalas devem permanecer explicitas. A escala impressa nao
  substitui dimensoes numericas.
- O carimbo mede 180 x 58 mm e ocupa o canto inferior direito da moldura.
- A tabela de revisoes fica imediatamente acima do carimbo.

A composicao segue como referencia nacional a
[ABNT NBR 16752:2020](https://www.abntcatalogo.com.br/pnm.aspx?Q=WDZpNW1lb2pNdzJNOTB6RXZPTlZNTE1kQTJuaGJNSVZRMGI2cW10c3I2ND0=).
Os campos do carimbo tambem se inspiram na
[ISO 7200:2004](https://www.iso.org/standard/35446.html). Essas referencias nao
dispensam a consulta aos textos licenciados e as edicoes vigentes.

## Carimbo obrigatorio

Cada prancha deve mostrar, sem abreviacoes ambiguas:

- titulo do projeto;
- autor: Rogério Eduardo Moreira Menegueli;
- data em ISO 8601 (`AAAA-MM-DD`);
- revisao com dois algarismos;
- numero da prancha no formato `NN/TT`;
- nome do arquivo-fonte;
- unidades;
- escala;
- formato da folha;
- estado documental, como `MODELO`, `REVISAO` ou `ACADEMICO`.

O bloco DXF reutilizavel chama-se `CARIMBO_A3`. Os atributos nao devem ser
explodidos sem necessidade, pois eles permitem atualizacao e validacao automatica.

## Layers

As cores ACI usadas no DXF tambem precisam permanecer distinguiveis e escuras na
renderizacao sobre fundo branco. Evite amarelo, ciano, verde-lima e cinza-claro em
linhas finas. Para impressao, uma tabela CTB monocromatica e apropriada quando
preserva os pesos e a hierarquia visual.

| Layer | Uso | ACI | Peso |
|---|---|---:|---:|
| `00_MOLDURA` | moldura e referencias de zona | 7 | 0,50 mm |
| `01_CARIMBO` | linhas do carimbo e revisoes | 7 | 0,25 mm |
| `02_TEXTO` | titulos, rotulos e identificadores | 7 | 0,18 mm |
| `03_COTAS` | cotas e linhas auxiliares | 152 | 0,18 mm |
| `04_EQUIPAMENTOS` | contornos de equipamentos | 32 | 0,35 mm |
| `05_POTENCIA` | circuitos de potencia | 12 | 0,50 mm |
| `06_COMANDO` | circuitos de comando | 94 | 0,25 mm |
| `07_INSTRUMENTACAO` | sinais e instrumentacao | 202 | 0,25 mm |
| `08_CABOS` | cabos e identificadores associados | 124 | 0,35 mm |
| `09_BORNES` | bornes e pontos de conexao | 145 | 0,25 mm |
| `10_ELETROCALHAS` | leitos, eletrocalhas e rotas | 251 | 0,35 mm |
| `11_ARQUITETURA` | base arquitetonica de apoio | 253 | 0,18 mm |
| `12_LEGENDA` | legenda e chaves de leitura | 7 | 0,18 mm |
| `13_NOTAS` | notas, ressalvas e aviso obrigatorio | 7 | 0,18 mm |

Os nomes sao exatos, em maiusculas e sem acentos. O layer `0` pode existir por
compatibilidade DXF, mas nunca substitui um layer funcional.

## Texto e linhas

- Familia preferencial: Arial; o DXF usa `arial.ttf` e `arialbd.ttf` com fallback
  controlado pelo aplicativo CAD.
- Texto comum: 1,8 a 2,5 mm na folha.
- Subtitulo: 3,0 a 3,5 mm.
- Titulo: 4,0 a 5,0 mm.
- Evitar altura inferior a 1,8 mm em informacao que precise ser lida no PDF A3.
- Usar maiusculas para titulos e identificadores; usar frase normal em notas
  extensas.
- Manter espacamento visual minimo de 0,5 vez a altura do texto entre blocos.
- Tipos e espessuras de linha devem formar hierarquia coerente; a
  [ISO 128-2:2022](https://www.iso.org/standard/83355.html) e referencia indicativa.

## Simbolos eletricos

O template inclui blocos internos de demonstracao:

- `SIM_DISJUNTOR`;
- `SIM_MOTOR`;
- `SIM_TERMINAL`;
- `SIM_TERRA`.

Novos simbolos devem ser blocos nomeados, ter ponto-base funcional, escala 1:1 em
milimetros, layer semantico e identificador documentado. A biblioteca deve consultar
a [IEC 60617:2026 DB](https://webstore.iec.ch/en/publication/2723) e as regras de
apresentacao da [IEC 61082-1:2014](https://webstore.iec.ch/en/publication/4469).
Como a base IEC e licenciada, nao se deve copiar seu conteudo indiscriminadamente.
A ABNT NBR 5444:1989 esta cancelada sem substituicao e pode aparecer apenas como
referencia historica, nunca como conformidade vigente.

## Nomes e formatos

- Pastas de projeto: `NN-nome-curto`, com numero de `01` a `12`.
- Pranchas-fonte: `NN_nome_da_prancha.dxf`, com `NN` sequencial dentro do projeto.
- Arquivos derivados conservam exatamente o mesmo nome-base e usam `.pdf`, `.svg`
  e `.png`.
- DXF e sempre a fonte CAD principal.
- Um `.dwg` so pode surgir por conversao real e ser acompanhado da evidencia de
  reabertura; mudar apenas a extensao e proibido.
- SVG deve preservar `viewBox`; PDF deve manter MediaBox A3 paisagem; PNG deve ter
  no minimo 300 dpi no processo oficial.

## Aviso e privacidade

O texto abaixo deve aparecer no README e nas pranchas de cada projeto:

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

Nao registrar CPF, RG, telefone, endereco residencial ou outros identificadores
pessoais desnecessarios.

## Inspecao visual

Depois de cada alteracao significativa:

1. gerar novamente DXF, SVG, PDF e PNG;
2. executar o validador em modo estrito;
3. rasterizar o PDF com Poppler, sem reutilizar apenas o PNG direto;
4. inspecionar a pagina inteira e ampliar carimbo, notas, legenda e extremidades;
5. corrigir cortes, desalinhamentos, glifos ausentes, linhas excessivas ou textos
   sobrepostos;
6. registrar a revisao visual antes do commit.
