import pygame
from game import ChessGame
from settings import *
from button import Button


def main():
    screen, game, clock = getConf()

    game_state = 'menu'

    # Crear botones en el estado menu
    pvp_button = Button(center_x, HEIGHT//2 - button_height - 20,
                        button_width, button_height,
                        "JUGADOR vs JUGADOR",
                        primary_color, secondary_color)

    pvc_button = Button(center_x, HEIGHT//2 + 20,
                        button_width, button_height,
                        "JUGADOR vs CPU",
                        primary_color, secondary_color)

    highlighted_moves = []
    selected_piece = None

    while True:
        if game_state == 'menu':  # Dibujar menú
            screen.fill(background_color)

            # Dibujar botones
            pvp_button.draw(screen)
            pvc_button.draw(screen)

            # Manejar eventos del menú
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if pvp_button.handle_event(event):
                    game_state = 'pvp'
                if pvc_button.handle_event(event):
                    game_state = 'pvc'

        else:  # Estado de juego
            game.draw_board()
            game.draw_pieces()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = 'menu'
                        highlighted_moves = []
                        selected_piece = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // SQUARE_SIZE
                    row = mouse_y // SQUARE_SIZE

                    piece = game.board[row][col]
                    if selected_piece:
                        if highlighted_moves and (row, col) in highlighted_moves:
                            game.move_piece(selected_piece, (row, col))
                        selected_piece = None
                        highlighted_moves = []
                    elif piece:
                        selected_piece = (row, col)
                        highlighted_moves = game.get_possible_moves(
                            piece, selected_piece, game_state)

            draw_highlighted_moves(screen, highlighted_moves)

        pygame.display.flip()
        clock.tick(60)


def getConf():
    """
    Inicializa pygame y configura el entorno del juego de ajedrez.

    Esta función inicializa pygame, configura la pantalla con un tamaño específico, establece el título de la ventana, crea una instancia del juego de ajedrez y un reloj para controlar el tiempo del juego.

    Returns:
        tuple: Una tupla que contiene la pantalla de pygame, el juego de ajedrez y el reloj.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ajedrez")
    game = ChessGame(screen)
    clock = pygame.time.Clock()
    return screen, game, clock


def draw_highlighted_moves(screen, highlighted_moves):
    """
    Dibuja los movimientos destacados en la pantalla.

    Esta función itera sobre una lista de movimientos destacados y dibuja un círculo blanco en la pantalla para cada uno de ellos. Los círculos se dibujan en el centro de la casilla correspondiente al movimiento.

    Parámetros:
    - screen (pygame.Surface): La superficie de pygame donde se dibujan los movimientos.
    - highlighted_moves (list): Una lista de tuplas que representan los movimientos destacados. Cada tupla contiene la fila y la columna del movimiento.
    """
    if highlighted_moves:
        for move in highlighted_moves:
            # Calcula la posición x del centro de la casilla
            center_x = move[1] * SQUARE_SIZE + SQUARE_SIZE // 2
            # Calcula la posición y del centro de la casilla
            center_y = move[0] * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(screen, (255, 255, 255),  # Dibuja un círculo blanco
                               (center_x, center_y), 5)  # En el centro de la casilla, con un radio de 5 píxeles


if __name__ == "__main__":
    main()
