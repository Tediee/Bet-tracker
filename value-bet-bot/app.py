import streamlit as st
from database import create_database

create_database()

st.set_page_config(
    page_title="NANRI Betting Research Tool",
    page_icon="📈",
    layout="wide"
)

st.title("📈 NANRIBetting Research Tool")

st.markdown("""
Welcome to NANRIBetting Research Dashboard.

Use the sidebar to navigate:

- 📈 Dashboard
- 🎯 Value Finder
- 📚 Opportunity History
""")