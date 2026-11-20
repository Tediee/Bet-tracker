import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "bets.db"
)

st.set_page_config(
    page_title="BET_NANRI Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 BET_NANRI Dashboard")

try:

    conn = sqlite3.connect(DB_PATH)

    opportunities = pd.read_sql_query(
        """
        SELECT *
        FROM value_opportunities
        """,
        conn
    )

    alerts = pd.read_sql_query(
        """
        SELECT *
        FROM pinnacle_alerts
        """,
        conn
    )

    conn.close()

except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

    st.stop()

# =========================
# Latest Alert
# =========================

if not alerts.empty:

    latest_alert = (
        alerts.sort_values(
            "date",
            ascending=False
        )
        .head(1)
    )

    latest = latest_alert.iloc[0]

    st.success(
        f"""
🆕 Latest Alert

⚽ Match: {latest['match']}

🔥 Movement: {latest['movement']:.2f}%

📅 Time: {latest['date']}
"""
    )

# =========================
# Top 3 Alerts
# =========================

if not alerts.empty:

    st.subheader("🔥 Top 3 Alerts Right Now")

    top_three = (
        alerts.sort_values(
            "movement",
            ascending=False
        )
        .head(3)
    )

    for rank, (_, row) in enumerate(
        top_three.iterrows(),
        start=1
    ):

        st.info(
            f"""
#{rank}

⚽ {row['match']}

🏆 {row['league']}

📊 {row['market_type']}

📈 Pinnacle: {row['pinnacle_odds']}

🔥 Movement: {row['movement']:.2f}%
"""
        )

# =========================
# Alert Metrics
# =========================

if not alerts.empty:

    new_alerts = len(
        alerts[
            alerts["status"] == "NEW"
        ]
    )

else:

    new_alerts = 0

if opportunities.empty:

    opportunities_found = 0
    average_edge = 0
    best_edge = 0

else:

    opportunities_found = len(
        opportunities
    )

    average_edge = (
        opportunities["edge"]
        .mean()
    )

    best_edge = (
        opportunities["edge"]
        .max()
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚨 New Alerts",
    new_alerts
)

col2.metric(
    "💰 Opportunities",
    opportunities_found
)

col3.metric(
    "📈 Avg Edge",
    f"{average_edge:.2f}%"
)

col4.metric(
    "🏆 Best Edge",
    f"{best_edge:.2f}%"
)

# =========================
# Opportunities Section
# =========================

if not opportunities.empty:

    st.divider()

    st.subheader(
        "🏆 Top 10 Value Opportunities"
    )

    top_df = (
        opportunities
        .sort_values(
            "edge",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_df,
        use_container_width=True
    )

    # Bookmaker Counts

    bookmaker_counts = (
        opportunities["bookmaker"]
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

    # Market Distribution

    market_counts = (
        opportunities["market_type"]
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

    # Bookmaker Leaderboard

    st.subheader(
        "📊 Bookmaker Performance"
    )

    leaderboard = (
        opportunities
        .groupby(
            "bookmaker"
        )
        .agg({
            "edge": [
                "count",
                "mean",
                "max"
            ]
        })
    )

    st.dataframe(
        leaderboard,
        use_container_width=True
    )

    # Edge Distribution

    fig = px.histogram(
        opportunities,
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

st.divider()

st.caption(
    "BET_NANRI • Pinnacle Monitoring Dashboard"
)