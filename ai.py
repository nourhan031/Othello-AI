from copy import deepcopy
from utils import evaluate_board, get_valid_moves, make_move, opposite_player

def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or not get_valid_moves(board, player):
        return evaluate_board(board), None
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_valid_moves(board, player):
            board_copy = deepcopy(board)
            make_move(board_copy, move[0], move[1], player)
            eval, _ = alpha_beta_pruning(board_copy, depth - 1, alpha, beta, False, player)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_valid_moves(board, opposite_player(player)):
            board_copy = deepcopy(board)
            make_move(board_copy, move[0], move[1], opposite_player(player))
            eval, _ = alpha_beta_pruning(board_copy, depth - 1, alpha, beta, True, player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
