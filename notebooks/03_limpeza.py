"""
Etapa 03 - Limpeza e padronização dos dados do Olist.

Entrada : data/raw/*.csv  (baixados do Kaggle, ver README)
Saída   : data/processed/*.csv (tabelas limpas, prontas para carregar em banco)

Cada decisão de limpeza está explicada em docs/03-limpeza.md.
Uso: python notebooks/03_limpeza.py
"""
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

# Traduções que faltam na tabela oficial (conferidas na etapa 01)
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


def limpar_pedidos() -> pd.DataFrame:
    pedidos = pd.read_csv(RAW / "olist_orders_dataset.csv", parse_dates=COLUNAS_DATA)

    # Colunas calculadas usadas nas análises
    pedidos["dias_para_entrega"] = (
        pedidos["order_delivered_customer_date"] - pedidos["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    pedidos["dias_de_atraso"] = (
        pedidos["order_delivered_customer_date"] - pedidos["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400
    # Fica vazio (NA) quando o pedido não tem data de entrega
    pedidos["entregue_com_atraso"] = (pedidos["dias_de_atraso"] > 0).astype("boolean").where(
        pedidos["dias_de_atraso"].notna()
    )
    pedidos["mes_compra"] = pedidos["order_purchase_timestamp"].dt.to_period("M").astype(str)

    # Pedido "delivered" sem data de entrega é inconsistente: marcamos em vez de apagar
    pedidos["entrega_sem_data"] = (pedidos["order_status"] == "delivered") & pedidos[
        "order_delivered_customer_date"
    ].isna()
    # (esses 8 já ficam vazios nas colunas calculadas acima, pois não têm data de entrega)

    # Meses com poucos pedidos (2016 e set/out 2018) ficam fora das tendências
    pedidos["periodo_completo"] = pedidos["order_purchase_timestamp"].between(
        "2017-01-01", "2018-08-31 23:59:59"
    )
    return pedidos


def limpar_avaliacoes() -> pd.DataFrame:
    av = pd.read_csv(
        RAW / "olist_order_reviews_dataset.csv",
        parse_dates=["review_creation_date", "review_answer_timestamp"],
    )
    # Há pedidos com mais de uma avaliação: ficamos com a mais recente
    av = av.sort_values(["order_id", "review_answer_timestamp"]).drop_duplicates(
        "order_id", keep="last"
    )
    return av[["order_id", "review_id", "review_score", "review_creation_date"]]


def limpar_produtos() -> pd.DataFrame:
    prod = pd.read_csv(RAW / "olist_products_dataset.csv")
    prod = prod.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        }
    )
    trad = pd.read_csv(
        RAW / "product_category_name_translation.csv", encoding="utf-8-sig"
    )
    mapa = dict(zip(trad["product_category_name"], trad["product_category_name_english"]))
    mapa.update(TRADUCAO_MANUAL)
    prod["categoria"] = prod["product_category_name"].map(mapa).fillna("sem_categoria")
    return prod


def main() -> None:
    pedidos = limpar_pedidos()
    avaliacoes = limpar_avaliacoes()
    produtos = limpar_produtos()

    itens = pd.read_csv(
        RAW / "olist_order_items_dataset.csv", parse_dates=["shipping_limit_date"]
    )
    pagamentos = pd.read_csv(RAW / "olist_order_payments_dataset.csv")
    clientes = pd.read_csv(RAW / "olist_customers_dataset.csv")
    vendedores = pd.read_csv(RAW / "olist_sellers_dataset.csv")

    tabelas = {
        "orders": pedidos,
        "order_reviews": avaliacoes,
        "products": produtos,
        "order_items": itens,
        "order_payments": pagamentos,
        "customers": clientes,
        "sellers": vendedores,
    }
    for nome, df in tabelas.items():
        df.to_csv(OUT / f"{nome}.csv", index=False)
        print(f"{nome}: {len(df):,} linhas".replace(",", "."))


if __name__ == "__main__":
    main()
