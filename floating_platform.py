import pygame


class Platform:
    def __init__(self, x=100, y=100, w=100, h=10):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 80, 80), self.rect)