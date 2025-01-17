# student name: Bryan Zhang
# student number: 69238335

# A command-line 2048 game

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
            print(f"|{str(cell).center(5)}", end="")
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

def addANewTwoToBoard() -> None:
    """ 
        adds a new 2 at an available randomly-selected cell of the board
    """
    open_positions: list = [] # a 2-D list that stores the coordinates of open positions on board
    for row in range(4):
        for column in range(4):
            if board[row][column] == '':
                open_positions.append([row,column])
    
    random_position = random.choice(open_positions) # choose a random coordinate from the open positions
    board[random_position[0]][random_position[1]] = 2

def isFull() -> bool:
    """ 
        returns True if no empty cell is left, False otherwise 
    """
    flag = True
    for row in range(4):
        for column in range(4):
            if board[row][column] == '':
                flag = False 
    
    return flag
    
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


if __name__ == "__main__":  # Use as is  
    init()
    displayGame()
    while True:  # Super-loop for the game
        print(f"Score: {getCurrentScore()}")
        userInput = promptGamerForTheNextMove()
        if(userInput == 'Q'):
            print("Exiting the game. Thanks for playing!")
            break
        updateTheBoardBasedOnTheUserMove(userInput)
        addANewTwoToBoard()
        displayGame()

        if isFull(): #game is over once all cells are taken
            print("Game is Over. Check out your score.")
            print("Thanks for playing!")
            break