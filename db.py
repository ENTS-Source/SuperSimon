import sqlite3

_conn = sqlite3.connect('simon.db')
_cursor = _conn.cursor()

def init():
  _cursor.execute('CREATE TABLE IF NOT EXISTS scores (score NUMERIC, recorded DATETIME);')
  _cursor.execute('ALTER TABLE scores ADD COLUMN IF NOT EXISTS game_mode (TEXT);')
  _conn.commit()

def save_score(game_mode: str, score: int):
  _cursor.execute("INSERT INTO scores (game_mode, score, recorded) VALUES (?, ?, NOW());", (game_mode, score))
  _conn.commit()
