from database import create_database

create_database

import tkinter as tk
from tkinter import messagebox
from database import save_value_opportunity


def save_opportunity():

    try:

        match = match_entry.get()

        market_type = market_var.get()

        bookmaker = bookmaker_var.get()

        pinnacle_odds = float(
            pinnacle_entry.get()
        )

        bookmaker_odds = float(
            bookmaker_entry.get()
        )

        edge = (
            (bookmaker_odds / pinnacle_odds)
            - 1
        ) * 100

        result_label.config(
            text=f"Edge: {edge:.2f}%"
        )

        save_value_opportunity(
            match,
            market_type,
            bookmaker,
            pinnacle_odds,
            bookmaker_odds,
            edge
        )

        messagebox.showinfo(
            "Saved",
            "Value opportunity saved."
        )

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter valid odds."
        )


window = tk.Tk()

window.title(
    "Value Betting Research Tool"
)

window.geometry("600x500")


title = tk.Label(
    window,
    text="Value Finder",
    font=("Arial", 18)
)

title.pack(pady=10)

#
# Match
#

tk.Label(
    window,
    text="Match"
).pack()

match_entry = tk.Entry(
    window,
    width=40
)

match_entry.pack(pady=5)

#
# Market
#

tk.Label(
    window,
    text="Market Type"
).pack()

market_var = tk.StringVar()
market_var.set(
    "Soccer Moneyline"
)

market_menu = tk.OptionMenu(
    window,
    market_var,
    "Soccer Moneyline",
    "Soccer Totals",
    "Soccer Spreads",
    "Basketball Moneyline",
    "Basketball Totals",
    "Basketball Spreads"
)

market_menu.pack(pady=5)

#
# Bookmaker
#

tk.Label(
    window,
    text="Bookmaker"
).pack()

bookmaker_var = tk.StringVar()
bookmaker_var.set(
    "BETWGB"
)

tk.Radiobutton(
    window,
    text="BETWGB",
    variable=bookmaker_var,
    value="BETWGB"
).pack()

tk.Radiobutton(
    window,
    text="BetXchange",
    variable=bookmaker_var,
    value="BetXchange"
).pack()

#
# Odds
#

tk.Label(
    window,
    text="Pinnacle Odds"
).pack()

pinnacle_entry = tk.Entry(
    window
)

pinnacle_entry.pack(pady=5)

tk.Label(
    window,
    text="Bookmaker Odds"
).pack()

bookmaker_entry = tk.Entry(
    window
)

bookmaker_entry.pack(pady=5)

#
# Save Button
#

tk.Button(
    window,
    text="Save Opportunity",
    command=save_opportunity,
    bg="green",
    fg="white"
).pack(pady=15)

#
# Result
#

result_label = tk.Label(
    window,
    text="Edge:"
)

result_label.pack()

window.mainloop()