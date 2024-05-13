# Importing the necessary libraries
import pygame  # Pygame library for game development
import copy    # Copy module for creating copies of objects
import random  # Random module for generating random numbers

# Define RGB color constants
BLACK = (0, 0, 0)    # RGB tuple for black color
WHITE = (255, 255, 255)  # RGB tuple for white color
GREEN = (0, 128, 0)   # RGB tuple for green color

# Define window size and grid size constants
WINDOW_SIZE = (400, 400)  # Size of the game window
GRID_SIZE = 8              # Size of the game grid
SQUARE_SIZE = WINDOW_SIZE[0] // GRID_SIZE  # Size of each square in the grid

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)  # Creating the game window
pygame.display.set_caption("Othello")  # Setting the window title

# Function to draw the board
def draw_board(board):
    screen.fill(GREEN)  # Fill the screen with green color

    # Drawing the grid and pieces on the board
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Define the rectangle for the current grid square
            rect = pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Draw grid lines

            # Draw a black circle if the current square contains a black piece
            if board[i][j] == 'B':
                pygame.draw.circle(screen, BLACK,
                                   (j * SQUARE_SIZE + SQUARE_SIZE // 2, i * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 2)
            # Draw a white circle if the current square contains a white piece
            elif board[i][j] == 'W':
                pygame.draw.circle(screen, WHITE,
                                   (j * SQUARE_SIZE + SQUARE_SIZE // 2, i * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 2)

    pygame.display.flip()  # Update the display




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
# Function to make a move and flip the disks
def make_move(board, row, col, player):
    board[row][col] = player  # Place the player's piece on the board
    # Check in the left, right, up, and down directions for flipping disks
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        if is_valid_direction(board, row, col, dr, dc, player):
            r, c = row + dr, col + dc
            # Flip disks in the valid direction
            #condition checks if the current position (r, c) on the board does not contain the player's piece
            # . If it doesn't,
            # it means there is an opponent's piece at that position that needs to be flipped.
            while board[r][c] != player:
                board[r][c] = player
                r += dr
                c += dc

# Function to get the opposite player
def opposite_player(player):
    return 'B' if player == 'W' else 'W'




# Function to get the valid moves for a player
def get_valid_moves(board, player):
    valid_moves = []  # Initialize an empty list to store valid moves
    # Iterate over all squares on the board
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if is_valid_move(board, i, j, player):  # Check if the move is valid for the player
                valid_moves.append((i, j))  # Add valid moves to the list
    return valid_moves  # Return the list of valid moves

# Function to evaluate the board for the alpha-beta pruning algorithm
def evaluate_board(board):
    # Count the number of black pieces on the board
    black_count = sum(row.count('B') for row in board)
    # Count the number of white pieces on the board
    white_count = sum(row.count('W') for row in board)
    # Return the difference between the counts of black and white pieces
    return black_count - white_count


# Alpha-beta pruning algorithm
def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or not get_valid_moves(board, player):  # Check for terminal condition
        return (evaluate_board(board), None)  # Returning evaluation and None for move
    if maximizing_player:
        max_eval = float('-inf')  # Initialize maximum evaluation
        best_move = None  # Initialize the best move
        for move in get_valid_moves(board, player):  # Iterate over valid moves
            board_copy = copy.deepcopy(board)  # Create a copy of the board
            make_move(board_copy, move[0], move[1], player)  # Make the move
            # Recursively evaluate the board for the next player
            eval, _ = alpha_beta_pruning(board_copy, depth - 1, alpha, beta, False, player)
            if eval > max_eval:
                max_eval = eval  # Update maximum evaluation
                best_move = move  # Update the best move
            alpha = max(alpha, eval)  # Update alpha value
            if beta <= alpha:
                break  # Beta cutoff
        return (max_eval, best_move)  # Return maximum evaluation and best move
    else:
        min_eval = float('inf')  # Initialize minimum evaluation
        best_move = None  # Initialize the best move
        for move in get_valid_moves(board, opposite_player(player)):  # Iterate over valid moves
            board_copy = copy.deepcopy(board)  # Create a copy of the board
            make_move(board_copy, move[0], move[1], opposite_player(player))  # Make the move
            # Recursively evaluate the board for the next player
            eval, _ = alpha_beta_pruning(board_copy, depth - 1, alpha, beta, True, player)
            if eval < min_eval:
                min_eval = eval  # Update minimum evaluation
                best_move = move  # Update the best move
            beta = min(beta, eval)  # Update beta value
            if beta <= alpha:
                break  # Alpha cutoff
        return (min_eval, best_move)  # Return minimum evaluation and best move

# Function to prompt the user to choose the difficulty level
def choose_difficulty():
    while True:
        print("Choose difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in ['1', '2', '3']:
            return int(choice)  # Return the selected difficulty level
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Main game loop
def main():
    difficulty = choose_difficulty()  # Choose the difficulty level
    depth = 4  # Default depth for the alpha-beta pruning algorithm
    if difficulty == 1:
        depth = 2
    elif difficulty == 2:
        depth = 4
    elif difficulty == 3:
        depth = 6

    # Initialize the game board with initial pieces
    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    board[3][3] = 'W'  # Initial setup: Place two white disks at the center
    board[4][4] = 'W'
    board[3][4] = 'B'  # Initial setup: Place two black disks at the center
    board[4][3] = 'B'
    player = 'B'  # Black always moves first

    # Game loop
    # Game loop
    running = True  # Set the game loop flag to True
    while running:  # Start the game loop
        for event in pygame.event.get():  # Iterate through all pygame events
            if event.type == pygame.QUIT:  # Check if the user closes the window
                running = False  # Set the game loop flag to False to exit the loop
            if event.type == pygame.MOUSEBUTTONDOWN and player == 'B':  # Check if it's the human player's turn
                # Human player's turn
                mouse_pos = pygame.mouse.get_pos()  # Get the mouse position
                col = mouse_pos[0] // SQUARE_SIZE  # Calculate the column based on the mouse position
                row = mouse_pos[1] // SQUARE_SIZE  # Calculate the row based on the mouse position
                if is_valid_move(board, row, col, player):  # Check if the move is valid
                    make_move(board, row, col, player)  # Make the move
                    player = opposite_player(player)  # Switch to the opposite player's turn
            elif player == 'W':  # Check if it's the computer player's turn
                # Computer player's turn
                _, move = alpha_beta_pruning(board, depth, float('-inf'), float('inf'), True,
                                             player)  # Apply alpha-beta pruning to find the best move
                if move is not None:  # Check if a valid move is found
                    make_move(board, move[0], move[1], player)  # Make the move
                    player = opposite_player(player)  # Switch to the opposite player's turn

        draw_board(board)  # Draw the updated board

    # Start the game
    main()  # Call the main function to start the game


# Quit pygame
pygame.quit()
