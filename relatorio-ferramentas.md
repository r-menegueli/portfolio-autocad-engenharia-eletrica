# Ferramentas e reprodutibilidade

Este documento resume como reproduzir as verificações documentadas sem expor detalhes de uma máquina ou de um ambiente temporário.

## Dependências e comandos

A reconstrução dos desenhos e as verificações Python usam as dependências fixadas em [requirements.txt](requirements.txt) e Python 3.11 ou superior. A partir da raiz do repositório:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
.\.venv\Scripts\python.exe .\scripts\construir.py --root . --strict
.\.venv\Scripts\python.exe .\scripts\revisar_portfolio.py --root .
.\.venv\Scripts\python.exe .\scripts\revisar_workbooks.py --root .
```

Os DXFs usam AC1027 e milímetros. A validação por AutoCAD Core Console depende de instalação compatível do AutoCAD; o script correspondente permite informar o executável sem gravar caminhos locais no projeto. A conversão para DWG não faz parte do fluxo público.

MATLAB e Simulink são ferramentas de desenvolvimento para os estudos P23–P25, mas a presença dos arquivos-fonte ou modelos não prova que uma execução terminou com sucesso. Os resultados e suas limitações estão descritos no [relatório consolidado de validação](relatorio-validacao.md) e, para a revisão independente, no [relatório da branch revisao/p23-p25](https://github.com/r-menegueli/portfolio-autocad-engenharia-eletrica/blob/revisao/p23-p25/RELATORIO_FINAL_AUDITORIA_P23_P24_P25.md).

## Estado das evidências

- O relatório histórico P01–P10 registra verificações de estrutura, arquivos CAD, derivados e testes executados em setembro de 2026. Esses resultados são registros históricos e não foram reexecutados nesta auditoria da conta.
- O relatório de `main` registra validações para P01–P25, mas não inclui evidência suficiente para confirmar, nesta branch, a execução atual de MATLAB/Simulink descrita ali.
- A auditoria mais recente de P23–P25 está em uma branch separada. Ela registra testes Python e caminhos estáticos MATLAB executados; não confirma uma simulação Simulink concluída. As pendências técnicas permanecem abertas.
- Validações estruturais e testes automatizados não certificam dimensionamento, conformidade normativa, segurança, fabricação ou aptidão para obra.

Use os relatórios por projeto para conferir entradas, premissas, resultados e limitações. Não trate a instalação de uma ferramenta como evidência de aprovação de engenharia.
