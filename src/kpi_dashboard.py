import sqlite3
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "bankview.db"
REPORTS_DIR = BASE_DIR / "reports" / "charts"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_kpis():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(DISTINCT c.customer_id) AS total_customers,
            SUM(p.deposit) AS total_deposits,
            ROUND(AVG(p.deposit) * 100, 2) AS conversion_rate
        FROM customers c
        JOIN products p ON c.customer_id = p.customer_id
    """)
    total_customers, total_deposits, conversion_rate = cursor.fetchone()

    cursor.execute("""
        SELECT
            p.deposit,
            ROUND(AVG(c.balance), 2)
        FROM customers c
        JOIN products p ON c.customer_id = p.customer_id
        GROUP BY p.deposit
        ORDER BY p.deposit
    """)
    balances = cursor.fetchall()

    conn.close()

    return {
        "total_customers": total_customers,
        "total_deposits": total_deposits,
        "conversion_rate": conversion_rate,
        "avg_balance_no_deposit": balances[0][1],
        "avg_balance_deposit": balances[1][1],
    }


def create_kpi_dashboard(kpis):
    fig = make_subplots(
        rows=2,
        cols=3,
        specs=[[{"type": "indicator"}] * 3,
               [{"type": "indicator"}] * 3],
        horizontal_spacing=0.08,
        vertical_spacing=0.25,
    )

    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["total_customers"],
        title={"text": "Total Customers"},
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["total_deposits"],
        title={"text": "Total Deposits"},
    ), row=1, col=2)

    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["conversion_rate"],
        number={"suffix": "%"},
        title={"text": "Conversion Rate"},
    ), row=1, col=3)

    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["avg_balance_no_deposit"],
        number={"prefix": "€"},
        title={"text": "Avg Balance (No Deposit)"},
    ), row=2, col=1)

    fig.add_trace(go.Indicator(
        mode="number",
        value=kpis["avg_balance_deposit"],
        number={"prefix": "€"},
        title={"text": "Avg Balance (Deposit)"},
    ), row=2, col=2)

    fig.update_layout(
        title=" BankView - KPI Summary Dashboard",
        height=600,
        margin=dict(t=80, l=40, r=40, b=40),
    )

    html_path = REPORTS_DIR / "kpi_summary.html"
    png_path = REPORTS_DIR / "kpi_summary.png"

    fig.write_html(html_path)
    fig.write_image(png_path, scale=2)

    print(f"Dashboard saved to:\n- {html_path}\n- {png_path}")

    fig.show()


if __name__ == "__main__":
    kpis = load_kpis()

    print("\n BANKVIEW KPI SUMMARY ")
    for k, v in kpis.items():
        print(f"{k}: {v}")

    create_kpi_dashboard(kpis)
