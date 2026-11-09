"""Valida arquivos deste estudo com o validador focado do portfólio."""
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parents[2]
raise SystemExit(subprocess.call([sys.executable,str(root/'scripts'/'validar_estudos_p23_p25.py'),'--project','p23'],cwd=root))
