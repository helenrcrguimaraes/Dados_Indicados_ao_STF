"""
03_tramitacao.py — Análise do tempo de tramitação das indicações.

Gera:
    - Tabela 13 (tempos por indicado)
    - Tabela 14 (descritivas, n = 28, com Mendonça)
    - Tabela 15 (descritivas, n = 27, sem Mendonça)
    - Linhas da Tabela 3 referentes à Tramitação (Mann-Kendall)
    - Quadro 6 (incidentes processuais)

Entradas: dados/tramitacao_tempos.csv
          dados/incidentes_procedimentais.csv

Sobre a exclusão de Mendonça (n=27):
    A indicação de André Mendonça (2021) é outlier formal pelo critério de
    Tukey em ambas as variáveis de tramitação (n=28):

    - Tempo total: Q1 = 11,75; Q3 = 26,25; IQR = 14,50;
      limite superior (Q3 + 1,5·IQR) = 48,00; Mendonça = 105.
    - Tempo até distribuição: Q1 = 0,00; Q3 = 5,25; IQR = 5,25;
      limite superior (Q3 + 1,5·IQR) = 13,125; Mendonça = 101.

    O script verifica esses limites e imprime a confirmação no console.
    A exclusão justifica-se estatisticamente para a análise de tendência.
"""

import pandas as pd
import numpy as np
import pymannkendall as mk
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from utilidades_00 import describe  # noqa: E402


DIR_BASE = Path(__file__).parent.parent

# Tempos
df = pd.read_csv(DIR_BASE / "dados" / "tramitacao_tempos.csv")

# Critério de Tukey (n = 28): limite superior = Q3 + 1,5·IQR.
# Registra os valores exatos e confirma que Mendonça é outlier em ambas as
# variáveis antes de produzir a amostra n = 27.
tukey = []
for col, label in [("tempo_total", "Tempo total"),
                    ("tempo_distribuicao", "Tempo até distribuição")]:
    q1 = float(np.percentile(df[col], 25))
    q3 = float(np.percentile(df[col], 75))
    iqr = q3 - q1
    lim_sup = q3 + 1.5 * iqr
    mendonca_val = float(df.loc[df["indicado"] == "André Mendonça", col].iloc[0])
    tukey.append({
        "Variável": label, "Q1": round(q1, 2), "Q3": round(q3, 2),
        "IQR": round(iqr, 2),
        "Limite superior (Q3 + 1,5·IQR)": round(lim_sup, 3),
        "Valor Mendonça": mendonca_val,
        "Outlier por Tukey?": "Sim" if mendonca_val > lim_sup else "Não",
    })
tukey_df = pd.DataFrame(tukey)
tukey_df.to_csv(DIR_BASE / "outputs" / "criterio_tukey_tramitacao.csv",
                index=False)

df27 = df[df["indicado"] != "André Mendonça"].reset_index(drop=True)

# Tabela 13 (dados brutos)
df.to_csv(DIR_BASE / "outputs" / "tabela_13_tramitacao_tempos.csv", index=False)

# Tabela 14 — descritivas n=28
desc_28 = {
    "Tempo total (dias)": describe(df["tempo_total"]),
    "Tempo até distribuição (dias)": describe(df["tempo_distribuicao"]),
}
tab14 = pd.DataFrame(desc_28).T
tab14.index.name = "Variável"
tab14.to_csv(DIR_BASE / "outputs" / "tabela_14_tramitacao_n28.csv",
             float_format="%.2f")

# Tabela 15 — descritivas n=27
desc_27 = {
    "Tempo total (dias)": describe(df27["tempo_total"]),
    "Tempo até distribuição (dias)": describe(df27["tempo_distribuicao"]),
}
tab15 = pd.DataFrame(desc_27).T
tab15.index.name = "Variável"
tab15.to_csv(DIR_BASE / "outputs" / "tabela_15_tramitacao_n27.csv",
             float_format="%.2f")

# Tabela 3 - Mann-Kendall (com e sem Mendonça)
linhas = []
for label_amostra, d in [("n=28 (com Mendonça)", df),
                          ("n=27 (sem Mendonça)", df27)]:
    for nome, col in [("Tempo total", "tempo_total"),
                       ("Tempo até distribuição", "tempo_distribuicao")]:
        r = mk.original_test(d[col].values)
        linhas.append({
            "Variável": nome, "Amostra": label_amostra, "n": len(d),
            "tau": round(r.Tau, 4), "p_valor": round(r.p, 4),
            "S": int(r.s), "Z": round(r.z, 4),
            "sig_alfa_0_05": "Sim" if r.p < 0.05 else "Não",
            "tendencia": r.trend,
        })
tab3 = pd.DataFrame(linhas)
tab3.to_csv(DIR_BASE / "outputs" / "tabela_03_tramitacao_mann_kendall.csv",
            index=False)

# Quadro 6 — incidentes processuais (tabulação)
df_inc = pd.read_csv(DIR_BASE / "dados" / "incidentes_procedimentais.csv")
df_inc.to_csv(DIR_BASE / "outputs" / "quadro_06_incidentes.csv", index=False)

# Verificação: Gilmar Mendes é único com os 4 incidentes?
tudo_sim = df_inc[
    (df_inc["sem_pauta"] == "Sim") &
    (df_inc["adiada"] == "Sim") &
    (df_inc["vista"] == "Sim") &
    (df_inc["interstic"] == "Sim")
]

# Resumo de contagens
contagens = pd.DataFrame({
    "Incidente": ["Sem pauta prévia", "Sabatina adiada/suspensa",
                   "Vista coletiva", "Dispensa do interstício"],
    "Sim": [(df_inc["sem_pauta"] == "Sim").sum(),
            (df_inc["adiada"] == "Sim").sum(),
            (df_inc["vista"] == "Sim").sum(),
            (df_inc["interstic"] == "Sim").sum()],
    "Não": [(df_inc["sem_pauta"] == "Não").sum(),
            (df_inc["adiada"] == "Não").sum(),
            (df_inc["vista"] == "Não").sum(),
            (df_inc["interstic"] == "Não").sum()],
})
contagens["Sem dado"] = 28 - contagens["Sim"] - contagens["Não"]
contagens.to_csv(DIR_BASE / "outputs" / "incidentes_contagens.csv", index=False)

print("=" * 70)
print("BLOCO 3 — TRAMITAÇÃO")
print("=" * 70)
print(f"\nCritério de Tukey (n=28):\n{tukey_df.to_string(index=False)}")
print(f"\nTabela 14 (n=28):\n{tab14.to_string()}")
print(f"\nTabela 15 (n=27):\n{tab15.to_string()}")
print(f"\nTabela 3 (Mann-Kendall):\n{tab3.to_string(index=False)}")
print(f"\nIncidentes processuais (contagens):\n{contagens.to_string(index=False)}")
print(f"\nIndicações com os 4 incidentes simultâneos: {tudo_sim['indicado'].tolist()}")
