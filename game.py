import json

import pygame
import serial
import serial.tools.list_ports


from press_start_state import PressStartState
from playing_state import PlayingState
from game_over_state import GameOverState
from leaderboard_state import LeaderboardState


BAUD_RATE = 115220


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

        print("AVAILABLE PORTS:")
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
                print(f" - {port}: {desc} [{hwid}]")

        try:
            self.serial = serial.Serial("COM3", BAUD_RATE)
        except serial.SerialException as e:
            print(e)
            self.serial = None

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

        self.delta_time = 0.0
        self.runtime = 0.0

    def change_state(self, new_state):
        self.current_state = new_state
        self.current_state.reset()
        self.current_state.enter()

    def load_sprites(self):
        sprites = {}
        try:
            sprites['player_0'] = pygame.image.load('assets/sprites/player_0.png').convert_alpha()
            sprites['player_1'] = pygame.image.load('assets/sprites/player_1.png').convert_alpha()
            sprites['hat_0'] = pygame.image.load('assets/sprites/hat_0.png').convert_alpha()
            sprites['hat_1'] = pygame.image.load('assets/sprites/hat_0.png').convert_alpha()
            sprites['flying_0'] = pygame.image.load('assets/sprites/flying_0.png').convert_alpha()
            sprites['flying_1'] = pygame.image.load('assets/sprites/flying_0.png').convert_alpha()
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
            
            if self.serial is not None:
                # Read input from the Arduino
                line = self.serial.readline().decode('utf-8').strip()
                print(f"'{line}'")
                try:
                    data = json.loads(line)
                    print("Received:", data)
                except json.JSONDecodeError:
                    print("Invalid JSON:", line)

            self.current_state.update()
            self.current_state.draw()
            self.render_scaled()

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000.0
            self.runtime += self.delta_time

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
