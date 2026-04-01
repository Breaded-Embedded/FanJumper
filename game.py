import json
import pygame
import serial
import serial.tools.list_ports
import math

from press_start_state import PressStartState
from playing_state import PlayingState
from game_over_state import GameOverState
from leaderboard_state import LeaderboardState
import leaderboard

BAUD_RATE = 115200
DEAD_ZONE = 0.1
JOYSTICK_MAX = 1024

FAN_MIN = 10
FAN_MAX = 100

pygame.mixer.pre_init(22050, -16, 1, 32)

class Game:
    def __init__(self, width=320, height=180, title="Fan Jumper"):
        pygame.init()

        self.width = width
        self.height = height
        self.title = title

        self.hud_height = 16 # Size of the HUD on the top of the screen

        # Resizable window
        self.window = pygame.display.set_mode((1920 //2, 1200//2))
        pygame.display.set_caption(self.title)

        # Internal render surface
        self.screen = pygame.Surface((self.width, self.height))

        leaderboard.init()

        self.clock = pygame.time.Clock()
        self.running = True

        # Serial controller input state
        self.controller = {"x": 0, "y": 0, "button": 0}
        self._serial_buf = ""

        self.serial = None
        ports = serial.tools.list_ports.comports()
        if len(ports) > 0:
            port = None
            print("AVAILABLE PORTS:")
            for p in sorted(ports):
                selected_text = ""
                if port is None and "arduino" in p.description.lower():
                    port = p
                    selected_text = " (Selected)"
                print(f" - {p.device}: {p.description} [{p.hwid}]" + selected_text)
            
            if port is not None:
                print(f"Connecting to port {port.device}")
                try:
                    self.serial = serial.Serial(port.device, BAUD_RATE, timeout=0)
                    print(f"Serial connected on {port.device}")
                except serial.SerialException as e:
                    print(f"Serial connection failed: {e}")
                    self.serial = None

        # Load resources
        self.font = pygame.font.Font("assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 8)
        self.sprites = self.load_sprites()
        pygame.mixer.music.load("assets/music/DayAndNight.wav")
        pygame.mixer.music.play(loops=-1)

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
            sprites['hat_1'] = pygame.image.load('assets/sprites/hat_1.png').convert_alpha()
            sprites['flying_0'] = pygame.image.load('assets/sprites/flying_0.png').convert_alpha()
            sprites['flying_1'] = pygame.image.load('assets/sprites/flying_1.png').convert_alpha()
            sprites['game_title'] = pygame.image.load('assets/sprites/game_title.png').convert_alpha()
            sprites['bomb'] = pygame.image.load('assets/sprites/bomb.png').convert_alpha()
        except pygame.error as e:
            print(f"Error loading image: {e}")
            pygame.quit()
            exit()
        return sprites

    def read_serial(self):
        """Non-blocking serial read. Accumulates chars into a buffer,
        parses complete JSON objects, and updates self.controller."""

        if not self.serial or not self.serial.is_open:
            return

        try:
            bytes_waiting = self.serial.in_waiting
            if bytes_waiting == 0:
                return

            chunk = self.serial.read(bytes_waiting).decode('utf-8', errors='replace')
            self._serial_buf += chunk

            while '{' in self._serial_buf and '}' in self._serial_buf:
                start = self._serial_buf.index('{')
                end = self._serial_buf.index('}') + 1

                if start > 0:
                    garbage = self._serial_buf[:start]
                    if garbage.strip():
                        print(f"Discarding unexpected data: {repr(garbage)}")
                    self._serial_buf = self._serial_buf[start:]
                    end = self._serial_buf.index('}') + 1

                candidate = self._serial_buf[:end]
                self._serial_buf = self._serial_buf[end:]

                try:
                    data = json.loads(candidate)
                    if 'x' in data:
                        x = ((data['x'] / JOYSTICK_MAX) - 0.5) * 2.0
                        if (abs(x) < DEAD_ZONE):
                            x = 0
                        else:
                            if self.controller['x'] == 0:
                                self.current_state.handle_joystick_pressed()
                        self.controller['x'] = x
                    if 'y' in data:
                        y = data['y']
                        y = min(max((y - FAN_MIN) / (FAN_MAX - FAN_MIN), 0.0), 1.0)
                        self.controller['y'] = y
                    if 'button' in data:
                        self.controller['button'] = data['button']
                    print(f"Controller: {self.controller}")  # Remove once confirmed working
                except json.JSONDecodeError:
                    print(f"Invalid JSON: {repr(candidate)}")

        except serial.SerialException as e:
            print(f"Serial read error: {e}")
            self.serial = None

    def render_scaled(self):
        win_w, win_h = self.window.get_size()

        scale = min(win_w / self.width, win_h / self.height)
        scaled_w = int(self.width * scale)
        scaled_h = int(self.height * scale)

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.running = False
                else:
                    self.current_state.handle_event(event)

            if self.serial is None:
                keys = pygame.key.get_pressed()

                self.controller['x'] = 0
                self.controller['y'] = 0

                # Horizontal movement
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.controller['x'] = -1
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.controller['x'] = 1
                
                # Jump
                if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]):
                    self.controller['y'] = 1
                print(f"Controller (keyboard): {self.controller}")

            # Non-blocking serial read — updates self.controller if new data arrived
            self.read_serial()

            self.current_state.update()
            self.current_state.draw()
            self.render_scaled()

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000.0
            self.runtime += self.delta_time

        if self.serial and self.serial.is_open:
            self.serial.close()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
