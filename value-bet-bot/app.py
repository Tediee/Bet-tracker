import streamlit as st
from database import (
    create_database,
    save_value_opportunity
)

create_database()

st.set_page_config(
    page_title="Value Betting Research Tool",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Value Betting Research Tool")

st.subheader("Value Opportunity Finder")

match = st.text_input(
    "Match"
)

market = st.selectbox(
    "Market Type",
    [
        "Soccer Moneyline",
        "Soccer Totals",
        "Soccer Spreads",
        "Basketball Moneyline",
        "Basketball Totals",
        "Basketball Spreads"
    ]
)

bookmaker = st.radio(
    "Bookmaker",
    [
        "BETWGB",
        "BetXchange"
    ]
)

pinnacle_odds = st.number_input(
    "Pinnacle Odds",
    min_value=1.01,
    step=0.01
)

bookmaker_odds = st.number_input(
    "Bookmaker Odds",
    min_value=1.01,
    step=0.01
)

if st.button("Calculate & Save"):

    edge = (
        (bookmaker_odds / pinnacle_odds)
        - 1
    ) * 100

    st.metric(
        "Edge",
        f"{edge:.2f}%"
    )

    if edge >= 5:

        save_value_opportunity(
            match,
            market,
            bookmaker,
            pinnacle_odds,
            bookmaker_odds,
            edge
        )

        st.success(
            "✅ Value opportunity saved."
        )

    else:

        st.warning(
            "No value found."
        )

import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "bets.db"
)

df = pd.read_sql_query(
    "SELECT * FROM value_opportunities",
    conn
)

st.subheader(
    "Saved Opportunities"
)

st.dataframe(
    df,
    use_container_width=True
)

st.subheader(
    "Bookmaker Statistics"
)

if not df.empty:

    st.metric(
        "Total Opportunities",
        len(df)
    )

    st.metric(
        "Average Edge",
        round(
            df["edge"].mean(),
            2
        )
    )

    st.metric(
        "Best Edge",
        round(
            df["edge"].max(),
            2
        )
    )
