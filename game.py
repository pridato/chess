import pygame
from settings import *
from utils import load_images
from movements import *


class ChessGame:
    """
    Clase que representa un juego de ajedrez.

    Atributos:
    -----------
    screen : pygame.Surface
        La superficie de la pantalla donde se dibuja el juego.
    board : list
        La representación del tablero de ajedrez con las piezas en sus posiciones iniciales.
    pieces_images : dict
        Un diccionario que contiene las imágenes de las piezas de ajedrez.

    """

    def __init__(self, screen):
        self.screen = screen
        self.board = self.create_start_board()
        self.pieces_images = load_images()
        self.white_time = 600
        self.black_time = 600
        self.current_player = 'white'
        self.last_time_update = pygame.time.get_ticks()  # tiempo en milisegundos

    def update_time(self):
        """
        Actualiza el tiempo restante para el jugador actual.

        Esta función calcula el tiempo transcurrido desde la última actualización y lo resta del tiempo total del jugador actual. El tiempo restante se almacena en `self.white_time` o `self.black_time`, dependiendo del jugador actual.

        """
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time_update) / \
            1000  # Convertir a segundos

        if self.current_player == 'white':
            self.white_time -= elapsed
        else:
            self.black_time -= elapsed

        self.last_time_update = current_time

    def switch_player(self):
        """
        Cambia el jugador actual.

        Esta función cambia el jugador actual de 'white' a 'black' o viceversa. También actualiza el tiempo de la última actualización.
        """
        self.current_player = 'white' if self.current_player == 'black' else 'black'
        self.last_time_update = pygame.time.get_ticks()

    def draw_time(self):
        """
        Dibuja los temporizadores en la parte superior de la pantalla.
        """
        # Dibujar fondo para el tiempo
        time_rect = pygame.Rect(0, 0, WIDTH, TIME_HEIGHT)
        pygame.draw.rect(self.screen, background_color, time_rect)

        font = pygame.font.Font(None, 36)

        # Formato mm:ss
        white_minutes = int(self.white_time // 60)
        white_seconds = int(self.white_time % 60)
        black_minutes = int(self.black_time // 60)
        black_seconds = int(self.black_time % 60)

        # Textos de tiempo
        white_text = f"Blancas: {white_minutes:02d}:{white_seconds:02d}"
        black_text = f"Negras: {black_minutes:02d}:{black_seconds:02d}"

        # Renderizar textos
        white_surface = font.render(white_text, True, (255, 255, 255))
        black_surface = font.render(black_text, True, (255, 255, 255))

        # Posicionar en la parte superior
        self.screen.blit(white_surface, (20, TIME_HEIGHT//2 - 15))
        self.screen.blit(black_surface, (WIDTH - 170, TIME_HEIGHT//2 - 15))

    def create_start_board(self):
        """
        Crea y devuelve la configuración inicial del tablero de ajedrez.

        El tablero se representa como una lista de listas, donde cada lista
        interna representa una fila en el tablero de ajedrez. Cada pieza se
        representa con una cadena en el formato 'color_pieza', y las casillas
        vacías se representan con None.

        Returns:
            list: Una lista 2D que representa las posiciones iniciales de todas
            las piezas en un tablero de ajedrez.
        """
        return [
            ["black_rook", "black_knight", "black_bishop", "black_queen",
                "black_king", "black_bishop", "black_knight", "black_rook"],
            ["black_pawn"] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ["white_pawn"] * 8,
            ["white_rook", "white_knight", "white_bishop", "white_queen",
                "white_king", "white_bishop", "white_knight", "white_rook"]
        ]

    def draw_board(self):
        """
        Dibuja el tablero de ajedrez en la pantalla, con el margen superior ajustado.
        """
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color,
                                 (col * SQUARE_SIZE,
                                  row * SQUARE_SIZE + MARGIN_TOP,  # Usar MARGIN_TOP
                                  SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        """
        Dibuja las piezas en el tablero, ajustando la posición vertical.
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(
                        self.pieces_images[piece],
                        (col * SQUARE_SIZE,
                         row * SQUARE_SIZE + MARGIN_TOP))  # Usar MARGIN_TOP

    def get_possible_moves(self, piece, position, game_state):
        """
        Devuelve una lista de movimientos posibles para una pieza dada.

        Parámetros:
        - piece: La pieza para la que se calculan los movimientos.
        - position: La posición actual de la pieza en el formato (fila, columna).

        Returns:
            list: Una lista de posiciones (fila, columna) que son movimientos válidos.
        """
        possible_moves = []
        row, col = position

        if "pawn" in piece:
            return get_pawn_moves(
                piece, possible_moves, row, col, self.board, game_state)

        elif "knight" in piece:
            return get_knight_moves(piece, possible_moves, row, col, self.board, game_state)

        elif "rook" in piece:
            return get_rook_moves(piece, possible_moves, row, col, self.board, game_state)

        elif "bishop" in piece:
            return get_bishop_moves(piece, possible_moves, row, col, self.board, game_state)

        elif "queen" in piece:
            return get_queen_moves(piece, possible_moves, row, col, self.board, game_state)

        elif "king" in piece:
            return get_king_moves(piece, possible_moves, row, col, self.board, game_state)

    def move_piece(self, start_pos, end_pos):
        """
        Mueve una pieza de una posición a otra en el tablero.

        Parámetros:
        - start_pos: La posición inicial de la pieza en el formato (fila, columna).
        - end_pos: La posición final a la que se moverá la pieza en el formato (fila, columna).
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Mover la pieza
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
