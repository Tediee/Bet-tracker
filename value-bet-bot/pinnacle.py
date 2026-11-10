import requests

def get_pinnacle_odds():

    url = "https://sword.pinnacleoddsdropper.com/alerts/user_2ib1Weq6qiKPFR19iNoTqmSoFoD"

    response = requests.get(url)

    data = response.json()

    return data["data"]