import pygame
from game import main_game_loop

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Othello")
    main_game_loop(screen)
    pygame.quit()

if __name__ == "__main__":
    main()
