import os
import pygame

from chess.chess import ChessEngine
from chess.classes.board import Board
from chess.classes.cell import Cell
from chess.classes.pieces.pieces_factory import PiecesFactory

board_scheme = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
]

pieces = {}
for (_, _, filenames) in os.walk('./images/pieces'):
    for filename in filenames:
        pieces[filename.split('.')[0]] = pygame.image.load("./images/pieces/" + filename)


def create_start_board():
    board = [[Cell(0, 0, None)] * Board.DIMENSION for _ in range(Board.DIMENSION)]
    pieces_factory = PiecesFactory()

    for y, row in enumerate(board_scheme):
        for x, column in enumerate(row):
            color = Board.COLORS[(y + x) % 2]
            cell = Cell(x, y, color)

            if column != '--':
                piece = pieces_factory.create(name=column, cell=cell, color=column[0], image=pieces[column])
                cell.piece = piece
            board[y][x] = cell
    return board


def collect_kings(board):
    kings = {}
    for row in board:
        for cell in row:
            if cell.piece and 'K' in cell.piece.name:
                kings[cell.piece.color] = cell.piece
    return kings


def main():
    start_board = create_start_board()
    kings = collect_kings(start_board)
    chess_engine = ChessEngine(start_board, kings, pieces)
    chess_engine.play()


if __name__ == '__main__':
    main()
