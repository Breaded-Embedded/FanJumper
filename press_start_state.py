import pygame

from game_state import GameState

class PressStartState(GameState):
    def reset(self):
        pass

    def handle_joystick_pressed(self):
        self.game.change_state(self.game.states['playing'])

    def draw(self):
        self.game.states['playing'].draw()

        text = self.game.font.render("PROPELLER BOY!", True, (0,0,0))
        rect = text.get_rect(center=(self.game.width//2, 100))
        self.game.screen.blit(text, rect)

        text = self.game.font.render("PRESS ANY KEY TO START", True, (0,0,0))
        rect = text.get_rect(center=(self.game.width//2, self.game.height//2))
        self.game.screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.game.change_state(self.game.states['playing'])
