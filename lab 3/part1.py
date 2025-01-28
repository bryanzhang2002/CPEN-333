#student name: Bryan Zhang
#student number: 69238335

def checkColumn(puzzle: list, column: int):
    """ 
        param puzzle: a list of lists containing the puzzle 
        param column: the column to check (a value between 0 to 8)

        This function checks the indicated column of the puzzle, and 
        prints whether it is valid or not. 
        
        As usual, this function must not mutate puzzle 
    """
    buffer: list = []
    for row in range(len(puzzle)):
        if type(puzzle[row][column]) != int or puzzle[row][column] < 1 or puzzle[row][column] > 9:  # ensures valid entry in the cell
            print(f"Column {column} not valid")
            return

        for i in range(len(buffer)):    # checks for duplicate values
            if puzzle[row][column] == buffer[i]:
                print(f"Column {column} not valid")
                return
        
        buffer.append(puzzle[row][column])        
    
    print(f"Column {column} valid")


def checkRow(puzzle: list, row: int):
    """ 
        param puzzle: a list of lists containing the puzzle 
        param row: the row to check (a value between 0 to 8)

        This function checks the indicated row of the puzzle, and 
        prints whether it is valid or not. 
        
        As usual, this function must not mutate puzzle 
    """
    buffer: list = []
    for column in range(len(puzzle)):
        if type(puzzle[row][column]) != int or puzzle[row][column] < 1 or puzzle[row][column] > 9:  # ensures valid entry in the cell
            print(f"Row {row} not valid")
            return

        for i in range(len(buffer)):    # checks for duplicate values
            if puzzle[row][column] == buffer[i]:
                print(f"row {row} not valid")
                return
        
        buffer.append(puzzle[row][column])        
    
    print(f"row {row} valid")

def checkSubgrid(puzzle: list, subgrid: int):
    """ 
        param puzzle: a list of lists containing the puzzle 
        param subgrid: the subgrid to check (a value between 0 to 8)
        Subgrid numbering order:    0 1 2
                                    3 4 5
                                    6 7 8
        where each subgrid itself is a 3x3 portion of the original list
        
        This function checks the indicated subgrid of the puzzle, and 
        prints whether it is valid or not. 
        
        As usual, this function must not mutate puzzle 
    """
    # calculate the starting row and column coordinates (top left cell) of each 3x3 subgrid
    row_start = (subgrid//3) * 3    
    col_start = (subgrid%3) * 3
    
    # iterate through the 3x3 subgrid's coordinates
    buffer: list = []
    for col in range(col_start, col_start+3):
        for row in range(row_start, row_start+3):
            if type(puzzle[row][col]) != int or puzzle[row][col] < 1 or puzzle[row][col] > 9:   # ensures valid entry in the cell
                print(f"Subgrid {subgrid} not valid")
                return
            
            for i in range(len(buffer)):    # checks for duplicate values
                if puzzle[row][col] == buffer[i]:
                    print(f"Subgrid {subgrid} not valid")
                    return
            
            buffer.append(puzzle[row][col])
    
    print(f"Subgrid {subgrid} valid")


if __name__ == "__main__":
    test1 = [ [6, 2, 4, 5, 3, 9, 1, 8, 7],
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5],
              [1, 4, 3, 8, 6, 5, 7, 2, 9],
              [9, 5, 8, 2, 4, 7, 3, 6, 1],
              [7, 6, 2, 3, 9, 1, 4, 5, 8],
              [3, 7, 1, 9, 5, 6, 8, 4, 2],
              [4, 9, 6, 1, 8, 2, 5, 7, 3],
              [2, 8, 5, 4, 7, 3, 9, 1, 6]
            ]
    test2 = [ [6, 2, 4, 5, 3, 9 , 1, 6, 7],
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5 ],
              [6, 2, 4, 5, 3, 9 , 1, 8, 7],
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5 ],
              [6, 2, 4, 5, 3, 9 , 1, 8, 7],
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5 ]
            ]
    
    test3 = [ [6, 6, 4, 5, 3, 9 , 1, 8, 7],
            [5, 1, 9, 7, 2, 8, 6, 3, 4],
            [8, 3, 7, 6, 1, 4, 2, 9, 5 ],
            [6, 2, 4, 5, 3, 9 , 1, 8, 7],
            [5, 1, 9, 7, 2, 8, 6, 3, 4],
            [8, 3, 7, 6, 1, 4, 2, 9, 5 ],
            [6, 2, 4, 5, 3, 9 , 1, 8, 7],
            [5, 1, 9, 7, 2, 8, 6, 3, 4],
            [8, 3, 7, 6, 1, 4, 2, 100, 5 ]
        ]
    
    testcase = test2   #modify here for other testcases
    SIZE = 9

    for col in range(SIZE):  #checking all columns
        checkColumn(testcase, col)
    for row in range(SIZE):  #checking all rows
        checkRow(testcase, row)
    for subgrid in range(SIZE):   #checking all subgrids
        checkSubgrid(testcase, subgrid)