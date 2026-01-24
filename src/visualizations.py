import plotly.graph_objects as go
import pandas as pd

def deposits_by_job_chart(df: pd.DataFrame, channel: str) -> go.Figure:
    """
    Returns a bar chart of deposits by job for a given channel.
    """
    filtered = df[df['channel'] == channel]
    summary = filtered[filtered['deposit'] == 1].groupby('job').size().reset_index(name='deposits')

    fig = go.Figure([go.Bar(x=summary['job'], y=summary['deposits'])])
    fig.update_layout(
        title=f"Deposits by Job - Channel: {channel}",
        xaxis_title="Job",
        yaxis_title="Number of Deposits"
    )
    return fig

def campaign_effectiveness_chart(df: pd.DataFrame, channel: str, start_date: str, end_date: str) -> go.Figure:
    """
    Returns a line chart of campaign effectiveness over time for a given channel and date range.
    """
    filtered = df[
        (df['channel'] == channel) &
        (df['contact_date'] >= start_date) &
        (df['contact_date'] <= end_date)
    ]
    summary = filtered.groupby('contact_date')['deposit'].agg(['count', 'sum']).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=summary['contact_date'], y=summary['count'],
        mode="lines+markers", name="Total Contacts"
    ))
    fig.add_trace(go.Scatter(
        x=summary['contact_date'], y=summary['sum'],
        mode="lines+markers", name="Total Deposits"
    ))
    fig.update_layout(
        title=f"Campaign Effectiveness - Channel: {channel}",
        xaxis_title="Date",
        yaxis_title="Count"
    )
    return fig
