# Dicionário de dados

## `ccj_votacao.csv`
- `indicado`: pessoa indicada ao STF.
- `favoraveis`: votos favoráveis na CCJ.
- `contrarios`: votos contrários na CCJ.
- `abstencoes`: abstenções registradas na CCJ.
- `ausencias`: ausências registradas na CCJ.
- `quorum`: total de membros considerado para cálculo percentual.

## `plenario_votacao.csv`
- Mesma lógica de votação, aplicada ao Plenário do Senado.

## `tramitacao_tempos.csv`
- `tempo_total`: dias entre a indicação e a decisão final.
- `tempo_distribuicao`: dias até a distribuição/relatoria.

## `incidentes_procedimentais.csv`
- Variáveis binárias de incidentes procedimentais: sem pauta prévia, adiamento/suspensão, vista coletiva e dispensa do interstício.

## `partidos_posicoes.csv`
- Partidos e pessoas ocupantes das posições-chave em cada indicação: Presidência da República, Presidência do Senado, Presidência da CCJ e relatoria.

## `sabatinas_quantitativo.csv`
- `senadores`: número de senadores que formularam indagações.
- `indagacoes`: total de indagações registradas.
- `elogios`: manifestações positivas sem indagação.
- `rejeicao`: manifestações negativas sem indagação.
- `outras`: manifestações sem indagação e sem caráter claro de elogio ou rejeição.
- `tempo_h`: duração da sabatina em horas.

## `temas_indagacoes.csv`
- Uma linha por indagação classificada.
- `indicado`: pessoa indicada associada à sabatina.
- `macrocategoria`: grupo temático agregado.
- `categoria`: categoria temática específica.

## Observação metodológica
As séries usadas em Mann-Kendall e Pettitt devem permanecer em ordem cronológica. Não reordenar os CSVs antes da execução, salvo se for acrescentada variável temporal explícita e `sort_values()` nos scripts.
