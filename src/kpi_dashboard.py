import sqlite3
import pandas as pd

DB_PATH = "data/bankview.db"

def load_kpis():
    conn = sqlite3.connect(DB_PATH)
    customers = pd.read_sql("SELECT * FROM customers", conn)
    campaigns = pd.read_sql("SELECT * FROM campaigns", conn)
    products = pd.read_sql("SELECT * FROM products", conn)
    conn.close()

    total_customers = len(customers)
    total_deposits = products["deposit"].sum()
    conversion_rate = round(total_deposits / total_customers * 100, 2)
    avg_balance_deposit = round(customers[customers["customer_id"].isin(
        products[products["deposit"] == 1]["customer_id"]
    )]["balance"].mean(), 2)
    avg_balance_no_deposit = round(customers[~customers["customer_id"].isin(
        products[products["deposit"] == 1]["customer_id"]
    )]["balance"].mean(), 2)

    return {
        "total_customers": total_customers,
        "total_deposits": total_deposits,
        "conversion_rate": conversion_rate,
        "avg_balance_deposit": avg_balance_deposit,
        "avg_balance_no_deposit": avg_balance_no_deposit,
        "customers": customers,
        "campaigns": campaigns,
        "products": products
    }

def main():
    kpis = load_kpis()
    print("\n BANKVIEW KPI SUMMARY ")
    for key, value in kpis.items():
        if key not in ["customers", "campaigns", "products"]:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
