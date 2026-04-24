"""
08_dispersao_associacoes.py — Testa associações entre o índice de dispersão
partidária e as variáveis de votação, tramitação e sabatinas. Corresponde
aos três parágrafos de análise da seção 3.7 da tese que começam com
"Os votos favoráveis ou contrários...", "O tempo de tramitação..." e
"As variáveis das sabatinas...".

Entradas: múltiplos CSVs de dados/
Saída:    outputs/dispersao_associacoes.csv

Testes:
    - Tau de Kendall (scipy.stats.kendalltau, variant='b') para correlação
      entre o índice e cada variável.
    - Mann-Whitney U (scipy.stats.mannwhitneyu, alternative='two-sided')
      comparando grupo de baixa dispersão (1 ou 2 partidos distintos) com
      grupo de alta dispersão (3 ou 4 partidos distintos).
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from utilidades_00 import indice_dispersao_partidaria  # noqa: E402


DIR_BASE = Path(__file__).parent.parent

# Carregar
par = pd.read_csv(DIR_BASE / "dados" / "partidos_posicoes.csv")
ccj = pd.read_csv(DIR_BASE / "dados" / "ccj_votacao.csv")
pln = pd.read_csv(DIR_BASE / "dados" / "plenario_votacao.csv")
tram = pd.read_csv(DIR_BASE / "dados" / "tramitacao_tempos.csv")
sab = pd.read_csv(DIR_BASE / "dados" / "sabatinas_quantitativo.csv")

# Dispersão
par["disp"] = par.apply(indice_dispersao_partidaria, axis=1)

ccj["pct_fav_ccj"] = ccj["favoraveis"] / ccj["quorum"] * 100
ccj["pct_con_ccj"] = ccj["contrarios"] / ccj["quorum"] * 100
pln["pct_fav_pln"] = pln["favoraveis"] / pln["quorum"] * 100
pln["pct_con_pln"] = pln["contrarios"] / pln["quorum"] * 100

# Merges (usando "disp" de par)
disp_ccj = par[["indicado", "disp"]].merge(ccj, on="indicado")
disp_pln = par[["indicado", "disp"]].merge(pln, on="indicado")
disp_tram = par[["indicado", "disp"]].merge(tram, on="indicado")
disp_tram27 = disp_tram[disp_tram["indicado"] != "André Mendonça"].reset_index(
    drop=True)
disp_sab = par[["indicado", "disp"]].merge(sab, on="indicado")

# Função para rodar Kendall + Mann-Whitney
def testa(df_, col, n_esperado=None):
    tau, p_k = stats.kendalltau(df_["disp"], df_[col], variant="b")
    g_baixa = df_[df_["disp"] <= 2][col]
    g_alta = df_[df_["disp"] >= 3][col]
    U, p_mw = stats.mannwhitneyu(g_baixa, g_alta, alternative="two-sided")
    return {
        "n": len(df_),
        "tau": round(tau, 4), "p_Kendall": round(p_k, 4),
        "baixa_media": round(g_baixa.mean(), 2), "n_baixa": len(g_baixa),
        "alta_media": round(g_alta.mean(), 2), "n_alta": len(g_alta),
        "U": round(U, 1), "p_MannWhitney": round(p_mw, 4),
    }

linhas = []
# Votação
for label, d, col in [
    ("% Favoráveis CCJ", disp_ccj, "pct_fav_ccj"),
    ("% Contrários CCJ", disp_ccj, "pct_con_ccj"),
    ("% Favoráveis Plenário", disp_pln, "pct_fav_pln"),
    ("% Contrários Plenário", disp_pln, "pct_con_pln"),
    ("Tempo total (n=28)", disp_tram, "tempo_total"),
    ("Tempo até distribuição (n=28)", disp_tram, "tempo_distribuicao"),
    ("Tempo total (n=27, s/ Mendonça)", disp_tram27, "tempo_total"),
    ("Tempo até distribuição (n=27)", disp_tram27, "tempo_distribuicao"),
    ("Senadores que indagaram", disp_sab, "senadores"),
    ("Indagações", disp_sab, "indagacoes"),
    ("Tempo de sabatina", disp_sab, "tempo_h"),
    ("Elogios", disp_sab, "elogios"),
    ("Rejeição", disp_sab, "rejeicao"),
]:
    r = testa(d, col)
    r["Variável"] = label
    linhas.append(r)

tab_disp = pd.DataFrame(linhas)
# Reordenar colunas
colunas = ["Variável", "n", "tau", "p_Kendall", "baixa_media", "n_baixa",
           "alta_media", "n_alta", "U", "p_MannWhitney"]
tab_disp = tab_disp[colunas]
tab_disp.to_csv(DIR_BASE / "outputs" / "dispersao_associacoes.csv", index=False)

print("=" * 70)
print("BLOCO 8 — ASSOCIAÇÕES COM DISPERSÃO PARTIDÁRIA")
print("=" * 70)
print(tab_disp.to_string(index=False))
