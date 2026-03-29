import random

import pygame

from game_state import GameState
from player import Player
from floating_platform import Platform, MovingPlatform

MAX_LIVES = 3

class PlayingState(GameState):
    def init(self):
        self.player = Player(self.game, self.game.sprites, 200, 100)
        self.state = 0

    def reset(self):
        starting_platform = Platform(0, self.game.height-10, 130, 10)
        self.platforms = [starting_platform]
        self.last_platform_x = starting_platform.rect.x + starting_platform.rect.width

        self.camera_x = 0
        self.score = int(self.camera_x / 10)
        self.lives = MAX_LIVES

        self.player.rect.x = 50
        self.player.rect.y = self.game.height - 30
        self.player.vel_x = 0
        self.player.vel_y = 0
        
        for _ in range(4):
            self.spawn_platform()

    def spawn_platform(self):
        gap = random.randint(40, 90)
        width = random.randint(40, 80)

        x = self.last_platform_x + gap
        y = random.randint(120, 170)

        moving = random.random() > 0.9

        p = Platform(x, y, width, 7)
        #if moving:
        #    p = MovingPlatform()

        self.platforms.append(p)
        self.last_platform_x = x + width

    def update(self):
        self.player.update(self.game.controller)

        for p in self.platforms:
            if pygame.Rect.colliderect(p.rect, self.player.rect):
                if self.player.vel_y >= 0:
                    self.player.rect.bottom = p.rect.top
                    self.player.vel_y = 0
                    self.player.on_ground = True

        for p in self.platforms:
            p.update()

        # camera follow
        center = self.game.width // 2
        if self.player.rect.x - self.camera_x > center:
            self.camera_x = max(self.player.rect.x - center, 0)

        # spawn platforms
        while self.last_platform_x < self.camera_x + self.game.width * 2:
            self.spawn_platform()

        # cleanup
        self.platforms = [
            p for p in self.platforms
            if p.rect.right > self.camera_x - 100
        ]

        # game over condition
        if self.player.rect.y > self.game.height + 50:
            self.on_death()
        
        self.score = int(self.camera_x / 10)

    def draw(self):
        self.game.screen.fill((200, 200, 255))

        for p in self.platforms:
            screen_x = p.rect.x - self.camera_x
            pygame.draw.rect(self.game.screen, (60, 60, 60),
                            (screen_x, p.rect.y, p.rect.w, p.rect.h))

        self.player.draw(self.game.screen, self.camera_x, self.game.delta_time, self.game.runtime)
        
        # HUD Bar
        pygame.draw.rect(self.game.screen, (0, 0, 0), (0, 0, self.game.width, self.game.hud_height))

        # Draw HUD only if playing
        if self.game.current_state is self:
            # Current Score
            text = self.game.font.render(f"{self.score}m", True, (255, 255, 255))
            rect = text.get_rect(center=(self.game.width//2, self.game.hud_height // 2))
            self.game.screen.blit(text, rect)

            # Lives Remaining
            for i in range(self.lives - 1):
                self.game.screen.blit(self.game.sprites['hat_1'], (i * 20, 2))

    def on_death(self):
        self.lives = self.lives - 1
        
        if self.lives > 0:
            # Respawn
            tmp_lives = self.lives
            self.reset()
            self.lives = tmp_lives
        else:
            # Game Over!
            self.game.change_state(self.game.states['game_over'])
