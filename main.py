import pygame
from game import ChessGame
from settings import *
from button import Button
import sys


def main():
    # Inizializamos todas las configuraciones y creamos menú
    screen, game, clock = getConf()
    game_state = 'menu'

    while True:
        if game_state == 'menu':
            # manejamos el menú y creamos un estado
            new_state = handle_menu(screen)
            if new_state:
                # creamos un estado de juego (al pasar el menú)
                game_state = new_state
        elif game_state == 'difficulty_select':

            difficulty_buttons = create_difficulty_buttons()
            new_state, new_game = handle_difficulty_select(
                screen, difficulty_buttons)
            if new_state:
                game_state = new_state
                if new_game:
                    game = new_game
        else:  # Estados de juego (pvp o pvc)
            # manejamos el juego hasta su reinicio
            new_state = handle_game(screen, game)
            if new_state:
                game_state = new_state
                game = ChessGame(screen)  # Reiniciar juego al volver al menú

        pygame.display.flip()
        clock.tick(60)


def handle_game(screen, game):
    """
    Maneja la lógica del juego activo
    """
    # Actualizar estado del juego
    game.update()

    # Dibujar el estado actual
    game.draw_board()
    game.draw_pieces()
    game.draw_time()

    # si hay movimientos resaltados, dibujarlos
    if hasattr(game, 'highlighted_moves') and game.highlighted_moves:
        draw_highlighted_moves(screen, game.highlighted_moves)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Salir del juego
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Volver al menú (con la tecla ESC)
            if event.key == pygame.K_ESCAPE:
                return 'menu'
        # Manejar clicks en el tablero
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(event.pos)

    return None


def handle_menu(screen):
    """
    Maneja la lógica del menú principal del juego.

    Parámetros:
    -----------
    screen : pygame.Surface
        La superficie de la pantalla donde se dibuja el menú.

    Returns:
    -------
    str
        El estado del juego después de manejar el menú. Puede ser 'pvp', 'difficulty_select' o None.
    """
    screen.fill(background_color)

    # Dibujar título del menú
    font = pygame.font.Font(None, 74)
    title = font.render("Ajedrez", True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH//2, 100))
    screen.blit(title, title_rect)

    # Dibujar botones del menú
    pvp_button.draw(screen)
    pvc_button.draw(screen)

    # Manejar eventos del menú
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Manejar eventos de los botones
        if pvp_button.handle_event(event):
            return 'pvp'
        if pvc_button.handle_event(event):
            return 'difficulty_select'

    return None


def handle_difficulty_select(screen, difficulty_buttons):
    """
    Maneja la selección de dificultad
    Returns:
        tuple: (nuevo_estado, nuevo_juego)
    """
    screen.fill(background_color)

    # Dibujar título
    font = pygame.font.Font(None, 74)
    title = font.render("Selecciona Dificultad", True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH//2, 100))
    screen.blit(title, title_rect)

    # Dibujar botones y descripciones
    font_desc = pygame.font.Font(None, 28)
    for diff_key, button in difficulty_buttons:
        button.draw(screen)
        desc = font_desc.render(DIFFICULTY[diff_key]['description'],
                                True, (200, 200, 200))
        desc_rect = desc.get_rect(
            center=(WIDTH//2, button.rect.bottom + 10))
        screen.blit(desc, desc_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'menu', None

        # Manejar clicks en botones de dificultad
        for diff_key, button in difficulty_buttons:
            if button.handle_event(event):
                new_game = ChessGame(screen, 'pvc', diff_key)
                return 'pvc', new_game

    return None, None


def create_difficulty_buttons():
    difficulty_buttons = []
    for i, (diff_key, diff_data) in enumerate(DIFFICULTY.items()):
        y_pos = HEIGHT//4 + i*100
        button = Button(center_x, y_pos,
                        button_width, button_height,
                        diff_data['name'],
                        diff_data['color'],
                        diff_data['hover_color'])
        difficulty_buttons.append((diff_key, button))
    return difficulty_buttons


def getConf():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ajedrez")
    game = ChessGame(screen)
    clock = pygame.time.Clock()
    return screen, game, clock


def draw_highlighted_moves(screen, highlighted_moves):
    """
    Dibuja los movimientos destacados en la pantalla.

    Parámetros:
    - screen: La superficie de la pantalla donde se dibujan los movimientos.
    - highlighted_moves: Una lista de movimientos destacados, cada uno representado como una tupla (fila, columna).

    Esta función itera sobre los movimientos destacados y dibuja un círculo blanco en la posición correspondiente en el tablero.
    """
    if highlighted_moves:
        for move in highlighted_moves:
            center_x = move[1] * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = move[0] * SQUARE_SIZE + SQUARE_SIZE // 2 + MARGIN_TOP
            pygame.draw.circle(screen, (255, 255, 255),
                               (center_x, center_y), 5)


if __name__ == "__main__":
    main()
