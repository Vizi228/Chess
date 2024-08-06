from chess.classes.pieces.piece import Piece


class Knight(Piece):
    moves = [
        (2, 1),
        (-2, 1),
        (2, -1),
        (-2, -1),
        (1, 2),
        (-1, 2),
        (1, -2),
        (-1, -2),
    ]

    def generate_valid_moves(self, board):
        row, column = self.cell.get_coors()

        for r_move, c_move in Knight.moves:
            coors = (row + r_move, column + c_move)
            if Piece.is_possible_coors(coors):
                self.general_moves[coors] = self.cell
