from chess.classes.pieces.piece import Piece


class Pawn(Piece):
    moves = {
        'b': [1, 2],
        'w': [-1, -2]
    }

    def generate_valid_moves(self, board):
        row, column = self.cell.get_coors()

        r_move = (row + 1) if self.color == 'b' else (row - 1)
        c_moves = [1, -1]
        for c_move in c_moves:
            c_attack_move = column + c_move
            if Piece.is_possible_move(c_attack_move):
                attack_move = (r_move, c_attack_move)
                self.attack_moves[attack_move] = True

        moves = self.moves[self.color]
        for i in range(0, len(moves) - (1 - int(self.is_first_move))):
            move = moves[i]
            r_move = row + move
            forward_move = (r_move, column)
            target = board.get_cell_by_coors(forward_move)
            if not Piece.is_possible_move(r_move) or target.piece:
                break
            self.forward_moves[forward_move] = True

