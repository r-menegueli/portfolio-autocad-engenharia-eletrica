# Guia de organização dos projetos acadêmicos

Os dez projetos descritos no [plano de projetos](../docs/plano-projetos.md) foram
criados na raiz por instruções explícitas e não devem ser movidos ou duplicados aqui.
Esta pasta conserva as convenções de organização e aceitação.

Consulte o [padrão gráfico](../docs/padrao-grafico.md), os [critérios técnicos](../docs/criterios-tecnicos.md) e o [manifesto do portfólio](../portfolio.toml).

## Ordem e identificadores reservados

| Ordem | Pasta futura | Tema |
| ---: | --- | --- |
| 1 | [`../01-painel-motor-inversor/`](../01-painel-motor-inversor/README.md) | painel de motor com inversor de frequência - concluído |
| 2 | [`../02-projeto-eletrico-residencial/`](../02-projeto-eletrico-residencial/README.md) | projeto elétrico residencial - concluído |
| 3 | [`../03-painel-automacao-clp/`](../03-painel-automacao-clp/README.md) | painel de automação com CLP para duas bombas - concluído |
| 4 | [`../04-controle-nivel-reservatorio/`](../04-controle-nivel-reservatorio/README.md) | controle de nível com instrumentação, CLP e inversor - concluído |
| 5 | [`../05-instalacao-eletrica-industrial/`](../05-instalacao-eletrica-industrial/README.md) | instalação elétrica industrial - concluído |
| 6 | [`../06-centro-controle-motores/`](../06-centro-controle-motores/README.md) | centro de controle de motores - concluído |
| 7 | [`../07-arquitetura-veiculo-eletrico/`](../07-arquitetura-veiculo-eletrico/README.md) | arquitetura elétrica de veículo elétrico - concluído |
| 8 | [`../08-sistema-fotovoltaico/`](../08-sistema-fotovoltaico/README.md) | sistema fotovoltaico residencial - concluído |
| 9 | [`../09-fonte-bancada/`](../09-fonte-bancada/README.md) | fonte de bancada ajustável - concluído |
| 10 | [`../10-rede-instrumentacao-industrial/`](../10-rede-instrumentacao-industrial/README.md) | rede acadêmica de instrumentação industrial - concluído |

Os nomes estão reservados para manter ordenação e links previsíveis. Eles não
devem ser criados vazios nem usados para armazenar rascunhos sem rastreabilidade.

## Estrutura obrigatória futura

Quando um projeto for iniciado, sua pasta deverá adotar a estrutura abaixo. O
gerador oficial poderá materializá-la, mas não deverá criar entregáveis vazios.

```text
Pxx-nome-do-projeto/
├── README.md
├── memorial-descritivo.md
├── criterios-premissas.md
├── memoria-calculo.md
├── dados/
│   ├── entradas.*
│   └── lista-materiais.csv
├── fontes/
│   └── gerar_projeto.py
├── cad/
│   └── Pxx-YY-titulo-r00.dxf
├── visualizacao/
│   ├── pdf/
│   ├── svg/
│   └── png/
└── validacao/
    ├── relatorio-validacao.*
    └── inspecao-visual.md
```

`Pxx` identifica o projeto, `YY` é o número sequencial da prancha e `r00` é a
revisão. Arquivos derivados deverão conservar o mesmo nome-base do DXF de origem.
Se a estrutura comum for alterada, este guia e os validadores deverão mudar no
mesmo commit.

## Conteúdo mínimo do README individual

Cada README de projeto deverá informar:

- título, código, autor, estado, data e revisão;
- objetivo, escopo, exclusões e público acadêmico;
- unidades adotadas, critérios, premissas e normas com edição;
- índice das pranchas e descrição dos arquivos de dados;
- comandos exatos para instalar dependências, gerar, renderizar e validar;
- formatos realmente disponíveis e limitações das ferramentas utilizadas;
- resultado da validação e data da inspeção visual;
- links relativos para memorial, critérios, memória, materiais e pranchas.

O aviso a seguir é obrigatório, sem abreviações:

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

Não deverão ser incluídos CPF, RG, telefone ou endereço residencial do autor.

## Regras para arquivos CAD e derivados

- O DXF verdadeiro é a fonte principal e deverá abrir sem erro em ferramenta
  compatível com AutoCAD.
- Um arquivo DXF nunca poderá ser apenas renomeado para `.dwg`.
- DWG é opcional e só poderá ser produzido por conversão real, seguida de
  verificação independente de abertura e registro da ferramenta/versão.
- Cada prancha deverá ter correspondentes PDF, SVG e PNG oriundos da mesma revisão.
- O desenho deverá usar folha A3 em paisagem, unidades declaradas, moldura,
  carimbo, legenda, notas, número da prancha e layers padronizados.
- Símbolos comuns deverão vir da biblioteca do portfólio; variantes locais
  precisarão ser justificadas e documentadas.

## Critério de conclusão de um projeto

Um projeto somente poderá ser marcado como concluído quando:

1. todos os documentos e dados mínimos existirem e não estiverem vazios;
2. os DXFs passarem pela leitura estrutural e pela conferência de layers e limites;
3. não houver elementos fora da moldura nem sobreposições de texto não justificadas;
4. PDF, SVG e PNG estiverem legíveis e coerentes com a mesma revisão do DXF;
5. links relativos forem válidos e não existirem arquivos temporários;
6. lista de materiais, tags, cálculos e desenhos estiverem consistentes;
7. a inspeção visual estiver registrada, com eventuais correções reaplicadas;
8. o commit local correspondente deixar a árvore Git limpa.

## Escopo atual

Este README permanece como guia histórico. A série P01–P10 está concluída; uma nova
pasta somente deve ser criada mediante solicitação explícita e com a mesma cadeia de
geração, validação, inspeção visual e congelamento em Git.
