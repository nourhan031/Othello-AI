"""
1- game state representation:
    1- board config
    2- player's turn
2- move generation:
    1- gen all possible moves for a given game state
3- eval function:
    *done from the perspective of a player (need to read more abt this)*
4- alpha-beta pruning:
    a search algorithm used to improve the performance of the minimax algorithm.
    It reduces the number of nodes that need to be evaluated by pruning branches
     of the game tree that are determined to be irrelevant.
5- loop:
    players alternate turns -> game state is updated after each move and the game
    ends when there are no valid moves left
"""

def create_board():
    # 8x8 board all init to " "
    board = [[' ' for _ in range(8)] for _ in range(8)]
    """
    [3][3],[4][4]: init to white
    [3][4],[4][3]: init to black
    """
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'

    return board

# for row in create_board():
#     print(' '.join(row))
# print()

def print_board(board):
    print("     ", end="") # print 5 spaces and prevent adding a new line
    for i in range(len(board)): # print col no. at the top
        print(f"{i}    ", end="") # f-str to format each i with 4 spaces after it
    print()
    for i, row in enumerate(board): # loop over each row, 'enum' provides the index 'i' (row no.) and 'row' (actual row data)
        print(f"{i} ", end=" ") # print row no. at the st of each row
        for j, cell in enumerate(row): # iterate over each cell in the current row
            print(f'| {cell} ', end=' ') # print '|' followed by the cell's value and a space
        print('|') # printed at the end of each row
        print("  ", end="") # space bet each printed no. at the top of the table
        print("------" * len(board)) # print a line of dashes under each row (its no. is eq. to that of the table's columns)

print_board(create_board())
