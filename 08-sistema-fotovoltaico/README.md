# Projeto 08 - Estudo acadêmico de sistema fotovoltaico residencial

Autor: Rogério Eduardo Moreira Menegueli

Pranchas: 01 a 06

Formato: A3 paisagem, unidades geométricas em milímetros, revisão 00

Estado: concluído e validado em 2026-09-09

Este projeto apresenta um sistema fotovoltaico residencial conceitual, conectado à
rede, com 6,60 kWp no lado CC e inversor string acadêmico de 6 kWca em 220 V. O arranjo
usa 12 módulos de 550 Wp, divididos em duas strings independentes de seis módulos, uma
por MPPT.

O estudo não seleciona fabricante, não substitui levantamento de campo, projeto
estrutural, consulta à distribuidora, análise de sombreamento, coordenação de proteção,
comissionamento ou responsabilidade técnica.

## Pranchas

1. [Disposição dos módulos](fonte/01_disposicao_modulos.dxf)
2. [Diagrama unifilar CC](fonte/02_diagrama_unifilar_cc.dxf)
3. [Diagrama unifilar CA](fonte/03_diagrama_unifilar_ca.dxf)
4. [String box](fonte/04_string_box.dxf)
5. [Aterramento e equipotencialização](fonte/05_aterramento.dxf)
6. [Layout dos equipamentos](fonte/06_layout_equipamentos.dxf)

Cada DXF possui derivados homônimos em `exports/` nos formatos PDF, SVG e PNG.

## Dados declarados

| Grandeza | Valor acadêmico |
| --- | ---: |
| potência unitária do módulo | 550 Wp |
| quantidade de módulos | 12 |
| potência instalada CC | 6,60 kWp |
| strings | 2 × 6 módulos em série |
| Vmp por string em STC | 250,8 Vcc |
| Voc por string em STC | 299,4 Vcc |
| Imp por string em STC | 13,16 A |
| Isc por string em STC | 13,92 A |
| inversor adotado | INV-FV-801, classe acadêmica 6 kWca, 220 V, 2 MPPT |
| relação CC/CA | 1,10 |

Os valores completos, coeficientes térmicos e limites do inversor estão em
[Parâmetros](parametros.csv). O inversor é uma especificação funcional fictícia, não
um modelo comercial homologado.

## Documentos e dados

- [Memorial descritivo](memorial-descritivo.md)
- [Critérios e premissas](criterios-premissas.md)
- [Memória de cálculo](memoria-calculo.md)
- [Referências normativas](referencias-normativas.md)
- [Lista de módulos](lista-modulos.csv)
- [Lista de proteções](lista-protecoes.csv)
- [Lista de cabos](lista-cabos.csv)
- [Lista de equipamentos e materiais](lista-materiais.csv)
- [Resultados dos cálculos](resultados-calculo.csv)
- [Inspeção visual](inspecao-visual.md)
- [Validação específica](validacao-fotovoltaico.json)
- [Validação estrita](validacao.json)

## Reprodução

Na raiz do portfólio:

```powershell
.venv\Scripts\python.exe 08-sistema-fotovoltaico\fonte\gerar_projeto_08.py --root .
.venv\Scripts\python.exe 08-sistema-fotovoltaico\fonte\validar_projeto_08.py --root .
.venv\Scripts\python.exe scripts\renderizar.py --root . --dpi 300
.venv\Scripts\python.exe scripts\validar_portfolio.py --root . --strict --report 08-sistema-fotovoltaico\validacao.json
```

O DXF AC1027 é a fonte principal. Nenhum DWG é fornecido nesta revisão.

## Verificação da revisão 00

- validador específico: `PASS`, 8.036 verificações e nenhum erro;
- validação estrita integrada: `PASS`, 297.598 verificações, nenhum erro e nenhum aviso;
- AutoCAD AcCoreConsole 2027: seis DXFs abertos e auditados, `PASS` em 6/6;
- derivados: 18 arquivos gerados e inspecionados (seis PDF, seis SVG e seis PNG);
- PDFs: uma página A3 por prancha, reabertos e rasterizados pelo Poppler;
- SVGs: abertos e rasterizados pelo Google Chrome;
- reprodutibilidade: hashes idênticos em 24/24 artefatos após nova geração;
- suíte automatizada do portfólio: nove testes aprovados.

Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.
