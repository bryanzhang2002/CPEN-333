# student name: Bryan Zhang
# student number: 69238335

# A command-line 2048 game

"""
Additional functionality: 
    - displays winning message when player creates 2048 tile
    - gives the option to continue playing after the game is won
    - implemented authentic colours based on the tile value
"""

import random

board: list[list] = []  # a 2-D list to keep the current status of the game board

def init() -> None:  # Use as is
    """ 
        initializes the board variable
        and prints a welcome message
    """
    # initialize the board cells with ''
    for _ in range(4):     
        rowList = []
        for _ in range(4):
            rowList.append('')
        board.append(rowList)
    # add two starting 2's at random cells
    twoRandomNumbers = random.sample(range(16), 2)   # randomly choose two numbers between 0 and 15   
    # correspond each of the two random numbers to the corresponding cell
    twoRandomCells = ((twoRandomNumbers[0]//4,twoRandomNumbers[0]%4),
                    (twoRandomNumbers[1]//4,twoRandomNumbers[1]%4))
    for cell in twoRandomCells:  # put a 2 on each of the two chosen random cells
        board[cell[0]][cell[1]] = 2

    print(); print("Welcome! Let's play the 2048 game."); print()

def displayGame() -> None:  # Use as is
    """ displays the current board on the console """
    print("+-----+-----+-----+-----+")
    for row in range(4): 
        for column in range(4):
            cell = board[row][column]

            # EXTRA FUNCTIONALITY: implementing authentic text colours based on the number of the tile
            if cell == 2:
                color = "\033[48;2;238;228;219m"
            elif cell == 4:
                color = "\033[48;2;238;224;203m"  
            elif cell == 8:
                color = "\033[48;2;243;178;122m"  
            elif cell == 16:
                color = "\033[48;2;244;148;100m"  
            elif cell == 32:
                color = "\033[48;2;246;124;95m"  
            elif cell == 64:
                color = "\033[48;2;244;99;60m"  
            elif cell == 128:
                color = "\033[48;2;208;114;255m" 
            elif cell == 256:
                color = "\033[48;2;236;204;100m" 
            elif cell == 512:
                color = "\033[48;2;238;201;80m"  
            elif cell == 1024:
                color = "\033[48;2;236;196;60m"  
            elif cell == 2048:
                color = "\033[48;2;236;196;44m"  
            else:
                color = "" 
            print(f"|{color}{str(cell).center(5)}\033[0m", end="")
        print("|")
        print("+-----+-----+-----+-----+")

def promptGamerForTheNextMove() -> str: # Use as is
    """
        prompts the gamer until a valid next move or Q (to quit) is selected
        (valid move direction: one of 'W', 'A', 'S' or 'D')
        returns the user input
    """
    print("Enter one of WASD (move direction) or Q (to quit)")
    while True:  # prompt until a valid input is entered
        move = input('> ').upper()
        if move in ('W', 'A', 'S', 'D', 'Q'): # a valid move direction or 'Q'
            break
        print('Enter one of "W", "A", "S", "D", or "Q"') # otherwise inform the user about valid input
    return move

def addANew2Or4ToBoard() -> None:
    """ 
        adds a new 2 or 4 at an available randomly-selected cell of the board in a position that is not easy to merge immediatly
    """
    chosen_value = random.choice([2,2,4])
    
    open_positions: list = [] # a 2-D list that stores the coordinates of open positions on board
    for row in range(4):
        for column in range(4):
            if board[row][column] == '':
                open_positions.append([row,column])
    
    optimal_positions: list = [] # a subset of open_positions that stores locations where the added number will make it harder to immediately do a slide/merge
    for row, column in open_positions:
        has_match = False   # this indicates if there is a possible merge in one move at this location

        # Check for the first non-empty neighbor in each direction
        if row > 0:
            for i in range(row - 1, -1, -1):  # Iterate upwards
                if board[i][column] != '':
                    if board[i][column] == chosen_value:
                        has_match = True
                    break

        if row < 3:
            for i in range(row + 1, 4):  # Iterate downwards
                if board[i][column] != '':
                    if board[i][column] == chosen_value:
                        has_match = True
                    break

        if column > 0:
            for i in range(column - 1, -1, -1):  # Iterate leftwards
                if board[row][i] != '':
                    if board[row][i] == chosen_value:
                        has_match = True
                    break

        if column < 3:
            for i in range(column + 1, 4):  # Iterate rightwards
                if board[row][i] != '':
                    if board[row][i] == chosen_value:
                        has_match = True
                    break

        if not has_match:
            optimal_positions.append([row, column])

    if len(optimal_positions) != 0:
        random_position = random.choice(optimal_positions) # choose a random coordinate from the optimal positions if possible
    elif len(open_positions) != 0:   # if there aren't any optimal positions select a random open position
        random_position = random.choice(open_positions)
    else:    # in case the board is full but there are still valid moves
        print("please enter a valid move")
        return
    
    board[random_position[0]][random_position[1]] = chosen_value

def isFullAndNoValidMove() -> bool:
    """
    Checks if the board is full and there are no valid moves left.
    """
    for row in range(4):
        for col in range(4):
            if board[row][col] == '':
                return False  # Empty cell exists
            if col < 3 and board[row][col] == board[row][col + 1]:
                return False  # Horizontal merge is possible
            if row < 3 and board[row][col] == board[row + 1][col]:
                return False  # Vertical merge is possible
    return True
 
def getCurrentScore() -> int:
    """ 
        calculates and returns the current score
        the score is the sum of all the numbers currently on the board
    """
    score = 0
    for row in range(4):    # iterate through board and sum up all the non-empty elements
        for column in range(4):
            if type(board[row][column]) == int:  # check that the element is an int, and if so add it to the score
                score += board[row][column]
    return score

def updateTheBoardBasedOnTheUserMove(move: str) -> None:
    """
        updates the board variable based on the move argument by sliding and merging
        the move argument is either 'W', 'A', 'S', or 'D'
        directions: W for up; A for left; S for down, and D for right
    """
    if move == 'W':
        for column in range(4):
            new_column = [] # this is a list that will store the numbers of the modified columns after shifting upward
            for row in board:
                new_column.append(row[column])
            
            new_column = slide_row(new_column, 'left') # even though the motion is upward, this is the same as tipping the column and sliding left
            
            for row in range(4):
                board[row][column] = new_column[row]
    
    if move == 'A':
        for row in range(4):
            board[row] = slide_row(board[row], 'left')
    
    if move == 'S':
        for column in range(4):
            new_column = [] # this is a list that will store the numbers of each column
            for row in board:
                new_column.append(row[column])
            
            new_column = slide_row(new_column, 'right') # even though the motion is downward, this is the same as tipping the column and sliding right
            
            for row in range(4):
                board[row][column] = new_column[row]

    if move == 'D':
        for row in range(4):
            board[row] = slide_row(board[row], 'right')

#up to two new functions allowed to be added (if needed)
#as usual, they must be documented well
#they have to be placed below this line
def slide_row(row: list, direction: str) -> list:
    """
    Slides a single row in the specified direction ('left' or 'right').
    Returns the new row.
    """
    new_row = [] 
    for tile in row: # save all non-empty tiles in the row to a list
        if type(tile) == int:
            new_row.append(tile)

    if direction == 'left':
        for _ in range(4 - len(new_row)): # fill empty spaces with '' until there are four elements in the row
            new_row.append('') 
        for i in range(3):
            if new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                new_row[i+1] = ''
        
        # run this code again in case there were consecutive merges
        new_row2 = []
        for tile in new_row: # save all non-empty tiles in the row to a list
            if type(tile) == int:
                new_row2.append(tile)
        for _ in range(4 - len(new_row2)):
            new_row2.append('')
        
        new_row = new_row2
        return new_row

    elif direction == 'right':
        for _ in range(4 - len(new_row)): # fill empty spaces with '' until there are four elements in the row
            new_row.insert(0, '')
        
        for i in range(3):
            if new_row[i] == new_row[i+1]:
                new_row[i+1] *= 2
                new_row[i] = ''
        
        new_row2 = []
        for tile in new_row: # save all non-empty tiles in the row to a list
            if type(tile) == int:
                new_row2.append(tile)
        for _ in range(4 - len(new_row2)): # fill empty spaces with '' until there are four elements in the row
            new_row2.insert(0, '')
        new_row = new_row2
        return new_row

def check_win() -> bool:
    """
    EXTRA FUNCTIONALITY
    Checks if the board contains the 2048 tile.
    Returns True if the player has won, otherwise False.
    """
    for row in range(4):
        for col in range(4):
            if board[row][col] == 2048:
                return True
    return False

if __name__ == "__main__":  # Use as is  
    player_won = False # flag that tracks if player won
    init()
    displayGame()
    while True:  # Super-loop for the game
        print(f"Score: {getCurrentScore()}")
        userInput = promptGamerForTheNextMove()
        if(userInput == 'Q'):
            print("Exiting the game. Thanks for playing!")
            break
        updateTheBoardBasedOnTheUserMove(userInput)
        addANew2Or4ToBoard()
        displayGame()

        if not player_won and check_win():  # EXTRA FUNCTIONALITY: checks if player won, and prompts them to continue playing or not
            print("Congratulations! You have created the 2048 tile and won!")
            while True:
                userInput = input("Do you want to continue playing? (Y/N): ").upper()
                if userInput in ('Y', 'N'):
                    break
                print('Enter one of "Y", "N"')
            if userInput == 'N':
                print("Thanks for playing!")
                break
            player_won = True
            displayGame()
        
        if isFullAndNoValidMove(): #game is over once all cells are taken
            print("Game is Over. Check out your score.")
            print("Thanks for playing!")
            break