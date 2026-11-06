from database import create_database, save_bet,show_bets
from profit_calculator import   calculate_roi
from pinnacle import get_Pinnacle_odds
from database import search_value_bets



create_database()

def calculate_value(odds,fair_odds):
    return((odds / fair_odds) - 1) * 100


while True:
    print("1. Add bet")
    print("2. View bets")
    print("3. Search value bets ")
    print("4. show ROI")
    print("5. Exit")
    print("6. Live pinnacle odds")
    print("7. Save Pinnacle Alerts")
    print("8. Top pinnacle drops")
    print("9. biggest movers today")
    print("10. Value finder")


    choice = input("choose: ")

    

    if choice == "1":
       match = input("Match: ")
       odds = float(input("odds: "))
       result = input("Result (won/lost): ").upper()
       fair_odds = float(input("Fair odds: "))

       value = calculate_value(odds, fair_odds)

       print(f"Value: {value:.2f}%")

       save_bet(
           match, 
           odds, 
           fair_odds, 
           value, 
           result,
           league="Manual Entry",
           percentage_change=0,
           timestamp=None
        )


       if value > 5:

           print("VALUE BET FOUND")

    elif choice == "2":
        show_bets()

    elif choice == "3":

        try:

            threshold_input = input("minimum value %(default 5): "
            )

            if threshold_input == "":
                threshold = 5
            else:
                threshold = float(threshold_input)
        
            search_value_bets(threshold)

        except ValueError:
        
            print("Invalid input. Please enter a number.")


    elif choice == "4":

        calculate_roi()

    elif choice == "5":
        print("Exiting...") 
        break

    elif choice == "6":
    
        games = get_Pinnacle_odds()
    
        for game in games:
    
         print("\n..............")
         print(f"{game.get('home', 'N/A')} vs {game.get('away', 'N/A')}")
         print(f"Home: {game.get('priceHome', 'N/A')}")
         print(f"Draw: {game.get('priceDraw', 'N/A')}")
         print(f"Away: {game.get('priceAway', 'N/A')}")
         print("................")

    elif choice == "7":

         games = get_Pinnacle_odds()

         for game in games:

             match = f"{game.get('home','N/A')} vs {game.get('away', 'N/A')}"
             odds = float(
                 game.get("priceHome", 0)
            )

             league = game.get("leagueName",
                               "Unknown")
   
             change = float(game.get("percentageChange",
                                     0
                            )
            
            )
             save_bet(
                 match,
                 odds,
                 odds,
                 0,
                "PENDING",
                league,
                change
                     )
            

             if change > 10:
                 print("\n🚨 MAJOR ODDS DROP")
                 print(f"League: {league}")
                 print(f"Match: {match}")
                 print(f"Movement: {change:.2f}%")

        
         print("Pinnacle alerts saved to database.")
            
    elif choice == "8":
        games = get_Pinnacle_odds()

        for game in games:

            change = float(game.get("percentageChange",0))

            if change >= 10:

                print("\n------------")
                print(
                    f"{game.get('home')} vs "
                    f"{game.get('away')}"
                )
                print(f"Drop: {change:2f}%")
                print("----------------")

    elif choice == "9":

         games = get_Pinnacle_odds()

         sorted_games = sorted(
             games,
             key=lambda game: float(
                 game.get("percentageChange", 0)
             ),
             reverse=True
             )  
         print("\nTOP ODDS MOVERS\n")

         for i, game in enumerate(sorted_games[:10], start=1):

                 change = float(game.get("percentageChange", 0))

                 print("------------")
                 print(
                     f"{i}. "
                     f"{game.get('home','N/A')} vs {game.get('away','N/A')}"
                 )
                 print(
                        f"League:{game.get('leagueName','Unknown')}"
                 )
                 print(f"movement:{change:.2f}%")
                 print("----------------")
    elif choice == "10":

        try:

             print("\nVALUE FINDER\n")

             match = input("Match: ")

             pinnacle_odds = float(
             input("Pinnacle Odds: ")
             )
             bookmaker = input(
             "Bookmaker (Betwgb/Betxchange): "   )

             bookmaker_odds = float(
              input("Bookmaker odds: ")
             )

             value_edge = ((bookmaker_odds / pinnacle_odds) - 1
                      ) * 100

             print("\n------------")
             print(f"Match: {match}")
             print(f"Pinnacle: {pinnacle_odds}")
             print(f"{bookmaker}: {bookmaker_odds}")
             print(f"Edge: {value_edge:.2f}%")
             print("DEBUG")
             print("Pinnacle =", pinnacle_odds)
             print("Bookmaker Odds =", bookmaker_odds)
             print("Edge Raw =", value_edge)
             print("----------------")
 
             if value_edge >= 5:
                 print("🚨 VALUE FOUND")
             else:
                 print("No value found.")

        except ValueError:

             print("enter valid odds")
            

        ""