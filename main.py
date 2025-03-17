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

        else:
            game.draw_board()
            game.draw_pieces()

            game.update_time()
            game.draw_time()

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
                    # Ajustar la posición Y restando el margen superior
                    adjusted_y = mouse_y - MARGIN_TOP

                    # Verificar que el clic esté dentro del tablero
                    if 0 <= mouse_x <= BOARD_SIZE and MARGIN_TOP <= mouse_y <= HEIGHT:
                        col = mouse_x // SQUARE_SIZE
                        row = adjusted_y // SQUARE_SIZE

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

            if game.white_time <= 0:
                print("¡Negras ganan por tiempo!")
                game_state = 'menu'
            elif game.black_time <= 0:
                print("¡Blancas ganan por tiempo!")
                game_state = 'menu'

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
    """
    if highlighted_moves:
        for move in highlighted_moves:
            center_x = move[1] * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = move[0] * SQUARE_SIZE + SQUARE_SIZE // 2 + MARGIN_TOP
            pygame.draw.circle(screen, (255, 255, 255),
                               (center_x, center_y), 5)


if __name__ == "__main__":
    main()
