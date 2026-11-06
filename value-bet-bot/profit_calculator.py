import sqlite3

def calculate_roi():
    conn = sqlite3.connect("bets.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT odds, result
    FROM bets
    """)
    bets = cursor.fetchall()


    total_staked = len(bets)
    total_profit = 0

    for odds, result in bets:
        if result == "WIN":
            total_profit += (odds - 1)
        elif result == "LOSS":
            total_profit -= 1
    

    if total_staked == 0:
        print("No bets found.")
        return
    
        roi = (total_profit / total_staked) * 100

        print(f"Total Bets: {total_staked}")
        print(f"Total Profit: {total_profit:.2f}units")
        print(f"ROI: {roi:.2f}%")

        conn.close()
    