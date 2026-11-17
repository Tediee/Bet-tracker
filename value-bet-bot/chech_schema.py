# check_schema.py

import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "bets.db"
)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
PRAGMA table_info(pinnacle_alerts)
""")

for column in cursor.fetchall():
    print(column)

conn.close()