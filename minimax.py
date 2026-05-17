"""
Minimax Algorithm Module
The AI decision-making engine for the Tic-Tac-Toe game.

The algorithm works by simulating all possible future moves up to a given depth,
and choosing the move that maximizes the AI's chance of winning.
"""

import math
import random
from game import check_winner, is_draw, get_available_moves, EMPTY


def evaluate(board, ai_mark, human_mark, depth):
    """
    Score the current board state.
      +10 (minus depth) if the AI wins  → prefers faster wins.
      -10 (plus depth)  if the human wins → prefers slower losses.
       0                if draw or no result yet.
    """
    if check_winner(board, ai_mark):
        return 10 - depth
    if check_winner(board, human_mark):
        return -10 + depth
    return 0


def minimax(board, ai_mark, human_mark, depth, max_depth, is_maximizing):
    """
    Recursively evaluate the board using the Minimax algorithm.

    Parameters:
        board        : current board state (list of 9 cells)
        ai_mark      : the AI's symbol ('X' or 'O')
        human_mark   : the human's symbol ('X' or 'O')
        depth        : how deep we've searched so far
        max_depth    : the maximum depth allowed (controls difficulty)
        is_maximizing: True when it's the AI's turn (maximize), False for human (minimize)

    Returns:
        The best score reachable from this board state.
    """
    score = evaluate(board, ai_mark, human_mark, depth)

    # Base cases: someone won, board is full, or depth limit reached
    if score != 0:
        return score
    if is_draw(board):
        return 0
    if depth >= max_depth:
        return 0

    available = get_available_moves(board)

    if is_maximizing:
        best = -math.inf
        for move in available:
            board[move] = ai_mark
            best = max(best, minimax(board, ai_mark, human_mark, depth + 1, max_depth, False))
            board[move] = EMPTY
        return best
    else:
        best = math.inf
        for move in available:
            board[move] = human_mark
            best = min(best, minimax(board, ai_mark, human_mark, depth + 1, max_depth, True))
            board[move] = EMPTY
        return best


def find_best_move(board, ai_mark, human_mark, max_depth):
    """
    Determine the best move for the AI.

    Evaluates every available cell using minimax and returns
    the index of the optimal move. If multiple moves share the
    same score, one is chosen at random for variety.

    Parameters:
        board      : current board state
        ai_mark    : the AI's symbol
        human_mark : the human's symbol
        max_depth  : search depth (1 = easy, 3 = medium, 9 = hard)

    Returns:
        The index (0-8) of the best cell to play.
    """
    available = get_available_moves(board)
    if not available:
        return None

    best_score = -math.inf
    best_moves = []

    for move in available:
        board[move] = ai_mark
        score = minimax(board, ai_mark, human_mark, 1, max_depth, False)
        board[move] = EMPTY

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)
