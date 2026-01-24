import sqlite3
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import os

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "bankview.db"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def load_kpis():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COUNT(*) AS total_customers,
            SUM(deposit) AS total_deposits,
            ROUND(SUM(deposit)*100.0/COUNT(*), 2) AS conversion_rate,
            ROUND(AVG(CASE WHEN deposit=0 THEN balance END), 2) AS avg_balance_no_deposit,
            ROUND(AVG(CASE WHEN deposit=1 THEN balance END), 2) AS avg_balance_deposit
        FROM customers c
        JOIN products p ON c.customer_id = p.customer_id
    """)
    row = cursor.fetchone()
    conn.close()
    kpis = {
        "total_customers": row[0],
        "total_deposits": row[1],
        "conversion_rate": row[2],
        "avg_balance_no_deposit": row[3],
        "avg_balance_deposit": row[4]
    }
    return kpis

def create_kpi_figure(kpis):
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["total_customers"],
        title={"text": "Total Customers"},
        domain={'row': 0, 'column': 0}
    ))
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["total_deposits"],
        title={"text": "Total Deposits"},
        domain={'row': 0, 'column': 1}
    ))
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["conversion_rate"],
        number={"suffix": "%"},
        title={"text": "Conversion Rate"},
        domain={'row': 1, 'column': 0}
    ))
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["avg_balance_no_deposit"],
        title={"text": "Avg Balance (No Deposit)"},
        domain={'row': 1, 'column': 1}
    ))
    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["avg_balance_deposit"],
        title={"text": "Avg Balance (Deposit)"},
        domain={'row': 2, 'column': 0}
    ))

    fig.update_layout(
        grid={"rows": 3, "columns": 2, "pattern": "independent"},
        height=600,
        title="BANKVIEW KPI SUMMARY"
    )

    return fig

if __name__ == "__main__":
    kpis = load_kpis()
    print("\n BANKVIEW KPI SUMMARY ")
    for k, v in kpis.items():
        print(f"{k}: {v}")

    fig = create_kpi_figure(kpis)
    png_path = REPORTS_DIR / "kpi_summary.png"
    try:
        fig.write_image(png_path, scale=2)
        print(f"\nKPI chart saved as: {png_path}")
    except ValueError as e:
        print("\nCannot save image: ", e)
        print("Install Kaleido: pip install --upgrade kaleido")
