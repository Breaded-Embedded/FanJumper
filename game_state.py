from enum import Enum

import pygame

class GameStates(Enum):
    PRESS_START = 0,
    PLAYING = 1,
    GAME_OVER = 2,
    LEADERBOARD = 3


class GameState:
    def __init__(self, game):
        self.game = game
        self.init()
        self.reset()
        
    def init(self):
        # Called when the game is opened
        pass

    def reset(self):
        # Called on initialization and state changes
        pass

    def enter(self):
        # Called when the state is entered
        pass

    def update(self):
        # Called every frame
        pass

    def draw(self):
        # Called every frame
        pass

    def handle_event(self, event: pygame.event):
        # Called when a PyGame event occurs
        pass

    def handle_joystick_pressed(self):
        # Called when the joystick is moved in a direction
        pass