from betwgb import get_betwgb_event
data = get_betwgb_event()
print("Bets:", len(data["bets"]))
print("Groups:", len(data["groups"]))

if len(data["bets"]) > 0:
    print(data["bets"][0])

if len(data["groups"]) > 0:
    print(data["groups"][0])
    
    