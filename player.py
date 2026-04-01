import pygame

from enum import Enum
import math

class PlayerState(Enum):
    WALKING = 0
    FLYING = 1


class Player:
    def __init__(self, game, sprites: list[pygame.Surface], x=100, y=100):
        self.game = game
        self.sprites = sprites
        self.rect = self.sprites['player_0'].get_rect(topleft=(x, y))

        # physics
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 24
        self.move_speed = 180
        self.fly_strength = 30
        self.fly_ratio = 0.15
        self.dir = 1

        self.on_ground = False

        self.state = PlayerState.WALKING
        self.bob_animation = [sprites['player_0'], sprites['player_1']]
        self.flying_animation = [sprites['flying_0'], sprites['flying_1']]
        self.hat_animation = [sprites['hat_0'], sprites['hat_1']]

    def update(self, controller, delta_time = 0.0):
        # Ground friction
        if self.on_ground:
            self.vel_x = 0

        # Horizontal movement
        if abs(controller['x']) > 0.0:
            self.vel_x = controller['x'] * self.move_speed * delta_time
            if controller['x'] > 0.0:
                self.dir = 1
            elif controller['x'] < 0.0:
                self.dir = -1
        
        # Flying
        if (controller['y'] > 0.0):
            self.vel_y -= self.fly_strength * delta_time
            self.vel_x += self.fly_strength * self.fly_ratio * delta_time
            self.state = PlayerState.FLYING
            self.on_ground = False
        else:
            self.state = PlayerState.WALKING
        
        # Apply gravity
        self.vel_y += self.gravity * delta_time

        # Apply movement
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.y < self.game.hud_height:
            self.rect.y = self.game.hud_height
            self.vel_y = 0.0

    def draw(self, screen, camera_x: float, delta_time = 0.0, runtime = 0.0):
        sprite = self.sprites['player_0']

        if self.state == PlayerState.WALKING:
            frame = int(runtime * 4.0) % len(self.bob_animation)
            sprite = self.bob_animation[frame]
        elif self.state == PlayerState.FLYING:
            frame = int(runtime * 8.0) % len(self.flying_animation)
            sprite = self.flying_animation[frame]

        player_screen_x = self.rect.x - camera_x
        screen.blit(pygame.transform.flip(sprite, self.dir == -1, False), (player_screen_x, self.rect.y))

        if self.state == PlayerState.WALKING:
            # Draw propeller
            hat_frame = int(runtime * 4.0) % len(self.hat_animation)
            sprite = self.hat_animation[hat_frame]
            screen.blit(pygame.transform.flip(sprite, self.dir == -1, False), (player_screen_x, self.rect.y + (1 if frame == 1 else 0)))

    def get_hitbox(self) -> pygame.Rect:
        hitbox = pygame.Rect(0, 0, self.rect.width - 4, self.rect.height - 4)
        hitbox.midbottom = self.rect.midbottom
        return hitbox