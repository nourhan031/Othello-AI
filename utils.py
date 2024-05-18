GRID_SIZE = 8

def opposite_player(player):
    return 'B' if player == 'W' else 'W'

def get_valid_moves(board, player):
    valid_moves = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if is_valid_move(board, i, j, player):
                valid_moves.append((i, j))
    return valid_moves

def is_valid_move(board, row, col, player):
    if board[row][col] != ' ':
        return False
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if is_valid_direction(board, row, col, dr, dc, player):
            return True
    return False

def is_valid_direction(board, row, col, dr, dc, player):
    r, c = row + dr, col + dc
    if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
        return False
    if board[r][c] != opposite_player(player):
        return False
    r += dr
    c += dc
    while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
        if board[r][c] == ' ':
            return False
        if board[r][c] == player:
            return True
        r += dr
        c += dc
    return False

def make_move(board, row, col, player):
    board[row][col] = player
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        if is_valid_direction(board, row, col, dr, dc, player):
            r, c = row + dr, col + dc
            while board[r][c] != player:
                board[r][c] = player
                r += dr
                c += dc

def evaluate_board(board):
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    return black_count - white_count
