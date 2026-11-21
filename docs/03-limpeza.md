# 03 - Limpeza e padronização

Data: 21/11/2026 | Status: concluído | Código: [`notebooks/03_limpeza.py`](../notebooks/03_limpeza.py)

## Objetivo
Transformar os CSVs brutos em tabelas confiáveis, resolvendo os problemas anotados no arquivo 01, sem apagar informação que possa ser útil.

## O que o script faz e o resultado conferido
| Problema (arquivo 01) | O que fiz | Conferência depois da limpeza |
|---|---|---|
| 551 avaliações repetidas por pedido | Mantive a mais recente de cada pedido | 99.224 linhas viraram 98.673; nenhum `order_id` repetido |
| 8 pedidos "delivered" sem data de entrega | Marquei com a coluna `entrega_sem_data` e deixei vazias as colunas calculadas de prazo e atraso | 8 marcados, nenhum apagado |
| Período irregular | Criei a coluna `periodo_completo` (jan/2017 a ago/2018) em vez de excluir linhas | 99.092 dos 99.441 pedidos estão no período completo |
| 610 produtos sem categoria | Categoria passou a ser `sem_categoria` | 610 produtos com esse valor |
| 2 categorias sem tradução | Acrescentei a tradução manualmente no código (`pc_gamer` e `portateis_cozinha_e_preparadores_de_alimentos`) | Nenhuma categoria com nome português restante, exceto as sem categoria |
| Erro de grafia nas colunas | Renomeei `product_name_lenght` e `product_description_lenght` | Colunas agora com `length` |

Colunas novas na tabela de pedidos: `dias_para_entrega`, `dias_de_atraso`, `entregue_com_atraso`, `mes_compra`, `entrega_sem_data` e `periodo_completo`.

## Correção do arquivo 01
No arquivo 01 escrevi que o prazo médio de entrega era 12,1 dias. Esse número usou apenas dias inteiros (a parte fracionária era descartada). Calculando com horas e minutos, o prazo médio é **12,6 dias**. O percentual de pedidos entregues com atraso continua **8,1%** (7.827 de 96.476). Registro aqui o erro para o histórico ficar honesto.

## Erro que encontrei durante o trabalho
A primeira versão do script falhou ao marcar os valores vazios na coluna de atraso, porque a coluna era do tipo booleano comum, que não aceita vazio. Troquei para o tipo booleano que aceita vazio. Efeito colateral importante que corrigi junto: pedidos sem data de entrega estavam sendo contados como "não atrasados" (falso) em vez de "sem informação" (vazio), o que reduziria o percentual de atraso.

## Como executar
```
pip install pandas
python notebooks/03_limpeza.py
```
Os dados brutos devem estar em `data/raw/` (ver README). As tabelas limpas saem em `data/processed/`, que não é versionada.

## Próximo passo
Carregar as tabelas limpas em um banco relacional e responder às perguntas do arquivo 02 com SQL (etapa 04).
