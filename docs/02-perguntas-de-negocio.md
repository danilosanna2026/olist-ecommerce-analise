# 02 - Perguntas de negócio

Data: 21/11/2026 | Status: concluído

## Como defini as perguntas (design thinking)
- **Empatizar:** quem usaria essa análise? Imaginei a gestão de um marketplace que vende produtos de vários lojistas e entrega pelo Brasil. Ela se preocupa com três coisas: o cliente receber no prazo, a nota que ele dá e de onde vem a receita.
- **Definir:** transformar essa preocupação em perguntas que os dados conseguem responder.
- **Idear e prototipar:** listar perguntas, descartar as que dependem de dados que não existem e ficar com poucas, bem respondidas.
- **Testar:** cada pergunta vira uma consulta SQL (etapa 04) e um visual no dashboard (etapa 05). Se a consulta não conseguir responder, a pergunta é refeita e a mudança fica registrada aqui.

## Perguntas escolhidas
| # | Pergunta | Métrica | Tabelas |
|---|---|---|---|
| 1 | Entregar depois do prazo prometido derruba a nota do cliente? | Nota média e % de notas 1 e 2, com e sem atraso | orders, order_reviews |
| 2 | Quais categorias geram mais receita, e quais têm pior nota ou mais atraso? | Receita (soma de `price`), nota média e % de atraso por categoria | order_items, products, orders, order_reviews |
| 3 | Como pedidos e receita evoluíram mês a mês? | Pedidos e receita por mês, apenas jan/2017 a ago/2018 | orders, order_items |
| 4 | Quais estados têm o pior prazo de entrega? | Dias médios de entrega e % de atraso por estado do cliente | orders, customers |
| 5 | Como os clientes pagam? | Participação de cada meio de pagamento e média de parcelas no cartão | order_payments |

## O que ficou de fora e por quê
- **Análise de comentários das avaliações:** exigiria tratamento de texto, que é outra habilidade; pode virar um projeto futuro.
- **Margem de lucro:** a base não tem custo dos produtos, então não dá para calcular.
- **Previsão de vendas:** a série completa tem só 20 meses, pouco para um modelo confiável.

## Regras de cálculo definidas antes de olhar os resultados
- Receita = soma de `price` dos itens, sem o frete, considerando pedidos que não foram cancelados nem estão indisponíveis.
- Atraso = data de entrega ao cliente maior que a data estimada. Só entra no cálculo pedido com data de entrega.
- Tendências mensais usam apenas jan/2017 a ago/2018, o período completo (ver arquivo 01).
- Uma avaliação por pedido (a mais recente).
