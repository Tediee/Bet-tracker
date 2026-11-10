import streamlit as st
import sqlite3
import pandas as pd

st.title("📚 Opportunity History")

conn = sqlite3.connect(
    "bets.db"
)

df = pd.read_sql_query(
    """
    SELECT *
    FROM value_opportunities
    ORDER BY date DESC
    """,
    conn
)

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No opportunities saved yet."
    )
    