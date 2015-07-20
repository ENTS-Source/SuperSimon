import sqlite3 as db
import bisect
import os.path

class ScoreTracker:
    def __init__(self):
        dbName = "../supersimon.db"
        doCreate = not os.path.isfile(dbName)
        self.__db = db.connect(dbName)
        self.__db.row_factory = db.Row
        if doCreate:
            cursor = self.__db.cursor()
            cursor.execute("CREATE TABLE scores(id INTEGER PRIMARY KEY, score NUMERIC, recorded DATETIME)")
            # TODO: Implement other tables
            cursor.execute("CREATE TABLE games(id INTEGER PRIMARY KEY, start DATETIME, end DATETIME NULL)")
            cursor.execute("CREATE TABLE rounds(id INTEGER PRIMARY KEY, number INTEGER, game INTEGER, FOREIGN KEY (game) REFERENCES games(id))")
            cursor.execute("CREATE TABLE roundResults(id INTEGER PRIMARY KEY, round INTEGER, player INTEGER, roundScore NUMERIC, FOREIGN KEY (round) REFERENCES rounds(id))")
            cursor.execute("CREATE TABLE reactionTimes(id INTEGER PRIMARY KEY, round INTEGER, player INTEGER, button INTEGER, reactionTime NUMERIC, FOREIGN KEY (round) REFERENCES rounds(id))")
            self.__db.commit()

    def getTopScores(self, top = 5):
        cursor = self.__db.cursor()
        cursor.execute("SELECT score FROM scores ORDER BY score DESC LIMIT " + str(top))
        results = []
        for row in cursor:
            results.append(row['score'])
        while len(results) < top:
            results.append(0)
        return results

    def recordScore(self, score):
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO scores(score, recorded) VALUES (?, datetime('now'))", (score,))
        self.__db.commit()

    def getRank(self, score):
        cursor = self.__db.cursor()
        cursor.execute("SELECT COUNT(id) AS rank FROM scores WHERE score > ?", (score,))
        return cursor.fetchone()['rank'] + 1

    def getTotalPlayers(self):
        cursor = self.__db.cursor()
        cursor.execute("SELECT COUNT(id) AS total FROM scores");
        return cursor.fetchone()['total']

    def close(self):
        self.__db.close()
