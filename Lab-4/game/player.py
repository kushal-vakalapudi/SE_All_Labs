import pygame
from game.maze import CELL

SPEED = 3

class Player:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        x = c*CELL + CELL//2
        y = r*CELL + CELL//2
        self.rect = pygame.Rect(x-10, y-10, 20, 20)
        self.color = (60,120,220)

    def move(self, keys, walls, rows, cols):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = SPEED

        new_rect = self.rect.move(dx, 0)
        if not self._hits_wall(self.rect, new_rect, walls, rows, cols):
            self.rect = new_rect

        new_rect = self.rect.move(0, dy)
        if not self._hits_wall(self.rect, new_rect, walls, rows, cols):
            self.rect = new_rect

        self.r = self.rect.centery // CELL
        self.c = self.rect.centerx // CELL

    @staticmethod
    def _hits_wall(old_rect, new_rect, walls, rows, cols):
        if (
            new_rect.left < 0
            or new_rect.top < 0
            or new_rect.right > cols * CELL
            or new_rect.bottom > rows * CELL
        ):
            return True

        if new_rect.left < old_rect.left:
            boundary = (old_rect.left // CELL) * CELL
            while boundary > new_rect.left:
                source_col = boundary // CELL
                for row in range(new_rect.top // CELL, (new_rect.bottom - 1) // CELL + 1):
                    if walls[row][source_col][3]:
                        return True
                boundary -= CELL
        elif new_rect.right > old_rect.right:
            boundary = ((old_rect.right + CELL - 1) // CELL) * CELL
            while boundary < new_rect.right:
                source_col = boundary // CELL - 1
                for row in range(new_rect.top // CELL, (new_rect.bottom - 1) // CELL + 1):
                    if walls[row][source_col][2]:
                        return True
                boundary += CELL

        if new_rect.top < old_rect.top:
            boundary = (old_rect.top // CELL) * CELL
            while boundary > new_rect.top:
                source_row = boundary // CELL
                for col in range(new_rect.left // CELL, (new_rect.right - 1) // CELL + 1):
                    if walls[source_row][col][0]:
                        return True
                boundary -= CELL
        elif new_rect.bottom > old_rect.bottom:
            boundary = ((old_rect.bottom + CELL - 1) // CELL) * CELL
            while boundary < new_rect.bottom:
                source_row = boundary // CELL - 1
                for col in range(new_rect.left // CELL, (new_rect.right - 1) // CELL + 1):
                    if walls[source_row][col][1]:
                        return True
                boundary += CELL

        return False

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
