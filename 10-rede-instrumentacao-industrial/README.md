# Projeto 10 — Rede acadêmica de instrumentação industrial

**Código:** P10  
**Autor:** Rogério Eduardo Moreira Menegueli  
**Estado:** concluído  
**Data:** 2026-11-05
**Revisão:** 01 (revisão gráfica)
**Folha:** A3 paisagem  
**Unidades:** milímetros nos desenhos; grandezas de processo indicadas por instrumento

Este projeto fecha a série acadêmica do portfólio com uma rede original e fictícia de
instrumentação industrial. A arquitetura integra quatro transmissores 4–20 mA, duas
entradas digitais, duas remotas, CLP, switch, SCADA e distribuição 24 Vcc. O DXF
AC1027 é a fonte principal; PDF, SVG e PNG são derivados de visualização da mesma
revisão.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Entregáveis

| Prancha | Fonte DXF | Visualizações | Conteúdo |
| ---: | --- | --- | --- |
| 01/06 | [arquitetura da rede](fonte/01_arquitetura_rede.dxf) | [PDF](exports/01_arquitetura_rede.pdf), [SVG](exports/01_arquitetura_rede.svg), [PNG](exports/01_arquitetura_rede.png) | SCADA, switch, PLC, remotas, instrumentos e 24 Vcc |
| 02/06 | [diagrama de instrumentação](fonte/02_diagrama_instrumentacao.dxf) | [PDF](exports/02_diagrama_instrumentacao.pdf), [SVG](exports/02_diagrama_instrumentacao.svg), [PNG](exports/02_diagrama_instrumentacao.png) | malhas TT, PT, FT, LT e entradas LSH/PSL |
| 03/06 | [diagrama de interligação](fonte/03_diagrama_interligacao.dxf) | [PDF](exports/03_diagrama_interligacao.pdf), [SVG](exports/03_diagrama_interligacao.svg), [PNG](exports/03_diagrama_interligacao.png) | cabos, bornes, canais, shield e PE |
| 04/06 | [topologia de comunicação](fonte/04_topologia_comunicacao.dxf) | [PDF](exports/04_topologia_comunicacao.pdf), [SVG](exports/04_topologia_comunicacao.svg), [PNG](exports/04_topologia_comunicacao.png) | Ethernet industrial acadêmica em estrela |
| 05/06 | [painel de instrumentação](fonte/05_painel_instrumentacao.dxf) | [PDF](exports/05_painel_instrumentacao.pdf), [SVG](exports/05_painel_instrumentacao.svg), [PNG](exports/05_painel_instrumentacao.png) | layout conceitual de PI-101 |
| 06/06 | [lista de instrumentos](fonte/06_lista_instrumentos.dxf) | [PDF](exports/06_lista_instrumentos.pdf), [SVG](exports/06_lista_instrumentos.svg), [PNG](exports/06_lista_instrumentos.png) | tags, faixas, sinais, canais e escalas |

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Filosofia e separação dos sinais](filosofia-sinais.md)
- [Referências normativas](referencias-normativas.md)
- [Inspeção visual](inspecao-visual.md)
- [Parâmetros](parametros.csv)
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
cabos, bornes e dimensões continuam dados acadêmicos; esta revisão atualiza a
apresentação gráfica e não valida tecnicamente o projeto.
