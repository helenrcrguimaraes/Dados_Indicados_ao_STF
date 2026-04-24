"""Executa todo o pipeline de replicação.

Uso:
    python run_all.py
"""
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
SCRIPTS = [
    "01_ccj.py",
    "02_plenario.py",
    "03_tramitacao.py",
    "04_partidos.py",
    "05_sabatinas_quantitativo.py",
    "06_temas.py",
    "07_associacoes.py",
    "08_dispersao_associacoes.py",
]

(BASE / "outputs").mkdir(exist_ok=True)

for script in SCRIPTS:
    path = BASE / "codigo" / script
    print(f"\n>>> Executando {script}")
    subprocess.run([sys.executable, str(path)], check=True)

print("\nPipeline concluído. Resultados em outputs/.")
