import sqlite3

_conn = sqlite3.connect('simon.db')
_cursor = _conn.cursor()

def init():
  _cursor.execute('CREATE TABLE IF NOT EXISTS scores (game_mode TEXT, score NUMERIC, recorded DATETIME);')
  _cursor.execute('CREATE INDEX IF NOT EXISTS idx_scores ON scores (game_mode, score);')
  _conn.commit()

def save_score(game_mode: str, score: int):
  _cursor.execute("INSERT INTO scores (game_mode, score, recorded) VALUES (?, ?, CURRENT_TIMESTAMP);", (game_mode, score))
  _conn.commit()
