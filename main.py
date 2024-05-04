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

for row in create_board():
    print(' '.join(row))
print()