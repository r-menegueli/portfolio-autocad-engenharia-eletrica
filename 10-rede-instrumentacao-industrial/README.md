# Projeto 10 — Rede acadêmica de instrumentação industrial

**Código:** P10  
**Autor:** Rogério Eduardo Moreira Menegueli  
**Estado:** revisão acadêmica 03; respostas de processo e diagnósticos finais pendentes
**Data:** 2026-11-05
**Revisão:** 03 (matriz de escala analógica)
**Folha:** A3 paisagem  
**Unidades:** milímetros nos desenhos; grandezas de processo indicadas por instrumento

Este projeto fecha a série acadêmica do portfólio com uma rede original e fictícia de
instrumentação industrial. A arquitetura integra quatro transmissores 4–20 mA, duas
entradas digitais, duas remotas, CLP, switch, SCADA e distribuição 24 Vcc. O DXF
AC1027 é a fonte principal; PDF, SVG e PNG são derivados de visualização da mesma
revisão. A revisão 02 acrescenta uma matriz conceitual para falhas de valor analógico,
remotas, supervisão, comunicação sem atualização, alimentação 24 Vcc e entradas
digitais. A revisão 03 detalha cinco pontos de escala em cada transmissor analógico,
sem apresentar valores calculados como calibração ou resultado de bancada.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Entregáveis

| Prancha | Fonte DXF | Visualizações | Conteúdo |
| ---: | --- | --- | --- |
| 01/08 | [arquitetura da rede](fonte/01_arquitetura_rede.dxf) | [PDF](exports/01_arquitetura_rede.pdf), [SVG](exports/01_arquitetura_rede.svg), [PNG](exports/01_arquitetura_rede.png) | SCADA, switch, PLC, remotas, instrumentos e 24 Vcc |
| 02/08 | [diagrama de instrumentação](fonte/02_diagrama_instrumentacao.dxf) | [PDF](exports/02_diagrama_instrumentacao.pdf), [SVG](exports/02_diagrama_instrumentacao.svg), [PNG](exports/02_diagrama_instrumentacao.png) | malhas TT, PT, FT, LT e entradas LSH/PSL |
| 03/08 | [diagrama de interligação](fonte/03_diagrama_interligacao.dxf) | [PDF](exports/03_diagrama_interligacao.pdf), [SVG](exports/03_diagrama_interligacao.svg), [PNG](exports/03_diagrama_interligacao.png) | cabos, bornes, canais, shield e PE |
| 04/08 | [topologia de comunicação](fonte/04_topologia_comunicacao.dxf) | [PDF](exports/04_topologia_comunicacao.pdf), [SVG](exports/04_topologia_comunicacao.svg), [PNG](exports/04_topologia_comunicacao.png) | Ethernet industrial acadêmica em estrela |
| 05/08 | [painel de instrumentação](fonte/05_painel_instrumentacao.dxf) | [PDF](exports/05_painel_instrumentacao.pdf), [SVG](exports/05_painel_instrumentacao.svg), [PNG](exports/05_painel_instrumentacao.png) | layout conceitual de PI-101 |
| 06/08 | [lista de instrumentos](fonte/06_lista_instrumentos.dxf) | [PDF](exports/06_lista_instrumentos.pdf), [SVG](exports/06_lista_instrumentos.svg), [PNG](exports/06_lista_instrumentos.png) | tags, faixas, sinais, canais e escalas |
| 07/08 | [matriz causa–efeito de sinais](fonte/07_matriz_causa_efeito_sinais.dxf) | [PDF](exports/07_matriz_causa_efeito_sinais.pdf), [SVG](exports/07_matriz_causa_efeito_sinais.svg), [PNG](exports/07_matriz_causa_efeito_sinais.png) | qualidade analógica, perda de remotas, SCADA, dados obsoletos, 24 Vcc e DI |
| 08/08 | [matriz de escala analógica](fonte/08_matriz_escala_analogica.dxf) | [PDF](exports/08_matriz_escala_analogica.pdf), [SVG](exports/08_matriz_escala_analogica.svg), [PNG](exports/08_matriz_escala_analogica.png) | quatro faixas com cinco pontos calculados em unidades de engenharia |

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Filosofia e separação dos sinais](filosofia-sinais.md)
- [Referências normativas](referencias-normativas.md)
- [Inspeção visual](inspecao-visual.md)
- [Parâmetros](parametros.csv), [matriz causa–efeito](causa-efeito.csv)
- [Instrumentos](lista-instrumentos.csv), [I/O](lista-io.csv), [cabos](lista-cabos.csv), [bornes](lista-bornes.csv), [rede](lista-redes.csv), [alimentação](lista-alimentacao.csv), [materiais](lista-materiais.csv) e [resultados](resultados-calculo.csv)
- [Relatório específico](validacao-instrumentacao.json) e [relatório integrado](validacao.json)

## Quatro naturezas de conexão

1. **Alimentação:** entrega energia em 24 Vcc aos equipamentos; é dimensionada por
   tensão, corrente, proteção e queda de tensão.
2. **Sinal analógico:** representa uma variável contínua por 4–20 mA. Nos transmissores
   de dois fios desta premissa, o mesmo par fecha a alimentação da malha e conduz a
   corrente medida, mas sua função informacional continua distinta da distribuição
   geral de 24 Vcc.
3. **Sinal digital:** representa somente estados discretos 0/1 em entradas 24 Vcc.
4. **Comunicação:** troca quadros digitais entre nós endereçados na rede Ethernet; não
   equivale a uma entrada discreta nem a uma malha de corrente.

## Reproduzir

Execute na raiz do repositório, com o ambiente virtual já instalado:

```powershell
.venv\Scripts\python.exe 10-rede-instrumentacao-industrial\fonte\gerar_projeto_10.py --root .
.venv\Scripts\python.exe 10-rede-instrumentacao-industrial\fonte\renderizar_projeto_10.py --root .
.venv\Scripts\python.exe 10-rede-instrumentacao-industrial\fonte\validar_projeto_10.py --root .
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict
```

O AutoCAD não é necessário para gerar os DXFs, mas o AcCoreConsole 2027 foi usado
para abri-los e auditá-los. Nenhum DWG foi produzido. LibreCAD, ODA File Converter e
Inkscape não estavam disponíveis; as limitações completas constam no
[relatório de ferramentas](../relatorio-ferramentas.md).

## Limites

Não há seleção de fabricante, protocolo industrial, hardware de segurança, estudo de
disponibilidade, classificação de áreas, SIL/PL, proteção contra surtos detalhada,
coordenação, ensaio EMC, cálculo térmico ou liberação executiva. Endereços, faixas,
cabos, bornes, dimensões, limiares de diagnóstico, timeouts e ações de processo
continuam premissas ou decisões pendentes; a matriz documenta requisitos conceituais,
não comprova diagnóstico nem comportamento de equipamentos reais.

## Revisão 02 — registro histórico

Na revisão 02, o validador específico confirmou as sete folhas e a matriz CSV com **64.261
verificações, sem erros ou avisos**. O portfólio inteiro passou por **467.885
verificações estritas**, sem erros ou avisos; o revisor visual confirmou 12 projetos,
88 pranchas, 352 arquivos gráficos e 60 CSVs. A revisão visual da folha 07 foi feita
no PNG de produção e em uma rasterização independente do PDF a 150 dpi. Os oito eventos e o
carimbo ficaram dentro da moldura, sem cortes ou colisões visíveis. As seis folhas
anteriores foram revistas na composição geral; a inspeção integral descrita acima
pertence à revisão 00. A abertura dos SVGs no navegador e uma nova inspeção visual no
AutoCAD ainda não foram feitas naquela revisão.

## Revisão 03 — escala analógica

A nova folha 08 apresenta cinco pontos de conversão por malha, e a tabela usa texto de
1,8 mm para leitura ampliada em A3. A fonte, PDF, SVG e PNG foram regenerados; os
derivados mantêm a mesma geometria e não representam calibração nem teste de bancada.
O validador específico passou em **64.309 verificações**, sem erros ou avisos. A
validação estrita do portfólio passou em **549.703 verificações**, sem erros ou avisos.
O revisor visual confirmou 12 projetos, 100 pranchas, 400 arquivos gráficos, 71 CSVs
e similaridade mínima PDF/PNG de **0,984061**. O AcCoreConsole 2027 abriu e auditou
8/8 DXFs P10. A prancha 08 foi inspecionada no PNG de produção e na rasterização
independente do PDF a 150 dpi; as oito folhas também foram conferidas na composição
atual. A inspeção visual dos SVGs no navegador segue pendente da autorização do
usuário.
