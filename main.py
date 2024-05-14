import pygame
import copy

# Define constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
WINDOW_SIZE = (400, 400)
GRID_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE[0] // GRID_SIZE

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Othello")

# Function to draw the board
def draw_board(board, valid_moves=None):
    screen.fill(GREEN)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if board[i][j] == 'B':
                pygame.draw.circle(screen, BLACK, (j * SQUARE_SIZE + SQUARE_SIZE // 2, i * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 2)
            elif board[i][j] == 'W':
                pygame.draw.circle(screen, WHITE, (j * SQUARE_SIZE + SQUARE_SIZE // 2, i * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 2)
            elif valid_moves and (i, j) in valid_moves:
                pygame.draw.circle(screen, BLACK, (j * SQUARE_SIZE + SQUARE_SIZE // 2, i * SQUARE_SIZE + SQUARE_SIZE // 2), 5)
    pygame.display.flip()

# Function to check if a move is valid
def is_valid_move(board, row, col, player):
    if board[row][col] != ' ':  # Check if the square is empty
        return False
    # Check in all directions for a valid move: left, down, up, right
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if is_valid_direction(board, row, col, dr, dc, player):
            return True
    return False

# Function to check if a direction is valid
def is_valid_direction(board, row, col, dr, dc, player):
    r, c = row + dr, col + dc
    if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
        return False
    if board[r][c] != opposite_player(player):
        return False
    r += dr
    c += dc
    while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
        if board[r][c] == ' ':  # Check if the chain is broken
            return False
        if board[r][c] == player:  # Check if the chain ends with the player's piece
            return True
        r += dr
        c += dc
    return False

# Function to make a move and flip the disks
def make_move(board, row, col, player):
    board[row][col] = player  # Place the player's piece on the board
    # Check in the left, right, up, and down directions for flipping disks
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        if is_valid_direction(board, row, col, dr, dc, player):
            r, c = row + dr, col + dc
            # Flip disks in the valid direction
            while board[r][c] != player:
                board[r][c] = player
                r += dr
                c += dc

# Function to get the opposite player
def opposite_player(player):
    return 'B' if player == 'W' else 'W'

# Function to get the valid moves for a player
def get_valid_moves(board, player):
    valid_moves = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if is_valid_move(board, i, j, player):
                valid_moves.append((i, j))
    return valid_moves

# Function to evaluate the board for the alpha-beta pruning algorithm
def evaluate_board(board):
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    return black_count - white_count

# Alpha-beta pruning algorithm
def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or not get_valid_moves(board, player):
        return (evaluate_board(board), None)  # Returning evaluation and None for move
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_valid_moves(board, player):
            board_copy = copy.deepcopy(board)
            make_move(board_copy, move[0], move[1], player)
            eval, _ = alpha_beta_pruning(board_copy, depth - 1, alpha, beta, False, player)
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
        for move in get_valid_moves(board, opposite_player(player)):
            board_copy = copy.deepcopy(board)
            make_move(board_copy, move[0], move[1], opposite_player(player))
            eval, _ = alpha_beta_pruning(board_copy, depth - 1, alpha, beta, True, player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return (min_eval, best_move)

# Function to prompt the user to choose the difficulty level
def choose_difficulty():
    while True:
        print("Choose difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Function to display game results and scoreboard
def display_results(screen, winner):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Winner: {winner}", True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

# Main game loop
def main():
    difficulty = choose_difficulty()
    depth = 4  # Default depth for the alpha-beta pruning algorithm
    if difficulty == 1:
        depth = 2
    elif difficulty == 2:
        depth = 4
    elif difficulty == 3:
        depth = 6

    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    board[3][3] = 'W'  # Initial setup: Place two white disks at the center
    board[4][4] = 'W'
    board[3][4] = 'B'  # Initial setup: Place two black disks at the center
    board[4][3] = 'B'
    player = 'B'  # Black always moves first

    consecutive_passes = 0  # Variable to track consecutive passes
    # Game loop
    running = True
    while running:
        valid_moves = get_valid_moves(board, player)
        draw_board(board, valid_moves)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and player == 'B':
                # Human player's turn
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // SQUARE_SIZE
                row = mouse_pos[1] // SQUARE_SIZE
                if (row, col) in valid_moves:
                    make_move(board, row, col, player)
                    player = opposite_player(player)
                    consecutive_passes = 0  # Reset consecutive passes if a move is made
            elif player == 'W':
                # Computer player's turn
                _, move = alpha_beta_pruning(board, depth, float('-inf'), float('inf'), True, player)
                if move is not None:
                    make_move(board, move[0], move[1], player)
                    player = opposite_player(player)
                    consecutive_passes = 0  # Reset consecutive passes if a move is made

        if not valid_moves:
            # If no valid moves for the current player
            player = opposite_player(player)
            consecutive_passes += 1
            if consecutive_passes >= 2:
                # If two consecutive passes occur, end the game
                running = False

    # Display final board state
    draw_board(board)

    # Count and display the winner
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    if black_count > white_count:
        display_results(screen, "Black")
    elif white_count > black_count:
        display_results(screen, "White")
    else:
        display_results(screen, "It's a tie!")

    # Wait for a few seconds before quitting
    pygame.time.wait(3000)

    # Quit pygame
    pygame.quit()

# Start the game
main()
