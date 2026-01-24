import pandas as pd

def aggregate_trends(customers, campaigns, products, start_date=None, end_date=None, product_filter=None):
    df = campaigns.merge(products, on="customer_id").merge(customers, on="customer_id")

    df["contact_date"] = pd.to_datetime(df["contact_date"], errors="coerce")

    df = df.dropna(subset=["contact_date"])

    if start_date:
        df = df[df["contact_date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["contact_date"] <= pd.to_datetime(end_date)]

    if product_filter == "deposit":
        df = df[df["deposit"] == 1]
    elif product_filter == "loan":
        df = df[df["loan"] == 1]

    trends = df.groupby("contact_date").agg(
        total_deposits=("deposit", "sum"),
        total_loans=("loan", "sum"),
        avg_balance=("balance", "mean"),
        total_customers=("customer_id", "nunique")
    ).reset_index()

    return trends
