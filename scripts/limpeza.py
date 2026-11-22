# Limpeza dos dados do Olist (etapa 03).
# Lê data/raw/*.csv e grava as tabelas limpas em data/processed/.
# As decisões estão explicadas em docs/03-limpeza.md.
# Uso: python scripts/limpeza.py
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

# duas categorias que ficaram sem tradução na tabela original (ver docs/01)
TRADUCAO_MANUAL = {
    "pc_gamer": "pc_gamer",
    "portateis_cozinha_e_preparadores_de_alimentos": "portable_kitchen_and_food_preparers",
}

COLUNAS_DATA = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def limpar_pedidos():
    pedidos = pd.read_csv(RAW / "olist_orders_dataset.csv", parse_dates=COLUNAS_DATA)

    # divido por 86400 para ter dias com fração (a versão só com .dt.days dava 12,1)
    pedidos["dias_para_entrega"] = (
        pedidos["order_delivered_customer_date"] - pedidos["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    pedidos["dias_de_atraso"] = (
        pedidos["order_delivered_customer_date"] - pedidos["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    # tipo "boolean" aceita vazio: pedido sem entrega não pode contar como "não atrasou"
    pedidos["entregue_com_atraso"] = (pedidos["dias_de_atraso"] > 0).astype("boolean").where(
        pedidos["dias_de_atraso"].notna()
    )
    pedidos["mes_compra"] = pedidos["order_purchase_timestamp"].dt.to_period("M").astype(str)

    # marco em vez de apagar os "delivered" sem data de entrega
    pedidos["entrega_sem_data"] = (pedidos["order_status"] == "delivered") & pedidos[
        "order_delivered_customer_date"
    ].isna()

    # 2016 e set/out de 2018 têm pouquíssimos pedidos; ficam fora das tendências
    pedidos["periodo_completo"] = pedidos["order_purchase_timestamp"].between(
        "2017-01-01", "2018-08-31 23:59:59"
    )
    return pedidos


def limpar_avaliacoes():
    av = pd.read_csv(
        RAW / "olist_order_reviews_dataset.csv",
        parse_dates=["review_creation_date", "review_answer_timestamp"],
    )
    # alguns pedidos têm mais de uma avaliação; fico com a mais recente
    av = av.sort_values(["order_id", "review_answer_timestamp"]).drop_duplicates(
        "order_id", keep="last"
    )
    return av[["order_id", "review_id", "review_score", "review_creation_date"]]


def limpar_produtos():
    prod = pd.read_csv(RAW / "olist_products_dataset.csv")
    prod = prod.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        }
    )
    trad = pd.read_csv(RAW / "product_category_name_translation.csv", encoding="utf-8-sig")
    mapa = dict(zip(trad["product_category_name"], trad["product_category_name_english"]))
    mapa.update(TRADUCAO_MANUAL)
    prod["categoria"] = prod["product_category_name"].map(mapa).fillna("sem_categoria")
    return prod


def main():
    tabelas = {
        "orders": limpar_pedidos(),
        "order_reviews": limpar_avaliacoes(),
        "products": limpar_produtos(),
        "order_items": pd.read_csv(
            RAW / "olist_order_items_dataset.csv", parse_dates=["shipping_limit_date"]
        ),
        "order_payments": pd.read_csv(RAW / "olist_order_payments_dataset.csv"),
        "customers": pd.read_csv(RAW / "olist_customers_dataset.csv"),
        "sellers": pd.read_csv(RAW / "olist_sellers_dataset.csv"),
    }
    for nome, df in tabelas.items():
        df.to_csv(OUT / f"{nome}.csv", index=False)
        print(f"{nome}: {len(df)} linhas")


if __name__ == "__main__":
    main()
