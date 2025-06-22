import sqlite3

_conn = sqlite3.connect('simon.db')
_cursor = _conn.cursor()

def init():
  _cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (score NUMERIC, recorded DATETIME);
                  ''')
  _conn.commit()

def save_score(score):
  _cursor.execute("INSERT INTO scores (score, recorded) VALUES (?, NOW());", (score))
  _conn.commit()
