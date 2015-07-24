import sqlite3 as db
import os.path


class ScoreTracker:
    def __init__(self):
        db_name = "../supersimon.db"
        file_missing = not os.path.isfile(db_name)
        self.__db = db.connect(db_name)
        self.__db.row_factory = db.Row
        if file_missing:
            cursor = self.__db.cursor()
            cursor.execute("CREATE TABLE scores(id INTEGER PRIMARY KEY, score NUMERIC, recorded DATETIME)")
            # TODO: Implement other tables
            cursor.execute("CREATE TABLE games(id INTEGER PRIMARY KEY, start DATETIME, end DATETIME NULL)")
            cursor.execute(
                "CREATE TABLE rounds(id INTEGER PRIMARY KEY, number INTEGER, game INTEGER, FOREIGN KEY (game) REFERENCES games(id))")
            cursor.execute(
                "CREATE TABLE roundResults(id INTEGER PRIMARY KEY, round INTEGER, player INTEGER, roundScore NUMERIC, FOREIGN KEY (round) REFERENCES rounds(id))")
            cursor.execute(
                "CREATE TABLE reactionTimes(id INTEGER PRIMARY KEY, round INTEGER, player INTEGER, button INTEGER, reactionTime NUMERIC, FOREIGN KEY (round) REFERENCES rounds(id))")
            self.__db.commit()

    def get_top_scores(self, top=5):
        cursor = self.__db.cursor()
        cursor.execute("SELECT score FROM scores ORDER BY score DESC LIMIT " + str(top))
        results = []
        for row in cursor:
            results.append(row['score'])
        while len(results) < top:
            results.append(0)
        return results

    def record_score(self, score):
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO scores(score, recorded) VALUES (?, datetime('now'))", (score,))
        self.__db.commit()

    def get_rank(self, score):
        cursor = self.__db.cursor()
        cursor.execute("SELECT COUNT(id) FROM scores WHERE score > ?", (score,))
        return cursor.fetchone()[0] + 1

    def get_total_players(self):
        cursor = self.__db.cursor()
        cursor.execute("SELECT COUNT(id) FROM scores")
        return cursor.fetchone()[0]

    def close(self):
        self.__db.close()
