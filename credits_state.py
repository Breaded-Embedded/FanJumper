import pygame

from game_state import GameState

class CreditsState(GameState):
    def reset(self):
        pass

    def handle_joystick_pressed(self):
        self.game.change_state(self.game.states['press_start'])

    def draw(self):
        self.game.states['playing'].draw()

        # Get surfaces
        start_text = self.game.font.render("  CREDITS:\n\nBRIJESH PATEL\nCONNOR LANGAN\nLOGAN DECOCK\nLOGAN FUREDI", True, (0,0,0))
        more_text = self.game.font.render("HOW IT WAS MADE:", True, (0,0,0))

        # Credits Text
        rect = start_text.get_rect(midright=(self.game.width // 2 - 15, self.game.height // 2))
        self.game.screen.blit(start_text, rect)

        # QR Code
        rect = self.game.sprites['qr_code'].get_rect(center=(self.game.width // 2 + 60, self.game.height // 2))
        self.game.screen.blit(self.game.sprites['qr_code'], rect)

        # How it Was Made Text
        rect = more_text.get_rect(center=(self.game.width // 2 + 60, self.game.height // 2 - 40))
        self.game.screen.blit(more_text, rect)

        # Credits Hint
        text = self.game.font.render("Press Any Key to Return", True, (255, 255, 255))
        rect = text.get_rect(midleft=(5, self.game.hud_height//2))
        self.game.screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
            self.game.change_state(self.game.states['press_start'])
