from stockfish import Stockfish
import os
import subprocess


class ChessAI:
    def __init__(self, difficulty):
        """
        Inicializa el motor de IA de ajedrez con Stockfish.

        Args:
            difficulty (dict): Diccionario con la configuración de dificultad
        """
        stockfish_path = self._get_stockfish_path()
        if not stockfish_path:
            raise FileNotFoundError(
                "No se pudo encontrar el ejecutable de Stockfish")

        self.stockfish = Stockfish(stockfish_path)
        self.stockfish.set_skill_level(difficulty['skill_level'])
        self.stockfish.set_depth(difficulty['depth'])
        self.reset_position()

    def reset_position(self):
        """Reinicia el tablero a la posición inicial"""
        self.stockfish.set_fen_position(
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    def get_best_move(self, moves):
        """
        Obtiene el mejor movimiento según Stockfish.

        Args:
            moves (list): Lista de movimientos previos en notación UCI

        Returns:
            str: Mejor movimiento en notación UCI
        """
        # Actualiza la posición con los movimientos previos
        if moves:
            self.stockfish.set_position(moves)

        # Obtiene el mejor movimiento con el tiempo límite configurado
        return self.stockfish.get_best_move()

    def make_move(self, move):
        """
        Realiza un movimiento en el motor.

        Args:
            move (str): Movimiento en notación UCI
        """
        self.stockfish.make_moves_from_current_position([move])

    def convert_to_uci(self, start_pos, end_pos):
        """
        Convierte las coordenadas del tablero a notación UCI.

        Args:
            start_pos (tuple): Posición inicial (fila, columna)
            end_pos (tuple): Posición final (fila, columna)

        Returns:
            str: Movimiento en notación UCI
        """
        files = 'abcdefgh'
        ranks = '87654321'

        start_square = files[start_pos[1]] + ranks[start_pos[0]]
        end_square = files[end_pos[1]] + ranks[end_pos[0]]

        return start_square + end_square

    def _get_stockfish_path(self):
        """
        Encuentra la ruta del ejecutable de Stockfish.
        """
        # Primero intenta encontrar Stockfish en el PATH
        try:
            result = subprocess.run(['which', 'stockfish'],
                                    capture_output=True,
                                    text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass

        # Rutas comunes donde Stockfish podría estar instalado
        possible_paths = [
            '/usr/local/bin/stockfish',
            '/opt/homebrew/bin/stockfish',
            os.path.join(os.getcwd(), 'stockfish')
        ]
