# 01 - Exploração inicial dos dados

Objetivo: entender cada tabela antes de analisar: tamanho, período, nulos e inconsistências.

## Tamanho das tabelas
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

Os pedidos vão de 04/09/2016 a 17/10/2018. Status: 96.478 delivered, 1.107 shipped, 625 canceled, 609 unavailable, 314 invoiced, 301 processing, 5 created e 2 approved.

## Problemas encontrados
1. **Período irregular.** Em 2016 há 4 pedidos em setembro, 324 em outubro e 1 em dezembro. Em set/2018 são 16 e em out/2018, 4, contra mais de 6.000 por mês em jul e ago. Vou analisar tendências só de jan/2017 a ago/2018.
2. **Datas nulas em orders.** 160 sem aprovação, 1.783 sem envio à transportadora e 2.965 sem entrega. Quase todas são pedidos não entregues, mas 8 pedidos "delivered" estão sem data de entrega (e 14 sem data de aprovação). Os 8 ficam fora do cálculo de prazo.
3. **Avaliações duplicadas.** 551 linhas repetem `order_id` em order_reviews. Fico com a mais recente de cada pedido.
4. **610 produtos sem categoria.** Agrupo como `sem_categoria`.
5. **3 pagamentos `not_defined`.** Mantidos e sinalizados.
6. **Erro de grafia na origem:** `product_name_lenght` e `product_description_lenght`.
7. **Tradução incompleta.** A tabela tem 71 categorias; `pc_gamer` e `portateis_cozinha_e_preparadores_de_alimentos` ficaram sem tradução.

## Primeiros números (sem tratamento)
- Entregas depois do prazo prometido: 7.827 de 96.476 (8,1%).
- Prazo médio entre compra e entrega: 12,6 dias.
- Nota média das avaliações: 4,09.
- Soma de `price`: R$ 13.591.644; soma de `freight_value`: R$ 2.251.910 (todos os status).
- Pagamentos por registro: cartão de crédito 76.795, boleto 19.784, voucher 5.775, débito 1.529.
