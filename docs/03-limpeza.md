# 03 - Limpeza e padronização

Código: [`scripts/limpeza.py`](../scripts/limpeza.py). Resolve os problemas do doc 01 sem apagar informação útil.

| Problema | O que fiz | Conferência |
|---|---|---|
| 551 avaliações repetidas por pedido | Mantive a mais recente | 99.224 linhas viraram 98.673, sem `order_id` repetido |
| 8 pedidos "delivered" sem data de entrega | Coluna `entrega_sem_data`; prazo e atraso ficam vazios | 8 marcados, nenhum apagado |
| Período irregular | Coluna `periodo_completo` (jan/2017 a ago/2018) | 99.092 dos 99.441 pedidos |
| 610 produtos sem categoria | Valor `sem_categoria` | 610 produtos |
| 2 categorias sem tradução | Tradução manual no código | Nenhuma sem tradução |
| Colunas com `lenght` | Renomeadas para `length` | Ok |

Colunas novas em `orders`: `dias_para_entrega`, `dias_de_atraso`, `entregue_com_atraso`, `mes_compra`, `entrega_sem_data` e `periodo_completo`.

## Dois erros que corrigi no caminho
- **Prazo de 12,1 dias.** No doc 01 eu tinha calculado o prazo médio só com dias inteiros. Com horas e minutos, o valor é 12,6 dias. O percentual de atraso não mudou (8,1%).
- **Atraso como booleano comum.** A primeira versão do script falhou ao deixar a coluna de atraso vazia, porque o tipo booleano comum não aceita vazio. Trocar para o tipo que aceita vazio corrigiu outro problema: pedidos sem entrega estavam sendo contados como "não atrasados", o que reduziria o percentual de atraso.

## Como executar
```
pip install pandas
python scripts/limpeza.py
```
Os dados brutos ficam em `data/raw/` (ver README); as tabelas limpas saem em `data/processed/`, que não é versionada.
