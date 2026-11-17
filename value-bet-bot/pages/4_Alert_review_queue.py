import streamlit as st
import sqlite3
import pandas as pd
import os

from database import (
    save_value_opportunity,
    update_alert_status
)

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "bets.db"
)

st.title(
    "🎯 Alert Review Queue"
)

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("""
SELECT *
FROM pinnacle_alerts
WHERE status='NEW'
ORDER BY movement DESC
""", conn)

conn.close()

if df.empty:

    st.success(
        "✅ No alerts waiting."
    )

    st.stop()

st.metric(
    "🚨 New Alerts",
    len(df)
)

for _, row in df.iterrows():

    with st.expander(
        f"{row['match']} | "
        f"{row['movement']:.2f}%"
    ):

        st.write(
            f"🏆 League: "
            f"{row['league']}"
        )

        st.write(
            f"📊 Market: "
            f"{row['market_type']}"
        )

        st.write(
            f"📈 Pinnacle Odds: "
            f"{row['pinnacle_odds']}"
        )

        bookmaker = st.selectbox(
            "Bookmaker",
            [
                "BETWGB",
                "BetXchange"
            ],
            key=f"b_{row['id']}"
        )

        bookmaker_odds = st.number_input(
            "Bookmaker Odds",
            min_value=1.01,
            step=0.01,
            key=f"o_{row['id']}"
        )

        edge = (
            (
                bookmaker_odds /
                row["pinnacle_odds"]
            ) - 1
        ) * 100

        st.metric(
            "Edge",
            f"{edge:.2f}%"
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "💰 Save Opportunity",
                key=f"s_{row['id']}"
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
                    "Saved"
                )

                st.rerun()

        with c2:

            if st.button(
                "❌ No Value",
                key=f"n_{row['id']}"
            ):

                update_alert_status(
                    row["id"],
                    "NO VALUE"
                )

                st.rerun()