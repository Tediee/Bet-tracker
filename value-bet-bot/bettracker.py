from database import create_database, save_bet,show_bets
from profit_calculator import   calculate_roi
from pinnacle import get_Pinnacle_odds
from database import search_value_bets
from database import (save_value_opportunity,
                      create_database,
                      search_value_bets,
                      save_value_opportunity,
                      show_value_opportunities,
                      bookmaker_statistics)

create_database()


def calculate_value(odds,fair_odds):
    return((odds / fair_odds) - 1) * 100


while True:
    print("6. Live pinnacle odds")
    print("7. Save Pinnacle Alerts")
    print("8. Top pinnacle drops")
    print("9. biggest movers today")
    print("10. Value finder")
    print("11. View Value Opportunities")
    print("12. Bookmaker Statistics")


    choice = input("choose: ")

    

    if choice == "1":
       match = input("Match: ")
       odds = float(input("odds: "))
       fair_odds = float(input("Fair odds: "))

       result = "PENDING"

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
            print("\nSelect Market Type")
            print("1. Soccer Moneyline")
            print("2. Soccer Totals")
            print("3. Soccer Spread")
            print("4. Basketball Moneyline")
            print("5.Basketball Totals")
            print("6. Basketball Spreads")

            market_choice = input("Choice: ")

            if market_choice == "1":
                market_type = "Soccer Moneyline"

            elif market_choice == "2":
                market_type = "Soccer Totals"

            elif market_choice == "3":
                market_type = "Soccer Spreads"

            elif market_choice == "4":
                market_type = "Basketball Moneyline"

            elif market_choice == "5":
                market_type = "Basketball Totals"

            elif market_choice == "6":
                market_type = "Basketball Spreads"

            else:
                print("invalid market.")
            pinnacle_odds = float(input("Pinnacle Odds: "))

            print("\n1. BETWGB")
            print("2. BetXchange")
            bookie_choice = input("Choose bookmaker: ")

            if bookie_choice == "1":
                bookmaker = "BETWGB"
            elif bookie_choice == "2":
                bookmaker = "BetXchange"
            else:
                print("Invalid bookmaker choice.")
                continue
        
            bookmaker_odds = float(input("Bookmaker Odds: "))
            
            value_edge = ((bookmaker_odds / pinnacle_odds) - 1) * 100

            print("\n------------")
            print(f"Match: {match}")
            print(f"Pinnacle:{pinnacle_odds}")
            print(f"{bookmaker} : {bookmaker_odds}")
            print(f"Edge: {value_edge:.2f}%")
            print("----------------")

            if value_edge >= 5:
                print("🚨 VALUE FOUND")
             
                save_value_opportunity(
                    match,
                    market_type,
                    bookmaker,
                    pinnacle_odds,
                    bookmaker_odds,
                    value_edge,
                )
                print("Value Saved.")
            else:
                print("No value found.")
        except Exception as e:
            print(f"ERROR: {e}")
            print("enter valid odds")

    elif choice == "11":

        show_value_opportunities()
        


    elif choice == "12":

        bookmaker_statistics()
""