from collections import defaultdict

import pygame

from chess.classes.cell import Cell
from chess.classes.pieces.pawn import Pawn
from chess.classes.pieces.pieces_factory import PiecesFactory


class Board:
    # consts
    DIMENSION = 8
    COLORS = [pygame.Color('white'), pygame.Color('gray')]

    def __init__(self, board, kings, pieces_images, screen):
        self.screen = screen

        self.pieces_factory = PiecesFactory()
        self.pieces_images = pieces_images
        self.board = board
        self.move_color = 'w'
        self.selected = None

        self.kings = kings
        self.all_general_moves = {}
        self.all_attack_moves = {}
        self.all_forward_moves = {}
        self.en_passant_moves = {'w': defaultdict(list), 'b': defaultdict(list)}

        self.judge()
        self.render()

    @property
    def king(self):
        return self.kings[self.move_color]

    @property
    def opposite_move_color(self):
        return 'w' if self.move_color == 'b' else 'b'

    @property
    def attacker(self):
        return self.selected.piece

    def render(self):
        for row in self.board:
            for cell in row:
                cell.draw(self.screen, highlight=self.has_highlight(cell))

    def has_highlight(self, cell):
        if not self.selected:
            return False
        if self.selected.piece.color != self.move_color:
            return False
        if self.selected.piece.can_move(cell, self):
            return True

    def get_cell_by_pos(self, pos):
        x, y = pos
        return self.board[y // Cell.SIZE][x // Cell.SIZE]

    def get_cell_by_coors(self, coors):
        row, column = coors
        return self.board[row][column]

    def move(self, target):
        if self.selected.piece.color != self.move_color:
            self.clear_selected()
            self.set_selected(target)
            return

        if self.selected.piece.can_move(target=target, board=self):
            self.en_passant(target)
            self.castling(target)
            target.piece = self.selected.piece
            target.piece.cell = target

            self.selected.remove_piece()
            self.clear_selected()
            self.promotion(target)

            self.change_turn()
            self.judge()
        elif target.piece:
            self.clear_selected()
            self.set_selected(target)

    def set_selected(self, cell) -> bool:
        if cell.piece:
            self.clear_selected()
            cell.selected = True
            self.selected = cell
            return True
        else:
            self.clear_selected()
            return False

    def clear_selected(self):
        if self.selected:
            self.selected.selected = False
            self.selected = None

    def en_passant(self, target):
        en_passant_cell = self.en_passant_moves[self.attacker.opposite_color].get(target.get_coors())
        if en_passant_cell:
            en_passant_cell.piece = None

        self.en_passant_moves = {'w': defaultdict(list), 'b': defaultdict(list)}
        if self.attacker.is_first_move:
            self.attacker.is_first_move = False
            if 'p' in self.attacker.name:
                row, column = self.selected.get_coors()
                t_row, t_column = target.get_coors()
                if t_column == column and t_row - row == Pawn.moves[self.attacker.color][1]:
                    coors = (row + Pawn.moves[self.attacker.color][0], column)
                    self.en_passant_moves[self.attacker.color][coors] = target
        print(self.en_passant_moves)

    def castling(self, target):
        if self.attacker is self.king:
            ally = self.king.castling_moves.get(target.get_coors())
            if ally:
                c_column = (self.king.cell.get_coors()[1] + target.get_coors()[1]) // 2
                coors = (target.get_coors()[0], c_column)
                castling_cell = self.get_cell_by_coors(coors)
                ally.cell.piece = None
                ally.cell = castling_cell
                castling_cell.piece = ally

    def promotion(self, target):
        color = target.piece.color
        promotion_row = 0 if color == 'w' else 7
        if 'p' in target.piece.name and target.get_coors()[0] == promotion_row:
            name = color + 'Q'
            target.piece = self.pieces_factory.create(name=name,
                                                      cell=target,
                                                      image=self.pieces_images[name],
                                                      color=color)

    def judge(self):
        self.generate_all_moves()
        forbidden_moves, pinned_pieces, is_check, uncheck_moves, castling = self.king.scan(self)
        self.king.filter_valid_moves(forbidden_moves, castling, self)

        if is_check:
            self.clear_moves(self.all_general_moves, uncheck_moves)
            self.clear_moves(self.all_forward_moves, uncheck_moves)
            self.clear_moves(self.all_attack_moves, uncheck_moves)
            if self.is_mate:
                print('Checkmate')
        elif self.is_mate:
            print('Stalemate')

        if pinned_pieces:
            for piece in pinned_pieces:
                to_remove = []
                for attack_move in piece.attack_moves:
                    if attack_move not in uncheck_moves:
                        to_remove.append(attack_move)
                for coors in to_remove:
                    del piece.attack_moves[coors]

                to_remove = []
                for forward_move in piece.forward_moves:
                    if forward_move not in uncheck_moves:
                        to_remove.append(forward_move)
                for coors in to_remove:
                    del piece.forward_moves[coors]

    @property
    def is_mate(self):
        return (not self.all_general_moves[self.move_color] and
                not self.all_attack_moves[self.move_color] and
                not self.all_forward_moves[self.move_color] and
                not self.king.has_valid_moves)

    def generate_all_moves(self):
        self.clear_all_moves()
        for row in self.board:
            for cell in row:
                if cell.piece and cell.piece is not self.king:
                    cell.piece.clear_valid_moves()
                    cell.piece.generate_valid_moves(self)
                    for valid_move in cell.piece.general_moves:
                        self.all_general_moves[cell.piece.color][valid_move].append(cell)
                    for attack_move in cell.piece.attack_moves:
                        self.all_attack_moves[cell.piece.color][attack_move].append(cell)
                    for forward_move in cell.piece.forward_moves:
                        self.all_forward_moves[cell.piece.color][forward_move].append(cell)

    def clear_moves(self, moves, to_save):
        to_remove = []
        for coors, cells in moves[self.move_color].items():
            if coors not in to_save:
                to_remove.append(coors)
                for cell in cells:
                    cell.piece.clear_valid_move(coors)
        for coors in to_remove:
            del moves[self.move_color][coors]

    def clear_all_moves(self):
        self.all_general_moves = {'w': defaultdict(list), 'b': defaultdict(list)}
        self.all_attack_moves = {'w': defaultdict(list), 'b': defaultdict(list)}
        self.all_forward_moves = {'w': defaultdict(list), 'b': defaultdict(list)}

    def change_turn(self):
        self.move_color = self.opposite_move_color

    def __str__(self):
        result = ''
        for row in self.board:
            result += '['
            for c in range(len(row)):
                cell = row[c]
                result += (cell.piece.name if cell.piece else '--')
                if c != len(row) - 1:
                    result += ', '
            result += ']\n'
        return result
