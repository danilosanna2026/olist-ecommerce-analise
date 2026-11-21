-- Etapa 04 - Respostas às 5 perguntas de negócio (docs/02-perguntas-de-negocio.md)
-- PostgreSQL. Regras: receita = soma de price (sem frete), sem pedidos
-- cancelados/indisponíveis; atraso = entrega depois da data estimada;
-- tendências só no período completo (jan/2017 a ago/2018).

-- P1. Pedido entregue com atraso recebe nota pior?
SELECT CASE WHEN o.entregue_com_atraso THEN 'com atraso' ELSE 'no prazo' END AS entrega,
       COUNT(*)                              AS pedidos,
       ROUND(AVG(r.review_score), 2)         AS nota_media,
       ROUND(100.0 * AVG((r.review_score <= 2)::int), 1) AS pct_notas_1_e_2
FROM orders o
JOIN order_reviews r ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.entregue_com_atraso IS NOT NULL
GROUP BY 1
ORDER BY 1 DESC;

-- P2. Categorias: receita, nota média e % de atraso (mín. 100 pedidos)
WITH itens AS (
    SELECT i.order_id, p.categoria, SUM(i.price) AS receita
    FROM order_items i
    JOIN orders o   ON o.order_id = i.order_id
    JOIN products p ON p.product_id = i.product_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY i.order_id, p.categoria
)
SELECT it.categoria,
       COUNT(DISTINCT it.order_id)                 AS pedidos,
       ROUND(SUM(it.receita), 0)                   AS receita,
       ROUND(AVG(r.review_score), 2)               AS nota_media,
       ROUND(100.0 * AVG(o.entregue_com_atraso::int), 1) AS pct_atraso
FROM itens it
JOIN orders o ON o.order_id = it.order_id
LEFT JOIN order_reviews r ON r.order_id = it.order_id
GROUP BY it.categoria
HAVING COUNT(DISTINCT it.order_id) >= 100
ORDER BY receita DESC
LIMIT 15;

-- P3. Pedidos e receita por mês (jan/2017 a ago/2018)
SELECT o.mes_compra,
       COUNT(DISTINCT o.order_id) AS pedidos,
       ROUND(SUM(i.price), 0)     AS receita
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
WHERE o.periodo_completo
  AND o.order_status NOT IN ('canceled', 'unavailable')
GROUP BY o.mes_compra
ORDER BY o.mes_compra;

-- P4. Estados com pior prazo de entrega (mín. 500 pedidos entregues)
SELECT c.customer_state                         AS estado,
       COUNT(*)                                    AS pedidos,
       ROUND(AVG(o.dias_para_entrega), 1)       AS dias_medios,
       ROUND(100.0 * AVG(o.entregue_com_atraso::int), 1) AS pct_atraso
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_status = 'delivered'
  AND o.dias_para_entrega IS NOT NULL
GROUP BY c.customer_state
HAVING COUNT(*) >= 500
ORDER BY dias_medios DESC;

-- P5a. Formas de pagamento: pedidos e valor
SELECT payment_type                              AS forma,
       COUNT(DISTINCT order_id)                  AS pedidos,
       ROUND(SUM(payment_value), 0)              AS valor,
       ROUND(100.0 * SUM(payment_value) / SUM(SUM(payment_value)) OVER (), 1) AS pct_valor
FROM order_payments
WHERE payment_type <> 'not_defined'
GROUP BY payment_type
ORDER BY valor DESC;

-- P5b. Cartão de crédito: parcelas escolhidas e ticket médio por faixa
SELECT CASE WHEN payment_installments = 1 THEN '1x (1 parcela)'
            WHEN payment_installments BETWEEN 2 AND 5  THEN '2 a 5x'
            WHEN payment_installments BETWEEN 6 AND 10 THEN '6 a 10x'
            ELSE 'mais de 10x' END               AS parcelas,
       COUNT(*)                                  AS pagamentos,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct,
       ROUND(AVG(payment_value), 0)              AS ticket_medio
FROM order_payments
WHERE payment_type = 'credit_card'
  AND payment_installments >= 1   -- 2 registros com 0 parcelas ficam de fora
GROUP BY 1
ORDER BY MIN(payment_installments);
