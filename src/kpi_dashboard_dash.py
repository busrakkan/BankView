import sqlite3
from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from visualization import deposits_by_job_chart, campaign_effectiveness_chart

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "bankview.db"

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

def load_channel_job_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT
            ca.contact AS channel,
            c.job,
            p.deposit
        FROM campaigns ca
        JOIN customers c ON ca.customer_id = c.customer_id
        JOIN products p ON c.customer_id = p.customer_id
    """, conn)
    conn.close()
    return df

def load_campaign_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT
            ca.contact_date,
            ca.contact AS channel,
            p.deposit
        FROM campaigns ca
        JOIN products p ON ca.customer_id = p.customer_id
    """, conn, parse_dates=["contact_date"])
    conn.close()
    return df

app = Dash(__name__)
channel_job_df = load_channel_job_data()
campaign_df = load_campaign_data()
kpis = load_kpis()

channels = channel_job_df['channel'].unique()
jobs = channel_job_df['job'].unique()
min_date, max_date = campaign_df['contact_date'].min(), campaign_df['contact_date'].max()

app.layout = html.Div([
    html.H1("BankView Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H3("Total Customers"),
            html.H4(f"{kpis['total_customers']}")
        ], style={"width": "18%", "display": "inline-block"}),

        html.Div([
            html.H3("Total Deposits"),
            html.H4(f"{kpis['total_deposits']}")
        ], style={"width": "18%", "display": "inline-block"}),

        html.Div([
            html.H3("Conversion Rate (%)"),
            html.H4(f"{kpis['conversion_rate']}")
        ], style={"width": "18%", "display": "inline-block"}),

        html.Div([
            html.H3("Avg Balance (No Deposit)"),
            html.H4(f"{kpis['avg_balance_no_deposit']}")
        ], style={"width": "22%", "display": "inline-block"}),

        html.Div([
            html.H3("Avg Balance (Deposit)"),
            html.H4(f"{kpis['avg_balance_deposit']}")
        ], style={"width": "22%", "display": "inline-block"})
    ], style={"textAlign": "center"}),

    html.Hr(),

    html.Div([
        html.H2("Deposits by Job & Channel"),
        html.Label("Select Channel:"),
        dcc.Dropdown(
            id="channel-dropdown",
            options=[{"label": ch, "value": ch} for ch in channels],
            value=channels[0]
        ),
        dcc.Graph(id="job-bar-chart")
    ]),

    html.Hr(),

    html.Div([
        html.H2("Campaign Effectiveness Over Time"),
        html.Label("Select Channel:"),
        dcc.Dropdown(
            id="campaign-channel-dropdown",
            options=[{"label": ch, "value": ch} for ch in channels],
            value=channels[0]
        ),
        dcc.DatePickerRange(
            id="date-range-picker",
            start_date=min_date,
            end_date=max_date,
            display_format="YYYY-MM-DD"
        ),
        dcc.Graph(id="campaign-line-chart")
    ])
])

@app.callback(
    Output("job-bar-chart", "figure"),
    Input("channel-dropdown", "value")
)
def update_job_chart(selected_channel):
    return deposits_by_job_chart(channel_job_df, selected_channel)

@app.callback(
    Output("campaign-line-chart", "figure"),
    [Input("campaign-channel-dropdown", "value"),
     Input("date-range-picker", "start_date"),
     Input("date-range-picker", "end_date")]
)
def update_campaign_chart(selected_channel, start_date, end_date):
    return campaign_effectiveness_chart(campaign_df, selected_channel, start_date, end_date)

if __name__ == "__main__":
    app.run_server(debug=True)
