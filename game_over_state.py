import pygame
import math

from game_state import GameState


class GameOverState(GameState):

    def reset(self):
        self.timer = 0

    def update(self):
        self.timer += 1

    def handle_joystick_pressed(self):
        self.game.change_state(self.game.states['leaderboard'])

    def draw(self):
        # Draw the frozen gameplay behind the overlay
        self.game.states['playing'].draw()

        # Blink every ~0.5 seconds
        blink = True# (self.timer // 20) % 2 == 0

        # Flash between red and white
        if (self.timer // 10) % 2 == 0:
            color = (255, 50, 50)
        else:
            color = (255, 255, 255)

        if blink:
            # Small floating animation
            offset = int(math.sin(self.timer * 0.1) * 4)

            text = self.game.font.render("GAME OVER", True, color)
            rect = text.get_rect(center=(
                self.game.width // 2,
                self.game.height // 2 + offset
            ))

            self.game.screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.game.change_state(self.game.states['leaderboard'])
