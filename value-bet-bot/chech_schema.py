# check_schema.py

import sqlite3
import os


conn = sqlite3.connect("bets.db")
cursor = conn.cursor()

cursor.execute("""
PRAGMA table_info(pinnacle_alerts)
""")

for column in cursor.fetchall():
    print(column)

conn.close()