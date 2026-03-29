import os
import csv
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(ROOT_DIR, 'data/leaderboard.csv')

data = {}

def init():
    os.makedirs(os.path.dirname(LEADERBOARD_FILE), exist_ok=True)
    if not os.path.exists(LEADERBOARD_FILE):
        save()
    load()

def _read_data():
    if os.path.exists(LEADERBOARD_FILE) and os.path.getsize(LEADERBOARD_FILE) > 0:
        try:
            df = pd.read_csv(LEADERBOARD_FILE)
            if df.empty:
                return {}
            return pd.Series(df.score.values, index=df.username).to_dict()
        except pd.errors.EmptyDataError:
            return {}
    else:
        return {}

def load():
    data = _read_data()

def save():
    df = pd.DataFrame(list(data.items()), columns=['username', 'score'])
    df.to_csv(LEADERBOARD_FILE, index=False)