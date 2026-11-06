# P17 — Automação digital de subestação com IEC 61850

Estudo conceitual do sistema de automação de uma subestação, com diagrama funcional de bays e IEDs, separação entre rede de processo e rede de estação, fluxos conceituais de SV, GOOSE e MMS e uma matriz de mensagens e verificações propostas. O escopo concentra-se em proteção, controle e comunicação; a representação elétrica é apenas contexto.

> Projeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.

## Pranchas

| Folha | Conteúdo | DXF editável | PDF | SVG | PNG |
| :---: | --- | :---: | :---: | :---: | :---: |
| 01/03 | Diagrama funcional do arranjo elétrico e associação ilustrativa dos IEDs | [DXF](fonte/01_unifilar_sas_ied.dxf) | [PDF](exports/01_unifilar_sas_ied.pdf) | [SVG](exports/01_unifilar_sas_ied.svg) | [PNG](exports/01_unifilar_sas_ied.png) |
| 02/03 | Rede de processo e rede de estação com MUs, IEDs e serviços | [DXF](fonte/02_rede_iec61850.dxf) | [PDF](exports/02_rede_iec61850.pdf) | [SVG](exports/02_rede_iec61850.svg) | [PNG](exports/02_rede_iec61850.png) |
| 03/03 | Matriz GOOSE de exemplo, ciclo SCL e plano proposto de verificação | [DXF](fonte/03_matriz_goose_testes.dxf) | [PDF](exports/03_matriz_goose_testes.pdf) | [SVG](exports/03_matriz_goose_testes.svg) | [PNG](exports/03_matriz_goose_testes.png) |

Documentos de apoio: [memorial](memorial-descritivo.md), [critérios e premissas](criterios-premissas.md), [referências](referencias-normativas.md), [inventário de IEDs](lista-ieds.csv), [matriz GOOSE](matriz-goose.csv), [lista de sinais](lista-sinais.csv), [plano de verificação](plano-verificacao.csv), [materiais](lista-materiais.csv), [gerador](fonte/gerar_projeto_17.py), [validador](fonte/validar_projeto_17.py), [resultado da validação](validacao-projeto-17.json) e [inspeção visual](inspecao-visual.md).

## Base do estudo

- Subestação de referência hipotética 138/13,8 kV, com duas linhas, um transformador, barramentos e dois alimentadores.
- IEDs de proteção, controle de bay e MUs, switches de processo e de estação, HMI, gateway SCADA, estação de engenharia e fonte de tempo são blocos conceituais.
- SV, GOOSE e MMS identificam classes de fluxo; datasets, topologia, endereços, VLANs, tempos e parâmetros não foram projetados.
- ICD, SSD, SCD e CID aparecem como etapas/documentos do fluxo de engenharia SCL. Não há arquivos SCL de fabricante nesta entrega.

## Como reproduzir

Na raiz do repositório, com Python 3.11+ e as dependências de `requirements.txt`:

```powershell
python .\17-automacao-subestacao-digital\fonte\gerar_projeto_17.py --root .
python .\scripts\renderizar.py --root . --artifact p17-01-unifilar-sas-ied --artifact p17-02-rede-iec61850 --artifact p17-03-matriz-goose-testes
python .\17-automacao-subestacao-digital\fonte\validar_projeto_17.py --root .
python .\scripts\validar_portfolio.py --root . --strict
```

Os DXFs AC1027 são as fontes editáveis em milímetros. PDF, SVG e PNG são derivados. Não há DWG nem configuração SCL executável no projeto.

## Limites

Os rótulos e mensagens não constituem configuração de proteção ou automação. Não existem arquivos de fabricante, datasets confirmados, endereçamento, ajustes, cálculo de seletividade, tempos de rede, política de cibersegurança, ensaios de interoperabilidade, FAT ou SAT executados. A topologia não prova redundância ou comportamento seguro perante falhas. Qualquer sistema real requer engenharia, revisão, estudos, testes e aprovação do responsável e do proprietário.
