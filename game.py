import pygame
import random
from enum import Enum

from player import Player
from platform import Platform


class GameState(Enum):
    PRESS_START = 0,
    PLAYING = 1,
    GAME_OVER = 2,
    LEADERBOARD = 3


class Game:
    def __init__(self, width=320, height=180, title="Fan Jumper"):
        pygame.init()

        self.width = width
        self.height = height
        self.title = title

        # Resizable window
        self.window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        pygame.display.set_caption(self.title)

        # Internal render surface
        self.screen = pygame.Surface((self.width, self.height))

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = GameState.PRESS_START
        self.font = pygame.font.Font("assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 8)

        self.sprites = self.load_sprites()

        self.reset_game()

    def load_sprites(self):
        sprites = {}
        try:
            sprites['player'] = pygame.image.load('assets/sprites/player_0.png').convert_alpha()
        except pygame.error as e:
            print(f"Error loading image: {e}")
            # Handle the error or exit the game
            pygame.quit()
            exit()
        return sprites

    def reset_game(self):
        self.player = Player(self.sprites['player'], 200, 100)

        self.platforms = []
        self.last_platform_x = 0
        self.camera_x = 0
        self.score = int(self.camera_x / 10)

        for _ in range(4):
            self.spawn_platform()

    def spawn_platform(self):
        gap = random.randint(40, 90)
        width = random.randint(40, 80)

        x = self.last_platform_x + gap
        y = random.randint(120, 170)

        p = Platform(x, y, width, 7)

        self.platforms.append(p)
        self.last_platform_x = x + width

    def draw(self):
        self.screen.fill((200, 200, 255))

        if self.state == GameState.PLAYING:
            self.draw_playing()

        elif self.state == GameState.PRESS_START:
            self.draw_press_start()

        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        elif self.state == GameState.LEADERBOARD:
            self.draw_leaderboard()

    def draw_playing(self):
        self.player.update()

        for p in self.platforms:
            if pygame.Rect.colliderect(p.rect, self.player.rect):
                if self.player.vel_y >= 0:
                    self.player.rect.bottom = p.rect.top
                    self.player.vel_y = 0
                    self.player.on_ground = True

        # camera follow
        center = self.width // 2
        if self.player.rect.x - self.camera_x > center:
            self.camera_x = self.player.rect.x - center

        # spawn platforms
        while self.last_platform_x < self.camera_x + self.width * 2:
            self.spawn_platform()

        # cleanup
        self.platforms = [
            p for p in self.platforms
            if p.rect.right > self.camera_x - 100
        ]

        # game over condition
        if self.player.rect.y > self.height + 50:
            self.state = GameState.GAME_OVER
        
        self.score = int(self.camera_x / 10)

        # DRAW
        for p in self.platforms:
            screen_x = p.rect.x - self.camera_x
            pygame.draw.rect(self.screen, (60, 60, 60),
                            (screen_x, p.rect.y, p.rect.w, p.rect.h))

        player_screen_x = self.player.rect.x - self.camera_x
        self.screen.blit(self.player.sprite,
                        (player_screen_x, self.player.rect.y))
        
        # draw score
        text = self.font.render(f"{self.score}m", True, (255, 255, 255))
        rect = text.get_rect(center=(self.width//2, 20))
        self.screen.blit(text, rect)

    def draw_press_start(self):
        text = self.font.render("PRESS ANY KEY TO START", True, (0,0,0))
        rect = text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(text, rect)

    def draw_game_over(self):
        text = self.font.render("GAME OVER - PRESS KEY", True, (0,0,0))
        rect = text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(text, rect)

    def draw_leaderboard(self):
        text = self.font.render("LEADERBOARD (placeholder)", True, (0,0,0))
        rect = text.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(text, rect)

    def render_scaled(self):
        win_w, win_h = self.window.get_size()

        # Maintain aspect ratio
        scale = min(win_w / self.width, win_h / self.height)

        scaled_w = int(self.width * scale)
        scaled_h = int(self.height * scale)

        # Center the image
        x = (win_w - scaled_w) // 2
        y = (win_h - scaled_h) // 2

        scaled_surface = pygame.transform.scale(self.screen, (scaled_w, scaled_h))

        self.window.fill((0, 0, 0))  # black bars
        self.window.blit(scaled_surface, (x, y))

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.state == GameState.PRESS_START:
                        self.reset_game()
                        self.state = GameState.PLAYING

                    elif self.state == GameState.GAME_OVER:
                        self.state = GameState.LEADERBOARD

                    elif self.state == GameState.LEADERBOARD:
                        self.state = GameState.PRESS_START

            self.draw()
            self.render_scaled()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
