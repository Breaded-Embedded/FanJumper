import pygame

from enum import Enum
import math

class PlayerState(Enum):
    WALKING = 0
    FLYING = 1


class Player:
    def __init__(self, sprites: list[pygame.Surface], x=100, y=100):
        self.sprites = sprites
        self.rect = self.sprites['player_0'].get_rect(topleft=(x, y))

        # physics
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.4
        self.move_speed = 3
        self.jump_strength = -8

        self.on_ground = False

        self.state = PlayerState.WALKING
        self.bob_animation = [sprites['player_0'], sprites['player_1']]
        self.flying_animation = [sprites['flying_0'], sprites['flying_1']]
        self.hat_animation = [sprites['hat_0'], sprites['hat_1']]

    def update(self, controlloer, delta_time = 0.0):
        keys = pygame.key.get_pressed()

        # # Horizontal movement
        # self.vel_x = 0
        # if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        #     self.vel_x = -self.move_speed
        # if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        #     self.vel_x = self.move_speed
        #
        # # Jump
        # if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
        #     self.vel_y = self.jump_strength
        #     self.on_ground = False

        # Apply gravity
        self.vel_y += self.gravity

        # Apply movement
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, screen, camera_x: float, delta_time = 0.0, runtime = 0.0):
        sprite = self.sprites['player_0']

        if self.state == PlayerState.WALKING:
            frame = int(runtime * 4.0) % len(self.bob_animation)
            sprite = self.bob_animation[frame]

        player_screen_x = self.rect.x - camera_x
        screen.blit(sprite, (player_screen_x, self.rect.y))

        if self.state == PlayerState.WALKING:
            # Draw propeller
            hat_frame = int(runtime * 4.0) % len(self.hat_animation)
            sprite = self.hat_animation[hat_frame]
            screen.blit(sprite, (player_screen_x, self.rect.y + (1 if frame == 1 else 0)))
