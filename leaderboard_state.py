import pygame
import pandas as pd
import os

from game_state import GameState

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(ROOT_DIR, 'data/leaderboard.csv')

class LeaderboardState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.leaderboard_file = LEADERBOARD_FILE
        self.leaderboard = self.read_leaderboard_data()
        self.curr_score = 0
        self.curr_username = "Player" + str(len(self.leaderboard))

    def reset(self):
        pass

    def enter(self):
        self.curr_score = self.game.states["playing"].score
        self.add_user_score(self.curr_username, self.curr_score)

    def update(self):
        pass

    def add_user_score(self, username, score):
        self.leaderboard[username] = int(score)
        self.write_leaderboard_data()

    def draw(self):
        self.game.states['playing'].draw()

        text = self.game.font.render("LEADERBOARD", True, (0,0,0))
        rect = text.get_rect(center=(self.game.width//2, 50))
        self.game.screen.blit(text, rect)

        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)

        start_y = 70
        spacing = 10

        flash_on = (pygame.time.get_ticks() // 500) % 2 == 0

        for i, (username, score) in enumerate(sorted_leaderboard[:10]):
            color = (0, 0, 0)

            if username == self.curr_username:
                color = (255, 255, 0) if flash_on else (0, 0, 0)

            entry_text = self.game.font.render(f"{i+1}. {username} - {score}", True, color)
            entry_rect = entry_text.get_rect(center=(self.game.width // 2, start_y + i * spacing))
            self.game.screen.blit(entry_text, entry_rect)

        instruction_text = self.game.font.render("Press any key to return", True, (100, 100, 100))
        instruction_rect = instruction_text.get_rect(center=(self.game.width // 2, self.game.height - 50))
        self.game.screen.blit(instruction_text, instruction_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.game.change_state(self.game.states['press_start'])

    def read_leaderboard_data(self):
        df = pd.read_csv(self.leaderboard_file)
        return pd.Series(df.score.values, index=df.username).to_dict()

    def write_leaderboard_data(self):
        df = pd.DataFrame(list(self.leaderboard.items()), columns=['username', 'score'])
        df.to_csv(self.leaderboard_file, index=False)
