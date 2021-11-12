"""
File: pyopoly.py
Gilbert Ijoma
Date: 10/21/20
Description: A 2 player simplified version of monopoly game
"""
from sys import argv
from random import randint, seed
from board_methods import load_map, display_board
if len(argv) >= 2:
    seed(argv[1])

def format_display(player1_or_2,icons,board):
            
    die_roll = randint(1,6)
    die_roll += randint(1,6)
        
    player1_icon = icons[0]
    player2_icon = icons[1]
         
    player1_and_2_icon = icons[0]
    player1_and_2_icon += ' '
    player1_and_2_icon += icons[1]
    
    position1 = 0
    position2 = 0
    position3 = 0
    list_places = []
    
    for line in load_map('proj1_board1.csv'):
        list_places.append(line['Place'])    

    #for loop to find the position of every symbol    
    for i in range(32):
        if board[i] == board[i][0:6] + player1_icon.ljust(5):
            position1 = i
        if board[i] == board[i][0:6] + player2_icon.ljust(5):
            position2 = i

        if board[i] == board[i][0:6] + player1_and_2_icon.ljust(5):
            position3 = i
            position1 = i
            position2 = i
            
    #decision structure used to determine the player, then add the die roll to the player's position
    if player1_or_2 == 'player1':
        
        position1 += int(die_roll)
        position1 %= len(the_board)
              
        if board[position1] != board[position1][0:6] + player2_icon.ljust(5):
            copy_board = list(the_board)
            copy_board[position1] = copy_board[position1][0:6] + player1_icon.ljust(5)
            copy_board[position2] = copy_board[position2][0:6] + player2_icon.ljust(5)
            display_board(copy_board)
            
            print(icons[3],"You rolled a",die_roll)
            print(icons[3],"You have landed on",list_places[position1])
        else:

            copy_board = list(the_board)
            copy_board[position1] = copy_board[position1][0:6] + player1_and_2_icon.ljust(5)
            display_board(copy_board)

            print(icons[3],"You rolled a",die_roll)
            print(icons[3],"You have landed on",list_places[position1])
    else:

        position2 += int(die_roll)
        position2 %= len(the_board)
        
              
        if board[position2] != board[position2][0:6] + player1_icon.ljust(5):
            copy_board = list(the_board)
            copy_board[position2] = copy_board[position2][0:6] + player2_icon.ljust(5)
            copy_board[position1] = copy_board[position1][0:6] + player1_icon.ljust(5)
            display_board(copy_board)
            
            print(icons[4],"You rolled a",die_roll)
            print(icons[4],"You have landed on",list_places[position2])
            

        else:
            
            copy_board = list(the_board)
            copy_board[position2] = copy_board[position2][0:6] + player1_and_2_icon.ljust(5)
            display_board(copy_board)

            print(icons[4],"you rolled a",die_roll)
            print(icons[4],"you have landed on",list_places[position2])
    return copy_board

def take_turn(player,icons,board,boardInfo):

    position1 = 0
    position2 = 0
    position3 = 0

    player1_icon = icons[0]
    player2_icon = icons[1]

    player1_and_2_icon = icons[0]
    player1_and_2_icon += ' '
    player1_and_2_icon += icons[1]

    #for loop to determine the position of every symbols position
    for i in range(32):
        if board[i] == board[i][0:6] + player1_icon.ljust(5):
            position1 = i
        if board[i] == board[i][0:6] + player2_icon.ljust(5):
            position2 = i

        if board[i] == board[i][0:6] + player1_and_2_icon.ljust(5):
            position3 = i
            position1 = i
            position2 = i

    boardInfo['board_position1'] = position1
    boardInfo['board_position2'] = position2
    action = ""
#I used this if statement so I wouldnt have repeat the same for player 2
    if player == 'player2':
        position1 = position2
        
#If statement to apply the rent based on the space, and if player goes bankrupt, finish the game
    if player == 'player1':
        if boardInfo['CurrentRent1'][position1] != -2:
            print("You have landed on",icons[4]+"'s property, you must pay the rent")
            print("You have paid",boardInfo['CurrentRent1'][position1],"to",icons[4])
            boardInfo['Funds1'] -= int(boardInfo['CurrentRent1'][position1])
            boardInfo['Funds2'] += int(boardInfo['CurrentRent1'][position1])
            if boardInfo['Funds1'] <= BANKRUPT:
                print("You have been knocked out of the game.")
                print("The game has finally ended.",icons[4],"is the winner and now we can all go home.")
                action = "5"                
    else:
        if boardInfo['CurrentRent2'][position1] != -2:
            print("You have landed on",icons[3]+"'s property, you must pay the rent")
            print("You have paid",boardInfo['CurrentRent2'][position1],"to",icons[3])
            boardInfo['Funds2'] -= int(boardInfo['CurrentRent2'][position1])
            boardInfo['Funds1'] += int(boardInfo['CurrentRent2'][position1])
            if boardInfo['Funds2'] <= BANKRUPT:
                print("You have been knocked out of the game.")
                print("The game has finally ended.",icons[3],"is the winner and now we can all go home.")
                action = "5"
    
    #while statement for the basic menu 
    while action != "5":
        
        print('\n')
        print("    1) Buy Property")
        print("    2) Get Property Info")
        print("    3) Get Player Info")
        print("    4) Build a Building")
        print("    5) End Turn")
        print('\n')
    
        action = input("What do you want to do? \n")

        if action == "1":
            if boardInfo['Price'][position1] == "-1":
                print("You cannot buy this property. It cannot be bought or sold")

            elif boardInfo['Ownership'][position1] == icons[3]:
                print("This property is owned by",icons[3])

            elif boardInfo['Ownership'][position1] == icons[4]:
                print("This property is owned by",icons[4])
                
            else:
                buy_or_not = input("This property is unowned, do you want to buy it? ")
                if buy_or_not.lower() == "yes" or buy_or_not.lower() == "y":
                    if player == 'player1':
                        if boardInfo['Funds1'] < int(boardInfo['Price'][position1]):
                            print("You dont have the funds for this purchase")

                        else:
                            print("You have bought",boardInfo['Place'][position1])
                            boardInfo['Ownership'][position1] = icons[3]
                            boardInfo['Funds1'] -= int(boardInfo['Price'][position1])
                            boardInfo['CurrentRent2'][position1] = int(boardInfo['Rent'][position1])
                            
                    elif player == 'player2':
                        if boardInfo['Funds2'] < int(boardInfo['Price'][position1]):
                            print("You dont have the funds for this purchase")

                        else:
                            print("You have bought",boardInfo['Place'][position1])
                            boardInfo['Funds2'] -= int(boardInfo['Price'][position1])
                            boardInfo['Ownership'][position1] = icons[4]
                            boardInfo['CurrentRent1'][position1] = int(boardInfo['Rent'][position1])
                else:
                    print("You have decided not to buy",boardInfo['Place'][position1])

        elif action == "2":
            propertyName = input("For which property do you want to get the information? ")
            if propertyName in boardInfo['Place']:

                for i in range(32):
                    if propertyName == boardInfo['Place'][i]:
                        index = i

                print("\n      ",propertyName)
                print("       Price:",boardInfo['Price'][index])
                if boardInfo['Ownership'][index] == "":
                    print("       Owner: BANK")
                else:
                    print("       Owner:",boardInfo['Ownership'][index])
                print("       Building:",boardInfo['Building'][index])
                print("       Rent",boardInfo['Rent'][index]+",",boardInfo['BuildingRent'][index],"(with building)")
                    
        elif action == "3":
            print("The players in the game are: \n")
            print("      ",icons[3])
            print("      ",icons[4])

            the_player = input("\n What player do you wish to know about? ")

            if the_player == icons[3]:
                print("Player name:",icons[3])
                print("Current money:",boardInfo['Funds1'])
                print("Player symbol:",icons[0],"\n")
                print("Properties Owned: \n")
                count = 0
                
                for i in range(32):
                    if boardInfo['Ownership'][i] == icons[3]:
                        print("               ",boardInfo['Place'][i])
                        count += 1
                        
                if count == 0:
                    print("               No properties yet")

            elif the_player == icons[4]:
                print("Player name:",icons[4])
                print("Current money:",boardInfo['Funds2'])
                print("Player symbol:",icons[1],"\n")
                print("Properties Owned: \n")
                
                count2 = 0

                for i in range(32):
                    if boardInfo['Ownership'][i] == icons[4]:
                        print("               ",boardInfo['Place'][i])
                        count2 += 1

                if count2 == 0:
                    print("               No properties yet")
                    
        elif action == "4":
            property2 = input("Which property do you want to build a building on? ")
            index2 = -1
            for i in range(32):
                    if property2 == boardInfo['Place'][i]:
                        index2 = i
                        
            if boardInfo['Ownership'][index2] != "" and boardInfo['Building'][index2] == "No":
                if player == 'player1':
                    if boardInfo['Funds1'] < int(boardInfo['BuildingCost'][index2]):
                        print("You don't have the funds for that purchase")
                    else:
                        print("You have built the building for",boardInfo['Place'][index2])
                        boardInfo['Building'][index2] = "Yes"
            
                        boardInfo['Funds1'] -= int(boardInfo['BuildingCost'][index2])
                        boardInfo['CurrentRent2'][index2] += int(boardInfo['BuildingRent'][index2])
                else:
                    if boardInfo['Funds2'] < int(boardInfo['BuildingCost'][index2]):
                        print("You don't have the funds for that purchase")

                    else:
                        print("You have built the building for",boardInfo['Place'][index2])
                        boardInfo['Building'][index2] = "Yes"

                        boardInfo['Funds2'] -= int(boardInfo['BuildingCost'][index2])
                        boardInfo['CurrentRent1'][index2] += int(boardInfo['BuildingRent'][index2])

            else:
                print("The property either has a building, isn't yours, or doesn't exist")
                
    return boardInfo
                        
                
def play_game(starting_money,pass_go_money,board_file):

    icons = ['','','','','']
    #set up the names, and the symbols
    icons[3] = input("First player, what is your name? ")
    while icons[0] not in ALPHABET:
        icons[0] = input("Fisrt player, what do you want your character to use? ")
    
    icons[4] = input("Second player, what is your name? ")
    
    while icons[1] not in ALPHABET:
        icons[1] = input("Second player, what do you want your character to use? ")

    icon1 = icons[0]
    icon2 = icons[1]
    iconjoin = icon1
    iconjoin += icon2
    icons[2] = iconjoin

    #Set up all the lists for the main dictionary
    
    list_abbrev = []
    list_price = []
    list_rent = []
    list_buildingRent = []
    list_buildingCost = []
    list_ownership = []
    list_places = []
    built_or_not = []
    current_rent1 = []
    current_rent2 = []

    for line in load_map('proj1_board1.csv'):
        list_places.append(line['Place'])
    
    for line in load_map('proj1_board1.csv'):
        list_abbrev.append(line['Abbrev'])

    for line in load_map('proj1_board1.csv'):
        list_price.append(line['Price'])

    for line in load_map('proj1_board1.csv'):
        list_rent.append(line['Rent'])

    for line in load_map('proj1_board1.csv'):
        list_buildingRent.append(line['BuildingRent'])

    for line in load_map('proj1_board1.csv'):
        list_buildingCost.append(line['BuildingCost'])
    
    for i in range(32):
        list_ownership.append("")

    for i in range(32):
        built_or_not.append("No")

    for i in range(32):
        current_rent1.append(-2)

    for i in range(32):
        current_rent2.append(-2)
    #main dictionary    
    boardInfo = {'Price': list_price, 'Rent': list_rent,'BuildingRent': list_buildingRent, 'BuildingCost': list_buildingCost,'Funds1': START_FUNDS, 'Funds2': START_FUNDS, 'Ownership': list_ownership, 'Place': list_places, 'Building': built_or_not, 'CurrentRent1': current_rent1, 'CurrentRent2': current_rent2, 'board_position1': 0, 'board_position2': 0}

    the_board = [] 

#creation of the board
    for i in range(32):
        the_board.append(list_abbrev[i].format(i)[0:5].ljust(5) + '\n     ')
    
    
    player1_icon = icons[0]
    player2_icon = icons[1]

#putting the icons in start position
    player1_and_2_icon = icons[0]
    player1_and_2_icon += ' '
    player1_and_2_icon += icons[1]    

    die_roll = START_POSITION
    position1 = 0
    position1 += int(die_roll)
    position1 %= len(the_board)
    copy_board = list(the_board)
    copy_board[position1] = copy_board[position1][0:6] + player1_and_2_icon.ljust(5)

    x = 0
    #initial casting of the functions  using copy_board and boardInfo    
    s = format_display('player1',icons,copy_board)
    t = take_turn('player1',icons,s,boardInfo)


    s = format_display('player2',icons,s)
    t = take_turn('player2',icons,s,t)
    
    pass_go_position1_player1 = 1000
    pass_go_position2_player1 = 1000
    pass_go_position1_player2 = 1000
    pass_go_position2_player2 = 1000

    #while loop for the whole game, it's all nested so that at any point in the running of the while loop if a player is bankrupt, it will just stop.
    while boardInfo['Funds1'] >= BANKRUPT and boardInfo['Funds2'] >= BANKRUPT:

        s = format_display('player1',icons,s)
        t = take_turn('player1',icons,s,t)

        if boardInfo['Funds1'] >= BANKRUPT:
            Done = "Rip to the woo"

            pass_go_position1_player1 = boardInfo['board_position1']
            #These if statements are for the pass go amount so that it gets accuratly implemented 
            if pass_go_position1_player1 in range(25,32) and pass_go_position2_player1 in range(0,13) or pass_go_position2_player1 in range(25,32) and pass_go_position1_player1 in range(0,13):
                boardInfo['Funds1'] += PASS_GO_AMOUNT
                

            else:
                if pass_go_position1_player1 in range(19,32) and pass_go_position2_player1 in range(0,6) or pass_go_position2_player1 in range(19,32) and pass_go_position1_player1 in range(0,6):
                    boardInfo['Funds1'] += PASS_GO_AMOUNT
                    

            s = format_display('player2',icons,s)
            t = take_turn('player2',icons,s,t)

            if boardInfo['Funds2'] >= BANKRUPT:
                

                pass_go_position1_player2 = boardInfo['board_position2']
        
                if pass_go_position1_player2 in range(25,32) and pass_go_position2_player2 in range(0,13) or pass_go_position2_player2 in range(25,32) and pass_go_position1_player2 in range(0,13):
                    boardInfo['Funds2'] += PASS_GO_AMOUNT

                else:
                    if pass_go_position1_player2 in range(19,32) and pass_go_position2_player2 in range(0,6) or pass_go_position2_player2 in range(19,32) and pass_go_position1_player2 in range(0,6):
                        boardInfo['Funds2'] += PASS_GO_AMOUNT
                        print(boardInfo['Funds2'])
            
                    s = format_display('player1',icons,s)
                    t = take_turn('player1',icons,s,t)

                    if boardInfo['Funds1'] >= BANKRUPT:
                        

                        pass_go_position2_player1 = boardInfo['board_position1']
            
                        if pass_go_position1_player1 in range(25,32) and pass_go_position2_player1 in range(0,13) or pass_go_position2_player1 in range(25,32) and pass_go_position1_player1 in range(0,13):
                            boardInfo['Funds1'] += PASS_GO_AMOUNT

                        else:
                            if pass_go_position1_player1 in range(19,32) and pass_go_position2_player1 in range(0,6) or pass_go_position2_player1 in range(19,32) and pass_go_position1_player1 in range(0,6):
                                boardInfo['Funds1'] += PASS_GO_AMOUNT

                            s = format_display('player2',icons,s)
                            t = take_turn('player2',icons,s,t)

                            if boardInfo['Funds2'] >= BANKRUPT:
                                

                                pass_go_position2_player2 = boardInfo['board_position2']
        
                                if pass_go_position1_player2 in range(25,32) and pass_go_position2_player2 in range(0,13) or pass_go_position2_player2 in range(25,32) and pass_go_position1_player2 in range(0,13):
                                    boardInfo['Funds2'] += PASS_GO_AMOUNT

                                else:
                                    if pass_go_position1_player2 in range(19,32) and pass_go_position2_player2 in range(0,6) or pass_go_position2_player2 in range(19,32) and pass_go_position1_player2 in range(0,6):
                                        boardInfo['Funds2'] += PASS_GO_AMOUNT


START_POSITION = 0
QUIT_STRING = 'quit'
START_FUNDS = 1500
PASS_GO_AMOUNT = 200
BANKRUPT = 0
ALPHABET = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']

if __name__ == '__main__':

    
    list_abbrev = []    
    the_board = []
    
    for line in load_map('proj1_board1.csv'):
        list_abbrev.append(line['Abbrev'])

#for loop to set up the board
    for i in range(32):
        the_board.append(list_abbrev[i].format(i)[0:5].ljust(5) + '\n     ')

#function call to start the game
    play_game(START_FUNDS,PASS_GO_AMOUNT,'proj1_board1.csv')
    
