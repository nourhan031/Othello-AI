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


class Game:
    def __init__(self):
        # init the board and set the first player's turn
        self.board = self.create_board()
        # self.player_turn = 'B'  # black goes first
        self.player_turn = None
        self.user_color = None  # the player's chosen color
        self.computer_color = None

    def create_board(self):
        # 8x8 board initialized with ' '
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

    def print_board(self):
        # Print column indices at the top
        print("     ", end="") # print 5 spaces and prevent adding a new line
        for i in range(len(self.board)): # print col no. at the top
            print(f"{i}    ", end="") # f-str to format each i with 4 spaces after it
        print()
        """
        loop over each row,
        'enum' provides the index 'i' (row no.) 
        and 'row' (actual row data)
        """
        for i, row in enumerate(self.board):
            print(f"{i} ", end=" ") # print row no. at the st of each row
            for cell in row: # iterate over each cell in the current row
                print(f"| {cell} ", end=" ") # print '|' followed by the cell's value and a space
            print("|") # printed at the end of each row
            print("  " + "------" * len(self.board)) # print a line of dashes under each row (its no. is eq. to that of the table's columns)

    def switch_turn(self):
        # switches the player turn between 'B' and 'W'
        self.player_turn = 'W' if self.player_turn == 'B' else 'B'

    def choose_color(self):
        color_choice = input("Choose a color to play with (W for White, B for Black): ").strip().upper()
        if color_choice in ["W", "B"]:
            self.user_color = color_choice
            self.computer_color = 'W' if color_choice == 'B' else 'B'
            # std rules: black goes first
            self.player_turn = 'B'
        else:
            print("Invalid choice, defaulting to Black.")
            self.user_color = 'B'  # default to Black if invalid input
            self.computer_color = 'W'
            self.player_turn = 'B'

    def user_move(self):
        # ask the user for a move and update the board
        while True:
            try:
                row = int(input("Enter the row: "))
                col = int(input("Enter the column: "))
                if 0 <= row < 8 and 0 <= col < 8 and self.board[row][col] == ' ':
                    self.board[row][col] = self.player_turn
                    break
                else:
                    print("Invalid move. The position is either out of bounds or already taken.")
            except ValueError:
                print("Invalid input. Please enter valid row and column numbers.")

    def play_game(self):
        # main game loop
        self.choose_color()  # ssk the user to choose a color

        while True:  # infinite loop (STOPPING CRITERIA IS TO BE IMPLEMENTED LATER)
            # print the current board
            self.print_board()

            print(f"It's {self.player_turn}'s turn.")

            if self.player_turn == self.user_color:
                # user's turn
                self.user_move()  # ask the user to make a move
            else:
                # computer's turn (TO BE IMPLEMENTED!!!!)
                print("computer's turn.")

            # switch turn after a move
            self.switch_turn()

            # IMPLEMENT STOPPING CRITERIA
            # fixed number of moves (for now)
            if sum(row.count(' ') for row in self.board) <= (64 - 10):  # 10 moves total
                break

        # final board state
        self.print_board()
        print("Game over!")


# create game instance
game = Game()

# st. game loop
game.play_game()
