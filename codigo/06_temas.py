"""
06_temas.py — Distribuição temática das 1.114 indagações classificadas.

Gera:
    - Tabela 1 (frequência por macrocategoria)
    - Tabela 2 (frequência por categoria com presença em sabatinas)

Entrada: dados/temas_indagacoes.csv
Saídas:  outputs/tabela_01_macrocategorias.csv
         outputs/tabela_02_categorias.csv
"""

import pandas as pd
from pathlib import Path


DIR_BASE = Path(__file__).parent.parent
df = pd.read_csv(DIR_BASE / "dados" / "temas_indagacoes.csv")

# Padronização mínima
df["macrocategoria"] = df["macrocategoria"].astype(str).str.strip()
df["categoria"] = df["categoria"].astype(str).str.strip()

n = len(df)
assert n == 1114, f"Esperado 1.114 indagações, encontrado {n}"

# Tabela 1 — macrocategorias
vc_macro = df["macrocategoria"].value_counts().reset_index()
vc_macro.columns = ["Macrocategoria", "Frequência"]
vc_macro["%"] = (vc_macro["Frequência"] / n * 100).round(1)
vc_macro.to_csv(DIR_BASE / "outputs" / "tabela_01_macrocategorias.csv",
                index=False)

# Tabela 2 — categorias (com "presença em sabatinas")
cats = df["categoria"].value_counts().reset_index()
cats.columns = ["Categoria", "Frequência"]
cats["%"] = (cats["Frequência"] / n * 100).round(1)
cats["Presença em sabatinas"] = cats["Categoria"].apply(
    lambda c: df[df["categoria"] == c]["indicado"].nunique()
)
n_sabs = df["indicado"].nunique()
cats["Presença em sabatinas"] = cats["Presença em sabatinas"].astype(str) + f"/{n_sabs}"
cats.to_csv(DIR_BASE / "outputs" / "tabela_02_categorias.csv", index=False)

# Verificação da diferença entre Tabela 22 (total declarado) e banco (classificado)
# Lê as contagens declaradas em sabatinas_quantitativo.csv e compara com as
# contagens efetivas por sabatina no banco de temas.
sab = pd.read_csv(DIR_BASE / "dados" / "sabatinas_quantitativo.csv")

mapa_nomes = {
    "Cézar Peluso": "Cezar Peluso",
    "Carlos Ayres Britto": "Ayres Britto",
    "Kássio Nunes Marques": "Nunes Marques",
    "Luis Roberto Barroso": "Luís Roberto Barroso",
}
count_banco = df["indicado"].value_counts().rename("Banco_classificado")
count_banco.index = count_banco.index.to_series().replace(mapa_nomes)

count_decl = sab.set_index("indicado")["indagacoes"].rename("Tabela_22")
comp = pd.concat([count_decl, count_banco], axis=1).fillna(0).astype(int)
comp["Diferença"] = comp["Banco_classificado"] - comp["Tabela_22"]
comp_div = comp[comp["Diferença"] != 0]
comp.to_csv(DIR_BASE / "outputs" / "verificacao_1119_vs_1114.csv")

print("=" * 70)
print("BLOCO 6 — TEMAS DAS INDAGAÇÕES")
print("=" * 70)
print(f"\nTotal de indagações classificadas: {n}")
print(f"Sabatinas únicas: {n_sabs}")
print(f"Macrocategorias: {df['macrocategoria'].nunique()}")
print(f"Categorias: {df['categoria'].nunique()}")
print(f"\nTabela 1:\n{vc_macro.to_string(index=False)}")

print(f"\n--- Verificação: 1.119 vs 1.114 indagações ---")
print(f"Total declarado (Tabela 22): {comp['Tabela_22'].sum()}")
print(f"Total classificado (banco):  {comp['Banco_classificado'].sum()}")
print(f"Diferença: {int(comp['Banco_classificado'].sum() - comp['Tabela_22'].sum())}")
print(f"\nSabatinas com divergência:\n{comp_div.to_string()}")
