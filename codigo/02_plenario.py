"""
02_plenario.py — Análise da votação no Plenário do Senado Federal.

Gera:
    - Tabela 10 (percentuais por indicado)
    - Tabela 11 (estatística descritiva, n = 27)
    - Linhas da Tabela 3 referentes ao Plenário (Mann-Kendall, 4 variáveis)
    - Linhas da Tabela 12 referentes ao Plenário (Pettitt, 2 variáveis)

Entrada: dados/plenario_votacao.csv
Saídas:  outputs/tabela_10_plenario_percentuais.csv
         outputs/tabela_11_plenario_descritivas.csv
         outputs/tabela_03_plenario_mann_kendall.csv
         outputs/tabela_12_plenario_pettitt.csv

Quórum fixo: 81 senadores.
"""

import pandas as pd
import numpy as np
import pymannkendall as mk
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from utilidades_00 import pettitt_test, describe  # noqa: E402


DIR_BASE = Path(__file__).parent.parent
df = pd.read_csv(DIR_BASE / "dados" / "plenario_votacao.csv")

# Validação
assert (df["favoraveis"] + df["contrarios"] +
        df["abstencoes"] + df["ausencias"] == df["quorum"]).all()

# Percentuais (quórum = 81)
df["pct_fav"] = df["favoraveis"] / df["quorum"] * 100
df["pct_con"] = df["contrarios"] / df["quorum"] * 100
df["pct_abs"] = df["abstencoes"] / df["quorum"] * 100
df["pct_aus"] = df["ausencias"] / df["quorum"] * 100

# Tabela 10 (percentuais)
tab10 = df[["indicado", "pct_fav", "pct_con", "pct_abs", "pct_aus"]].copy()
tab10.columns = ["Indicado(a)", "Favoráveis (%)", "Contrários (%)",
                 "Abstenções (%)", "Ausências (%)"]
tab10.to_csv(DIR_BASE / "outputs" / "tabela_10_plenario_percentuais.csv",
             index=False, float_format="%.2f")

# Tabela 11 (descritivas)
descritivas = {}
for nome, col in [("Favoráveis (%)", "pct_fav"),
                  ("Contrários (%)", "pct_con"),
                  ("Abstenções (%)", "pct_abs"),
                  ("Ausências (%)", "pct_aus")]:
    descritivas[nome] = describe(df[col])

tab11 = pd.DataFrame(descritivas).T
tab11.index.name = "Variável"
tab11.to_csv(DIR_BASE / "outputs" / "tabela_11_plenario_descritivas.csv",
             float_format="%.2f")

# Tabela 3 - Mann-Kendall
linhas = []
for nome, col in [("% Favoráveis", "pct_fav"),
                  ("% Contrários", "pct_con"),
                  ("% Abstenção", "pct_abs"),
                  ("% Ausências", "pct_aus")]:
    r = mk.original_test(df[col].values)
    linhas.append({
        "Variável": nome, "n": len(df),
        "tau": round(r.Tau, 4), "p_valor": round(r.p, 4),
        "S": int(r.s), "Z": round(r.z, 4),
        "sig_alfa_0_05": "Sim" if r.p < 0.05 else "Não",
        "tendencia": r.trend,
    })
tab3 = pd.DataFrame(linhas)
tab3.to_csv(DIR_BASE / "outputs" / "tabela_03_plenario_mann_kendall.csv",
            index=False)

# Tabela 12 - Pettitt (apenas variáveis significativas no MK)
linhas_pettitt = []
for nome, col in [("% Contrários", "pct_con"),
                  ("% Ausências", "pct_aus")]:
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
tab12 = pd.DataFrame(linhas_pettitt)
tab12.to_csv(DIR_BASE / "outputs" / "tabela_12_plenario_pettitt.csv",
             index=False)

print("=" * 70)
print("BLOCO 2 — PLENÁRIO DO SENADO FEDERAL")
print("=" * 70)
print(f"\nTabela 10 (percentuais) gerada — n = {len(df)}")
print(f"\nTabela 11 (descritivas):\n{tab11.to_string()}")
print(f"\nTabela 3 (Mann-Kendall):\n{tab3.to_string(index=False)}")
print(f"\nTabela 12 (Pettitt):\n{tab12.to_string(index=False)}")
