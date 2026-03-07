import pygame

from press_start_state import PressStartState
from playing_state import PlayingState
from game_over_state import GameOverState
from leaderboard_state import LeaderboardState


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

        # Load resources
        self.font = pygame.font.Font("assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 8)
        self.sprites = self.load_sprites()
        pygame.mixer.music.load("assets/music/DayAndNight.wav")
        pygame.mixer.music.play()

        # Create game states
        self.states = {
            'press_start': PressStartState(self),
            'playing': PlayingState(self),
            'game_over': GameOverState(self),
            'leaderboard': LeaderboardState(self)
        }
        
        # Set current state
        self.change_state(self.states['press_start'])

    def change_state(self, new_state):
        self.current_state = new_state
        self.current_state.reset()

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
                else:
                    self.current_state.handle_event(event)
                
            self.current_state.update()
            self.current_state.draw()
            self.render_scaled()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
