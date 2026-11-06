from urllib import response

import requests 

def get_betwgb_event():
    url = ("https://sport-shopapi.betwgb.com/AffSportBookCache/api/offer/betsAndGroups/1/87/13199/7035692")

    try:
        respomse = requests.get(url,timeout=10)

        response.raise_for_status()

        return response.json()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from BetWGB API: {e}")
        return None
if __name__ == "__main__":
      
 data = get_betwgb_event()

 if data:

    print(data.keys())

    print("Bets:", len(data.get("bets",[])))

    print("Groups:", len(data.get("groups",[])))
  