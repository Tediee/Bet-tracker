import streamlit as st
import sqlite3
import pandas as pd
import os

from datetime import datetime

from database import (
    save_value_opportunity,
    update_alert_status
)

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "bets.db"
)

st.set_page_config(
    page_title="Alert Review Queue",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Alert Review Queue")

if st.button("🔄 Refresh"):
    st.rerun()

# ----------------------------
# Load Alerts
# ----------------------------

try:

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("""
    SELECT *
    FROM pinnacle_alerts
    WHERE status = 'NEW'
    ORDER BY date DESC
    """, conn)

    conn.close()

except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

    st.stop()

if df.empty:

    st.success(
        "✅ No alerts awaiting review."
    )

    st.stop()

# ----------------------------
# Most Recent Alert
# ----------------------------

st.subheader("🆕 Most Recent Alert")

latest = (
    df.sort_values(
        "date",
        ascending=False
    )
    .head(1)
    .iloc[0]
)

latest_time = pd.to_datetime(
    latest["date"]
)

minutes_old = int(
    (
        datetime.now() - latest_time
    ).total_seconds()
    / 60
)

st.success(
    f"""
⚽ {latest['match']}

🏆 {latest['league']}

📊 {latest['market_type']}

📈 Pinnacle: {latest['pinnacle_odds']}

🔥 Movement: {latest['movement']:.2f}%

⏰ Received: {latest['date']}

🕒 Age: {minutes_old} mins ago
"""
)

st.divider()

# ----------------------------
# Top 3 Alerts
# ----------------------------

st.subheader("🔥 Top 3 Alerts Right Now")

top_three = (
    df.sort_values(
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

st.divider()

# ----------------------------
# Metrics
# ----------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "🚨 New Alerts",
    len(df)
)

col2.metric(
    "📈 Largest Move",
    f"{df['movement'].max():.2f}%"
)

col3.metric(
    "📊 Average Move",
    f"{df['movement'].mean():.2f}%"
)

st.divider()

# ----------------------------
# Review Queue
# ----------------------------

st.subheader(
    "📋 Alerts Awaiting Review"
)

review_df = (
    df.sort_values(
        "date",
        ascending=False
    )
)

for _, row in review_df.iterrows():

    alert_time = pd.to_datetime(
        row["date"]
    )

    minutes_old = int(
        (
            datetime.now()
            - alert_time
        ).total_seconds()
        / 60
    )

    with st.expander(

        f"""
⚽ {row['match']}
|
🔥 {row['movement']:.2f}%
|
🕒 {minutes_old} min ago
"""

    ):

        st.write(
            f"🏆 League: {row['league']}"
        )

        st.write(
            f"📊 Market: {row['market_type']}"
        )

        st.write(
            f"📈 Pinnacle Odds: {row['pinnacle_odds']}"
        )

        st.write(
            f"⏰ Received: {row['date']}"
        )

        bookmaker = st.selectbox(
            "Bookmaker",
            [
                "BETWGB",
                "BetXchange"
            ],
            key=f"bookmaker_{row['id']}"
        )

        bookmaker_odds = st.number_input(
            "Bookmaker Odds",
            min_value=1.01,
            step=0.01,
            key=f"odds_{row['id']}"
        )

        edge = (
            (
                bookmaker_odds
                / row["pinnacle_odds"]
            ) - 1
        ) * 100

        st.metric(
            "Edge",
            f"{edge:.2f}%"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            if st.button(
                "💰 Save Opportunity",
                key=f"save_{row['id']}"
            ):

                save_value_opportunity(
                    row["match"],
                    row["market_type"],
                    bookmaker,
                    row["pinnacle_odds"],
                    bookmaker_odds,
                    edge
                )

                update_alert_status(
                    row["id"],
                    "VALUE FOUND"
                )

                st.success(
                    "Opportunity Saved"
                )

                st.rerun()

        with c2:

            if st.button(
                "❌ No Value",
                key=f"novalue_{row['id']}"
            ):

                update_alert_status(
                    row["id"],
                    "NO VALUE"
                )

                st.rerun()

        with c3:

            if st.button(
                "✅ Reviewed",
                key=f"reviewed_{row['id']}"
            ):

                update_alert_status(
                    row["id"],
                    "REVIEWED"
                )

                st.rerun()