import pygame

# Define constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
GRID_SIZE = 8
SQUARE_SIZE = 400 // GRID_SIZE

def draw_board(screen, board, valid_moves=None):
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

def display_results(screen, winner):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Winner: {winner}", True, WHITE)
    text_rect = text.get_rect(center=(400 // 2, 400 // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
