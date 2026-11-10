MARKET_MAP = {

    # Soccer

    "Match Winner": "Soccer_moneyline",
    "1X2": "Soccer_moneyline",

    "Total": "Soccer_totals",
    "Home total": "Soccer_totals",
    "Away total": "Soccer_totals",

    "Handicap": "Soccer_spreads",
    "1st Half - Handicap": "Soccer_spreads",
    "2nd Half - Handicap": "Soccer_spreads",

    # Basketball

    "Moneyline": "Bball_moneyline",

    "Total Points": "Bball_totals",
    "Game Total": "Bball_totals",

    "Spread": "Bball_spreads",
    "Alternative Handicap": "Bball_spread2"
}


def classify_market(market_name):

    return MARKET_MAP.get(
        market_name,
        "UNKNOWN"
    )
