import streamlit as st
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "bets.db"
)

st.set_page_config(
    page_title="Live Alerts",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Live Pinnacle Alerts")

# Refresh Button

try:

    if st.button("🔄 Refresh Alerts"):
        st.rerun()

except Exception as e:

    st.error(
        f"Refresh Error: {e}"
    )

# Database

try:

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("""
    SELECT *
    FROM pinnacle_alerts
    WHERE date >= datetime('now', '-1 day')
    ORDER BY date DESC
    """, conn)

    conn.close()

except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

    st.stop()

# No alerts

if df.empty:

    st.warning(
        "No alerts recorded in the last 24 hours."
    )

    st.stop()

# League Filter

leagues = ["All"] + sorted(
    df["league"]
    .dropna()
    .unique()
)

selected_league = st.selectbox(
    "🏆 League Filter",
    leagues
)

if selected_league != "All":

    df = df[
        df["league"]
        == selected_league
    ]

# No results after filter

if df.empty:

    st.warning(
        "No alerts match selected filter."
    )

    st.stop()

# Metrics

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🚨 Total Alerts",
        len(df)
    )

with col2:

    st.metric(
        "📈 Biggest Move",
        f"{df['movement'].max():.2f}%"
    )

with col3:

    st.metric(
        "📊 Average Move",
        f"{df['movement'].mean():.2f}%"
    )

st.divider()

# High Severity Alerts

high_alerts = df[
    df["movement"] >= 20
]

if not high_alerts.empty:

    st.error(
        f"🚨 {len(high_alerts)} High Severity Alert(s) Above 20%"
    )

# Top Movers

st.subheader(
    "🔥 Top Movers"
)

top_movers = (
    df.sort_values(
        "movement",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_movers,
    use_container_width=True
)

st.divider()

# Latest Alerts

st.subheader(
    "📋 Latest Alerts"
)

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# Distribution Chart

st.subheader(
    "📈 Movement Distribution"
)

chart_df = (
    df.sort_values(
        "movement",
        ascending=False
    )
    .head(20)
)

if not chart_df.empty:

    st.bar_chart(
        chart_df.set_index(
            "match"
        )["movement"]
    )

else:

    st.info(
        "No chart data available."
    )

st.divider()

# Footer

st.caption(
    "BET_NANRI Alert Center • Powered By Pinnacle Listener"
)