import copy
import tkinter as tk

DEFAULT_DIFFICULTY = "Medium"

class OthelloGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello")

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.current_player = 'B'  # Initialize current player attribute
        self.game = OthelloGame(difficulty=DEFAULT_DIFFICULTY)

        self.draw_board()
        self.draw_info_panel()
        self.draw_difficulty_button()
        self.draw_scoreboard()

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                x0, y0 = i * 50, j * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")
                # Add logic to draw disks based on the game state
                if self.game.board[i][j] == 'B':
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="black")
                elif self.game.board[i][j] == 'W':
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="white")

    def draw_info_panel(self):
        self.info_panel = tk.Frame(self.root)
        self.info_panel.pack()

        self.status_label = tk.Label(self.info_panel, text=f"Current player: {self.current_player}")
        self.status_label.pack()

        self.result_label = tk.Label(self.info_panel, text="")
        self.result_label.pack()

    def draw_difficulty_button(self):
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack()

        self.difficulty_label = tk.Label(self.difficulty_frame, text="Select Difficulty:")
        self.difficulty_label.pack(side=tk.LEFT)

        self.easy_button = tk.Button(self.difficulty_frame, text="Easy", command=lambda: self.start_game("Easy"))
        self.easy_button.pack(side=tk.LEFT)

        self.medium_button = tk.Button(self.difficulty_frame, text="Medium", command=lambda: self.start_game("Medium"))
        self.medium_button.pack(side=tk.LEFT)

        self.hard_button = tk.Button(self.difficulty_frame, text="Hard", command=lambda: self.start_game("Hard"))
        self.hard_button.pack(side=tk.LEFT)

    def draw_scoreboard(self):
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack()

        self.black_score_label = tk.Label(self.score_frame, text="Black: 2")
        self.black_score_label.pack(side=tk.LEFT)

        self.white_score_label = tk.Label(self.score_frame, text="White: 2")
        self.white_score_label.pack(side=tk.LEFT)

    def start_game(self, difficulty):
        self.game = OthelloGame(difficulty=difficulty)
        self.current_player = 'B'  # Reset current player
        self.status_label.config(text=f"Current player: {self.current_player}")
        self.result_label.config(text="")
        self.update_board()
        self.update_scoreboard()
        if self.game.current_player == 'W':
            self.computer_move()

    def bind_board_clicks(self):
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        col = event.x // 50
        row = event.y // 50
        if self.game.is_valid_move(row, col):
            self.game.make_move(row, col)
            self.update_board()
            self.update_info()
            self.update_scoreboard()
            if not self.game.is_game_over() and self.game.current_player == 'W':
                self.computer_move()

    def update_board(self):
        self.canvas.delete("all")
        self.draw_board()

    def update_info(self):
        self.status_label.config(text=f"Current player: {self.game.current_player}")
        self.result_label.config(text="")
        if self.game.is_game_over():
            winner = self.game.get_winner()
            if winner == "Tie":
                self.result_label.config(text="The game is a tie!")
            else:
                self.result_label.config(text=f"The winner is {winner}!")

    def update_scoreboard(self):
        black_count = sum(row.count('B') for row in self.game.board)
        white_count = sum(row.count('W') for row in self.game.board)
        self.black_score_label.config(text=f"Black: {black_count}")
        self.white_score_label.config(text=f"White: {white_count}")

    def computer_move(self):
        if self.game.difficulty == "Easy":
            depth = 1
        else:
            depth = self.game.difficulty_to_depth()

        eval, move = self.game.alpha_beta_pruning(self.game.board, depth, float('-inf'), float('inf'), True)
        if move is not None:
            self.game.make_move(move[0], move[1])
            self.update_board()
            self.update_info()
            self.update_scoreboard()

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

def main():
    root = tk.Tk()
    gui = OthelloGUI(root)
    gui.bind_board_clicks()
    root.mainloop()

if __name__ == "__main__":
    main()
