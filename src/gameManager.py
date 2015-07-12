from communication.utils import *
from basicTimer import BasicTimer
import math
import random

POINTS_PER_ROUND = 200
POINTS_PER_MS = 0.085
POINTS_TIME_THRESHOLD = 2000
POINTS_BONUS_THRESHOLD = 1000

# TODO: Need 'all offline' check
class GameManager:
    def __init__(self, game):
        self.__game = game
        self.__lastDiscover = millis()
        self.__lastGameAction = millis()
        # Size can not change at runtime - whatever it is here is what we're stuck with
        self.leaderboard = [0, 0, 0, 0, 0] # TODO: Actually implement a leaderboard
        self.__starting = False
        self.__acceptingJoins = True
        self.__gameTimer = BasicTimer(5000)
        self.__playing = False
        self.__createSequence()

    def getPlayers(self):
        return self.__game.players

    def isGameInProgress(self):
        return self.__playing

    def getTimeToStart(self):
        return (int)(math.ceil(self.__gameTimer.valueSeconds()))

    def __createSequence(self):
        self.__sequence = []
        maxRound = 200
        for i in range(0, maxRound):
            self.__sequence.append(random.randint(1, 5)) # 5 buttons

    def tick(self, delta):
        self.__gameTimer.tick(delta)
        now = millis()
        if now - self.__lastDiscover >= 5000:
            self.__lastDiscover = now
            self.__game.discoverClients()
        if now - self.__lastGameAction >= 500:
            if self.__acceptingJoins:
                self.__game.checkJoins()
            if not self.__starting and not self.__playing:
                for player in self.getPlayers():
                    if player.joined and player.online:
                        self.__starting = True
                        self.__gameTimer.start()
                        self.__createSequence()
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
                        player.roundNumber = 1
                        player.gameOver = False
                        player.localRank = 0
                        player.globalRank = 0
                        player.roundCompleted = False
                        player.gotSequence = False
            if self.__playing:
                gameOver = True
                for player in self.getPlayers():
                    if not player.online: continue
                    if player.gameOver: continue
                    self.__game.checkGameInfo(player.address)
                    if player.roundCompleted:
                        self.__analyzeGameInfo(player)
                    if not player.gotSequence:
                        self.__sendSequence(player)
                    if not player.gameOver:
                        gameOver = False

    def __sendSequence(self, player):
        # TODO: Add forced game over
        sequence = []
        for i in range(0, player.roundNumber):
            sequence.append(self.__sequence[i])
        self.__game.sendSequence(player.address, sequence)
        self.__game.startGame()
        player.gotSequence = True

    def __analyzeGameInfo(self, player):
        gameInfo = player.lastGameInfo
        gameOver = False
        totalScore = 0.0
        totalTime = 0
        maximumBonusTime = POINTS_BONUS_THRESHOLD * len(gameInfo)
        for button in gameInfo:
            if button.time == 65535:
                gameOver = True
                break
            else:
                if button.time < POINTS_TIME_THRESHOLD:
                    msUnder = POINTS_TIME_THRESHOLD - button.time
                    totalScore += msUnder * POINTS_PER_MS
                totalTime += button.time
        if totalTime < maximumBonusTime and not gameOver:
            bonusTime = maximumBonusTime - totalTime
            totalScore += bonusTime * (POINTS_PER_MS * 2)
        if not gameOver:
            totalScore += POINTS_PER_ROUND
            player.roundCompleted = False # We've now analyzed it
            player.roundNumber += 1
            player.gotSequence = False # Indicates new round start
        else:
            print("Player " + str(player.address) + " is in game over!")
            player.gameOver = True
            # TODO: Local and global ranks
        player.score += (int)(round(totalScore))
