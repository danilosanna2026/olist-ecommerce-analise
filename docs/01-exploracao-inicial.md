# 01 - Exploração inicial dos dados

Data: 21/11/2026 | Status: concluído

## Objetivo desta etapa
Entender o que existe em cada tabela antes de qualquer análise: tamanho, período, valores nulos e inconsistências.

## O que encontrei

**Tamanho das tabelas (linhas)**
| Tabela | Linhas |
|---|---|
| orders | 99.441 |
| order_items | 112.650 |
| order_payments | 103.886 |
| order_reviews | 99.224 |
| customers | 99.441 |
| products | 32.951 |
| sellers | 3.095 |
| geolocation | 1.000.163 |
| category_translation | 71 |

**Período dos pedidos:** 04/09/2016 a 17/10/2018.

**Status dos pedidos:** 96.478 delivered, 1.107 shipped, 625 canceled, 609 unavailable, 314 invoiced, 301 processing, 5 created, 2 approved.

## Problemas encontrados nos dados (e o que fazer em cada um)
1. **Período irregular.** Em 2016 há só 4 pedidos em setembro, 324 em outubro e 1 em dezembro. Em 2018, setembro tem 16 e outubro 4, contra mais de 6.000 por mês em julho e agosto. *Decisão a tomar:* analisar tendência mensal apenas no período completo (jan/2017 a ago/2018) e registrar isso no README.
2. **Datas nulas em orders.** 160 sem data de aprovação, 1.783 sem data de envio à transportadora e 2.965 sem data de entrega ao cliente. Quase todas correspondem a pedidos não entregues (cancelados, indisponíveis, em trânsito etc.), mas **8 pedidos "delivered" estão sem data de entrega** e 14 "delivered" estão sem data de aprovação. *Decisão:* excluir esses 8 do cálculo de prazo e documentar.
3. **Reviews duplicadas.** 551 linhas de `order_id` repetido em order_reviews. *Decisão:* manter apenas a avaliação mais recente por pedido antes de juntar com orders, para não duplicar pedidos nas métricas.
4. **Produtos sem categoria.** 610 produtos com `product_category_name` nulo. *Decisão:* agrupar como "sem categoria" em vez de descartar.
5. **Tipo de pagamento "not_defined".** 3 registros. *Decisão:* manter e sinalizar.
6. **Nome de coluna com erro de grafia** na origem (`product_name_lenght`, `product_description_lenght`). Mantido como está na carga bruta e renomeado na camada limpa.
7. **Tradução de categorias incompleta.** A tabela de tradução tem 71 linhas e duas categorias de produtos não têm tradução: `pc_gamer` e `portateis_cozinha_e_preparadores_de_alimentos`. *Decisão:* traduzir manualmente essas duas e registrar no código.

## Primeiros números (ainda sem tratamento; servem só para orientar)
- Entregas com data real maior que a prometida: 7.827 de 96.476 (8,1%).
- Prazo médio entre compra e entrega: 12,1 dias.
- Nota média das avaliações: 4,09.
- Soma de `price` dos itens: R$ 13.591.644 e de `freight_value`: R$ 2.251.910 (todos os status juntos).
- Meios de pagamento por registro: cartão de crédito 76.795, boleto 19.784, voucher 5.775, cartão de débito 1.529.

## Próximos passos
- Definir as perguntas de negócio (arquivo 02).
- Limpar e padronizar com Python/pandas (arquivo 03).
- Carregar em banco relacional e escrever as consultas SQL (arquivo 04).
