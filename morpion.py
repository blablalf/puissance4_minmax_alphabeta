#EQUIPE BRANDON/ALFRED/TOM
import numpy as np
import random as rd
import time

COLOR_RED = '\033[1;31m'  #DEFAULT COLORS FOR PLAYER
COLOR_DEFAULT = '\033[0m' # DEFAULT WHITE COLOR FOR GRID
COLOR_YELLOW = '\033[33m' #DEFAULT COLORS FOR ai
DOT = '\u25cf'

#1ST PART
# Display grid
def print_grid():
    for line_index in range(6):
        print("|", end=' ')
        for column_index in range(12):
            if state[line_index][column_index] == 1:
                print(COLOR_YELLOW + DOT + COLOR_DEFAULT, end=' ') # Coloring the grid, put the dot and reset print color with default color
            elif state[line_index][column_index] == 2:
                print(COLOR_RED + DOT + COLOR_DEFAULT, end=' ')
            else:
                print(" ", end=' ')
            print("|", end=' ')
        print() #Just to go next line
    print("|", end=' ')
    for column_index in range(12):
        print("\u0305 ", end=" ")
        print("|", end=' ')
    print() #Just to go next line
    print("|", end=' ')
    for line_index in range(12):
        if line_index < 9:
            print(line_index + 1, end=" ")
        else:
            print(line_index + 1, end='')
        print("|", end=' ')
    print() #Just to go next line

# Place a new token into the grid
def write_token(grid, column_index, value_to_place):
    for line_index in range(5, -1, -1):
        if grid[line_index][column_index] == 0:
            grid[line_index][column_index] = value_to_place
            return grid

# Return the free columns (possibles actions)
def get_free_columns(state):
    response = []
    for column_index in range(12):
        if state[0][column_index] == 0: # If there is no any token into that column
            response.append(column_index) # Add it into the free columns 
    return response

# Return a copy of the given state with writted token (given with column_index)
def get_simulated_state_move(state, column_index):
    new_state = state.copy()
    new_state = write_token(new_state, column_index, player_minmax)
    return new_state

# Return a tuple with a boolan wich says if the game is ended or not and a column index
def terminal_test(state, move_nonce):
    response = (False, -1) # False = game not ended ; -1 -> not an existing column
    if move_nonce < 7: # Atm, there is no possibility of end, because the game start with the nonce "1" so nor player or AI may have already placed 4 tokens
        return response # So there is no end atm
    if move_nonce == 42: # Tokens supply reached 
        response = (True, 0) # Equality end
    for column_index in range(9): # Check for a possible victory line (beetween column_index 0 and 9 because the next 4 tokens are checked) for ai or player
        for line_index in range(5, -1, -1): # starting from the top line index (5 because bottom start at 0 and there is lines), to 0 (so we put -1 because it's reversed)
            if state[line_index][column_index] == state[line_index][column_index + 1] == state[line_index][column_index + 2] == state[line_index][column_index + 3] != 0: # If the next 4 tokens of the line are equal
                return True, state[line_index][column_index] # It's the end, return the first one
    for line_index in range(5, 2, -1): # Check for a possible victory column (we don't go to -1 because the next 4 are checked)
        for column_index in range(12): # testing each columns
            if state[line_index][column_index] == state[line_index - 1][column_index] == state[line_index - 2][column_index] == state[line_index - 3][column_index] != 0: # If the next 4 tokens (ordered by columns) are equals
                return True, state[line_index][column_index] # It's the end, return the first one
    for line_index in range(5, 2, -1): # Check for diagonals from left to right
        for column_index in range(9): # beetween column_index 0 and 9 because the next 4 tokens are checked
            if state[line_index][column_index] == state[line_index - 1][column_index + 1] == state[line_index - 2][column_index + 2] == state[line_index - 3][column_index + 3] != 0: # If the next 4 tokens (ordered by diagonals from left to the right) are equals
                return True, state[line_index][column_index] # Return the first checked one
    for line_index in range(5, 2, -1): # Check for diagonals from right to left
        for column_index in range(3, 12): # Check from the 9 last columns
            if state[line_index][column_index] == state[line_index - 1][column_index - 1] == state[line_index - 2][column_index - 2] == state[line_index - 3][column_index - 3] != 0: # If the next 4 tokens (ordered by diagonals from right to the left) are equals
                return True, state[line_index][column_index] # Return the first checked one

    return response

#2ND PART

# Define the weight of a node
# cordinate : List containing the coordinates of 4 tokens and their type of alignment (Line, column, diagonal)
# next_is_us: integer of type 0 or 1 indicating whether it is the turn of the human(0) or the computer(1).
# state: game grid at time t
# line_index: line number
# column_index: column number
def weight_utility(cordinate, next_is_us, state, line_index, column_index):
    weight_sum = 0 #The weight of a node
    ones = cordinate.count(1) #count the number of cases with computer tokens
    twos = cordinate.count(2) #count the number of cases with human tokens
    zeros = 4 - ones - twos #count the number of empty case
    if ones == 3 and zeros == 1: #If the number of tokens of the computer color is 3 and there is an empty space
        index_z_rel = cordinate.index(0)  # indicates the index of the empty case
        index_z_abs = 0 #indicate the index of dist between the first token and the list
        if cordinate[4] == 'RISING DIAGONALS':
            index_z_abs = line_index - index_z_rel 
        elif cordinate[4] == 'DESCENDING DIAGONALS':
            index_z_abs = line_index + index_z_rel
        else:
            index_z_abs = line_index
        if next_is_us and (cordinate[4] == 'COLUMN' or index_z_abs == 5 or state[index_z_abs + 1, column_index + index_z_rel]):
            return 20000
        weight_sum = 500
    elif ones == 2 and zeros == 2:
        weight_sum = 200
    elif ones == 1 and zeros == 3:
        weight_sum = 50
    elif twos == 3 and zeros == 1:
        index_z_rel = cordinate.index(0)
        index_z_abs = 0
        if cordinate[4] == 'RISING DIAGONALS':
            index_z_abs = line_index - index_z_rel
        elif  cordinate[4] == 'DESCENDING DIAGONALS':
            line_index + index_z_rel
        else:
            line_index
        if not next_is_us and (cordinate[4] == 'COLUMN' or index_z_abs == 5 or state[index_z_abs + 1, column_index + index_z_rel]):
            return -10000
        weight_sum = -500
    elif twos == 2 and zeros == 2:
        weight_sum = -200
    elif twos == 1 and zeros == 3:
        weight_sum = -50

    return weight_sum

# Evaluation function that calculates the weight of each type node @
def utility(state, weight=-1, next_is_us=0):
    if weight == 1:
        return 1000000
    elif weight == 0:
        return 0
    elif weight == 2:
        return -1000000

    weight_sum = 0
    for line_index in range(5, -1, -1):
        for column_index in range(12):
            # LINE
            if column_index < 9:
                cordinate = (state[line_index, column_index], state[line_index, column_index + 1], state[line_index, column_index + 2], state[line_index, column_index + 3], 'LINE')
                weight_sum += weight_utility(cordinate, next_is_us, state, line_index, column_index)
            # COLOMN
            if line_index > 2 and not state[line_index, column_index]:
                cordinate = (state[line_index, column_index], state[line_index - 1, column_index], state[line_index - 2, column_index], state[line_index - 3, column_index], 'COLOMN')
                weight_sum += weight_utility(cordinate, next_is_us, state, line_index, column_index)
           # RISING DIAGONALS
            if column_index < 9 and line_index > 2:
                cordinate = (state[line_index, column_index], state[line_index - 1, column_index + 1], state[line_index - 2, column_index + 2], state[line_index - 3, column_index + 3], 'RISING DIAGONALS')
                weight_sum += weight_utility(cordinate, next_is_us, state, line_index, column_index)
           # DESCENDING DIAGONALS
            if column_index < 9 and line_index < 3:
                cordinate = (state[line_index, column_index], state[line_index + 1, column_index + 1], state[line_index + 2, column_index + 2], state[line_index + 3, column_index + 3], 'DESCENDING DIAGONALS')
                weight_sum += weight_utility(cordinate, next_is_us, state, line_index, column_index)

    return weight_sum
    
#minmax decision function
#Fonction qui nous retourne le meilleur coup à joueur
def minmax(state):
    a = get_free_columns(state)
    return max(a, key=lambda x: min_value(get_simulated_state_move(state, x), move_nonce))

#Max_ val function
def max_value(state, move_nonce=1, depth=1):
    terminal_result = terminal_test(state, move_nonce)
    if terminal_result[0] or depth >= depth_limit:
        return utility(state, terminal_result[1], 1)
    value = -10000000
    for a in get_free_columns(state):
        global player_minmax
        player_minmax = 1
        value = max(value, min_value(get_simulated_state_move(state, a), move_nonce + 1, depth + 1))
    return value
    
#Min_val function
def min_value(state, move_nonce=1, depth=1):
    terminal_result = terminal_test(state, move_nonce)
    if terminal_result[0] or depth >= depth_limit:
        return utility(state, terminal_result[1], 0)
    value = 10000000
    for a in get_free_columns(state):
        global player_minmax
        player_minmax = 2
        value = min(value, max_value(get_simulated_state_move(state, a), move_nonce + 1, depth + 1))
    player_minmax = 1
    return value

#Alpha_Beta function
def alpha_beta(state):
    a = get_free_columns(state)
    return max(a, key=lambda x: min_value_alpha_beta(get_simulated_state_move(state, x), -10000000, 10000000, move_nonce))

#Max_ Val Alpha Beta function
def max_value_alpha_beta(state, alpha, beta, move_nonce=1, depth=1):
    terminal_result = terminal_test(state, move_nonce)
    if terminal_result[0] or depth >= depth_limit:
        return utility(state, terminal_result[1])
    value = -10000000
    for free_columns in get_free_columns(state):
        global player_minmax
        global action
        player_minmax = 1
        temp = min_value_alpha_beta(get_simulated_state_move(state, free_columns), alpha, beta, move_nonce + 1, depth + 1)
        if temp > value:
            value = temp
            action = free_columns
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value

#Min_ Val Alpha Beta function
def min_value_alpha_beta(state, alpha, beta, move_nonce=1, depth=1):
    terminal_result = terminal_test(state, move_nonce)
    if terminal_result[0] or depth >= depth_limit:
        return utility(state, terminal_result[1])
    value = 10000000
    for a in get_free_columns(state):
        global player_minmax
        player_minmax = 2
        value = min(value, max_value_alpha_beta(get_simulated_state_move(state, a), alpha, beta, move_nonce + 1, depth + 1))
        if value <= alpha:
            return value
        beta = min(beta, value)
    player_minmax = 1
    return value

# Return a tuple with boolan value equals true if it worked (ia wins directly) and the new state
#NOT FINISH
def win_directly(state, move_nonce):
    if terminal_test(state, move_nonce) == (False, -1):
        for column_index in range(9): # Check for a possible victory line (beetween column_index 0 and 9 because the next 4 tokens are checked) for ai or player
            for line_index in range(5, -1, -1): # starting from the top line index (5 because bottom start at 0 and there is lines), to 0 (so we put -1 because it's reversed)
                if state[line_index][column_index] == state[line_index][column_index + 1] and state[line_index][column_index + 1] == state[line_index][column_index + 2] and state[line_index][column_index + 3] == 0 and (line_index == 0 or state[line_index - 1][column_index] != 0): # If the next 4 tokens of the line are equal
                    return (True, write_token(state, column_index + 3, 1))
        for column_index in range(1,9):
            return 0
    return 0
    
#3RD PART
# Main code of the game, here we start
if __name__ == '__main__':
    play_again = "y"
    while play_again == "y": # Restart a game while the player select "y"
        print('\n\nBeginning of the game\n')
        depth_limit = 3 # Exponential difficulty (decrease to 3 for no powerful devices and increase up to 5 for higher high powered devices)
        move_nonce = 1 # lap count
        state = np.zeros((6, 12), dtype=int) # grid init
        print_grid() # Display the empty grid
        print('Lap nonce : ', move_nonce)
        action = 0
        human_player = 0 
        while human_player == 0:
            try:
                human_player = int(input('Which player starts ' + '1: AI, 2: Player : ')) #chose which player start to play.
            except ValueError:
                human_player = 0
        player_minmax = 1
        while not terminal_test(state, move_nonce - 1)[0]:
            if human_player == 1:
                print(COLOR_YELLOW + "AI's Turn")
                start = time.time()#Start time
                action = 0
                decision = alpha_beta(state) #take decision in the MINMAX A/B algo.
                end = time.time() #Finish time
                print("AI decision :", decision + 1)
                print(COLOR_DEFAULT + 'Time elapsed :', end - start, 'seconds\n') #Display the time to play the move
            else:
                print(COLOR_RED + "Player turn")
                possible_moves = get_free_columns(state) #return the free columns (possibles actions) after the AI played
                possible_mo0s = [x + 1 for x in possible_moves] # Increment possible_moves values of 1 because index start at 0
                decision = -1
                while decision not in possible_moves: #if the decision is not in the possible actions then we start again a decision
                    try:
                        decision = int(input(COLOR_DEFAULT + "Select a column between [1:12] : "))
                    except ValueError:
                        decision = -1
                decision -= 1

            state = write_token(state, decision, human_player )#write on the grid where we want to play
            move_nonce += 1
            human_player = human_player % 2 + 1
            print_grid() #DISPLAY GRID
            print('Lap nonce :', move_nonce)#Display counter
        win_state = terminal_test(state, move_nonce - 1)[1]
        if win_state == 1:
            print(COLOR_YELLOW + "Ai victory" + COLOR_DEFAULT)
        elif win_state == 2:
            print(COLOR_YELLOW + "Player Victory" + COLOR_DEFAULT)
        else:
            print("Equality")
        play_again = "z"
        
        #Here we choose if the player wants to replay or no.
        while not (play_again == "n" or play_again == "y"):
            try:
                play_again = str(input('Do you want to replay ? (n/y) : '))
            except ValueError:
                play_again = "n"
