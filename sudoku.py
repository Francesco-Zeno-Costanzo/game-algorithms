"""
Code for solve sudoku via backtracking
"""

board = [
    [0,1,0,0,0,6,4,0,0],
    [0,9,0,4,5,0,0,2,0],
    [5,0,0,0,0,7,3,0,0],
    [0,0,0,0,0,5,0,0,0],
    [9,0,0,1,8,0,7,0,0],
    [0,2,0,0,0,0,0,0,3],
    [8,0,0,9,4,0,1,0,0],
    [0,0,0,6,0,0,0,0,0],
    [0,0,1,0,0,0,0,7,0]
]


def print_board(grid):
    '''
    Function to print the grid
    
    Parameters
    ----------
    grid : 9x9 matrix 
    '''
    
    N = len(grid)

    line = lambda x : f"  {x[0]} {x[1]} {x[2]} | {x[3]} {x[4]} {x[5]} | {x[6]} {x[7]} {x[8]}" 
    
    for j in range(N):
        if j % 3 == 0 and j != 0:
            print("  - - - - - - - - - - -   ")
        print(line(grid[j]))
        

def empty(grid):
    '''
    Function to find an empty cell, i.e. a zero
    
    Parameters
    ----------
    grid : 9x9 matrix 
    '''
    
    N = len(grid)
    
    # check all grid
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                return i, j
    
    # If fthe grid is full return False
    return False


def check(grid, num, pos):
    '''
    Function to verify if num can be insert in pos
    
    Parameters
    ----------
    grid : 9x9 matrix 
    num : int
        number i want to put in grid
    pos : tuple
        position where i want to insert num
    '''
    
    N = len(grid)

    # Check row
    for i in range(N):
        if grid[pos[0]][i] == num :
            return False

    # Check column
    for i in range(N):
        if grid[i][pos[1]] == num :
            return False

    # Check box
    x0 = pos[1] // 3 * 3
    y0 = pos[0] // 3 * 3

    for i in range(y0, y0 + 3):
        for j in range(x0, x0 + 3):
            if grid[i][j] == num :
                return False

    return True      


def solve(grid):
    '''
    Function to find an empty cell, i.e. a zero
    
    Parameters
    ----------
    grid : 9x9 matrix 
    '''
    
    empty_cell = empty(grid)
    
    # if the grid is full, the game is over
    if not empty_cell :
        return True
    else:
        row, col = empty_cell

    for i in range(1,10):
        # try to insert a number
        if check(grid, i, (row, col)):
            grid[row][col] = i
            
            # recursive call until the grid is filled 
            if solve(grid):
                return True
            
            # if the try doesn't go well i have to return to the previous state
            grid[row][col] = 0

    return False


print("#########################")
print("Initial configuration:")
print("#########################")
print()

print_board(board)
solve(board)

print()
print("#########################")
print("Solution")
print("#########################")
print()
print_board(board)

