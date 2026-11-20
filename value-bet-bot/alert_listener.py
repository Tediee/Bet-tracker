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


def save_alert(match,
                league,
                  movement,
                   market_type,
                    pinnacle_odds,):

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
        movement,
        market_type,
        pinnacle_odds,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        match,
        league,
        movement,
        market_type,
        pinnacle_odds,
        "NEW"
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
            

            movement = float(
                game.get(
                    "percentageChange",
                    0
                )
            )

            print(
                f"{game.get('home')} vs "
                f"{game.get('away')} | "
                f"Movement: {movement:.2f}%"
            )

            # Alert filter

            if movement >= 15:

                match = (
                    f"{game.get('home', 'N/A')} vs "
                    f"{game.get('away', 'N/A')}"
                )

                league = game.get("leagueName","Unknown")

                line_type = game.get("lineType","Unknown")
                
                outcome = game.get("outcome", "Unknown")

                market_type = (f"{line_type} ({outcome})")

                pinnacle_odds = float(game.get("changeTo", 0))


                saved = save_alert(match,league,
                    movement,market_type,pinnacle_odds)

                if saved:

                    send_discord_alert(
 
 
                       f"""
 @everyone
 .....................................         
🚨 **PINNACLE ALERT**

⚽ Match: {match}

🏆 League: {league}

📈 Movement: {movement:.2f}%

🕰️ Time Sensitive
......................................
"""
                    )

                    print(
                        f"🚨 NEW ALERT: {match}"
                        
                    )

    #wait 60 secs

        time.sleep(60)
    except Exception as e:

        print(f"❌ Error: {e}")

    time.sleep(10)