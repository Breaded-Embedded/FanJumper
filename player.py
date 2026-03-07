import pygame


class Player:
    def __init__(self, sprite: pygame.Surface, x=100, y=100):
        self.sprite = sprite
        self.rect = self.sprite.get_rect(topleft=(x, y))

        # physics
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.4
        self.move_speed = 3
        self.jump_strength = -8

        self.on_ground = False

    def update(self, ground_y = 1000):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        self.vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -self.move_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = self.move_speed

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

        # Apply gravity
        self.vel_y += self.gravity

        # Apply movement
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Simple ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)