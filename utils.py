import pygame
import os
from settings import SQUARE_SIZE


def load_images():
    """
    Carga imágenes de piezas de ajedrez desde archivos PNG y las escala al tamaño de los cuadrados del tablero.

    La función busca imágenes de piezas de ajedrez en la carpeta "assets/images/imgs-128px/" y las carga en un diccionario.
    Las imágenes se escalan al tamaño definido por la constante SQUARE_SIZE.

    Return:
        dict: Un diccionario donde las claves son los nombres de las piezas y los valores son las imágenes escaladas.

    Advertencia:
        Si alguna imagen no se encuentra en la ruta especificada, se imprimirá una advertencia en la consola.
    """

    pieces = {}
    names = ["black_pawn", "black_rook", "black_knight", "black_bishop", "black_queen", "black_king",
             "white_pawn", "white_rook", "white_knight", "white_bishop", "white_queen", "white_king"]

    for name in names:
        path = os.path.join(f"assets/images/imgs-128px/{name}.png")
        if os.path.exists(path):  # si no existe sale
            image = pygame.image.load(path)
            pieces[name] = pygame.transform.scale(
                image, (SQUARE_SIZE, SQUARE_SIZE))  # redimensionamos la imagen

        else:
            print(f"Warning: {path} does not exist.")

    return pieces
