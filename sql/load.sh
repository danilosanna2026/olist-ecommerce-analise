#!/usr/bin/env bash
# Carrega os CSVs de data/processed/ no PostgreSQL.
# Uso: bash sql/load.sh <nome_do_banco>   (rode na raiz do projeto)
set -euo pipefail
DB="${1:-olist}"
PSQL="psql ${PSQLARGS:-} -d $DB -v ON_ERROR_STOP=1"
$PSQL -f sql/01_schema.sql
for t in customers sellers products orders order_items order_payments order_reviews; do
  $PSQL -c "\copy $t FROM 'data/processed/$t.csv' WITH (FORMAT csv, HEADER true)"
done
$PSQL -c "SELECT 'orders' t, count(*) FROM orders UNION ALL SELECT 'order_items', count(*) FROM order_items UNION ALL SELECT 'order_payments', count(*) FROM order_payments UNION ALL SELECT 'order_reviews', count(*) FROM order_reviews UNION ALL SELECT 'products', count(*) FROM products"
