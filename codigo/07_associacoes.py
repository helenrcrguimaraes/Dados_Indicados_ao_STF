"""
07_associacoes.py — Associações estatísticas entre as dimensões.

Gera:
    - Tabela 4 (correlação CCJ × Plenário)
    - Tabela 5 (sabatinas × votação)
    - Tabela 6 (macrocategorias × variáveis quantitativas)
    - Tabela 7 (Mann-Whitney: com casos × sem casos)
    - Testes da seção 3.7 sobre dispersão partidária

Entradas: múltiplos CSVs da pasta dados/
Saídas:   outputs/tabela_0{4,5,6,7}_*.csv
          outputs/dispersao_associacoes.csv

Decisões metodológicas:
    - Tau de Kendall com variant='b' (corrige empates) — diferente do tau
      usado nas Tabelas 3 e 12/26, que são Mann-Kendall clássico (tau-a).
      A Tabela 4 e seguintes testam CORRELAÇÃO entre duas variáveis, não
      tendência temporal em uma série — por isso o teste apropriado é
      Kendall tau-b via scipy.stats.kendalltau.
    - Para Mann-Whitney: scipy.stats.mannwhitneyu (alternative='two-sided').
    - Para Spearman: scipy.stats.spearmanr.
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path


DIR_BASE = Path(__file__).parent.parent

# -----------------------------------------------------------------------------
# 1. Carregar todos os dados relevantes
# -----------------------------------------------------------------------------
ccj = pd.read_csv(DIR_BASE / "dados" / "ccj_votacao.csv")
pln = pd.read_csv(DIR_BASE / "dados" / "plenario_votacao.csv")
sab = pd.read_csv(DIR_BASE / "dados" / "sabatinas_quantitativo.csv")
par = pd.read_csv(DIR_BASE / "dados" / "partidos_posicoes.csv")
tem = pd.read_csv(DIR_BASE / "dados" / "temas_indagacoes.csv")

# Percentuais
ccj["pct_fav_ccj"] = ccj["favoraveis"] / ccj["quorum"] * 100
ccj["pct_con_ccj"] = ccj["contrarios"] / ccj["quorum"] * 100
pln["pct_fav_pln"] = pln["favoraveis"] / pln["quorum"] * 100
pln["pct_con_pln"] = pln["contrarios"] / pln["quorum"] * 100

# -----------------------------------------------------------------------------
# 2. Tabela 4 — Correlação CCJ × Plenário (n = 20)
# -----------------------------------------------------------------------------
# Juntar pelas indicações em comum (todas as 20 da CCJ estão no Plenário)
m4 = ccj[["indicado", "pct_fav_ccj", "pct_con_ccj"]].merge(
    pln[["indicado", "pct_fav_pln", "pct_con_pln"]], on="indicado")

pares = [
    ("% Contrários CCJ × % Contrários Plenário",
     m4["pct_con_ccj"], m4["pct_con_pln"]),
    ("% Favoráveis CCJ × % Favoráveis Plenário",
     m4["pct_fav_ccj"], m4["pct_fav_pln"]),
]
linhas_t4 = []
for label, x, y in pares:
    tau_b, p_k = stats.kendalltau(x, y, variant="b")
    rho, p_s = stats.spearmanr(x, y)
    linhas_t4.append({
        "Variáveis cruzadas": label,
        "tau_Kendall": round(tau_b, 4), "p_Kendall": round(p_k, 6),
        "rho_Spearman": round(rho, 4), "p_Spearman": round(p_s, 6),
    })
tab4 = pd.DataFrame(linhas_t4)
tab4.to_csv(DIR_BASE / "outputs" / "tabela_04_ccj_plenario.csv", index=False)

# -----------------------------------------------------------------------------
# 3. Tabela 5 — Sabatinas × Votação (n = 19)
# -----------------------------------------------------------------------------
# Das 20 indicações da CCJ, 19 têm sabatina (exclui Ricardo Lewandowski).
m5 = sab.merge(ccj[["indicado", "pct_fav_ccj", "pct_con_ccj"]], on="indicado")
m5 = m5.merge(pln[["indicado", "pct_fav_pln", "pct_con_pln"]], on="indicado")

vars_vot = [("% Favoráveis Plenário", "pct_fav_pln"),
            ("% Contrários Plenário", "pct_con_pln"),
            ("% Favoráveis CCJ", "pct_fav_ccj"),
            ("% Contrários CCJ", "pct_con_ccj")]
vars_sab = [("Tempo de sabatina", "tempo_h"),
            ("Indagações", "indagacoes"),
            ("Senadores que indagaram", "senadores"),
            ("Elogios", "elogios"),
            ("Rejeições", "rejeicao")]

linhas_t5 = []
for v_label, v_col in vars_vot:
    for s_label, s_col in vars_sab:
        tau, p = stats.kendalltau(m5[v_col], m5[s_col], variant="b")
        linhas_t5.append({
            "Variável de votação": v_label,
            "Variável da sabatina": s_label,
            "tau": round(tau, 4), "p_valor": round(p, 4),
            "sig_alfa_0_05": "Sim" if p < 0.05 else "Não",
            "direcao": "Positiva" if tau > 0 else "Negativa" if tau < 0 else "Nula",
        })
tab5 = pd.DataFrame(linhas_t5)
tab5.to_csv(DIR_BASE / "outputs" / "tabela_05_sabatina_votacao.csv", index=False)

# -----------------------------------------------------------------------------
# 4. Tabela 6 — Macrocategorias × Quantitativas (n = 19)
# -----------------------------------------------------------------------------
# Calcular proporção de cada macrocategoria em cada sabatina
tem["macrocategoria"] = tem["macrocategoria"].astype(str).str.strip()
sabatinas = tem["indicado"].unique()
macros = sorted(tem["macrocategoria"].unique())

prop = pd.DataFrame(index=sorted(sabatinas), columns=macros, dtype=float)
for s in sabatinas:
    sub = tem[tem["indicado"] == s]
    total = len(sub)
    for mc in macros:
        prop.loc[s, mc] = (sub["macrocategoria"] == mc).sum() / total * 100
prop.index.name = "indicado"
prop = prop.reset_index()

# Alinhar nomes (tem banco usa "Luis"? Normalizar para "Luís")
prop["indicado"] = prop["indicado"].replace({
    "Luis Roberto Barroso": "Luís Roberto Barroso",
    "Kássio Nunes Marques": "Nunes Marques",
    "Carlos Ayres Britto": "Ayres Britto",
    "Cézar Peluso": "Cezar Peluso",
})

# Juntar com variáveis quantitativas
m6 = prop.merge(sab[["indicado", "senadores", "indagacoes", "tempo_h"]],
                on="indicado")
m6 = m6.merge(pln[["indicado", "pct_con_pln"]], on="indicado")

vars_q = [("Tempo de sabatina", "tempo_h"),
           ("Senadores que indagaram", "senadores"),
           ("% Contrários Plenário", "pct_con_pln"),
           ("Indagações", "indagacoes")]

linhas_t6 = []
for mc in macros:
    for q_label, q_col in vars_q:
        tau, p = stats.kendalltau(m6[mc], m6[q_col], variant="b")
        linhas_t6.append({
            "Macrocategoria (%)": mc,
            "Variável quantitativa": q_label,
            "tau": round(tau, 4), "p_valor": round(p, 4),
            "sig_alfa_0_05": "Sim" if p < 0.05 else "Não",
        })
tab6 = pd.DataFrame(linhas_t6)
tab6.to_csv(DIR_BASE / "outputs" / "tabela_06_macro_quantitativas.csv",
            index=False)

# -----------------------------------------------------------------------------
# 5. Tabela 7 — Mann-Whitney com casos × sem casos (n = 19)
# -----------------------------------------------------------------------------
casos = tem[tem["macrocategoria"] == "Casos e eventos específicos"][
    "indicado"].unique()
# Normalizar nomes
casos = [
    {"Luis Roberto Barroso": "Luís Roberto Barroso",
     "Kássio Nunes Marques": "Nunes Marques",
     "Carlos Ayres Britto": "Ayres Britto",
     "Cézar Peluso": "Cezar Peluso"}.get(c, c)
    for c in casos
]

m7 = sab.merge(pln[["indicado", "pct_con_pln"]], on="indicado")
m7["grupo"] = m7["indicado"].apply(lambda x: "com" if x in casos else "sem")

linhas_t7 = []
for label, col in [("Tempo de sabatina (h)", "tempo_h"),
                    ("Indagações", "indagacoes"),
                    ("Senadores que indagaram", "senadores"),
                    ("% Contrários Plenário", "pct_con_pln")]:
    g_com = m7[m7["grupo"] == "com"][col]
    g_sem = m7[m7["grupo"] == "sem"][col]
    U, p = stats.mannwhitneyu(g_com, g_sem, alternative="two-sided")
    linhas_t7.append({
        "Variável": label,
        f"Com casos (n={len(g_com)}) média": round(g_com.mean(), 2),
        f"Sem casos (n={len(g_sem)}) média": round(g_sem.mean(), 2),
        "U": round(U, 1), "p_valor": round(p, 4),
    })
tab7 = pd.DataFrame(linhas_t7)
tab7.to_csv(DIR_BASE / "outputs" / "tabela_07_casos_mann_whitney.csv",
            index=False)

print("=" * 70)
print("BLOCO 7 — ASSOCIAÇÕES (Tabelas 4, 5, 6, 7)")
print("=" * 70)
print(f"\nTabela 4 (CCJ × Plenário, n=20):\n{tab4.to_string(index=False)}")
print(f"\nTabela 5 (sabatina × votação, n=19):\n{tab5.to_string(index=False)}")
print(f"\nTabela 6 (macrocategorias × quantitativas, n=19):")
print(tab6.to_string(index=False))
print(f"\nTabela 7 (casos Mann-Whitney, n=19):\n{tab7.to_string(index=False)}")
