WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 255)


# MOVES
knight_moves = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]

bishop_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

king_moves = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]

rook_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
