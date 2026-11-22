# 02 - Perguntas de negócio

Imaginei a gestão de um marketplace que se preocupa com três coisas: o cliente receber no prazo, a nota que ele dá e de onde vem a receita. Fiquei com cinco perguntas que os dados conseguem responder.

| # | Pergunta | Métrica |
|---|---|---|
| 1 | Entregar depois do prazo derruba a nota do cliente? | Nota média e % de notas 1 e 2, com e sem atraso |
| 2 | Quais categorias geram mais receita, e quais têm pior nota ou mais atraso? | Receita, nota média e % de atraso por categoria |
| 3 | Como pedidos e receita evoluíram mês a mês? | Pedidos e receita por mês (jan/2017 a ago/2018) |
| 4 | Quais estados têm o pior prazo de entrega? | Dias médios e % de atraso por estado do cliente |
| 5 | Como os clientes pagam? | Participação de cada meio de pagamento e parcelas no cartão |

## Regras de cálculo
- Receita = soma de `price` (sem frete), sem pedidos cancelados ou indisponíveis.
- Atraso = entrega depois da data estimada; só entra pedido com data de entrega.
- Tendências mensais só de jan/2017 a ago/2018.
- Uma avaliação por pedido (a mais recente).

## Ficou de fora
- **Texto dos comentários:** exige tratamento de texto, outra habilidade.
- **Margem de lucro:** a base não tem o custo dos produtos.
- **Previsão de vendas:** são só 20 meses completos, pouco para um modelo confiável.
