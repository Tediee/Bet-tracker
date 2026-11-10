import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("📈 Dashboard")

conn = sqlite3.connect("bets.db")

df = pd.read_sql_query(
    "SELECT * FROM value_opportunities",
    conn
)

if not df.empty:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Opportunities",
        len(df)
    )

    col2.metric(
        "Average Edge",
        f"{df['edge'].mean():.2f}%"
    )

    col3.metric(
        "Best Edge",
        f"{df['edge'].max():.2f}%"
    )

    bookmaker_counts = (
        df["bookmaker"]
        .value_counts()
        .reset_index()
    )

    bookmaker_counts.columns = [
        "Bookmaker",
        "Count"
    ]

    fig = px.bar(
        bookmaker_counts,
        x="Bookmaker",
        y="Count",
        title="Value Opportunities by Bookmaker",
        color="Bookmaker"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    market_counts = (
        df["market_type"]
        .value_counts()
        .reset_index()
    )

    market_counts.columns = [
        "Market",
        "Count"
    ]

    fig = px.pie(
        market_counts,
        names="Market",
        values="Count",
        title="Market Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.histogram(
        df,
        x="edge",
        nbins=15,
        title="Edge Distribution (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No opportunities recorded yet."
    )