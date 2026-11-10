import streamlit as st
from database import save_value_opportunity

st.title("🎯 Value Finder")

match = st.text_input("Match")

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

if st.button("Save Opportunity"):

    edge = (
        (bookmaker_odds / pinnacle_odds)
        - 1
    ) * 100

    st.metric(
        "Edge",
        f"{edge:.2f}%"
    )

    save_value_opportunity(
        match,
        market,
        bookmaker,
        pinnacle_odds,
        bookmaker_odds,
        edge
    )

    st.success(
        "✅ Opportunity Saved"
    )