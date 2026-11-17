import os
import sqlite3
from datetime import datetime
from datetime import datetime

DB_PATH = os.path.join(
    os.path.dirname(__file__),"bets.db")
        

def create_database():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Value Opportunities

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS value_opportunities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match TEXT,
        market_type TEXT,
        bookmaker TEXT,
        pinnacle_odds REAL,
        bookmaker_odds REAL,
        edge REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Pinnacle Alerts

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pinnacle_alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match TEXT,
        league TEXT,
        movement REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_pinnacle_alert(
    match,
    league,
    movement
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO pinnacle_alerts(
        match,
        league,
        movement
    )
    VALUES (?, ?, ?)
    """, (
        match,
        league,
        movement
    ))

    conn.commit()
    conn.close()

def show_pinnacle_alerts():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM pinnacle_alerts
    ORDER BY date DESC
    """)

    alerts = cursor.fetchall()

    for alert in alerts:

        print("\n----------------")
        print(f"Match: {alert[1]}")
        print(f"League: {alert[2]}")
        print(f"Movement: {alert[3]:.2f}%")
        print(f"Date: {alert[4]}")
        print("----------------")

    conn.close()

def save_value_opportunity(
    match,
    market_type,
    bookmaker,
    pinnacle_odds,
    bookmaker_odds,
    edge
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO value_opportunities(
        match,
        market_type,
        bookmaker,
        pinnacle_odds,
        bookmaker_odds,
        edge
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        match,
        market_type,
        bookmaker,
        pinnacle_odds,
        bookmaker_odds,
        edge
    ))

    conn.commit()
    conn.close()