from chess.classes.pieces.bishop import Bishop
from chess.classes.pieces.piece import Piece
from chess.classes.pieces.rock import Rock


class Queen(Piece):
    moves = []

    def __init__(self, name, cell, image, color):
        super().__init__(name, cell, image, color)
        self.moves.extend(Rock.moves)
        self.moves.extend(Bishop.moves)

    def generate_valid_moves(self, board):
        row, column = self.cell.get_coors()

        for r_move, c_move in Queen.moves:
            for d in range(1, board.DIMENSION):
                coors = (row + r_move * d, column + c_move * d)
                if not Piece.is_possible_coors(coors):
                    break

                self.general_moves[coors] = True
                target = board.get_cell_by_coors(coors).piece
                if target:
                    break
