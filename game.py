import pygame
from settings import ROWS, COLS, SQUARE_SIZE, WHITE, BLACK, highlighted_moves
from utils import load_images


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
        Dibuja el tablero de ajedrez en la pantalla.

        Recorre cada fila y columna del tablero, alternando los colores de las casillas
        entre blanco y negro. Utiliza la librería pygame para dibujar los rectángulos
        que representan las casillas del tablero.

        """

        # recorremos filas y columnas e intercalamos casillas blancas y negras
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE,
                                 row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        """
        Dibuja las piezas en el tablero de ajedrez.

        Recorre cada celda del tablero y, si hay una pieza en esa celda,
        dibuja la imagen correspondiente en la pantalla.

        Parámetros:
        - self: referencia a la instancia actual del objeto.

        Variables:
        - ROWS: número de filas en el tablero.
        - COLS: número de columnas en el tablero.
        - SQUARE_SIZE: tamaño de cada celda del tablero.
        - self.board: matriz que representa el tablero de ajedrez.
        - self.screen: superficie donde se dibujan las piezas.
        - self.pieces_images: diccionario que mapea cada pieza a su imagen correspondiente.
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(
                        self.pieces_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def get_possible_moves(self, piece, position):
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

        # Ejemplo para un peón (puedes agregar lógica para otras piezas)
        if piece.startswith("white_pawn"):
            # Movimiento hacia adelante
            if row > 0 and self.board[row - 1][col] is None:
                possible_moves.append((row - 1, col))
            if row == 6 and self.board[row - 2][col] is None:  # Movimiento doble
                possible_moves.append((row - 2, col))
        elif piece.startswith("black_pawn"):
            # Movimiento hacia adelante
            if row < 7 and self.board[row + 1][col] is None:
                possible_moves.append((row + 1, col))
            if row == 1 and self.board[row + 2][col] is None:  # Movimiento doble
                possible_moves.append((row + 2, col))

        return possible_moves
