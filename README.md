# Othello AI

This project implements the classic Othello (Reversi) game using Python and Pygame. <br>The game includes a graphical interface, basic gameplay mechanics, and an AI opponent using the alpha-beta pruning algorithm.

## Project Structure

- **main.py**: The entry point of the application. Initializes Pygame and starts the main game loop.
- **board.py**: Contains functions related to drawing the board and displaying results.
- **game.py**: Includes the main game loop and related functions.
- **ai.py**: Implements the AI opponent using the alpha-beta pruning algorithm.
- **utils.py**: Contains utility functions for checking valid moves, making moves, and evaluating the board.

## How to Run

1. Ensure you have Python and Pygame installed.
2. Clone the repository or download the files.
3. Run `main.py` to start the game.
4. Choose the difficulty level when prompted.
5. The human player (Black) moves first by clicking on the board, while the AI opponent (White) makes moves automatically.

## Game Rules

1. Black always moves first.
2. Players take turns placing their disks on the board.
3. A move is valid if it captures at least one of the opponent's disks.<br> Capturing is done by bracketing opponent disks in one or more straight lines (horizontal, vertical, or diagonal).
4. The game ends when neither player can make a valid move.
5. The player with the most disks on the board at the end of the game wins.


