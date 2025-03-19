from settings import knight_moves, rook_moves, bishop_moves, king_moves


def get_pawn_moves(piece, possible_moves, row, col, board, game_state):
    """
    Calcula los movimientos posibles para un peón en una posición dada.
    En modo PvC, solo permite mover piezas blancas.

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
    # Si es modo PvC y es una pieza negra, no permitir movimientos
    moves = possible_moves
    if game_state == 'pvc' and piece.startswith("black"):
        return possible_moves

    direction = 1 if piece.startswith('black') else -1
    enemy_color = 'white' if piece.startswith('black') else 'black'

    # Movimiento hacia adelante
    if 0 <= row + direction < 8:
        # Movimiento simple hacia adelante si no hay pieza
        if not board[row + direction][col]:
            moves.append((row + direction, col))

            # Movimiento doble desde la posición inicial
            initial_row = 1 if piece.startswith('black') else 6
            if row == initial_row and not board[row + 2*direction][col]:
                moves.append((row + 2*direction, col))

    # Capturas diagonales
    for dx in [-1, 1]:  # Revisar ambas diagonales
        new_col = col + dx
        new_row = row + direction
        if 0 <= new_row < 8 and 0 <= new_col < 8:  # Dentro del tablero
            target_piece = board[new_row][new_col]
            if target_piece and target_piece.startswith(enemy_color):
                moves.append((new_row, new_col))

    return moves


def get_knight_moves(piece, possible_moves, row, col, board, game_state):
    """
    Calcula los movimientos posibles para un caballo en una posición dada.
    En modo PvC, solo permite mover piezas blancas.

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
    if game_state == 'pvc' and piece.startswith("black"):
        return possible_moves

    for move in knight_moves:
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            # Permitir movimiento si la casilla está vacía o tiene una pieza enemiga
            if (board[new_row][new_col] is None or
                    board[new_row][new_col].startswith("black" if piece.startswith("white") else "white")):
                possible_moves.append((new_row, new_col))

    return possible_moves


def get_rook_moves(piece, possible_moves, row, col, board, game_state):
    """
    Calcula los movimientos posibles para una torre en una posición dada.
    En modo PvC, solo permite mover piezas blancas.

    Parámetros:
    - piece (str): El nombre de la pieza, que indica si es una torre blanca o negra.
    - possible_moves (list): La lista de movimientos posibles que se van a calcular.
    - row (int): La fila actual de la pieza en el tablero.
    - col (int): La columna actual de la pieza en el tablero.
    - board (list): La representación del tablero de ajedrez como una lista de listas.

    Esta función determina los movimientos posibles para una torre, considerando su color y posición en el tablero.
    Las torres pueden moverse horizontal o verticalmente cualquier número de casillas, siempre y cuando no haya otra pieza del mismo color en el camino.
    """
    if game_state == 'pvc' and piece.startswith("black"):
        return possible_moves

    for direction in rook_moves:
        for i in range(1, 8):
            new_row, new_col = row + direction[0] * i, col + direction[1] * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    possible_moves.append((new_row, new_col))
                elif target.startswith("black" if piece.startswith("white") else "white"):
                    possible_moves.append((new_row, new_col))
                    break
                else:
                    break
            else:
                break

    return possible_moves


def get_bishop_moves(piece, possible_moves, row, col, board, game_state="pvc"):
    """
    Calcula los movimientos posibles para un alfil en una posición dada.
    En modo PvC, solo permite mover piezas blancas.

    Parámetros:
    - piece (str): El nombre de la pieza, que indica si es un alfil blanco o negro.
    - possible_moves (list): La lista de movimientos posibles que se van a calcular.
    - row (int): La fila actual de la pieza en el tablero.
    - col (int): La columna actual de la pieza en el tablero.
    - board (list): La representación del tablero de ajedrez como una lista de listas.

    Esta función determina los movimientos posibles para un alfil, considerando su color y posición en el tablero.
    Los alfiles pueden moverse en diagonal cualquier número de casillas, siempre y cuando no haya otra pieza del mismo color en el camino.
    """
    if game_state == 'pvc' and piece.startswith("black"):
        return possible_moves

    for direction in bishop_moves:
        for i in range(1, 8):
            new_row, new_col = row + direction[0] * i, col + direction[1] * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    possible_moves.append((new_row, new_col))
                elif target.startswith("black" if piece.startswith("white") else "white"):
                    possible_moves.append((new_row, new_col))
                    break
                else:
                    break
            else:
                break

    return possible_moves


def get_queen_moves(piece, possible_moves, row, col, board, game_state='pvc'):
    """
    Calcula los movimientos posibles para una reina en una posición dada.
    En modo PvC, solo permite mover piezas blancas.

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
    # Si es modo PvC y es una pieza negra, no permitir movimientos
    if game_state == 'pvc' and piece.startswith("black"):
        return possible_moves

    possible_moves = get_rook_moves(piece, possible_moves, row, col,
                                    board, game_state)  # Movimientos de torre
    possible_moves = get_bishop_moves(piece, possible_moves, row, col,
                                      board, game_state)  # Movimientos de alfil

    return possible_moves


def get_king_moves(piece, possible_moves, row, col, board, game_state):
    if game_state == 'pvc' and piece.startswith("black"):
        return possible_moves

    # Movimientos normales del rey
    for move in king_moves:
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if (target is None or
                    target.startswith("black" if piece.startswith("white") else "white")):
                possible_moves.append((new_row, new_col))

    # Verificar enroque
    if can_castle(piece, row, col, board):
        # Posición inicial del rey
        initial_row = 7 if piece.startswith("white") else 0

        # Enroque corto (lado del rey)
        if can_castle_kingside(piece, initial_row, board):
            possible_moves.append((initial_row, 6))  # Nueva posición del rey

        # Enroque largo (lado de la reina)
        if can_castle_queenside(piece, initial_row, board):
            possible_moves.append((initial_row, 2))  # Nueva posición del rey

    return possible_moves


def can_castle(piece, row, col, board):
    """
    Verifica si el rey está en su posición inicial para el enroque
    """
    # El rey debe estar en su posición inicial
    initial_row = 7 if piece.startswith("white") else 0
    initial_col = 4

    return row == initial_row and col == initial_col


def can_castle_kingside(piece, initial_row, board):
    """
    Verifica si es posible hacer enroque corto
    """
    # Verificar que las casillas entre el rey y la torre estén vacías
    if (board[initial_row][5] is None and
        board[initial_row][6] is None and
            board[initial_row][7] is not None):

        # Verificar que la torre esté en su lugar
        tower = "white_rook" if piece.startswith("white") else "black_rook"
        return board[initial_row][7] == tower

    return False


def can_castle_queenside(piece, initial_row, board):
    """
    Verifica si es posible hacer enroque largo
    """
    # Verificar que las casillas entre el rey y la torre estén vacías
    if (board[initial_row][3] is None and
        board[initial_row][2] is None and
        board[initial_row][1] is None and
            board[initial_row][0] is not None):

        # Verificar que la torre esté en su lugar
        tower = "white_rook" if piece.startswith("white") else "black_rook"
        return board[initial_row][0] == tower

    return False
