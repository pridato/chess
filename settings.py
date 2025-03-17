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

# BUTTON

primary_color = (48, 46, 43)       # Gris oscuro
secondary_color = (75, 73, 70)     # Gris más claro para hover
background_color = (28, 27, 24)    # Casi negro para el fondo

button_width = 280
button_height = 60
center_x = WIDTH // 2 - button_width // 2
