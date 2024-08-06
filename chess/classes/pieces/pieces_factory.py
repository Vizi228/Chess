from chess.classes.pieces.bishop import Bishop
from chess.classes.pieces.king import King
from chess.classes.pieces.knight import Knight
from chess.classes.pieces.piece import Piece
from chess.classes.pieces.pawn import Pawn
from chess.classes.pieces.queen import Queen
from chess.classes.pieces.rock import Rock


class PiecesFactory:
    pieces_models = {
        'wp': Pawn,
        'bp': Pawn,
        'wR': Rock,
        'bR': Rock,
        'wN': Knight,
        'bN': Knight,
        'wB': Bishop,
        'bB': Bishop,
        'wQ': Queen,
        'bQ': Queen,
        'wK': King,
        'bK': King,
    }

    def create(self, name, cell, image, color):
        model = self.pieces_models.get(name, Piece)
        return model(name=name, cell=cell, color=color, image=image)
