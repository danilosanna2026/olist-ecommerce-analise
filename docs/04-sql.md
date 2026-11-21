# 04 - SQL: tabelas e respostas às perguntas

Data: 21/11/2026 | Status: concluído | Código: [`sql/`](../sql/)

## O que foi feito
1. Criei as 7 tabelas no PostgreSQL com chaves primárias e estrangeiras ([`sql/01_schema.sql`](../sql/01_schema.sql)).
2. Carreguei os CSVs limpos com `\copy` ([`sql/load.sh`](../sql/load.sh)). As contagens batem com a etapa 3: 99.441 pedidos, 112.650 itens, 103.886 pagamentos, 98.673 avaliações. As chaves estrangeiras passaram sem erro, então não há item, pagamento ou avaliação sem pedido.
3. Escrevi uma consulta para cada pergunta do arquivo 02 ([`sql/02_consultas.sql`](../sql/02_consultas.sql)) e conferi duas delas com pandas (nota média por atraso e pedidos/receita por mês): os números são iguais.

## Respostas
**P1. Atraso e nota.** Pedidos entregues no prazo: nota média 4,29 (9,2% com nota 1 ou 2). Entregues com atraso: nota média 2,57 (54,1% com nota 1 ou 2). A diferença é grande, mas mostra associação, não prova que o atraso sozinho causa a nota baixa.

**P2. Categorias.** Maior receita: health_beauty (R$ 1,26 mi), watches_gifts (R$ 1,20 mi) e bed_bath_table (R$ 1,04 mi). Entre as 15 maiores, a pior nota é office_furniture (3,62); bed_bath_table (3,97) também fica abaixo da média geral de 4,09.

**P3. Evolução mensal.** Os pedidos passam de 787 em jan/2017 para 7.421 em nov/2017 (pico; o mês inclui a Black Friday, mas os dados não provam que essa é a causa) e ficam entre cerca de 6.100 e 7.200 por mês em 2018. Não há sinal claro de crescimento depois de jan/2018.

**P4. Estados.** Pior prazo médio: PA (23,8 dias), MA (21,6) e CE (21,3). SP tem o melhor (8,8 dias). O maior percentual de atraso é do MA (19,7%).

**P5. Pagamento.** Cartão de crédito concentra 78,3% do valor e boleto 17,9%. No cartão, 33,1% dos pagamentos são em 1 parcela, 45,9% em 2 a 5 e 20,6% em 6 a 10; quanto mais parcelas, maior o ticket médio (R$ 96 em 1x, R$ 303 em 6 a 10x).

## Decisões e cuidados
- Pagamentos `not_defined` (3) ficam fora da P5a.
- 2 pagamentos no cartão com 0 parcelas ficam fora da P5b; parcelas acima de 10 aparecem agrupadas.
- Categorias e estados só entram com volume mínimo (100 e 500 pedidos) para a média não depender de poucos casos.

## Como reproduzir
```
createdb olist
bash sql/load.sh olist        # na raiz do projeto, com data/processed/ gerado
psql -d olist -f sql/02_consultas.sql
```

## Próximo passo
Dashboard no Power BI com essas respostas (etapa 5).
