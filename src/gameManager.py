from communication.utils import *
from basicTimer import Timer as BasicTimer
import math

class GameManager:
    def __init__(self, game):
        self.__game = game
        self.__lastDiscover = millis()
        self.leaderboard = [50, 40, 30, 20, 10] # TODO: Actually implement a leaderboard
        self.__starting = False
        self.__acceptingJoins = True
        self.__sequence = []
        self.__gameTimer = BasicTimer(5000)
        self.__playing = False

    def getPlayers(self):
        return self.__game.players

    def isGameInProgress(self):
        return self.__playing

    def getTimeToStart(self):
        return (int)(math.ceil(self.__gameTimer.valueSeconds()))

    def tick(self, delta):
        self.__gameTimer.tick(delta)
        now = millis()
        if now - self.__lastDiscover >= 5000:
            self.__lastDiscover = now
            self.__game.discoverClients()
        if self.__acceptingJoins:
            self.__game.checkJoins()
        if not self.__starting and not self.__playing:
            for player in self.getPlayers():
                if player.joined and player.online:
                    self.__starting = True
                    self.__gameTimer.start()
                    break
        if self.__starting and not self.__gameTimer.isStarted():
            self.__starting = False
            self.__playing = True
            self.__acceptingJoins = False
            for player in self.getPlayers():
                if player.online and player.joined:
                    player.playing = True
                    player.joined = False # Needs to re-join post-match
                    player.score = 0
                    player.roundNumer = 1
                    player.gameOver = False
                    player.localRank = 0
                    player.globalRank = 0
                    player.roundCompleted = False
