# Dimensiones
BOARD_SIZE = 800
TIME_HEIGHT = 40  # Espacio para el tiempo
MARGIN_TOP = TIME_HEIGHT + 20  # Margen adicional entre el tiempo y el tablero
WIDTH = BOARD_SIZE
HEIGHT = BOARD_SIZE + MARGIN_TOP

# Tablero
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS

# Colores del tablero
WHITE = (240, 217, 181)  # Color claro del tablero
BLACK = (181, 136, 99)   # Color oscuro del tablero

# Colores de la interfaz
primary_color = (48, 46, 43)       # Gris oscuro para botones
secondary_color = (75, 73, 70)     # Gris más claro para hover
background_color = (28, 27, 24)    # Casi negro para el fondo

# Configuración de botones
button_width = 280
button_height = 60
center_x = WIDTH // 2 - button_width // 2

# MOVES (Movimientos posibles para las piezas)
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

# Tiempo inicial para cada jugador (en segundos)
INITIAL_TIME = 600  # 10 minutos
