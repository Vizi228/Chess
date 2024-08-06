import pygame

class Piece:
    DIMENSION = 8

    def __init__(self, name, cell, image, color):
        self.name = name
        self.color = color
        self.cell = cell
        self.opposite_color = 'w' if color == 'b' else 'b'
        self.image = image

        self.is_first_move = True
        self.is_pinned = False

        self.general_moves = {}
        self.forward_moves = {}
        self.attack_moves = {}
        self.castling_moves = {}

    def display(self, screen):
        i_x, i_y = self.image.get_size()
        c_x, c_y = self.cell.get_center(i_x, i_y)
        screen.blit(self.image,
                    pygame.Rect(c_x, c_y, self.cell.SIZE, self.cell.SIZE))

    def generate_valid_moves(self, board):
        raise NotImplementedError

    def clear_valid_move(self, coors):
        if coors in self.general_moves:
            self.general_moves.pop(coors)
        if coors in self.forward_moves:
            self.forward_moves.pop(coors)
        if coors in self.attack_moves:
            self.attack_moves.pop(coors)

    def clear_valid_moves(self):
        self.general_moves = {}
        self.forward_moves = {}
        self.attack_moves = {}
        self.castling_moves = {}

    @property
    def has_valid_moves(self):
        for coors, valid in self.general_moves.items():
            if valid:
                return True
        return False

    @staticmethod
    def is_possible_coors(coors):
        return Piece.is_possible_move(coors[0]) and Piece.is_possible_move(coors[1])

    @staticmethod
    def is_possible_move(move):
        return 0 <= move < Piece.DIMENSION

    def can_move(self, target, board):
        if self.general_moves.get(target.get_coors()):
            return not target.piece or target.piece.color != self.color
        if self.forward_moves.get(target.get_coors()):
            return True
        if self.castling_moves.get(target.get_coors()):
            return True
        if self.attack_moves.get(target.get_coors()):
            en_passant_cell = board.en_passant_moves[self.opposite_color].get(target.get_coors())
            return en_passant_cell or (target.piece and target.piece.color != self.color)
