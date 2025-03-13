import pygame
from game import ChessGame
from settings import WIDTH, HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ajedrez")
    game = ChessGame(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.draw_board()
        game.draw_pieces()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
