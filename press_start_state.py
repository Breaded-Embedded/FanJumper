import pygame

from game_state import GameState

class PressStartState(GameState):
    def reset(self):
        pass

    def handle_joystick_pressed(self):
        self.game.change_state(self.game.states['playing'])

    def draw(self):
        self.game.states['playing'].draw()

        # Get surfaces
        start_text = self.game.font.render("PRESS ANY KEY TO START", True, (0,0,0))
        title_sprite = self.game.sprites['game_title']

        gap_margin = 16
        total_height = start_text.get_height() + title_sprite.get_height() + gap_margin

        # Game Title
        rect = title_sprite.get_rect(midtop=(self.game.width // 2, self.game.hud_height + (self.game.height - self.game.hud_height) // 2 - total_height // 2))
        self.game.screen.blit(title_sprite, rect)

        # Press Any Key Text
        rect = start_text.get_rect(midtop=(self.game.width // 2, self.game.hud_height + (self.game.height - self.game.hud_height) // 2 - total_height // 2 + title_sprite.get_height() + gap_margin))
        self.game.screen.blit(start_text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.game.change_state(self.game.states['playing'])
