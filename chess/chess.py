import pygame

from chess.classes.board import Board
from chess.classes.cell import Cell


class ChessEngine:
    def __init__(self, start_board, kings, pieces):
        pygame.init()
        pygame.display.set_caption('Chess')
        screen_size = Board.DIMENSION * Cell.SIZE
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_size, screen_size))
        self.board = Board(start_board, kings, pieces, self.screen)

    def play(self):
        running = True
        render = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_down(event.pos)
                    render = True

            if render:
                self.board.render()
                pygame.display.flip()
                render = False

            self.clock.tick(15)

        pygame.quit()

    def on_mouse_down(self, pos):
        cell = self.board.get_cell_by_pos(pos)

        if self.board.selected:
            self.board.move(cell)
        elif cell.piece:
            self.board.set_selected(cell)
