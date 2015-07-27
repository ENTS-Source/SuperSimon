-- High scores
CREATE TABLE scores(id INTEGER PRIMARY KEY, score NUMERIC, recorded DATETIME);

-- Game tracking
CREATE TABLE games(id INTEGER PRIMARY KEY, start DATETIME, end DATETIME NULL);
CREATE TABLE rounds(id INTEGER PRIMARY KEY, number INTEGER, game INTEGER, FOREIGN KEY (game) REFERENCES games(id));
CREATE TABLE roundResults(id INTEGER PRIMARY KEY, round INTEGER, player INTEGER, roundScore NUMERIC, FOREIGN KEY (round) REFERENCES rounds(id));
CREATE TABLE reactionTimes(id INTEGER PRIMARY KEY, round INTEGER, player INTEGER, button INTEGER, reactionTime NUMERIC, FOREIGN KEY (round) REFERENCES rounds(id));
