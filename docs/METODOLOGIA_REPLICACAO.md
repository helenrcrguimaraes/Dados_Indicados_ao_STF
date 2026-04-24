# Metodologia de replicação

Este pacote reproduz as tabelas quantitativas da pesquisa por meio de scripts Python independentes.

## Métodos utilizados

- Estatística descritiva: média, mediana, desvio-padrão amostral, mínimo e máximo.
- Mann-Kendall clássico: usado para tendências temporais monotônicas. A estatística reportada é tau-a, conforme `pymannkendall.original_test`.
- Teste de Pettitt: usado para detecção de ponto de mudança em séries temporais. Implementação própria documentada em `codigo/utilidades_00.py`.
- Kendall tau-b: usado em associações entre variáveis, com correção de empates via `scipy.stats.kendalltau(variant="b")`.
- Spearman: usado como análise complementar de associação ordinal.
- Mann-Whitney U: usado para comparação entre grupos.

## Como replicar

1. Criar ambiente virtual.
2. Instalar dependências com `pip install -r requirements.txt`.
3. Executar `python run_all.py`.
4. Conferir os resultados na pasta `outputs/`.

## Integridade dos dados

Os hashes SHA-256 dos CSVs originais estão em `docs/SHA256SUMS.txt`.
