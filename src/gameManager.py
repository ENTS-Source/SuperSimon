from communication.utils import *

class GameManager:
    def __init__(self, game):
        self.__game = game
        self.__lastDiscover = millis()
        self.leaderboard = [50, 40, 30, 20, 10] # TODO: Actually implement a leaderboard
        self.gameStarting = False
        self.__acceptingJoins = True

    def getPlayers(self):
        return self.__game.players

    def tick(self, delta):
        now = millis()
        if now - self.__lastDiscover >= 5000:
            self.__lastDiscover = now
            self.__game.discoverClients()
            if self.__acceptingJoins:
                self.__game.checkJoins()

    def getTimeToStart(self):
        return 5 # TODO: Actually count down
