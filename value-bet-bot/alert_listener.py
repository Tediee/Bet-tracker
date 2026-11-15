import os
import time
import sqlite3

from database import create_database
from pinnacle import get_pinnacle_odds
from notifications import send_discord_alert

# Database path

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "bets.db"
)

# Create tables if they don't exist

create_database()


def save_alert(match, league, movement):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Prevent duplicates

    cursor.execute("""
    SELECT id
    FROM pinnacle_alerts
    WHERE match = ?
    AND movement = ?
    """, (match,movement))

    existing = cursor.fetchone()

    if existing:

        conn.close()
        return False

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

    return True


print("🚀 Pinnacle Listener Started...")


while True:

    try:

        games = get_pinnacle_odds()

        print(f"\nFound {len(games)} games")

        for game in games:

            moving = float(
                game.get(
                    "percentageChange",
                    0
                )
            )

            print(
                f"{game.get('home')} vs "
                f"{game.get('away')} | "
                f"Movement: {moving:.2f}%"
            )

            # Alert filter

            if moving >= 10:

                match = (
                    f"{game.get('home', 'N/A')} vs "
                    f"{game.get('away', 'N/A')}"
                )

                league = game.get(
                    "leagueName",
                    "Unknown"
                )

                saved = save_alert(
                    match,
                    league,
                    moving
                )

                if saved:

                    send_discord_alert(
                        f"""
🚨 PINNACLE ALERT

⚽ Match: {match}

🏆 League: {league}

📈 Movement: {moving:.2f}%

🕰️ Time Sensitive
"""
                    )

                    print(
                        f"🚨 NEW ALERT: "
                        f"{match} "
                        f"({moving:.2f}%)"
                    )

    #wait 60 secs

        time.sleeep(60)
    except Exception as e:

        print(f"❌ Error: {e}")

    time.sleep(10)