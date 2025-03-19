import pygame
from settings import BOARD_SIZE, HEIGHT, MOVEMENT_BOX, ROWS, COLS, SQUARE_SIZE, WHITE, BLACK, DIFFICULTY, MARGIN_TOP, WIDTH, TIME_HEIGHT, background_color
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
        La representación del tablero de ajedrez con las piezas.
    pieces_images : dict
        Diccionario que contiene las imágenes de las piezas.
    game_mode : str
        Modo de juego ('pvp' o 'pvc').
    difficulty : dict
        Configuración de dificultad para modo PvC.
    current_turn : str
        Color del jugador actual ('white' o 'black').
    white_time : int
        Tiempo restante para el jugador blanco en segundos.
    black_time : int
        Tiempo restante para el jugador negro en segundos.
    selected_piece : tuple
        Posición de la pieza seleccionada.
    highlighted_moves : list
        Lista de movimientos posibles para la pieza seleccionada.
    waiting_for_player : bool
        Controlar el flujo de turnos.
    game_over : bool
        Estado del juego.
    waiting_for_cpu : bool
        Controlar el movimiento de la CPU.
    last_move_time : int
        Tiempo del último movimiento de la CPU.
    """

    def __init__(self, screen, game_mode='pvp', difficulty_level=None):
        """
        Inicializa un nuevo juego de ajedrez.

        Parámetros:
        -----------
        screen : pygame.Surface
            Superficie donde se dibujará el juego.
        game_mode : str
            Modo de juego ('pvp' o 'pvc').
        difficulty_level : str
            Nivel de dificultad para modo PvC (None para pvp).
        """
        self.screen = screen
        self.board = self.create_start_board()
        self.pieces_images = load_images()

        # Configuración del juego
        self.game_mode = game_mode
        self.difficulty = None
        self.ai_engine = None

        if game_mode == 'pvc' and difficulty_level:
            self.difficulty = DIFFICULTY[difficulty_level]
            from ai_engine import ChessAI
            self.ai_engine = ChessAI(self.difficulty)

        # Turno por jugadores y tiempo máximo por jugador
        self.current_turn = 'white'
        self.white_time = 600  # 10 minutos
        self.black_time = 600
        self.last_time_update = pygame.time.get_ticks()

        self.selected_piece = None
        self.highlighted_moves = []
        self.waiting_for_player = True
        self.game_over = False
        self.waiting_for_cpu = False
        self.last_move_time = pygame.time.get_ticks()

        self.cpu_start_pos = None
        self.cpu_end_pos = None
        self.cpu_move_time = 0

    def make_cpu_move(self):
        """
        Realiza el movimiento de la CPU y pinta el resaltado
        """
        if not self.ai_engine or self.current_turn != 'black':
            return

        # Obtener el mejor movimiento
        best_move = self.ai_engine.get_best_move([])

        if best_move:
            # Convertir notación UCI a coordenadas del tablero
            start_file = ord(best_move[0]) - ord('a')
            start_rank = 8 - int(best_move[1])
            end_file = ord(best_move[2]) - ord('a')
            end_rank = 8 - int(best_move[3])

            # Pintar cuadrado en posición inicial
            pygame.draw.rect(self.screen, (255, 150, 150),
                             (start_file * SQUARE_SIZE,
                             start_rank * SQUARE_SIZE + MARGIN_TOP,
                             SQUARE_SIZE, SQUARE_SIZE))

            # Pintar cuadrado en posición final
            pygame.draw.rect(self.screen, (255, 150, 150),
                             (end_file * SQUARE_SIZE,
                             end_rank * SQUARE_SIZE + MARGIN_TOP,
                             SQUARE_SIZE, SQUARE_SIZE))

            # Redibujar la pieza en la posición final
            piece = self.board[start_rank][start_file]
            if piece:
                self.screen.blit(
                    self.pieces_images[piece],
                    (end_file * SQUARE_SIZE,
                     end_rank * SQUARE_SIZE + MARGIN_TOP))

            # Actualizar el display para mostrar los cambios
            pygame.display.update()

            # Pequeña pausa para que se vea el efecto
            pygame.time.wait(1000)

            # Realizar el movimiento
            self.move_piece((start_rank, start_file), (end_rank, end_file))

    def create_start_board(self):
        """
        Crea y devuelve la configuración inicial del tablero.
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

    def handle_click(self, mouse_pos):
        """
        Maneja los clicks del usuario
        """

        # si es el turno de la computadora en modo PvC, no hacer nada
        if self.current_turn == 'black' and self.game_mode == 'pvc':
            return False

        # guardamos posiciones del tablero para guardar
        mouse_x, mouse_y = mouse_pos
        adjusted_y = mouse_y - MARGIN_TOP

        # Verificar que el clic esté dentro del tablero
        if 0 <= mouse_x <= BOARD_SIZE and MARGIN_TOP <= mouse_y <= HEIGHT:
            col = mouse_x // SQUARE_SIZE
            row = adjusted_y // SQUARE_SIZE

            # identificamos la pieza seleccionada
            piece = self.board[row][col]

            if self.selected_piece:
                if self.highlighted_moves and (row, col) in self.highlighted_moves:
                    # Realizar el movimiento
                    self.move_piece(self.selected_piece, (row, col))
                    # reiniciar la pieza seleccionada y sus movimientos posibles
                    self.selected_piece = None
                    self.highlighted_moves = []

                    # Después de mover la pieza, cambiar de turno (si es pvc se mueve solo)
                    if self.game_mode == 'pvc':
                        self.waiting_for_cpu = True
                        self.last_move_time = pygame.time.get_ticks()
                    return True

                self.selected_piece = None
                self.highlighted_moves = []

            # Si se selecciona una nueva pieza
            elif piece and piece.startswith(self.current_turn):
                self.selected_piece = (row, col)
                self.highlighted_moves = self.get_possible_moves(
                    piece, (row, col))

        return False

    def move_piece(self, start_pos, end_pos):
        """
        Mueve una pieza y actualiza el estado del juego.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Mover la pieza
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None

        # Si estamos en modo PvC, actualizar el estado del motor de IA
        if self.game_mode == 'pvc' and self.ai_engine:
            move_uci = self.ai_engine.convert_to_uci(start_pos, end_pos)
            self.ai_engine.make_move(move_uci)

        # Cambiar turno
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        self.last_time_update = pygame.time.get_ticks()

    def switch_turn(self):
        """
        Cambia el turno y actualiza el tiempo.
        """
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        self.last_time_update = pygame.time.get_ticks()

        # Si es modo PvC y es turno de la CPU
        if self.game_mode == 'pvc':
            self.waiting_for_player = (self.current_turn == 'white')
        else:
            self.waiting_for_player = True

    def get_possible_moves(self, piece, position):
        """
        Obtiene los movimientos posibles para una pieza.
        """
        # Verificar si es el turno correcto
        piece_color = 'white' if piece.startswith('white') else 'black'
        if piece_color != self.current_turn:
            return []
        if self.game_mode == 'pvc' and piece_color == 'black':
            return []

        possible_moves = []
        row, col = position

        game_state = 'pvc' if self.difficulty is not None else 'pvp'

        if "pawn" in piece:
            return get_pawn_moves(piece, possible_moves, row, col, self.board, game_state)
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

    def update_time(self):
        """
        Actualiza el tiempo del jugador actual.
        """
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time_update) / 1000

        if self.current_turn == 'white':
            self.white_time -= elapsed
        else:
            self.black_time -= elapsed

        self.last_time_update = current_time

    def draw_board(self):
        """
        Dibuja el tablero de ajedrez.
        """
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BLACK

                pygame.draw.rect(self.screen, color,
                                 (col * SQUARE_SIZE,
                                  row * SQUARE_SIZE + MARGIN_TOP,
                                  SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        """
        Dibuja las piezas en el tablero.
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(
                        self.pieces_images[piece],
                        (col * SQUARE_SIZE,
                         row * SQUARE_SIZE + MARGIN_TOP))

    def draw_time(self):
        """
        Dibuja los temporizadores y el estado del juego.
        """
        time_rect = pygame.Rect(0, 0, WIDTH, TIME_HEIGHT)
        pygame.draw.rect(self.screen, background_color, time_rect)

        font = pygame.font.Font(None, 36)

        # Formato mm:ss
        white_minutes = int(self.white_time // 60)
        white_seconds = int(self.white_time % 60)
        black_minutes = int(self.black_time // 60)
        black_seconds = int(self.black_time % 60)

        # Textos
        white_text = f"Blancas: {white_minutes:02d}:{white_seconds:02d}"
        black_text = f"Negras: {black_minutes:02d}:{black_seconds:02d}"
        mode_text = f"Modo: {'JvJ' if self.game_mode == 'pvp' else ''}"
        if self.difficulty:
            mode_text += f" {self.difficulty['name']}"

        # Renderizar y posicionar textos
        white_surface = font.render(white_text, True, (255, 255, 255))
        black_surface = font.render(black_text, True, (255, 255, 255))
        mode_surface = font.render(mode_text, True, (255, 255, 255))

        self.screen.blit(white_surface, (20, TIME_HEIGHT//2 - 15))
        self.screen.blit(black_surface, (WIDTH - 170, TIME_HEIGHT//2 - 15))
        self.screen.blit(mode_surface, (WIDTH//2 - 100, 10))

    def reset_game(self):
        """
        Reinicia el estado del juego.
        """
        self.board = self.create_start_board()
        self.current_turn = 'white'
        self.white_time = 600
        self.black_time = 600
        self.last_time_update = pygame.time.get_ticks()

        if self.ai_engine:
            self.ai_engine.reset_position()

    def update(self):
        """
        Actualiza el estado del juego
        """
        current_time = pygame.time.get_ticks()

        # Actualizar tiempos
        self.update_time()

        # Limpiar el resaltado después de 3 segundos
        if self.cpu_move_time and current_time - self.cpu_move_time > 3000:
            self.cpu_start_pos = None
            self.cpu_end_pos = None
            self.cpu_move_time = 0

        # Verificar si el juego terminó por tiempo
        if self.white_time <= 0:
            print("¡Negras ganan por tiempo!")
            return
        elif self.black_time <= 0:
            print("¡Blancas ganan por tiempo!")
            return

        # Si estamos esperando el movimiento de la CPU y ha pasado suficiente tiempo
        if self.waiting_for_cpu and current_time - self.last_move_time > 500:  # 500ms de delay
            self.make_cpu_move()
            self.waiting_for_cpu = False
