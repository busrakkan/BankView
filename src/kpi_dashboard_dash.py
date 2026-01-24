import pandas as pd
import sqlite3
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from visualization import aggregate_trends

DB_PATH = "data/bankview.db"

conn = sqlite3.connect(DB_PATH)
customers = pd.read_sql("SELECT * FROM customers", conn)
campaigns = pd.read_sql("SELECT * FROM campaigns", conn)
products = pd.read_sql("SELECT * FROM products", conn)
conn.close()

campaigns["contact_date"] = pd.to_datetime(campaigns["contact_date"], errors="coerce")

app = Dash(__name__)
app.title = "BankView KPI Dashboard"

app.layout = html.Div([
    html.H1("BANKVIEW KPI DASHBOARD", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id="date-picker",
                min_date_allowed=campaigns["contact_date"].min(),
                max_date_allowed=campaigns["contact_date"].max(),
                start_date=campaigns["contact_date"].min(),
                end_date=campaigns["contact_date"].max()
            )
        ], style={"display": "inline-block", "margin-right": "30px"}),

        html.Div([
            html.Label("Select Product Type:"),
            dcc.Dropdown(
                id="product-dropdown",
                options=[
                    {"label": "All", "value": "all"},
                    {"label": "Deposit", "value": "deposit"},
                    {"label": "Loan", "value": "loan"}
                ],
                value="all"
            )
        ], style={"display": "inline-block"})
    ], style={"margin": "20px"}),

    dcc.Tabs([
        dcc.Tab(label="Deposits Trend", children=[dcc.Graph(id="deposits-trend")]),
        dcc.Tab(label="Loans Trend", children=[dcc.Graph(id="loans-trend")]),
        dcc.Tab(label="Average Balance", children=[dcc.Graph(id="avg-balance")]),
        dcc.Tab(label="Customer Growth", children=[dcc.Graph(id="customer-growth")])
    ])
])

@app.callback(
    Output("deposits-trend", "figure"),
    Output("loans-trend", "figure"),
    Output("avg-balance", "figure"),
    Output("customer-growth", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    Input("product-dropdown", "value")
)
def update_charts(start_date, end_date, product_filter):
    product_filter_value = product_filter if product_filter != "all" else None
    trends = aggregate_trends(customers, campaigns, products, start_date, end_date, product_filter_value)

    fig_deposits = px.line(trends, x="contact_date", y="total_deposits", title="Total Deposits Over Time")
    fig_loans = px.line(trends, x="contact_date", y="total_loans", title="Total Loans Over Time")
    fig_avg_balance = px.line(trends, x="contact_date", y="avg_balance", title="Average Balance Over Time")
    fig_customers = px.line(trends, x="contact_date", y="total_customers", title="Total Customers Over Time")

    return fig_deposits, fig_loans, fig_avg_balance, fig_customers

if __name__ == "__main__":
    app.run(debug=True, port=8050)
