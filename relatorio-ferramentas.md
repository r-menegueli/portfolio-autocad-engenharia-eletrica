# Ferramentas e validação

## Reprodução

A geração e a validação dos arquivos usam as dependências fixadas em `requirements.txt`. Com Python 3.11 ou superior, execute na raiz:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe .\scripts\validar_portfolio.py --root . --strict
```

Os DXFs usam AC1027 e milímetros. A auditoria por AutoCAD Core Console requer instalação compatível; os comandos e relatórios por projeto distinguem resultados efetivamente registrados de verificações que não foram feitas.

## Estado deste snapshot

- A branch `revisao/portfolio-2026-11` contém 22 estudos e 144 pranchas A3, confirmados pelo inventário de arquivos desta revisão.
- A validação estrita registrada em `docs/auditoria-portfolio-2026-11.md` cobre 794.464 verificações, sem erros ou avisos. Ela é evidência histórica desta branch; não foi reexecutada depois das mudanças documentais desta auditoria.
- Os arquivos e verificações MATLAB/Simulink presentes no repositório devem ser interpretados conforme os relatórios individuais. A existência de um modelo não comprova simulação concluída.
- Testes e verificações estruturais não certificam dimensionamento, segurança, conformidade normativa ou aptidão para obra.

Consulte as auditorias e os relatórios individuais para premissas, resultados e limitações técnicas.
