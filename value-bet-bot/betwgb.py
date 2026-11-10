import requests
from pprint import pprint

from market_mapper import classify_market


def get_betwgb_event():

    url = "https://sport-shopapi.betwgb.com/AffSportBookCache/api/offer/CacheChangesMinimalByNumberAsStringAndFilterFromLocalCache"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        print(
            f"Error fetching data from BETWGB API: {e}"
        )

        return None


def parse_market(market):

    try:

        market_name = market["t"][0]

        market_type = classify_market(
            market_name
        )

        print(
            f"{market_name} -> {market_type}"
        )

        print("Full Market:")

        pprint(market)

        print("-" * 50)

    except Exception as e:

        print(
            f"Error parsing market: {e}"
        )


if __name__ == "__main__":

    data = get_betwgb_event()

    if data:

        print("\nBETWGB DATA LOADED\n")

        if isinstance(data, list):

            print(
                f"Markets Found: {len(data)}"
            )

            for market in data[:10]:

                parse_market(market)

        elif isinstance(data, dict):

            print(
                "Response Type: Dictionary"
            )

            print(
                "Keys:",
                data.keys()
            )

            if "bets" in data:

                print(
                    "\nBets:",
                    len(data["bets"])
                )

                for market in data["bets"][:10]:

                    parse_market(market)

        else:

            print(
                f"Unexpected type: {type(data)}"
            )