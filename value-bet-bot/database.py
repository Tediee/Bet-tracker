import sqlite3

from datetime import datetime


date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_database():
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()

    #Main bets table

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
    date TEXT)""")

    #Value opportunities table

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
 
def save_value_opportunity(match,
                           market_type,
                           bookmaker,
                           pinnacle_odds,
                           bookmaker_odds,
                           edge):
    conn = sqlite3.connect("bets.db")
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
    VALUES(?, ?, ?, ?, ?, ?)
    """,(match,
         market_type,
         bookmaker,
         pinnacle_odds,
         bookmaker_odds,
         edge
    ))

    conn.commit()
    conn.close()
    
def show_value_opportunities():

    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM
        value_opportunities
        ORDER BY edge DESC""")

    opportunities = cursor.fetchall()
    if not opportunities:
            
            print("No value opportunities found.")

            conn.close()

            return


    for opp in opportunities:
            print("\n-----------------")
            print(f"ID: {opp[0]}")
            print(f"Match: {opp[1]}")
            print(f"Market: {opp[2]}")
            print(f"Bookmaker: {opp[3]}")
            print(f"Pinnacle: {opp[4]}")
            print(f"Bookmaker odds: {opp[5]}")
            print(f"Edge: {opp[6]:.2f}%")
            print(f"Date: {opp[7]}")
            print("------------------")

        
    conn.close()

    input("\nPress Enter to continue....")

def bookmaker_statistics():

    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        bookmaker,
        COUNT(*),
        AVG(edge),
        MAX(edge)
    FROM value_opportunities
    GROUP BY bookmaker
    """)

    stats = cursor.fetchall()

    if not stats:

        print("No bookmaker statistics available.")

        conn.close()

        return

    for stat in stats:

        print("\n------------------")
        print(f"Bookmaker: {stat[0]}")
        print(f"Value Opportunities: {stat[1]}")
        print(f"Average Edge: {stat[2]:.2f}%")
        print(f"Best Edge: {stat[3]:.2f}%")
        print("------------------")

    conn.close()

    input("\nPress Enter to continue...")
