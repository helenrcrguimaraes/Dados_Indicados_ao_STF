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

## Citação

Após publicar o repositório no GitHub e arquivá-lo no Zenodo/OSF, atualizar `CITATION.cff` com a URL e o DOI.

## DOI

Fluxo recomendado:

1. Criar repositório no GitHub.
2. Fazer commit e push desta estrutura.
3. Criar uma release `v1.0.0`.
4. Conectar o GitHub ao Zenodo.
5. Arquivar a release no Zenodo.
6. Copiar o DOI gerado para `CITATION.cff` e para a tese.

## Licença

Sugerida: CC BY 4.0 para dados e documentação. Caso os scripts sejam separados, pode-se usar MIT para código e CC BY 4.0 para dados.
