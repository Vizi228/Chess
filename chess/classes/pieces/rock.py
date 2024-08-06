from chess.classes.pieces.piece import Piece


class Rock(Piece):
    moves = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def generate_valid_moves(self, board):
        row, column = self.cell.get_coors()

        for r_move, c_move in Rock.moves:
            for d in range(1, board.DIMENSION):
                coors = (row + r_move * d, column + c_move * d)
                if not Piece.is_possible_coors(coors):
                    break

                self.general_moves[coors] = True
                target = board.get_cell_by_coors(coors).piece
                if target:
                    break
