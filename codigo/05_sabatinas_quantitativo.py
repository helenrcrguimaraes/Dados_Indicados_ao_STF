"""
05_sabatinas_quantitativo.py — Análise quantitativa das sabatinas.

Gera:
    - Tabela 20 (senadores que indagaram por sabatina)
    - Tabela 21 (descritiva de senadores que indagaram, n = 19)
    - Tabela 22 (total de indagações por sabatina)
    - Tabela 23 (manifestações sem indagação: elogios, rejeição, outras)
    - Tabela 24 (tempo de sabatina por indicado)
    - Tabela 25 (descritiva do tempo de sabatina)
    - Linhas da Tabela 3 referentes às sabatinas (Mann-Kendall, 5 variáveis)
    - Tabela 26 (Pettitt, 3 variáveis com tendência significativa)

Entrada: dados/sabatinas_quantitativo.csv
Saídas:  outputs/tabela_20_a_26_*.csv

Observação sobre a categoria "Outras":
    Manifestações sem indagação e sem caráter de elogio ou rejeição (ex.:
    registro de presença, declaração de preenchimento de requisitos
    constitucionais sem qualificação avaliativa).

Observação sobre o total de indagações (1119) vs classificadas (1114):
    Cinco indagações (-1 em Toffoli, -1 em Fux, -1 em Nunes Marques, -2 em
    Dino) não foram classificáveis nas macrocategorias e ficaram de fora
    da análise temática. A diferença é reconhecida no cabeçalho das
    Tabelas 1 e 2 ("n = 1.114").
"""

import pandas as pd
import numpy as np
import pymannkendall as mk
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from utilidades_00 import pettitt_test, describe  # noqa: E402


DIR_BASE = Path(__file__).parent.parent
df = pd.read_csv(DIR_BASE / "dados" / "sabatinas_quantitativo.csv")

# Tabela 20 — senadores que indagaram
tab20 = df[["indicado", "senadores"]].copy()
tab20.columns = ["Indicado(a)", "Senadores que indagaram"]
tab20.to_csv(DIR_BASE / "outputs" / "tabela_20_senadores.csv", index=False)

# Tabela 21 — descritiva de senadores
d = describe(df["senadores"])
tab21 = pd.DataFrame([d], index=["Senadores que indagaram"])
tab21.index.name = "Variável"
tab21.to_csv(DIR_BASE / "outputs" / "tabela_21_senadores_descritiva.csv",
             float_format="%.2f")

# Tabela 22 — total de indagações
tab22 = df[["indicado", "indagacoes"]].copy()
tab22.columns = ["Indicado(a)", "Total de indagações"]
tab22.to_csv(DIR_BASE / "outputs" / "tabela_22_indagacoes.csv", index=False)

# Tabela 23 — manifestações sem indagação
tab23 = df[["indicado", "elogios", "rejeicao", "outras"]].copy()
tab23["total"] = tab23["elogios"] + tab23["rejeicao"] + tab23["outras"]
tab23.columns = ["Indicado(a)", "Elogios", "Rejeição", "Outras", "Total"]
tab23.to_csv(DIR_BASE / "outputs" / "tabela_23_manifestacoes.csv", index=False)

# Tabela 24 — tempo de sabatina
tab24 = df[["indicado", "tempo_h"]].copy()
tab24.columns = ["Indicado(a)", "Tempo de sabatina (h)"]
tab24.to_csv(DIR_BASE / "outputs" / "tabela_24_tempo.csv", index=False)

# Tabela 25 — descritiva do tempo
d = describe(df["tempo_h"])
tab25 = pd.DataFrame([d], index=["Tempo de sabatina (h)"])
tab25.index.name = "Variável"
tab25.to_csv(DIR_BASE / "outputs" / "tabela_25_tempo_descritiva.csv",
             float_format="%.2f")

# Tabela 3 — Mann-Kendall (5 variáveis)
linhas = []
for nome, col in [("Senadores que indagaram", "senadores"),
                  ("Total de indagações", "indagacoes"),
                  ("Tempo de sabatina", "tempo_h"),
                  ("Elogios", "elogios"),
                  ("Rejeição", "rejeicao")]:
    r = mk.original_test(df[col].values)
    linhas.append({
        "Variável": nome, "n": len(df),
        "tau": round(r.Tau, 4), "p_valor": round(r.p, 4),
        "S": int(r.s), "Z": round(r.z, 4),
        "sig_alfa_0_05": "Sim" if r.p < 0.05 else "Não",
        "tendencia": r.trend,
    })
tab3 = pd.DataFrame(linhas)
tab3.to_csv(DIR_BASE / "outputs" / "tabela_03_sabatinas_mann_kendall.csv",
            index=False)

# Tabela 26 — Pettitt (3 variáveis significativas)
linhas_pettitt = []
for nome, col in [("Senadores que indagaram", "senadores"),
                  ("Total de indagações", "indagacoes"),
                  ("Tempo de sabatina", "tempo_h")]:
    y = df[col].values
    res = pettitt_test(y)
    tau_idx = res["tau_idx"]
    antes = df["indicado"].iloc[tau_idx - 1]
    depois = df["indicado"].iloc[tau_idx]
    linhas_pettitt.append({
        "Variável": nome,
        "ponto_mudanca": f"{antes} → {depois}",
        "K": res["K"], "p_valor": round(res["p_value"], 4),
        "media_antes": round(y[:tau_idx].mean(), 2),
        "media_depois": round(y[tau_idx:].mean(), 2),
    })
tab26 = pd.DataFrame(linhas_pettitt)
tab26.to_csv(DIR_BASE / "outputs" / "tabela_26_sabatinas_pettitt.csv",
             index=False)

print("=" * 70)
print("BLOCO 5 — SABATINAS (QUANTITATIVO)")
print("=" * 70)
print(f"\nTabela 21 (senadores):\n{tab21.to_string()}")
print(f"\nTabela 25 (tempo):\n{tab25.to_string()}")
print(f"\nTabela 3 (sabatinas):\n{tab3.to_string(index=False)}")
print(f"\nTabela 26 (Pettitt):\n{tab26.to_string(index=False)}")

# Totais para texto da seção 3.5.1
print(f"\nTotais: elogios={df['elogios'].sum()}, rejeição={df['rejeicao'].sum()}, "
      f"outras={df['outras'].sum()}, total manifestações={tab23['Total'].sum()}")
