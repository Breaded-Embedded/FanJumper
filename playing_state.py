import random

import pygame

from game_state import GameState
from player import Player
from floating_platform import Platform, MovingPlatform
import leaderboard

MAX_LIVES = 3

class PlayingState(GameState):
    def init(self):
        self.player = Player(self.game, self.game.sprites, 200, 100)
        self.state = 0

    def reset(self):
        random.seed(88)

        starting_platform = Platform(0, self.game.height-10, 130, 10)
        self.platforms = [starting_platform]
        self.bombs = []
        self.last_platform_x = starting_platform.rect.x + starting_platform.rect.width
        self.last_bomb_x = 0

        self.camera_x = 0
        self.score = int(self.camera_x / 10)
        self.personal_best = 0
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

    def spawn_bomb(self):
        bomb_size = self.game.sprites['bomb'].get_rect().width
        x = self.last_bomb_x + random.randint(100, 600)
        y = random.randint(0, self.game.height - self.game.hud_height - bomb_size)
        self.bombs.append(self.game.sprites['bomb'].get_rect(topleft=(x, y)))
        self.last_bomb_x = x + bomb_size

    def update(self):
        self.player.update(self.game.controller, self.game.delta_time)

        for p in self.platforms:
            if pygame.Rect.colliderect(p.rect, self.player.rect):
                if self.player.vel_y >= 0:
                    self.player.rect.bottom = p.rect.top
                    self.player.vel_y = 0
                    self.player.on_ground = True

        for b in self.bombs:
            if pygame.Rect.colliderect(b, self.player.rect):
                self.on_death()
                return

        for p in self.platforms:
            p.update()

        # camera follow
        center = self.game.width // 2
        if self.player.rect.x - self.camera_x > center:
            self.camera_x = max(self.player.rect.x - center, 0)

        # spawn platforms
        while self.last_platform_x < self.camera_x + self.game.width * 2:
            self.spawn_platform()
        
        # Spawn bombs
        while self.last_bomb_x < self.camera_x + self.game.width * 2:
            self.spawn_bomb()

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

        for b in self.bombs:
            screen_x = b.x - self.camera_x
            self.game.screen.blit(self.game.sprites['bomb'], (screen_x, b.y, b.w, b.h))

        self.player.draw(self.game.screen, self.camera_x, self.game.delta_time, self.game.runtime)
        
        # HUD Bar
        pygame.draw.rect(self.game.screen, (0, 0, 0), (0, 0, self.game.width, self.game.hud_height))

        # Draw HUD only if playing
        if self.game.current_state is self:
            # Current Score
            score_text = self.game.font.render(f"{self.score}m", True, (255, 255, 255))
            rect = score_text.get_rect(center=(self.game.width//2, self.game.hud_height // 2))
            self.game.screen.blit(score_text, rect)

            # Personal Best
            score_text = self.game.font.render(f"PB {self.personal_best}m", True, (255, 255, 100))
            rect = score_text.get_rect(midleft=((MAX_LIVES-1) * 20 + 4, self.game.hud_height // 2))
            self.game.screen.blit(score_text, rect)

            # Lives Remaining
            for i in range(self.lives - 1):
                self.game.screen.blit(self.game.sprites['hat_1'], (i * 20, 2))
            
            # High Score
            high_score_text = self.game.font.render(f"HI {leaderboard.get_high_score()}m", True, (100, 100, 200))
            rect = high_score_text.get_rect(midright=(self.game.width - 4, self.game.hud_height // 2))
            self.game.screen.blit(high_score_text, rect)

    def on_death(self):
        self.lives = self.lives - 1
    
        if self.score > self.personal_best:
            self.personal_best = self.score
        
        if self.lives > 0:
            # Respawn
            tmp_lives = self.lives
            tmp_pb = self.personal_best
            self.reset()
            self.lives = tmp_lives
            self.personal_best = tmp_pb
        else:
            # Game Over!
            self.game.change_state(self.game.states['game_over'])

    def handle_event(self, event):
        super().handle_event(event)
        
        # Reset with 'R'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.game.change_state(self.game.states['press_start'])
