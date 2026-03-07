import pygame


class Platform:
    def __init__(self, x=100, y=100, w=100, h=10):
        self.rect = pygame.Rect(x, y, w, h)

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 80, 80), self.rect)


class MovingPlatform(Platform):
    def __init__(self, x=100, y=100, w=100, h=10, min_y=0, max_y = 100):
        self.rect = pygame.Rect(x, y, w, h)
        self.max_y = max_y
        self.min_y = min_y
        self.dir = 1

    def update(self, delta):
        pass