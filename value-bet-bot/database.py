import sqlite3

from datetime import datetime


date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_database():
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS bets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match TEXT,
        odds REAL,
        fair_odds REAL,
        value_percent REAL,
        result TEXT,
        league TEXT,
        percentage_change REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_bet(match,
             odds, 
              fair_odds,
                value_percent,
                  result,
                    league="Manual Entry",
                      percentage_change=0,
                        timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bets (
        match,
        odds,
        fair_odds,
        value_percent,
        result,
        league,
        percentage_change,
        date

    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (match,
        odds, 
        fair_odds,
        value_percent, 
        result,
        league,
        percentage_change,
        timestamp
    ))

    conn.commit()
    conn.close()

def show_bets():
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bets")

    bets = cursor.fetchall()

    if not bets:
        print("No bets found.")

    for bet in bets:
        print("\n...........")
        print(f"ID: {bet[0]}")
        print(f"Match: {bet[1]}")
        print(f"Odds: {bet[2]}")
        print(f"Fair Odds: {bet[3]}")
        print(f"Value %: {bet[4]:.2f}%")
        print(f"Result: {bet[5]}")

        print("............")

    conn.close()

    input("\nPress Enter to continue...")
    
def search_value_bets(threshold):
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM bets
    WHERE value_percent >= ?
    """, (threshold,))

    bets = cursor.fetchall()

    if not bets:
        print(f"No value bets found with a threshold of {threshold}%.")
        return

    for bet in bets:
        print("\n...........")
        print(f"ID: {bet[0]}")
        print(f"Match: {bet[1]}")
        print(f"Odds: {bet[2]}")
        print(f"Fair Odds: {bet[3]}")
        print(f"Value %: {bet[4]:.2f}%")
        print(f"Result: {bet[5]}")
        print("............")

    conn.close()

    input("\nPress Enter to continue...")

    