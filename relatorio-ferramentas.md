# Ferramentas e evidências de validação

## Reprodução

A geração e os testes Python usam as dependências fixadas em `requirements.txt`. Com Python 3.11 ou superior, execute a partir da raiz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

Os DXFs são arquivos AC1027 em milímetros. A auditoria com AutoCAD Core Console requer uma instalação compatível; a interface gráfica e a saída de plotter não foram verificadas na revisão mais recente. MATLAB e Simulink são dependências opcionais para os estudos dinâmicos.

## Evidências nesta revisão

- A auditoria de 09/11/2026 registra 36 testes Python aprovados e 651.139 verificações estruturais sem erros ou avisos.
- O CSV versionado registra auditoria AutoCAD Core Console aprovada para 30/30 DXFs, sem erros nem reparos. Essa execução não foi repetida durante a auditoria posterior.
- Os caminhos estáticos MATLAB de P23, P24 e P25 foram executados e têm registros de saída. Eles verificam apenas as rotinas e os casos codificados, sob entradas sintéticas ou provisórias.
- Nenhuma simulação dinâmica MATLAB/Simulink concluída está comprovada. A tentativa P23 não produziu simulação; P24 não contém `.slx`; o modelo P25 não foi executado.

Consulte [RELATORIO_FINAL_AUDITORIA_P23_P24_P25.md](RELATORIO_FINAL_AUDITORIA_P23_P24_P25.md) e os relatórios de cada projeto para detalhes, premissas e pendências. Resultados de software não constituem certificação de segurança, conformidade normativa ou aptidão para obra.
