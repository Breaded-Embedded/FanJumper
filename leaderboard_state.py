import random
import pygame
import re
from enum import Enum

from game_state import GameState
import utils
import leaderboard

USERNAME_NUMBER_RE = re.compile(r'[^\d]+(\d+)$')

class AnimationStates(Enum):
    IDLE = 0,
    SCROLLING = 1

IDLE_TIME = 6.0
SCROLL_SPEED = 4.0

class LeaderboardState(GameState):
    def reset(self):
        pass

    def enter(self):
        self.animation_timer = 0.0
        self.animation_state = AnimationStates.IDLE
        self.scroll_dir = -1
    
        self.current_username = self.generate_unique_username()
        score = self.game.states["playing"].personal_best
        leaderboard.data[self.current_username] = int(score)
        leaderboard.save()

        self.sorted_leaderboard = sorted(leaderboard.data.items(), key=lambda x: x[1], reverse=True)

        # Get the current user's index in the leaderboard
        self.user_index = 0
        for i, (username, score) in enumerate(self.sorted_leaderboard):
            if username == self.current_username:
                self.user_index = i

        # Set the target index to display on the leaderboard
        self.target_index = self.user_index

    def handle_joystick_pressed(self):
        self.game.change_state(self.game.states['press_start'])

    def generate_unique_username(self) -> str:
        new_username = utils.generate_username()
        while new_username in leaderboard.data.keys():
            random_number = random.randint(1, 99)
            m = USERNAME_NUMBER_RE.match(new_username)
            if m:
                number = m.group(1)
                new_username = new_username[:m.start(1)] + str(random_number) + new_username[m.end(1):]
            else:
                new_username += str(random_number)
        return new_username

    def format_column_string(self, values: list[tuple[str, int]]) -> str:
        result = ""
        for (string, width) in values:
            if len(string) > width:
                string = string[:width]
            elif len(string) < width:
                string += " " * (width - len(string))
            result += string + " "
        return result

    def draw(self):
        self.game.states['playing'].draw()

        self.animation_timer += self.game.delta_time

        if self.animation_state == AnimationStates.IDLE:
            if self.animation_timer > IDLE_TIME:
                self.animation_timer = 0.0
                self.animation_state = AnimationStates.SCROLLING
                if self.target_index == 0:
                    self.target_index = len(self.sorted_leaderboard) - 1
        elif self.animation_state == AnimationStates.SCROLLING:
            if self.animation_timer > 1.0 / SCROLL_SPEED:
                self.animation_timer = 0.0
                self.target_index -= 1

                if self.target_index == 0:
                    self.animation_state = AnimationStates.IDLE
                    self.animation_timer = 0.0

        text = self.game.font.render("LEADERBOARD", True, (255, 255, 255))
        rect = text.get_rect(center=(self.game.width // 2, self.game.hud_height // 2))
        self.game.screen.blit(text, rect)

        start_y = 40
        spacing = 10

        flash_on = (pygame.time.get_ticks() // 500) % 2 == 0

        # Determine the first and last entries to display
        start_index = max(self.target_index - 5, 0)
        end_index = start_index + 10
        if len(self.sorted_leaderboard) > 10 and end_index > len(self.sorted_leaderboard):
            end_index = len(self.sorted_leaderboard)
            start_index = end_index - 10

        for i, (username, score) in enumerate(self.sorted_leaderboard[start_index:end_index]):
            color = (0, 0, 0)
            placement = i + start_index + 1

            if username == self.current_username:
                color = (255, 255, 0) if flash_on else (0, 0, 0)
            elif placement == 1:
                color = (0, 0, 255) if flash_on else (0, 0, 0)

            entry_string = self.format_column_string([
                (f"{placement}.", 3),
                (f"{str.upper(username)}", 12),
                (f"- {score}", 8)
                ])
            entry_text = self.game.font.render(entry_string, True, color)
            entry_rect = entry_text.get_rect(center=(self.game.width // 2, start_y + i * spacing))
            self.game.screen.blit(entry_text, entry_rect)

        instruction_text = self.game.font.render("PRESS ANY KEY TO RETURN", True, (0, 0, 0))
        instruction_rect = instruction_text.get_rect(center=(self.game.width // 2, self.game.height - 20))
        self.game.screen.blit(instruction_text, instruction_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
            self.game.change_state(self.game.states['press_start'])
            self.game.states['playing'].reset()