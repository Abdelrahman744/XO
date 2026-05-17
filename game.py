"""
Game Logic Module
Handles the board state, win/draw checks, and available moves.
"""

EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

# All possible winning combinations (rows, columns, diagonals)
WIN_PATTERNS = [
    (0, 1, 2),  # top row
    (3, 4, 5),  # middle row
    (6, 7, 8),  # bottom row
    (0, 3, 6),  # left column
    (1, 4, 7),  # center column
    (2, 5, 8),  # right column
    (0, 4, 8),  # main diagonal
    (2, 4, 6),  # anti diagonal
]


def create_board():
    """Create and return an empty 3x3 board (flat list of 9 cells)."""
    return [EMPTY] * 9


def get_available_moves(board):
    """Return a list of indices for all empty cells on the board."""
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def make_move(board, position, player):
    """Place a player's mark at the given position. Returns True if successful."""
    if board[position] == EMPTY:
        board[position] = player
        return True
    return False


def check_winner(board, player):
    """
    Check if the given player has won.
    Returns the winning pattern (tuple of 3 indices) if won, otherwise None.
    """
    for pattern in WIN_PATTERNS:
        if all(board[i] == player for i in pattern):
            return pattern
    return None


def is_draw(board):
    """Check if the board is full with no winner (a draw)."""
    return EMPTY not in board


def is_game_over(board):
    """Check if the game has ended (win or draw)."""
    return (check_winner(board, PLAYER_X) is not None or
            check_winner(board, PLAYER_O) is not None or
            is_draw(board))
