# Relatório final de auditoria — P23, P24 e P25

**Data da auditoria:** 2026-11-09

**Repositório:** `r-menegueli/portfolio-autocad-engenharia-eletrica`

**Branch atual:** `revisao/p23-p25` (a auditoria de 09/11/2026 foi registrada quando a branch ainda se chamava `codex/p23-p25-reengineering`).

**Base de comparação:** `origin/main` em `bec032760fc836d7a441f2efbd08a161bf3ccf3e`

**HEAD antes dos arquivos desta auditoria:** `bc923fffb620d46bf6e4bdcd58428748bf6de9d4`

## Conclusão executiva

A auditoria inicial encontrou reengenharia parcial e lacunas relevantes. Na continuação registrada abaixo, foram executados os caminhos estáticos MATLAB dos três projetos, a dinâmica Python P25 foi regenerada e investigada, e a prancha P25-05 foi redesenhada. A reengenharia integral continua **incompleta**; os resultados e limitações desta continuação substituem as afirmações anteriores sobre execução MATLAB, valores dinâmicos P25 e desenho P25-05.

Os modelos Simulink continuam sem execução bem-sucedida comprovada: uma tentativa P23 foi interrompida durante a construção do modelo por memória física baixa; o modelo P25 não foi iniciado; P24 não contém `.slx`. Os validadores finais e 36 testes Python passaram. `CONCLUÍDO E VALIDADO` refere-se somente ao escopo identificado e não significa conformidade normativa, segurança, dimensionamento profissional ou aptidão para construção.

## Atualização da continuação — 2026-11-09

**Nome atual da branch:** `revisao/p23-p25`, após renomeação em 10/11/2026. Esta atualização é a fotografia do conteúdo auditado e prevalece sobre as seções históricas abaixo quando houver divergência. As seções 1–8 foram escritas antes desta continuação, no estado publicado `475358b`; elas preservam o registro da auditoria inicial. O trabalho foi comparado com `main` (`bec032760fc836d7a441f2efbd08a161bf3ccf3e`) e permanece em branch separada. Não foi feito merge em `main`.

### Mudanças locais desta continuação

O inventário com cada caminho, status Git (`A`, `M` ou `D`) e escopo desta continuação está em [`docs/evidencias/inventario-continuidade-2026-11-09.csv`](docs/evidencias/inventario-continuidade-2026-11-09.csv): desde `475358b`, são 86 caminhos (23 criados, 63 alterados, 0 removidos). A comparação completa dos arquivos dos três projetos com `origin/main` está em [`docs/evidencias/inventario-arquivos-p23-p25.csv`](docs/evidencias/inventario-arquivos-p23-p25.csv). Não foram removidos arquivos dos projetos nesta continuação. Os cadernos PDF e o ZIP compilado foram gerados fora do repositório, em `outputs/`.

| Projeto | Mudanças de conteúdo nesta continuação | Desenhos/exportações | Removidos |
|---|---|---|---:|
| **P23** | Rotina MATLAB agora executa o caminho estático sem construir Simulink; leitor de parâmetros e teste MATLAB corrigidos; tabelas estáticas recalculadas; relatório técnico atualizado. | Nenhum DXF redesenhado nesta continuação. | 0 |
| **P24** | Leitor MATLAB de parâmetros corrigido; caminho estático e `test_project_24` executados; resumo e tabela mecânica recalculados; relatório técnico atualizado. | Nenhum DXF redesenhado nesta continuação. | 0 |
| **P25** | Caminho estático MATLAB/teste executados; dinâmica Python corrigida para separar eventos e avaliar sensibilidade; diagnóstico de potência negativa, testes, CSVs, memória de cálculo, resumo e relatório técnico atualizados. | P25-05 redesenhada; as dez folhas foram reexportadas; prévia de contato e cadernos derivados recriados. | 0 |
| **Comum** | Corrigida compatibilidade do renderizador com pypdf 7; adicionados medidor MATLAB e evidências de MATLAB, Simulink, recursos, testes, validadores e empacotamento. | Não se aplica. | 0 |

Nos desenhos, **P25-05 é a única nova alteração geométrica/material desta continuação**: passou a mostrar barramento trifásico, disjuntor de campo 41E, transformador TE1 e ponte BR1, circuito de campo e descarga KFD/RFD, medição PT/CT, AVR PI e limites, OEL/UEL, TCF/TEF, permissivos 52G/86G, trip 64F/41E e tabela ilustrativa de bornes. Fonte: [`25-usina-cogeracao-biomassa/fonte/05_sistema_excitacao_avr.dxf`](25-usina-cogeracao-biomassa/fonte/05_sistema_excitacao_avr.dxf); imagem inspecionada: [`25-usina-cogeracao-biomassa/exports/05_sistema_excitacao_avr.png`](25-usina-cogeracao-biomassa/exports/05_sistema_excitacao_avr.png). O teste CAD verifica rótulos, camadas, quantidade mínima de entidades e texto pesquisável no PDF. O AutoCAD Core Console 2027 também abriu e auditou esta DXF: exit code 0, zero erros, zero correções e zero objetos apagados. Os dez PDFs/PNGs/SVGs do P25 foram regenerados; as outras nove fontes DXF não tiveram redesenho nesta continuação. P23 e P24 também não tiveram DXFs redesenhados nesta continuação. A maioria das folhas ainda é conceitual/esquemática.

### MATLAB executado e resultados

MATLAB R2026a foi realmente iniciado e executou os caminhos estáticos e os respectivos testes. Os JSONs vinculados guardam comando batch, opções de inicialização, tempos, códigos de saída, RAM, stdout e stderr.

| Projeto | Execução/saída MATLAB observada | Duração; pico da árvore; RAM física livre mínima | Estado |
|---|---|---|---|
| **P23** | `run_analysis(false,false)` + `test_project_23`: 28,000000 MW; 24,273576 MVAr brutos; 7,570421 MVAr STATCOM; 123,308982 A no PCC; 5,262977 kA de curto; THDi sintético 0,244131 pu (24,4131%). O teste declarou verificados balanço, curto e harmônicos; dinâmica não executada. | 12,77 s; 1.206,8 MB; 1,206 GB. | Estático MATLAB **CONCLUÍDO E VALIDADO**. Evidência: [`matlab-p23-estatico.json`](docs/evidencias/matlab-p23-estatico.json). |
| **P24** | `run_analysis` + `test_project_24`: 9 casos elétricos, 900 mecânicos, 9 térmicos e 101 posições estruturais; Imax 650,797405 A; ampacidade mínima 892,044159 A; clearance sintético mínimo 12,678747 m. | 14,74 s; 1.126,1 MB; 0,486 GB. | Cálculos estáticos MATLAB **CONCLUÍDO E VALIDADO**. Evidência: [`matlab-p24-estatico.json`](docs/evidencias/matlab-p24-estatico.json). |
| **P25** | `run_analysis(false,false)` + `test_project_25`: P líquido 22,800000 MW; S gerador 27,777778 MVA; fp POI 0,955459; Iop 1.162,138 A versus 1.338,783 A nominais; curtos equivalentes 13,713664 kA em 13,8 kV e 21,441324 kA em 138 kV; combustível 104,166667 MW; rendimento útil agregado 0,528; energia líquida 164.160 MWh/ano. Dinâmica não executada nessa chamada. | 11,97 s; 1.213,3 MB; 1,058 GB. | Estático MATLAB **CONCLUÍDO E VALIDADO**. Evidência: [`matlab-p25-estatico.json`](docs/evidencias/matlab-p25-estatico.json). |

P23 e P25 usaram `-nojvm -singleCompThread`; P24 executou com as opções padrão registradas. O script [`scripts/medir_execucao_matlab.ps1`](scripts/medir_execucao_matlab.ps1) registrou consumo e interrompeu as tentativas de risco. A estática passou, mas não foram executadas as rotinas dinâmicas MATLAB nem os modelos Simulink. O teste MATLAB comprova apenas os checks codificados para estes dados e pressupostos.

### Simulink e recursos

| Projeto | Arquivo | Abriu | Compilou | Simulou | Resultado verificável |
|---|---|---|---|---|---|
| **P23** | `23-complexo-siderurgico-eaf/simulink/modelo_eaf_dinamico.slx` existe e seu blob local continua igual ao de `origin/main`. | Não confirmado | Não | Não | Três tentativas monitoradas pararam dentro de `build_model`; a última registrou apenas `P23_STAGE_BUILD_MODEL_BEGIN`, 31,92 s, pico de árvore de 2.451,2 MB e mínimo de 0,17 GB livre. Não se produziu resultado de simulação. Evidências: [`matlab-p23-simulink.json`](docs/evidencias/matlab-p23-simulink.json), [`matlab-p23-simulink-nojvm.json`](docs/evidencias/matlab-p23-simulink-nojvm.json) e [`matlab-p23-simulink-tentativa2.json`](docs/evidencias/matlab-p23-simulink-tentativa2.json). |
| **P24** | Não existe `.slx` no projeto. | Não se aplica | Não se aplica | Não se aplica | Dinâmica Simulink **NÃO EXECUTADO**. |
| **P25** | `25-usina-cogeracao-biomassa/simulink/modelo_cogeracao_dinamico.slx` existe e seu blob local continua igual a `origin/main`. | Não | Não | Não | A tentativa P25 não foi iniciada. A medição de 21:20 encontrou 1,93 GB livres; ficou abaixo do pico de 2,45 GB já medido para construir P23. Evidência do estado do sistema: [`diagnostico-recursos-memoria-2026-11-09.json`](docs/evidencias/diagnostico-recursos-memoria-2026-11-09.json). |

As tentativas de dinâmica P23 foram interrompidas durante a construção e não produziram uma simulação concluída. P24 não contém modelo `.slx` e P25 não foi iniciado. **Nenhum resultado MATLAB/Simulink dinâmico está apresentado como sucesso.**

### Dinâmica Python P25 — resultado e limite

A alternativa reduzida foi executada novamente em oito cenários e 8.008 amostras. O integrador RK4 agora divide os intervalos nos instantes de mudança da tensão e da referência; os testes incluem essa descontinuidade, convergência de um degrau suave e conservação do sinal quando a potência ativa muda de sentido. Não foi invertido nem cortado o valor negativo.

No afundamento sintético de 0,2 pu por 0,12 s, com passo de 5 ms e horizonte de 5 s, o cálculo termina em −6,291 MW, atinge −21,242 MW e +72,827 MW, e calcula pico de corrente de 5.578,3 A. A sensibilidade do valor final entre passo 5 ms e 0,625 ms é −6,291 a −4,864 MW; diferenças entre passos adjacentes não são monotônicas por causa dos limitadores rígidos do modelo. A interpretação assinada é reversão transitória dentro do modelo quando o ângulo cruza zero. Os picos excedem as bases assumidas e não existem limite de corrente, rede detalhada, proteção ou dinâmica de carga; portanto a curva **não valida** estabilidade, suportabilidade, desempenho de máquina comercial ou ajuste de proteção. Evidências: [`diagnostico-potencia-negativa-python.json`](25-usina-cogeracao-biomassa/resultados/relatorios/diagnostico-potencia-negativa-python.json), [memória de resultados](25-usina-cogeracao-biomassa/resultados/relatorios/diagnostico-potencia-negativa-python.md) e [`resultados-python-p23-p25.json`](docs/evidencias/resultados-python-p23-p25.json).

### Validação final desta continuação

| Comando | Resultado observado | Evidência |
|---|---|---|
| `python -m pytest -v tests 23-complexo-siderurgico-eaf/validacao 24-linha-transmissao-138kv/validacao 25-usina-cogeracao-biomassa/validacao` | **36 passed in 46.05s**, código de saída 0. | [`testes-python-final-p23-p25.txt`](docs/evidencias/testes-python-final-p23-p25.txt) |
| `python scripts/validar_estudos_p23_p25.py --project all` | **aprovado**, erros 0, avisos 0; leitura estrutural DXF/PDF/PNG das 30 folhas. | [`validacao-estudos-p23-p25-2026-11-09.txt`](docs/evidencias/validacao-estudos-p23-p25-2026-11-09.txt) |
| `python scripts/validar_portfolio.py --root . --strict --format human --report docs/evidencias/validacao-portfolio-strict-2026-11-09.json` | **PASS**, 655.982 verificações, 0 erros, 0 avisos. | [`validacao-portfolio-strict-2026-11-09.txt`](docs/evidencias/validacao-portfolio-strict-2026-11-09.txt), [JSON](docs/evidencias/validacao-portfolio-strict-2026-11-09.json) |
| `python scripts/engineering_studies.py --root . --project p25` | **10 DXFs gerados e renderizados**, incluindo o P25-05 revisado. | [`regeneracao-prancha-p25-05.txt`](docs/evidencias/regeneracao-prancha-p25-05.txt) |
| `accoreconsole.exe /i 25-usina-cogeracao-biomassa/fonte/05_sistema_excitacao_avr.dxf /s scripts/autocad/auditar.scr` | AutoCAD Core Console 2027, exit code 0; **0 erros, 0 corrigidos, 0 apagados**. | [Resumo](docs/evidencias/auditoria-autocad-p25-05-2026-11-09.txt), [log integral](docs/evidencias/auditoria-autocad-p25-05-2026-11-09.log) |
| `python scripts/empacotar_pranchas_p23_p25.py` | Gerou prévias e cadernos P23/P24/P25 e ZIP-fonte dos desenhos. | [`empacotamento-pranchas-p23-p25-2026-11-09.txt`](docs/evidencias/empacotamento-pranchas-p23-p25-2026-11-09.txt) |

As classificações atuais por projeto são:

| Projeto/escopo | Estado | Evidência principal e limite |
|---|---|---|
| **P23 — cálculos estáticos MATLAB** | CONCLUÍDO E VALIDADO | MATLAB R2026a e teste do projeto passaram; pressupostos de carga, rede e harmônicos permanecem sintéticos. |
| **P23 — desenhos** | CONCLUÍDO COM RESTRIÇÕES | Estado anterior registra P23-06/07 com alterações parciais; nenhuma prancha P23 foi redesenhada nesta continuação e plantas/equipamentos continuam conceituais. |
| **P23 — Simulink/dinâmica MATLAB** | INCOMPLETO | Tentativa medida parou durante `build_model`; sem abertura/compilação/simulação concluída. |
| **P24 — cálculos estáticos MATLAB** | CONCLUÍDO E VALIDADO | Checks elétricos, mecânicos, térmicos e estruturais passaram; rota, clima e condutor são sintéticos. |
| **P24 — desenhos** | CONCLUÍDO COM RESTRIÇÕES | P24-02 já havia sido redesenhada; nenhum novo DXF foi alterado nesta continuação e o conjunto ainda não é executivo. |
| **P24 — Simulink** | NÃO EXECUTADO | O projeto não contém modelo `.slx`. |
| **P25 — cálculo estático MATLAB** | CONCLUÍDO E VALIDADO | Testes e balanços estáticos passaram; dados de máquina/rede não são dados de placa confirmados. |
| **P25 — dinâmica Python** | CONCLUÍDO COM RESTRIÇÕES | 8 cenários/8.008 amostras; sensibilidade temporal e picos acima da base tornam a resposta inadequada para concluir estabilidade ou suportabilidade. |
| **P25 — desenhos** | CONCLUÍDO COM RESTRIÇÕES | P25-05 ganhou detalhe funcional verificável; os demais desenhos continuam em grande parte genéricos/esquemáticos. |
| **P25 — Simulink** | NÃO EXECUTADO | Arquivo existe, mas não foi aberto, compilado nem simulado. |
| **P23, P24 e P25 — prontidão de engenharia executiva** | INCOMPLETO | Faltam dados de fabricante e campo, coordenação/estudos normativos e revisão profissional independente. |

### Comparação e publicação

Desde o estado `475358b`, houve três melhorias verificáveis: (1) execução real dos caminhos estáticos MATLAB e testes específicos de P23/P24/P25, com JSON de consumo e saída; (2) regeneração da dinâmica Python P25 com integração nos eventos e apresentação explícita da sensibilidade, sem camuflar a potência negativa; (3) redesenho funcional da P25-05, com inspeção visual e testes DXF/PDF. Também foi corrigida a ordem de associação/mesclagem de páginas do renderizador para pypdf 7 e foram atualizadas as prévias/cadernos. A comparação geométrica e os registros técnicos anteriores permanecem úteis como histórico; estes passos não completam a reengenharia das 30 folhas.

As alterações desta continuação permanecem na branch atual `revisao/p23-p25`, cujo nome anterior era `codex/p23-p25-reengineering`; os commits anteriores estão preservados. `main` continua sem merge. A revisão não declara conformidade normativa nem liberação para construção/instalação.

## Registro histórico da auditoria inicial

As seções a seguir preservam métodos, comparações e evidências da auditoria anterior. Para o estado atual de MATLAB, P25-05, dinâmica P25, quantidade de testes, validadores e inventário desta continuação, use as tabelas acima.

## 1. Base, método e estado do Git

O repositório local estava na branch de revisão publicada, no mesmo commit que `origin/codex/p23-p25-reengineering`. Antes desta auditoria, essa branch continha dois commits à frente de `origin/main`: `3051c47` (*Reengineer P23-P25 portfolio studies*) e `bc923ff` (*Add P23-P25 dynamic evidence and previews*). A branch principal remota permanecia no commit-base `bec0327`.

Foram comparados os 30 DXFs entre `origin/main` e o estado atual. A comparação de entidades separa geometria, conteúdo textual e estilo; ela localiza mudanças, mas não avalia por si só se o desenho representa corretamente uma instalação. As folhas de maior alteração também foram confrontadas visualmente com as exportações da base. O detalhamento completo por arquivo e folha está nos CSVs de evidência abaixo.

O repositório não apresenta remoções nos três projetos. O diff de projeto contra `origin/main` contém:

| Projeto | Criados | Alterados | Removidos | Total |
|---|---:|---:|---:|---:|
| P23 | 10 | 47 | 0 | 57 |
| P24 | 11 | 56 | 0 | 67 |
| P25 | 16 | 51 | 0 | 67 |

O inventário linha a linha, com o status Git (`A`, `M` ou `D`) e o caminho completo dentro do repositório, está em [`docs/evidencias/inventario-arquivos-p23-p25.csv`](docs/evidencias/inventario-arquivos-p23-p25.csv). Inclui as dez fontes DXF e os 30 derivados PDF/PNG/SVG de cada projeto.

### Principais arquivos por projeto

- **P23 — 10 criados:** `dados/origem-parametros.csv`, `pranchas-preview.png`, `resultados/graficos/resposta-cenarios-python.png`, duas tabelas de cenários Python e os scripts/testes independentes em `validacao/`. Entre os alterados estão as 10 fontes em `fonte/`, 30 exportações em `exports/`, `matlab/calculos/run_analysis.m`, `memoria-calculo.md`, README e tabelas estáticas.
- **P24 — 11 criados:** `dados/origem-parametros.csv`, prévia, seis gráficos de triagem, `validacao/plotar_resultados_p24.py`, `validacao/test_resultados_p24.py` e o relatório técnico. Entre os alterados estão as dez pranchas e exportações, `matlab/calculos/run_analysis.m`, `matlab/testes/test_project_24.m`, parâmetros, memoriais e tabelas de resultados. Nesta auditoria, o texto final do `README.md` também foi ajustado para conter literalmente o aviso obrigatório do repositório.
- **P25 — 16 criados:** rastreabilidade dos parâmetros, prévia, gráficos e tabelas dos cenários Python, scripts de cálculos independentes e dinâmicos e seus testes, mais o diagnóstico de potência negativa (Python, JSON e Markdown) e o teste da prancha P25-05. Foram alterados os dez DXFs e derivados, scripts MATLAB, memoriais e tabelas de potência, energia e curto-circuito.

Além das pastas dos projetos, a branch-base alterou arquivos compartilhados como `portfolio.toml`, `scripts/engineering_studies.py`, `scripts/renderizar.py`, `scripts/validar_estudos_p23_p25.py`, `renders/manifesto.json`, `README.md`, `docs/galeria-visual.md`, `relatorio-ferramentas.md` e `relatorio-validacao.md`, e criou `scripts/empacotar_pranchas_p23_p25.py` e `docs/auditoria-reengenharia-p23-p25.md`. Os CSVs desta auditoria e este relatório são novas evidências adicionadas agora.

## 2. Desenhos AutoCAD: mudança real por prancha

“Geometria principal igual” significa que a comparação não encontrou mudança geométrica relevante nas entidades do modelo; as alterações se concentram em texto, revisão, paleta ou apresentação. “Ajuste geométrico” indica mudança localizada, não redesenho integral.

| Projeto | Redesenho substantivo | Ajuste geométrico/composição | Geometria praticamente igual |
|---|---|---|---|
| **P23** | Nenhum | **P23-06** reorganiza símbolos/tabela de proteção; **P23-07** reorganiza blocos e tabela de compensação e corrige o alvo de STATCOM para cerca de 7,57 MVAr | P23-01 a P23-05, P23-08 a P23-10 |
| **P24** | **P24-02**: perfil longitudinal substituído por perfil sintético com 101 posições de estrutura e envelopes de flecha | **P24-03** atualiza curvas/envelopes; **P24-04 e P24-05** têm mudanças pontuais de geometria/rotulagem; **P24-07** revê a representação do feixe e cotas | P24-01, P24-06, P24-08, P24-09, P24-10 |
| **P25** | **P25-02**: fluxograma anterior substituído por implantação conceitual cotada de 100 × 65 m, inserida em bloco 1:500; **P25-05**: diagrama de excitação com potência, medição, AVR/limites, permissivos, trip e borneamento | **P25-08** reposiciona zonas/tabela para eliminar colisão; **P25-10** interrompe trechos da malha nas envolventes e separa a tabela | P25-01, P25-03, P25-04, P25-06, P25-07, P25-09 |

As 30 classificações, quantidades de entidades da base e do estado atual e contagens de diferenças geométricas/textuais/de estilo estão em [`docs/evidencias/comparativo-pranchas-p23-p25.csv`](docs/evidencias/comparativo-pranchas-p23-p25.csv). Os pontos visuais principais foram comparados lado a lado com a base.

Prévias de contato das dez folhas atuais: [P23](23-complexo-siderurgico-eaf/pranchas-preview.png), [P24](24-linha-transmissao-138kv/pranchas-preview.png) e [P25](25-usina-cogeracao-biomassa/pranchas-preview.png). Os DXFs editáveis e os PDFs individuais estão nas pastas `fonte/` e `exports/` de cada projeto.

### O que mudou e o que continua esquemático

- **P23-06:** o símbolo do transformador saiu da área da tabela. A prancha ainda não contém secundários completos de TC/TP, matriz de trip/86/52, ajustes ou coordenação.
- **P23-07:** o valor antigo de compensação de 15,06 MVAr foi substituído pelo cálculo atual de aproximadamente 7,57 MVAr para as hipóteses cadastradas. Isso corrige uma inconsistência interna; não valida desempenho dinâmico, curva Q–V ou dimensionamento do STATCOM.
- **P23-01 a 05 e 08 a 10:** houve principalmente atualização de texto, revisão e estilo. As plantas são conceituais, o circuito secundário é uma referência de 1,0 kV com taps hipotéticos de 0,8–1,2 kV, os filtros não têm sintonia/varredura de impedância e aterramento/proteção continuam sem dimensionamento completo.
- **P24-02:** a nova prancha acrescenta terreno e perfil calculado, mas os dados de rota e elevação são sintéticos; a escala vertical tem exagero de 100×. P24-03/04/05/07 receberam alterações parciais. Traçado, torres, cadeias, fundações, interfaces e aterramento permanecem representações de estudo, sem corredor/topografia, cargas estruturais, dados confirmados de fabricante ou solo.
- **P25-02:** agora é uma implantação conceitual, não apenas um fluxograma. As dimensões dos prédios e equipamentos são envelopes assumidos, sem levantamento civil nem catálogo. P25-08 e P25-10 corrigem apresentação; a proteção ainda não tem circuitos secundários/coordenação e a malha não tem estudo de solo, GPR ou tensões de toque/passo.
- **P25-01, 03–07 e 09:** a representação é majoritariamente unifilar ou em blocos. Gerador, turbina, AVR, governador, sincronismo e serviços auxiliares ainda usam agrupamentos genéricos, sem todos os terminais, limites, curvas, sinais, lista de cargas e dados de fabricante.

As pranchas foram regeneradas como DXF e derivados. A evidência AutoCAD já versionada registra Core Console com saída zero e `AUDIT` sem erros/reparos em 30/30 arquivos. **Esse registro não é uma nova execução desta auditoria**; não houve alteração de DXF durante esta auditoria. O validador estrutural atual reabriu os 30 conjuntos DXF/PDF/SVG/PNG. Não foi feita conferência de plotter nem nova abertura no AutoCAD GUI.

## 3. MATLAB, cálculos executados e resultados

Os arquivos `.m` e os testes MATLAB existem, mas não foram executados nesta auditoria. O código-fonte não comprova resultado. Os números abaixo são os cálculos Python independentes efetivamente executados e os testes que passaram; não são resultados MATLAB.

| Projeto | Código MATLAB existente | Cálculo executado nesta auditoria e resultado | Testes atuais |
|---|---|---|---|
| **P23** | `matlab/calculos/run_analysis.m`, `matlab/calculos/build_model.m`, `matlab/funcoes/read_project_parameters.m`, `matlab/testes/test_project_23.m` | `validacao/calculos_independentes_p23.py` recalculou balanço, corrente, curto e THDi; resultado: 28,0 MW, 24,274 MVAr brutos, 7,570 MVAr STATCOM, 123,309 A no PCC de 138 kV, 493,236 A na barra de 34,5 kV, 5,26298 kA de curto e THDi sintético de 24,413%. A alternativa dinâmica Python executou 8 cenários/4.008 amostras; a resposta nominal calculada ficou em 0,968 pu com STATCOM e 0,944 pu sem ele. | 7 testes Python passaram; 3 verificam cálculos estáticos e 4 exercitam a alternativa dinâmica Python. Os testes MATLAB não foram executados. |
| **P24** | `matlab/calculos/run_analysis.m`, `matlab/testes/test_project_24.m` | O teste Python independente recalculou e conferiu 9 casos elétricos, 900 estados mecânicos, 9 casos térmicos e 101 posições de estrutura. Para 140 MW/fp 0,90: 650,797 A; ampacidade mínima estimada do feixe: 892,044 A; margem simplificada mínima: 27,044%; flecha vertical máxima: 9,046 m; lateral máxima: 6,546 m; clearance vertical sintético mínimo: 12,679 m; tração máxima no apoio: 32,758 kN. | 4 testes Python passaram. Eles conferem as tabelas contra cálculo independente, incluindo modelo nominal π, flecha/tração/clearance e balanço térmico. Os testes MATLAB não foram executados. |
| **P25** | `matlab/calculos/run_analysis.m`, `matlab/calculos/build_model.m`, `matlab/funcoes/read_project_parameters.m`, `matlab/testes/test_project_25.m` | `validacao/calculos_independentes_p25.py` recalculou balanços, corrente e curto. Resultado: 25,0 MW brutos, 22,8 MW líquidos, 27,778 MVA na operação do gerador, 1.162,14 A de operação contra 1.338,78 A nominais, fp no POI 0,95546, curto transitório de triagem 13,714 kA em 13,8 kV e 21,441 kA em 138 kV. A alternativa dinâmica Python executou 8 cenários/8.008 amostras. No afundamento sintético de 0,2 pu por 0,12 s, o pico calculado foi 5.536,94 A; ao fim de 5 s a potência ativa calculada era −6,935 MW. O resultado não é uma prova de suportabilidade ou estabilidade. | 10 testes Python passaram: 4 estáticos, 2 de implantação CAD e 4 da alternativa dinâmica. Os testes MATLAB não foram executados. |

O JSON [`docs/evidencias/resultados-python-p23-p25.json`](docs/evidencias/resultados-python-p23-p25.json) preserva os resultados completos recalculados nesta auditoria. Limitações principais: P23 usa espectro harmônico sintético, não tem rede por frequência nem cálculo final de filtros/proteção/terra; P24 usa rota/clima e equivalência do condutor hipotéticos, térmica simplificada (não validada como implementação IEEE 738) e clearance sem blowout lateral; P25 usa dados de máquina/rede assumidos e X′d, sem X″d, componente CC, sequência completa, limites de fabricante, cargas locais ou curva P–Q validada. Os três permanecem estudos conceituais.

## 4. Simulink: arquivos e evidência de execução

| Projeto | Arquivo `.slx` | Abriu? | Compilou? | Simulou com sucesso? | Conclusão baseada em evidência |
|---|---|---|---|---|---|
| **P23** | `23-complexo-siderurgico-eaf/simulink/modelo_eaf_dinamico.slx` existe. O blob Git é igual ao de `origin/main`; a branch de reengenharia não alterou o modelo. | Não confirmado | Não confirmado | Não confirmado | Nenhum log durável de abertura, atualização/compilação ou `sim` com resultado foi localizado. Há um `.slxc` local ignorado pelo Git, que não prova simulação bem-sucedida. |
| **P24** | Não existe `.slx` no projeto | Não executado | Não executado | Não executado | O projeto tem rotina MATLAB de cálculo de linha e testes, mas não modelo Simulink. |
| **P25** | `25-usina-cogeracao-biomassa/simulink/modelo_cogeracao_dinamico.slx` existe. O blob Git é igual ao de `origin/main`; a branch de reengenharia não alterou o modelo. | Não confirmado | Não confirmado | Não confirmado | Nenhum log durável de abertura, atualização/compilação ou `sim` com resultado foi localizado. Há um `.slxc` local ignorado pelo Git, que não prova simulação bem-sucedida. |

**Declaração expressa:** nenhum modelo MATLAB/Simulink foi executado nesta auditoria. Não foi possível confirmar que os modelos P23 ou P25 tenham sido realmente executados com sucesso em uma execução anterior; portanto, não declaro qualquer resultado de Simulink como válido. A documentação global antiga contém uma linha “PASS” para Simulink, mas não fornece logs, saídas ou artefatos de simulação reproduzíveis. Os relatórios técnicos atuais dos projetos dizem que as versões MATLAB/Simulink não foram reexecutadas. O P24 não tem modelo `.slx`.

O MATLAB R2026a está instalado e a licença Simulink foi anteriormente consultada, mas no momento da auditoria havia cerca de **0,49 GB de RAM livre** em 7,8 GB visíveis. Para não provocar encerramento por falta de memória nem modificar os modelos/saídas, a auditoria não iniciou MATLAB. A licença `Simscape Electrical` não estava disponível na consulta histórica; isso não afeta a classificação porque os modelos encontrados usam blocos genéricos, mas limita qualquer alegação de modelo eletromagnético físico.

Hashes SHA-256, blobs Git e estados de abertura/compilação/simulação estão em [`docs/evidencias/estado-modelos-simulink-p23-p25.csv`](docs/evidencias/estado-modelos-simulink-p23-p25.csv).

## 5. Tabelas de conformidade

### P23 — Complexo siderúrgico EAF

| Escopo | Estado | Evidência e limite |
|---|---|---|
| Integridade estrutural de DXF/PDF/SVG/PNG | CONCLUÍDO E VALIDADO | Validador estrito global: 0 erros/avisos; validador focado: 30 folhas válidas. Isso não valida conteúdo de engenharia. |
| Pacote de desenhos e alterações pedidas | CONCLUÍDO COM RESTRIÇÕES | 10 folhas regeneradas; só P23-06/07 mudaram geometria de modo relevante; 8 mantiveram geometria praticamente igual; sem GUI/plotter nesta auditoria. |
| Cálculos e dinâmica Python independentes | CONCLUÍDO COM RESTRIÇÕES | 7 testes passaram e os cálculos foram executados; dados de arco/rede e premissas de equipamentos são sintéticos. |
| Scripts MATLAB e testes MATLAB | NÃO VERIFICADO | Fontes existem; nenhuma execução atual/log confiável confirmado. |
| Simulink | NÃO VERIFICADO | `.slx` existe, mas abertura, compilação e simulação com sucesso não foram comprovadas. |
| Dimensionamento, coordenação e prontidão executiva | INCOMPLETO | Faltam dados de fabricante/rede, filtros, proteção, aterramento e desenho físico validado. |

### P24 — Linha de transmissão 138 kV

| Escopo | Estado | Evidência e limite |
|---|---|---|
| Integridade estrutural de DXF/PDF/SVG/PNG | CONCLUÍDO E VALIDADO | Validador estrito global: 0 erros/avisos; validador focado: 10 folhas válidas. |
| Pacote de desenhos e alterações pedidas | CONCLUÍDO COM RESTRIÇÕES | P24-02 redesenhada substantivamente e quatro folhas tiveram revisão geométrica parcial; cinco permaneceram praticamente iguais. Perfil e corredor são sintéticos. |
| Cálculos e verificações Python independentes | CONCLUÍDO COM RESTRIÇÕES | 4 testes passaram; resultados de fluxo, flecha e térmica conferidos contra equações independentes simplificadas. |
| Scripts/testes MATLAB | NÃO VERIFICADO | Fontes existem; a documentação registra execução anterior parcial com falha na exportação gráfica, e a versão atual não foi executada integralmente nesta auditoria. |
| Simulink | NÃO EXECUTADO | Não existe modelo `.slx` no projeto. |
| Dimensionamento e liberação da linha | INCOMPLETO | Faltam rota/topografia reais, validação do condutor/clima, curto, isolamento, estruturas, fundações e aterramento. |

### P25 — Cogeração a biomassa

| Escopo | Estado | Evidência e limite |
|---|---|---|
| Integridade estrutural de DXF/PDF/SVG/PNG | CONCLUÍDO E VALIDADO | Validador estrito global: 0 erros/avisos; validador focado: 10 folhas válidas. |
| Pacote de desenhos e alterações pedidas | CONCLUÍDO COM RESTRIÇÕES | P25-02 redesenhada substantivamente; P25-08/10 ajustadas; sete folhas mantiveram geometria praticamente igual. Implantação é conceitual. |
| Cálculos e dinâmica Python independentes | CONCLUÍDO COM RESTRIÇÕES | 10 testes passaram. O cenário de afundamento termina com potência negativa e não serve para concluir suportabilidade. |
| Scripts/testes MATLAB | NÃO VERIFICADO | Fontes existem; nenhuma execução atual/log confiável confirmado. |
| Simulink | NÃO VERIFICADO | `.slx` existe, mas abertura, compilação e simulação com sucesso não foram comprovadas. |
| Capacidade, proteção, estabilidade e prontidão executiva | INCOMPLETO | Faltam dados de fabricante, rede, cargas auxiliares detalhadas, modelo dinâmico validado, coordenação e estudo de terra. |

## 6. Comparação: melhorias reais e pendências

Em relação a `origin/main`, há melhorias verificáveis: parâmetros com origem/limitação documentadas em P23/P24/P25; tabelas estáticas P23/P25 recalculáveis de forma independente em Python; cálculos de linha/estrutura/térmica P24 conferidos independentemente; modelos reduzidos dinâmicos Python em P23/P25; atualização de resultados e memoriais; correções localizadas de composição; texto pesquisável nos PDFs; novas prévias de contato e empacotamento das pranchas. A escala 1:500 de P25-02 agora corresponde ao bloco inserido, mas os envelopes físicos continuam assumidos.

O progresso é parcial. A maioria das pranchas não teve redesenho geométrico; equipamentos e controles seguem genéricos em vários diagramas; não há comprovação de MATLAB/Simulink; e dados críticos de campo/fabricante/rede continuam ausentes. P01–P22 não aparecem no diff desta branch.

## 7. Validação executada e logs

Os comandos e saídas são preservados em [`docs/evidencias/testes-auditoria-p23-p25.txt`](docs/evidencias/testes-auditoria-p23-p25.txt) e [`docs/evidencias/validacao-estrita-portfolio-p23-p25.txt`](docs/evidencias/validacao-estrita-portfolio-p23-p25.txt).

| Comando/checagem | Resultado final |
|---|---|
| `python -m pytest -q tests` | **11 passed** depois da correção literal do aviso obrigatório em `24-linha-transmissao-138kv/README.md`. A primeira execução apontou exatamente `NOTICE_MISSING`; a correção foi incluída antes da publicação do relatório. |
| `python -m pytest -q 23-complexo-siderurgico-eaf/validacao` | **7 passed** |
| `python -m pytest -q 24-linha-transmissao-138kv/validacao` | **4 passed** |
| `python -m pytest -q 25-usina-cogeracao-biomassa/validacao` | **10 passed** |
| `python scripts/validar_estudos_p23_p25.py --project all` | **PASS**, sem erros nem avisos nas 30 pranchas/derivados; é validação estrutural, não cálculo normativo. |
| `python scripts/validar_portfolio.py --root . --strict` | **PASS**, 651.139 verificações, 0 erros e 0 avisos. |
| Evidência AutoCAD Core Console por DXF | CSV versionado registra **30/30** com código 0 e auditoria sem erros/reparos; não foi repetido nesta auditoria porque nenhum DXF foi alterado durante ela. |
| MATLAB/Simulink | **Não executado nesta auditoria**; sem confirmação de sucesso anterior. |

O `pytest` geral ainda emite seis `DeprecationWarning` internos do `ezdxf` ao usar NumPy 2.5.2; não alteraram o resultado. Os testes verificam código Python, tabelas e integridade, não certificação de norma, equipamento ou instalação.

## 8. Publicação no GitHub

O trabalho auditado foi publicado sob o nome `codex/p23-p25-reengineering`, depois renomeado para `revisao/p23-p25`, sem integração em `main`. O relatório e as evidências permanecem na mesma branch. `main` não recebeu merge porque o escopo continua incompleto e os modelos MATLAB/Simulink não têm execução bem-sucedida comprovada.

## Evidências vinculadas

- [Inventário completo de arquivos P23–P25](docs/evidencias/inventario-arquivos-p23-p25.csv)
- [Comparação das 30 pranchas](docs/evidencias/comparativo-pranchas-p23-p25.csv)
- [Estado e hashes dos modelos Simulink](docs/evidencias/estado-modelos-simulink-p23-p25.csv)
- [Resultados de cálculos Python executados](docs/evidencias/resultados-python-p23-p25.json)
- [Testes e validação estrutural](docs/evidencias/testes-auditoria-p23-p25.txt)
- [Validador estrito global](docs/evidencias/validacao-estrita-portfolio-p23-p25.txt)
- [Auditoria AutoCAD Core Console por prancha](docs/evidencias/auditoria-autocad-p23-p25.csv)
- [Relatório técnico P23](23-complexo-siderurgico-eaf/validacao/relatorio-validacao-tecnica.json)
- [Relatório técnico P24](24-linha-transmissao-138kv/validacao/relatorio-validacao-tecnica.json)
- [Relatório técnico P25](25-usina-cogeracao-biomassa/validacao/relatorio-validacao-tecnica.json)
