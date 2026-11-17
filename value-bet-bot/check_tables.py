# upgrade_alerts_table.py

import sqlite3

conn = sqlite3.connect("bets.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE pinnacle_alerts
    ADD COLUMN market_type TEXT
    """)
except:
    pass

try:
    cursor.execute("""
    ALTER TABLE pinnacle_alerts
    ADD COLUMN pinnacle_odds REAL
    """)
except:
    pass

try:
    cursor.execute("""
    ALTER TABLE pinnacle_alerts
    ADD COLUMN status TEXT DEFAULT 'NEW'
    """)
except:
    pass

conn.commit()
conn.close()

print("Upgrade complete")