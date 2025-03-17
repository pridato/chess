import pygame
from game import ChessGame
from settings import WIDTH, HEIGHT, SQUARE_SIZE


def main():
    screen, game, clock = getConf()

    highlighted_moves = []  # Inicializar la lista de movimientos destacados

    while True:

        game.draw_board()
        game.draw_pieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic del mouse
                mouse_x, mouse_y = event.pos
                col = mouse_x // SQUARE_SIZE
                row = mouse_y // SQUARE_SIZE

                piece = game.board[row][col]
                if piece:
                    highlighted_moves = game.get_possible_moves(
                        piece, (row, col))

        draw_highlighted_moves(screen, highlighted_moves)

        pygame.display.flip()
        clock.tick(60)


def getConf():
    """
    Inicializa pygame y configura la pantalla y el juego de ajedrez.

    Returns:
        tuple: Una tupla que contiene la superficie de la pantalla, el objeto del juego de ajedrez y el reloj del juego. (fps)
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

    Parámetros:
    - screen: La superficie de la pantalla donde se dibujan los movimientos.
    - highlighted_moves: La lista de movimientos destacados.

    Variables:
    - SQUARE_SIZE: tamaño de cada celda del tablero.
    """
    if highlighted_moves:
        for move in highlighted_moves:
            # Calcular la posición del centro del cuadrado
            center_x = move[1] * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = move[0] * SQUARE_SIZE + SQUARE_SIZE // 2

            pygame.draw.circle(screen, (255, 255, 255),
                               (center_x + (1) * 5, center_y), 5)


if __name__ == "__main__":
    main()
