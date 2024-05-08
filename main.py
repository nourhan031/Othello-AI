import copy

DEFAULT_DIFFICULTY = "Medium"

def choose_difficulty():
    while True:
        print("Choose difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            return "Easy"
        elif choice == '2':
            return "Medium"
        elif choice == '3':
            return "Hard"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

class OthelloGame:
    def __init__(self, difficulty=DEFAULT_DIFFICULTY):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'  # Initial setup: Place two white disks at the center
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'  # Initial setup: Place two black disks at the center
        self.board[4][3] = 'B'
        self.current_player = 'B'
        self.other_player = 'W'
        self.difficulty = difficulty  # Difficulty level attribute

        # Distribute remaining disks evenly between players
        self.remaining_disks = 60
        self.black_disks = 30
        self.white_disks = 30

    def play(self):
        while not self.is_game_over():
            self.print_board()
            if self.current_player == 'B':
                self.human_move()
            else:
                self.computer_move()
            self.current_player, self.other_player = self.other_player, self.current_player
        self.print_board()
        self.print_winner()

    def print_board(self):
        print("\n  0 1 2 3 4 5 6 7")
        print(" +-+-+-+-+-+-+-+-+")
        for i in range(8):
            print(f"{i}|{'|'.join(self.board[i])}|")
            print(" +-+-+-+-+-+-+-+-+")

    def human_move(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            print("No valid moves. Skipping turn.")
            return
        print("Valid moves:", valid_moves)
        move_str = input("Enter row and column separated by space (e.g., 2 3): ")
        try:
            row, col = map(int, move_str.split())
            if (row, col) in valid_moves:
                # self.make_move(row, col)
                self.make_move(self.board, row, col)
            else:
                print("Invalid move. Try again.")
                self.human_move()
        except ValueError:
            print("Invalid input format. Please enter two integers separated by space.")
            self.human_move()

    def computer_move(self):
        # depth = self.difficulty_to_depth()
        if self.difficulty == "Easy":
            depth = 1
        else:
            depth = self.difficulty_to_depth()

        eval, move = self.alpha_beta_pruning(self.board, depth, float('-inf'), float('inf'), True)
        if move is not None:
            # self.make_move(*move)
            self.make_move(self.board, move[0], move[1])
            self.print_board()
            print(f"Computer plays at row {move[0]}, column {move[1]}")
        else:
            print("No valid moves for the computer.")

    def is_valid_move(self, board, row, col):
        if board[row][col] != ' ':
            return False
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self.is_valid_direction(board, row, col, dr, dc):
                    return True
        return False

    def is_valid_direction(self, board, row, col, dr, dc):
        r, c = row + dr, col + dc
        if not (0 <= r < 8 and 0 <= c < 8):
            return False
        if board[r][c] != self.other_player:
            return False
        r += dr
        c += dc
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == ' ':
                return False
            if board[r][c] == self.current_player:
                return True
            r += dr
            c += dc
        return False

    # operates on the existing self.board and takes 2 args: row and col -> caused the error in the pruning func
    # therefore, i modified it so that
    # it accepts the board as an additional arg,
    # allowing it to make a move on any board -> (board_copy)

    def make_move(self, board, row, col):
        # self.board[row][col] = self.current_player
        board[row][col] = self.current_player
        self.remaining_disks -= 1

        if self.current_player == 'B':
            self.black_disks += 1
            self.white_disks -= 1
        else:
            self.white_disks += 1
            self.black_disks -= 1

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                # if self.is_valid_direction(self.board, row, col, dr, dc):
                if self.is_valid_direction(board, row, col, dr, dc):
                    self.flip_discs(board, row, col, dr, dc)
                    # self.flip_discs(row, col, dr, dc) <- MISSING ARG

    # modified it to work with any board instead of relying on self.board
    def flip_discs(self, board, row, col, dr, dc):
        r, c = row + dr, col + dc
        # while self.board[r][c] == self.other_player:
        while board[r][c] == self.other_player:
            # self.board[r][c] = self.current_player
            board[r][c] = self.current_player
            r += dr
            c += dc

    def is_game_over(self):
        return self.remaining_disks == 0 or not self.get_valid_moves()

    def get_winner(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        if black_count > white_count:
            return 'Black'
        elif white_count > black_count:
            return 'White'
        else:
            return 'Tie'

    def get_valid_moves(self):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(self.board, i, j):
                    valid_moves.append((i, j))
        return valid_moves

    def alpha_beta_pruning(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return (self.evaluate_board(board), None)  # Returning evaluation and None for move
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_valid_moves():
                board_copy = copy.deepcopy(board)
                # if move is not None:
                self.make_move(board_copy, move[0], move[1])
                eval, _ = self.alpha_beta_pruning(board_copy, depth - 1, alpha, beta, False)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)

                if beta <= alpha:
                    break
            return (max_eval, best_move)
        else:
            min_eval = float('inf')
            best_move = None

            for move in self.get_valid_moves():
                board_copy = copy.deepcopy(board)
                # if move is not None:
                self.make_move(board_copy, move[0], move[1])
                eval, _ = self.alpha_beta_pruning(board_copy, depth - 1, alpha, beta, True)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)

                if beta <= alpha:
                    break

            return (min_eval, best_move)

    def evaluate_board(self, board):
        black_count = sum(row.count('B') for row in board)
        white_count = sum(row.count('W') for row in board)
        return black_count - white_count

    def difficulty_to_depth(self):
        if self.difficulty == "Easy":
            return 1
        elif self.difficulty == "Medium":
            return 3
        elif self.difficulty == "Hard":
            return 5
        else:
            return 3 # default

    def print_winner(self):
        winner = self.get_winner()

        if winner == "Tie":
            print("The game is a tie!")
        else:
            print(f"The winner is {winner}!")
        # print(f"The winner is {winner}!")


# Create an instance of the Othello game with the initial setup
difficulty_level = choose_difficulty()
game = OthelloGame(difficulty=difficulty_level)

# Start the game
game.play()
