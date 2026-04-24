# Pacote de replicação — indicações ao STF sob a Constituição de 1988

Este repositório contém os dados e scripts necessários para replicar as análises quantitativas da pesquisa empírica sobre o processo de apreciação, pelo Senado Federal, das indicações ao Supremo Tribunal Federal.

## Estrutura

```text
.
├── codigo/      # scripts Python da análise
├── dados/       # bases CSV utilizadas
├── outputs/     # tabelas geradas pela execução
├── docs/        # dicionário, metodologia e hashes
├── tests/       # espaço para testes de validação
├── run_all.py   # executa todo o pipeline
├── requirements.txt
├── CITATION.cff
└── LICENSE
```

## Replicação

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python run_all.py
```

Os arquivos gerados aparecerão em `outputs/`.

## Dados

Os dados estão em `dados/`. As séries temporais devem permanecer em ordem cronológica, pois os testes de Mann-Kendall e Pettitt dependem da ordem das observações.
