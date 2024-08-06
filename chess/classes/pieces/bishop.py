from chess.classes.pieces.piece import Piece


class Bishop(Piece):
    moves = [
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    ]

    def generate_valid_moves(self, board):
        row, column = self.cell.get_coors()

        for r_move, c_move in Bishop.moves:
            for d in range(1, board.DIMENSION):
                coors = (row + r_move * d, column + c_move * d)
                if not Piece.is_possible_coors(coors):
                    break

                self.general_moves[coors] = True
                target = board.get_cell_by_coors(coors).piece
                if target:
                    break
