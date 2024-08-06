import pygame


class Cell:
    SIZE = 96

    def __init__(self, x, y, color, piece=None):
        self.x = x * self.SIZE
        self.y = y * self.SIZE
        self.color = color
        self.piece = piece
        self.selected = False

    def draw(self, screen, highlight=None):
        pygame.draw.rect(screen, self.get_display_color, pygame.Rect(self.x, self.y, self.SIZE, self.SIZE))
        if highlight:
            self.highlight(screen)
        if self.piece:
            self.piece.display(screen)

    def highlight(self, screen):
        if self.piece:
            pygame.draw.rect(screen, pygame.Color('red'), pygame.Rect(self.x, self.y, self.SIZE, self.SIZE))
        else:
            surface = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
            pygame.draw.circle(surface,
                               (0, 120, 120, 70), (self.SIZE // 2, self.SIZE // 2), self.SIZE // 4, 0)
            screen.blit(surface, surface.get_rect(x=self.x, y=self.y))

    def remove_piece(self):
        if self.piece:
            self.piece = None

    @property
    def get_display_color(self):
        color = self.color
        if self.selected:
            color = pygame.Color('green')
        return color

    def get_center(self, d_x, d_y):
        return self.x + (self.SIZE - d_x) / 2, self.y + (self.SIZE - d_y) / 2

    def get_coors(self):
        return self.y // self.SIZE, self.x // self.SIZE

    def __str__(self):
        return f'Cell({self.x}, {self.y}, {self.color}, {self.piece.name if self.piece else '--'})'
