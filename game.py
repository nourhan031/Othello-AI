import pygame
from copy import deepcopy
from board import draw_board, display_results
from ai import alpha_beta_pruning
from utils import opposite_player, get_valid_moves, make_move

GRID_SIZE = 8

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

def main_game_loop(screen):
    difficulty = choose_difficulty()
    depth = {1: 2, 2: 4, 3: 6}[difficulty]

    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    board[3][3] = 'W'
    board[4][4] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    player = 'B'

    consecutive_passes = 0
    running = True

    while running:
        valid_moves = get_valid_moves(board, player)
        draw_board(screen, board, valid_moves)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and player == 'B':
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // (400 // GRID_SIZE)
                row = mouse_pos[1] // (400 // GRID_SIZE)
                if (row, col) in valid_moves:
                    make_move(board, row, col, player)
                    player = opposite_player(player)
                    consecutive_passes = 0
            elif player == 'W':
                _, move = alpha_beta_pruning(board, depth, float('-inf'), float('inf'), True, player)
                if move is not None:
                    make_move(board, move[0], move[1], player)
                    player = opposite_player(player)
                    consecutive_passes = 0

        if not valid_moves:
            player = opposite_player(player)
            consecutive_passes += 1
            if consecutive_passes >= 2:
                running = False

    draw_board(screen, board)
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    winner = "Black" if black_count > white_count else "White" if white_count > black_count else "It's a tie!"
    display_results(screen, winner)
    pygame.time.wait(3000)
