from chess.classes.pieces.bishop import Bishop
from chess.classes.pieces.knight import Knight
from chess.classes.pieces.piece import Piece
from chess.classes.pieces.rock import Rock


class King(Piece):
    moves = {
        'R': Rock.moves,
        'B': Bishop.moves,
    }

    def generate_valid_moves(self, board):
        row, column = self.cell.get_coors()

        for _ in King.moves:
            for r_move, c_move in King.moves[_]:
                coors = (row + r_move, column + c_move)
                if Piece.is_possible_coors(coors):
                    target = board.get_cell_by_coors(coors)
                    self.general_moves[coors] = not target.piece or target.piece.color != self.color

    def filter_valid_moves(self, forbidden, castling, board):
        for coors, valid in self.general_moves.items():
            row, column = coors
            d_r, d_l = (row - column), (row + column)
            target = board.get_cell_by_coors(coors)
            if ((row not in forbidden['rows'] and
                 column not in forbidden['columns'] and
                 d_r not in forbidden['d-r'] and
                 d_l not in forbidden['d-l']) or target.piece):
                can_move = (coors not in board.all_general_moves[self.opposite_color] and
                            coors not in board.all_attack_moves[self.opposite_color])
                self.general_moves[coors] = can_move and (not target.piece or target.piece.color != self.color)
            else:
                self.general_moves[coors] = False

        for coors, ally in castling.items():
            self.castling_moves[coors] = ally

    def scan(self, board):
        row, column = self.cell.get_coors()

        forbidden_moves = {
            'rows': [],
            'columns': [],
            'd-r': [],
            'd-l': [],
        }
        is_check = False
        pinned_pieces = []
        uncheck_moves = {}
        castling = {}

        for expected_piece in King.moves:
            for r_move, c_move in King.moves[expected_piece]:
                allies = []
                expected_opponent = None
                to_uncheck = {}

                for d in range(1, self.DIMENSION):
                    coors = (row + r_move * d, column + c_move * d)
                    if not Piece.is_possible_coors(coors):
                        break

                    target_cell = board.get_cell_by_coors(coors)
                    to_uncheck[coors] = True
                    if target_cell.piece:
                        if target_cell.piece.color == self.color:
                            allies.append(target_cell.piece)
                        else:
                            f_row, f_column = coors
                            if expected_piece in target_cell.piece.name:
                                if expected_piece == 'R':
                                    forbidden_moves['rows'].append(f_row)
                                    forbidden_moves['columns'].append(f_column)
                                if expected_piece == 'B':
                                    forbidden_moves['d-r'].append(f_row - f_column)
                                    forbidden_moves['d-l'].append(f_row + f_column)
                                expected_opponent = True
                            if 'Q' in target_cell.piece.name:
                                forbidden_moves['rows'].append(f_row)
                                forbidden_moves['columns'].append(f_column)
                                forbidden_moves['d-r'].append(f_row - f_column)
                                forbidden_moves['d-l'].append(f_row + f_column)
                                expected_opponent = True
                            break

                if expected_opponent:
                    uncheck_moves.update(to_uncheck)
                    if not allies:
                        is_check = True
                    elif len(allies) == 1:
                        pinned_pieces.append(allies[0])
                elif self.is_first_move and len(allies) == 1 and expected_piece == 'R':
                    ally = allies[0]
                    if 'R' in ally.name and ally.color == self.color and ally.is_first_move:
                        coors = (row, column + c_move * 2)
                        castling[coors] = ally

        for r_move, c_move in Knight.moves:
            coors = (row + r_move, column + c_move)
            if Piece.is_possible_coors(coors):
                target_cell = board.get_cell_by_coors(coors)
                if target_cell.piece and 'N' in target_cell.piece.name and target_cell.piece.color != self.color:
                    uncheck_moves[coors] = True
                    is_check = True

        pawn_moves = [(1, 1), (1, -1)] if self.color == 'b' else [(-1, -1), (-1, 1)]
        for r_move, c_move in pawn_moves:
            coors = (row + r_move, column + c_move)
            if not Piece.is_possible_coors(coors):
                break
            target_cell = board.get_cell_by_coors(coors)
            if target_cell.piece and 'p' in target_cell.piece.name and target_cell.piece.color != self.color:
                uncheck_moves[coors] = True
                is_check = True

        return forbidden_moves, pinned_pieces, is_check, uncheck_moves, castling
