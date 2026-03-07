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
        pass

    def reset(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event: pygame.event):
        pass