#Ryan Tan Jia Jun - (S10265914J)
#"Only god and I knows what this code does. Now only god knows." - Some dude on stackoverflow


# Game variables
game_vars = {
    'day': 1,
    'energy': 10,
    'money': 20,
    'bag': {}, #stores the seeds as {seed: amount} e.g. {'LET': 5, 'POT': 3} etc.
}

seed_list = ['LET', 'POT', 'CAU'] #list of seeds available in the game, used for the shop menu as a key to show the names
seeds = {                         #Dictionary of seeds, used to store the seed information
    'LET': {'name': 'Lettuce',
            'price': 2,
            'growth_time': 2,
            'crop_price': 3
            },

    'POT': {'name': 'Potato',
            'price': 3,
            'growth_time': 3,
            'crop_price': 6
            },

    'CAU': {'name': 'Cauliflower',
            'price': 5,
            'growth_time': 6,
            'crop_price': 14
            },
}

farm = [ 
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, 'House', None, None],
    [None, None, None, None, None],
    [None, None, None, None, None] 
         ]


#---------------------------------GAME FUNCTIONS---------------------------------#
#Each game fucntions has a docstring that explains what the function does
def in_town(game_vars):
    """
    Shows the menu of Albatross Town and returns the player's choice
    Players can
      1) Visit the shop to buy seeds
      2) Visit the farm to plant seeds and harvest crops
      3) End the day, resetting Energy to 10 and allowing crops to grow

      9) Save the game to file
      0) Exit the game (without saving)
    """
    while True:
        show_stats(game_vars)
        print("You are in Albatross Town.")
        print("------------------------")
        print("1) Visit the Seed Shop\n"
            "2) Visit the Farm\n"
            "3) End the Day\n")
        print()
        print("9) Save the Game\n"
            "0) Exit the Game\n")
        try:
            choice = int(input("Your choice?: "))
        except ValueError:
            print("Invalid choice. Please try again.\n")
            continue
        if choice == 1:
            in_shop(game_vars)
        elif choice == 2:
            in_farm(game_vars, farm)
        elif choice == 3:
            if game_vars['day'] != 20:
                end_day(game_vars)
            else:
                end_game(game_vars)
                return
        elif choice == 9:
            save_game(game_vars, farm)
        elif choice == 0:
            break 
        else:
            print("Invalid choice. Please try again.\n")

def buy_item(game_vars, itemcode):
    """
    Buys an item from the shop
    If the player has enough money, the item is added to the bag
    If the player does not have enough money, an error message is shown
    If the item is already in the bag, the amount is increased
    If the item is not in the bag, it is added
    The player's money is reduced by the price of the item times the amount
    Returns the updated game_vars
    """
    total_count = sum(game_vars['bag'].values())
    while True:
        try:
            amount = int(input(f"How many {seeds[itemcode]['name']} seeds would you like to buy? "))
        except ValueError:
            print("Invalid choice. Please try again.\n")
            continue
        if total_count + amount > 10 or total_count == 10:
            print("You can't carry that many seeds!")
            return game_vars

        if amount < 0:
            print("You are NOT allowed to buy negative amount of seeds.")
            continue
        if game_vars['money'] < seeds[itemcode]['price'] * amount:
            print("You don't have enough money to buy that many seeds.")
            continue
        else:
            game_vars['money'] -= seeds[itemcode]['price'] * amount
        
        
    
        if itemcode in game_vars['bag']:
            game_vars['bag'][itemcode] += amount
        else:
            game_vars['bag'][itemcode] = amount
        return game_vars

def in_shop(game_vars):
    """
    Shows the menu of the seed shop, and allows players to buy seeds
    seeds can be bought if player has enough money
    Ends when player selects to leave the shop
    """
    while True:
        print("Welcome to the Pierce's Seed Shop!")
        show_stats(game_vars)
        print("What do you wish to buy?")
        print(f"{"Seed":<20}{"Price":<20}{"Days to Grow":<25}{"Crop Price":<20}")
        print("-"*75)
        i = 1
        for seed in seed_list:
            print(f"{i}) {seeds[seed]['name']:<20}${seeds[seed]['price']:<20}{seeds[seed]['growth_time']:<25}${seeds[seed]['crop_price']:<20}") #print out the seed list
            i += 1
        print()
        print("0) Leave the shop")
        try:
            choice = int(input("Your choice: "))
        except ValueError:
            continue
        if choice == 0:
            return  # Leave the shop
        elif choice == 1:
            #Buy Lettuce
            buy_item(game_vars, 'LET')
        elif choice == 2: 
            #buy Potato
            buy_item(game_vars, 'POT')
        elif choice == 3:
            # buy Cauliflower
            buy_item(game_vars, 'CAU')
        else:
            print("Invalid choice. Please try again.\n")
            continue  
        
        pass

def draw_farm(farm, x_PosX, x_PosY):
    """
   Draws the farm
   Each space on the farm has 3 rows:
     TOP ROW:
       - If a seed is planted there, shows the crop's abbreviation
       - If it is the house at (2,2), shows 'HSE'
       - Blank otherwise
     MIDDLE ROW:
       - If the player is there, shows X
       - Blank otherwise
     BOTTOM ROW:
       - If a seed is planted there, shows the number of turns before
         it can be harvested
       - Blank otherwise
    """
    x_cord = 0
    y_cord = 0
    def print_line():
        print("+-----" * len(farm[0]) + "+")

    map_legend = {
    "House": "HSE",
    "Lettuce": "LET",
    "Potato": "POT",
    "Cauliflower": "CAU",
    }

    print_line() #print the top line

    for row in farm:
        for i in range(3):
            x_cord = 0
            for item in row:
                if item == None and i != 1:
                    print("|     ", end="")
                elif i == 0: #print the top row
                    if type(item) == dict:
                        for plant in item: #print the plant abbreviation
                            print(f"| {map_legend[plant]} ", end="")
                    else:
                        print(f"| {map_legend[item]} ", end="") #print the house abbreviation
                elif i == 1: #print the middle row
                    if x_cord  == x_PosX and y_cord == x_PosY:
                        print("|  X  ", end="")
                    else:
                        print("|     ", end="")
                elif i == 2: #print the bottom row
                    if type(item) == dict:
                        for plant in item: #print the number of days left to grow
                            print(f"|  {item[plant]}  ", end="")
                    else:
                        print("|     ", end="")
                else:
                    print("|     ", end="")
                x_cord += 1
                
            print("|", end="") #print the right border of the map
            print() #creates a new line
            
        print_line() #print the middle line for each row
        y_cord += 1  
    return

def in_farm(game_vars, farm):
    """
    this functions will allow the player to move around the farm
    the player can move around the farm using the WASD keys
    the player can plant seeds using the P key
    the player can harvest crops using the H key
    the player can return to town using the R key
    """
    seed_legend = {"Lettuce": "LET", "Potato": "POT", "Cauliflower": "CAU"}
    x_PosX = 2
    x_PosY = 2
    while True:
        moved = False
        canhav = False
        draw_farm(farm, x_PosX, x_PosY)
        print(f"Energy: {game_vars['energy']}")
        print("[WASD] Move\n"
            "P)lant\n"
            "R)eturn to town\n")
        
        if type(farm[x_PosY][x_PosX]) == dict:
            if farm[x_PosY][x_PosX] != None:
                for plant in farm[x_PosY][x_PosX]:
                    if farm[x_PosY][x_PosX][plant] == 0:
                        print(f"H)arvest {plant} for ${seeds[seed_legend[plant]]['crop_price']}")
                        canhav = True
        try:   
            option = input("Your choice: ").upper()
        except ValueError:
            print("Invalid choice. Please try again.\n")
            continue  
        if option in ["W", "A", "S", "D", "H"] and game_vars['energy'] != 0:
            if option == "W":
                new_x_PosY = x_PosY - 1
                new_x_PosX = x_PosX
                moved = True 
            elif option == "A":
                new_x_PosX = x_PosX - 1
                new_x_PosY = x_PosY
                moved = True 
            elif option == "S":
                new_x_PosY = x_PosY + 1
                new_x_PosX = x_PosX
                moved = True 
            elif option == "D":
                new_x_PosX = x_PosX + 1
                new_x_PosY = x_PosY
                moved = True 
            
            elif option == "H" and canhav == True:
                for plant in farm[x_PosY][x_PosX]:
                    game_vars['money'] += seeds[seed_legend[plant]]['crop_price']
                    farm[x_PosY][x_PosX] = None
                    game_vars['energy'] -= 1
                    print(f"You harvested {plant} for ${seeds[seed_legend[plant]]['crop_price']}!")
                    print(f"You now have ${game_vars['money']} !")
                    continue
            else:
                print("Invalid choice. Please try again.\n")
                continue      
        elif option == "P" and farm[x_PosY][x_PosX] == None:
            planting(game_vars, farm, x_PosX, x_PosY)
        elif option == "R":
            break
        elif game_vars['energy'] == 0:
            print("You have no energy left. You must end the day.")
            continue
        else:
            print("Invalid choice. Please try again.\n")
            continue

        #checks if the new position is within the farm
        if  0 <= new_x_PosX <= len(farm)-1 and 0 <= new_x_PosY < len(farm[0]):
            x_PosX = new_x_PosX
            x_PosY = new_x_PosY
        else:
            moved = False
            print("You can't move there!")
        #decrease engery if the player moves
        if moved == True:
            game_vars['energy'] -= 1

def planting(game_vars, farm, x_PosX, x_PosY):
    """
    This function allows the player to plant seeds
    the player can only plant seeds where there is no crop
    the player can only plant seeds if there is energy
    available_seeds is a dictionary that stores the available seeds
    so that the player can choose which seed to plant
    """
    available_seeds = {}
    i = 1
    print("What do you wish to plant?")
    print("-" * 65)
    print(f"     {"Seed":<12}{"Days to Grow":<20}{"Crop Price":<20}{"Available":<20}")
    print("-" * 65)
    for item in game_vars['bag']:
        if game_vars['bag'][item] != 0:
            print(f"{i}) {seeds[item]['name']:<20}{seeds[item]['growth_time']:<20}{seeds[item]['crop_price']:<20}{game_vars['bag'][item]:<20}")
            available_seeds[i] = item
            i += 1
    print()
    print("0) Return to town")
    try:
        option = int(input("Your choice: "))
        if farm[x_PosY][x_PosX] == None:
            if option != 0 and game_vars['energy'] != 0:
                if game_vars['bag'][available_seeds[option]] != 0:
                    farm[x_PosY][x_PosX] = {seeds[available_seeds[option]]['name']: seeds[available_seeds[option]]['growth_time']}
                    game_vars['bag'][available_seeds[option]] -= 1
                    game_vars['energy'] -= 1
                else:
                    print("somethings wrong!")
                    return
            elif game_vars['energy'] == 0:
                print("You are too tired to plant!")
                return
            elif option == 0:
                return
            else:
                print("You can't plant a seed here.")
                return
    except ValueError:
        print("Invalid choice. Please try again.\n")
        return
    except KeyError:
        print("Invalid choice. Please try again.\n")
        return
    
            
def show_stats(game_vars):
    """
    This functions shows the states of the game
    this includes:
    - the day
    - the energy
    - the money
    - the seeds in the bag

    
    """
    print("+----------------------------------------------------------+")
    #prints the day, energy and money
    if game_vars['day'] >= 10: #ensure that the layout is consistent
        if game_vars['money'] >= 10 and game_vars['money'] < 100:
            print(f"| Day {game_vars['day']}{" "* 15}Energy: {game_vars['energy']}{" "* 16}Money ${game_vars['money']} |")
        elif game_vars['money'] < 10:
            print(f"| Day {game_vars['day']}{" "* 15}Energy: {game_vars['energy']}{" "* 17}Money ${game_vars['money']} |")
        else:
            print(f"| Day {game_vars['day']}{" "* 15}Energy: {game_vars['energy']}{" "* 15}Money ${game_vars['money']} |")
        
    else:
        if game_vars['money'] >= 10 and game_vars['money'] < 100:
            print(f"| Day {game_vars['day']}{" "* 16}Energy: {game_vars['energy']}{" "* 16}Money ${game_vars['money']} |")
        elif game_vars['money'] < 10:
            print(f"| Day {game_vars['day']}{" "* 16}Energy: {game_vars['energy']}{" "* 17}Money ${game_vars['money']} |")
        else:
            print(f"| Day {game_vars['day']}{" "* 16}Energy: {game_vars['energy']}{" "* 15}Money ${game_vars['money']} |")

    #prints the seeds in the bag
    if game_vars['bag'] == {}: #if the bag is empty
        print(f"| You have no seeds.{" "*38} |")
    else:
        print(f"| Your seeds:{" "* 45} |")
        for items in game_vars['bag']:
            if game_vars['bag'][items] >= 10: #ensure that the layout is consistent
                print(f"|   {seeds[items]['name']:<11}:  {game_vars['bag'][items]} {"|":>39}")
            else:
                print(f"|   {seeds[items]['name']:<11}:  {game_vars['bag'][items]} {"|":>40}")
    print("+----------------------------------------------------------+")
    
def end_day(game_vars):
    """
    This function ends the days
    increases the day counter
    energy is reset to 10
    planted crops have their growth time reduced by 1
    """
    game_vars['day'] += 1
    game_vars['energy'] = 10
    for row in farm:
        for item in row:
            if type(item) == dict:
                for plant in item:
                    if item[plant] != 0:
                        item[plant] -= 1
                    
    pass

def end_game(game_vars):
    """
    this function will only run if the player has reached day 20
    it will calculate the profit the player has made
    if the player has made a profit and pays off 100, they will win
    else they will lose
    """
    profit = game_vars['money'] - 100
    print(f"You have ${game_vars['money']} dollars after 20 days")
    if profit < 0:
        print(f"You lose!")
        return
    else:
        print(f"Your profit is ${profit}")
        print("You win!")
        option = input("Would you like to add your name to the leaderboard? (Y/N): ").upper()
        match option:
            case "Y":
                name = input("Enter your name: ")
                with open("leaderboard.csv", "a") as f:
                    f.write(f"\n{name},{profit}")
                return profit
            case "N":
                return profit
            case _:
                print("Invalid choice. Please try again.")

    return profit
        
def sort_leaderboard(stats):
    leaderboard = []
    #Sort the leaderboard using insertion sort
    for names in stats:
        name, value = names.split(",")
        if len(leaderboard) == 0:
            leaderboard.append([name, int(value)])
        else:
            for i in range(len(leaderboard)):
                if int(value) > leaderboard[i][1]:
                    leaderboard.insert(i, [name, int(value)])
                    break
                elif i == len(leaderboard) - 1:
                    leaderboard.append([name, int(value)])
                    break
    return leaderboard


def leaderboard():
    with open("leaderboard.csv", "r+") as f: #read and write the file
        stats = f.readlines()
        stats = [x.strip().strip(",") for x in stats]

        leaderboard = sort_leaderboard(stats)

        #shows leaderboard
        print(f"Leaderboard:")
        for placing in range(5):
            print(f"{str(placing+1)+")":<5}{leaderboard[placing][0]:10} {leaderboard[placing][1]:10}")
    return
    

            



def save_game(game_vars, farm):
    """
    Saves the game into the file "savegame.txt"
    the first line is the day
    second is the energy, third is the money
    fourth is the bag, fifth is the farm.
    """
    with open("savegame.txt", "w") as file:
        file.write(f"{game_vars['day']}\n")
        file.write(f"{game_vars['energy']}\n")
        file.write(f"{game_vars['money']}\n")
        for key, value in game_vars['bag'].items():
            if key != None:
                file.write(f"{key}:{value},")
            else:
                file.write("None")
        file.write("\n")    
        

        for line in farm:
            file.write(f"{line}\n")
    pass

def load_game(game_vars):
    """
    attempts to load the game from the file "savegame.txt"
    if the file is not found, an error message is shown

    To understand how the map is loaded, we need to understand how the map is saved
    the map is saved as a list, something like this:
    [None, None....]
    So can use a for loop to iterate through the list and append the items to the map
    as we always know that the map is from line 4 of the savegame.txt file
    we can hardcode the line number to start from line 4
    the list "a" is a placeholder to list and map the is a list to recreate the farm map.
    for some reason, we are required to declare a global farm variable to ensure the farm map actually gets updated.
    My assumption is that the farm map is a global variable and we need to update it globally.
    the code will  break the list and update the farm map.
    since the variable will have spaces, strip is needed to remove the spaces and for the crops, since is stored something like {"lettuces": 5},
    we need to strip the {}, space and split the key and value.
    and then append them as a dictionary.
    """
    global farm
    map = []
    try:
        with open("savegame.txt", "r") as file:
            data = file.readlines()
    except FileNotFoundError as e:
        print("No save game found!")
        return
    #load the game variables
    game_vars['day'] = int(data[0])
    game_vars['energy'] = int(data[1])
    game_vars['money'] = int(data[2])
    bag = data[3].strip().split(",")
    for item in bag:
        if item != "": #as the list is ['LET:5', 'POT:3', 'CAU:2', ''], we need to ignore the "" at the end.
            key, value = item.split(":")
            game_vars['bag'][key] = int(value)

    #load the farm
    for map_row in data[4:]:
        a =[] #placeholder list, to ensure that the map is recorded properly as the orignal map.
        map_row = map_row.strip().strip("[]").split(",")
        for crop in map_row:
            if crop.strip(" ") == "'House'": 
                a.append("House")
            elif crop.strip(" ") != "None":
                crop = crop.strip(" ").strip("{").strip("}")
                key, value = crop.split(":")
                a.append({key.strip("'").strip("'"): int(value)})
            else:
                a.append(None)
        map.append(a)
    
    
    farm = map #updates the farm.
    return 
    


def main():
    """
    Main game loop.
    Also serves as the main menu
    (Yes, Im lazy to put this in a function)
    """
    while True:
        print("----------------------------------------------------------")
        print("Welcome to Sundrop Farm!")
        print()
        print("You took out a loan to buy a small farm in Albatross Town.")
        print("You have 20 days to pay off your debt of $100.")
        print("You might even be able to make a little profit.")
        print("How successful will you be?")
        print("----------------------------------------------------------")
        print("1) Start a new Game")
        print("2) Load your saved game")
        print("3) Show Leaderboard\n")
        print("0) Exit the game")
        try:
            choice = int(input("Your choice: "))
        except ValueError:
            print("Invalid choice. Please try again.\n")
            continue
        match choice:
            case 1:
                in_town(game_vars)
            case 2:
                load_game(game_vars)
                in_town(game_vars)
            case 3:
                leaderboard()
            case 0:
                break
            case _:
                print("Invalid choice. Please try again.\n")
                continue
        
        
            
        
# Write your main game loop here
if __name__ == "__main__":
    main()                 