from settings import knight_moves, rook_moves, bishop_moves, king_moves


def get_pawn_moves(piece, possible_moves, row, col, board, game_state):
    """
    Calcula los movimientos posibles para un peón en una posición dada.

    Parámetros:
    - piece (str): El nombre de la pieza, que indica si es un peón blanco o negro.
    - possible_moves (list): La lista de movimientos posibles que se van a calcular.
    - row (int): La fila actual de la pieza en el tablero.
    - col (int): La columna actual de la pieza en el tablero.
    - board (list): La representación del tablero de ajedrez como una lista de listas.

    Esta función determina los movimientos posibles para un peón, considerando su color y posición en el tablero.
    Los peones pueden moverse una o dos casillas hacia adelante si la casilla está vacía, dependiendo de si están en su posición inicial.
    También pueden comerse una pieza del color opuesto si está en diagonal.
    """
    if piece.startswith("white"):
        # Movimiento hacia adelante
        if row > 0 and board[row - 1][col] is None:
            possible_moves.append((row - 1, col))
        if row == 6 and board[row - 2][col] is None:  # Movimiento doble
            possible_moves.append((row - 2, col))
        # Comer pieza negra en diagonal
        if row > 0 and col > 0 and board[row - 1][col - 1] is not None and board[row - 1][col - 1].startswith("black"):
            possible_moves.append((row - 1, col - 1))
        if row > 0 and col < 7 and board[row - 1][col + 1] is not None and board[row - 1][col + 1].startswith("black"):
            possible_moves.append((row - 1, col + 1))
    elif piece.startswith("black") and game_state == 'pvp':
        # Movimiento hacia adelante
        if row < 7 and board[row + 1][col] is None:
            possible_moves.append((row + 1, col))
        if row == 1 and board[row + 2][col] is None:  # Movimiento doble
            possible_moves.append((row + 2, col))
        # Comer pieza blanca en diagonal
        if row < 7 and col > 0 and board[row + 1][col - 1] is not None and board[row + 1][col - 1].startswith("white"):
            possible_moves.append((row + 1, col - 1))
        if row < 7 and col < 7 and board[row + 1][col + 1] is not None and board[row + 1][col + 1].startswith("white"):
            possible_moves.append((row + 1, col + 1))

    return possible_moves


def get_knight_moves(piece, possible_moves, row, col, board, game_state):
    """
    Calcula los movimientos posibles para un caballo en una posición dada.

    Parámetros:
    - piece (str): El nombre de la pieza, que indica si es un caballo blanco o negro.
    - possible_moves (list): La lista de movimientos posibles que se van a calcular.
    - row (int): La fila actual de la pieza en el tablero.
    - col (int): La columna actual de la pieza en el tablero.
    - board (list): La representación del tablero de ajedrez como una lista de listas.
    - game_state (str): El estado del juego, que puede ser 'pvp' o 'pvc'.

    Esta función determina los movimientos posibles para un caballo, considerando su color, posición en el tablero y el estado del juego.
    Los caballos pueden moverse en forma de L (dos casillas en una dirección y una en otra perpendicular).
    """
    for move in knight_moves:
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] is None or (game_state == 'pvp' and board[new_row][new_col].startswith("black" if piece.startswith("white") else "white")):
                possible_moves.append((new_row, new_col))

    return possible_moves


def get_rook_moves(piece, possible_moves, row, col, board, game_state):
    """
    Calcula los movimientos posibles para una torre en una posición dada.

    Parámetros:
    - piece (str): El nombre de la pieza, que indica si es una torre blanca o negra.
    - possible_moves (list): La lista de movimientos posibles que se van a calcular.
    - row (int): La fila actual de la pieza en el tablero.
    - col (int): La columna actual de la pieza en el tablero.
    - board (list): La representación del tablero de ajedrez como una lista de listas.

    Esta función determina los movimientos posibles para una torre, considerando su color y posición en el tablero.
    Las torres pueden moverse horizontal o verticalmente cualquier número de casillas, siempre y cuando no haya otra pieza del mismo color en el camino.
    """

    for direction in rook_moves:
        for i in range(1, 8):  # Máximo de 7 casillas en cualquier dirección
            new_row, new_col = row + direction[0] * i, col + direction[1] * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # Verificar si la nueva posición está dentro del tablero
                # Si la casilla está vacía, es un movimiento válido
                if board[new_row][new_col] is None:
                    possible_moves.append((new_row, new_col))
                # Si la casilla contiene una pieza del color opuesto, es un movimiento válido y se detiene aquí
                elif game_state == 'pvp' and board[new_row][new_col].startswith("black" if piece.startswith("white") else "white"):
                    possible_moves.append((new_row, new_col))
                    break
                else:  # Si la casilla contiene una pieza del mismo color, se detiene aquí
                    break
            else:  # Si la nueva posición está fuera del tablero, se detiene aquí
                break

    return possible_moves


def get_bishop_moves(piece, possible_moves, row, col, board, game_state="pvc"):
    """
    Calcula los movimientos posibles para un alfil en una posición dada.

    Parámetros:
    - piece (str): El nombre de la pieza, que indica si es un alfil blanco o negro.
    - possible_moves (list): La lista de movimientos posibles que se van a calcular.
    - row (int): La fila actual de la pieza en el tablero.
    - col (int): La columna actual de la pieza en el tablero.
    - board (list): La representación del tablero de ajedrez como una lista de listas.

    Esta función determina los movimientos posibles para un alfil, considerando su color y posición en el tablero.
    Los alfiles pueden moverse en diagonal cualquier número de casillas, siempre y cuando no haya otra pieza del mismo color en el camino.
    """
    for direction in bishop_moves:
        for i in range(1, 8):  # Máximo de 7 casillas en cualquier dirección
            new_row, new_col = row + direction[0] * i, col + direction[1] * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # Verificar si la nueva posición está dentro del tablero
                # Si la casilla está vacía, es un movimiento válido
                if board[new_row][new_col] is None:
                    possible_moves.append((new_row, new_col))
                # Si la casilla contiene una pieza del color opuesto, es un movimiento válido y se detiene aquí
                elif game_state == 'pvp' and board[new_row][new_col].startswith("black" if piece.startswith("white") else "white"):
                    possible_moves.append((new_row, new_col))
                    break
                else:  # Si la casilla contiene una pieza del mismo color, se detiene aquí
                    break
            else:  # Si la nueva posición está fuera del tablero, se detiene aquí
                break

    return possible_moves


def get_queen_moves(piece, possible_moves, row, col, board, game_state='pvc'):
    """
    Calcula los movimientos posibles para una reina en una posición dada.

    Parámetros:
    - piece (str): El nombre de la pieza, que indica si es una reina blanca o negra.
    - possible_moves (list): La lista de movimientos posibles que se van a calcular.
    - row (int): La fila actual de la pieza en el tablero.
    - col (int): La columna actual de la pieza en el tablero.
    - board (list): La representación del tablero de ajedrez como una lista de listas.

    Esta función determina los movimientos posibles para una reina, considerando su color y posición en el tablero.
    Las reinas pueden moverse en cualquier dirección (horizontal, vertical o diagonal) cualquier número de casillas,
    siempre y cuando no haya otra pieza del mismo color en el camino.
    """
    possible_moves = get_rook_moves(piece, possible_moves, row, col,
                                    board, game_state)  # Movimientos de torre
    possible_moves = get_bishop_moves(piece, possible_moves, row, col,
                                      board, game_state)  # Movimientos de alfil

    return possible_moves


def get_king_moves(piece, possible_moves, row, col, board, game_state):
    """
    Calcula los movimientos posibles para un rey en una posición dada.

    Parámetros:
    - piece (str): El nombre de la pieza, que indica si es un rey blanco o negro.
    - possible_moves (list): La lista de movimientos posibles que se van a calcular.
    - row (int): La fila actual del rey en el tablero.
    - col (int): La columna actual del rey en el tablero.
    - board (list): La representación del tablero de ajedrez como una lista de listas.

    Esta función determina los movimientos posibles para un rey, considerando su color y posición en el tablero.
    Los reyes pueden moverse una casilla en cualquier dirección (horizontal, vertical o diagonal), siempre y cuando no haya otra pieza del mismo color en el camino.
    """
    for move in king_moves:
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] is None and game_state == 'pvp' or board[new_row][new_col].startswith("black" if piece.startswith("white") else "white"):
                possible_moves.append((new_row, new_col))

    return possible_moves
