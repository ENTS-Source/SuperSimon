from communication.utils import *
from basicTimer import BasicTimer
import math
import random
import matrix

POINTS_PER_ROUND = 200.0
POINTS_PER_MS = 0.085
POINTS_TIME_THRESHOLD = 2000.0
POINTS_BONUS_THRESHOLD = 1000.0


class GameManager:
    def __init__(self, game, score_tracker):
        self.__game = game
        self.__scoreTracker = score_tracker
        self.__lastDiscover = millis()
        self.__lastGameAction = millis()
        # Size can not change at runtime - whatever it is here is what we're stuck with
        self.leaderboard = [0, 0, 0, 0, 0]  # Placeholder for when we do actually load it
        self.__starting = False
        self.__acceptingJoins = True
        self.__gameTimer = BasicTimer(3000)
        self.__gameOverTimer = BasicTimer(3500)
        self.__playing = False
        self.__gameOver = False
        self._create_sequence()
        self._reload_leaderboard()

    def get_total_players(self):
        return self.__scoreTracker.get_total_players()

    def _reload_leaderboard(self):
        print("Reloading leaderboard...")
        self.leaderboard = self.__scoreTracker.get_top_scores(len(self.leaderboard))

    def get_players(self):
        return self.__game.players

    def is_game_in_progress(self):
        return self.__playing

    def get_time_to_start(self):
        return int(math.ceil(self.__gameTimer.value_in_seconds()))

    def _create_sequence(self):
        self.__sequence = []
        max_round = 200
        for i in range(0, max_round):
            val = None
            while val == None or (i > 0 and self.__sequence[i - 1] == val):
                val = random.randint(1, 5)  # 5 buttons
            self.__sequence.append(val)

    def tick(self, delta):
        self.__gameTimer.tick(delta)
        self.__gameOverTimer.tick(delta)
        now = millis()
        if now - self.__lastDiscover >= 5000:
            self.__lastDiscover = now
            self.__game.discover_clients()
        if now - self.__lastGameAction >= 500:
            self.__lastGameAction = now
            if self.__acceptingJoins:
                self.__game.check_joins()
            if not self.__starting and not self.__playing and not self.__gameOver:
                for player in self.get_players():
                    if player.joined and player.online:
                        self.__starting = True
                        self.__gameTimer.start()
                        self._create_sequence()
                        break
            if self.__starting and not self.__gameTimer.is_started():
                self.__starting = False
                self.__gameTimer.reset()
                self.__playing = True
                self.__acceptingJoins = False
                for player in self.get_players():
                    if player.online and player.joined:
                        player.playing = True
                        player.joined = False  # Needs to re-join post-match
                        player.score = 0
                        player.roundNumber = 1
                        player.gameOver = False
                        player.localRank = 0
                        player.globalRank = 0
                        player.roundCompleted = False
                        player.gotSequence = False
            if self.__playing and not self.__gameOverTimer.is_started():
                game_over = True
                for player in self.get_players():
                    if not player.online or player.gameOver or not player.playing:
                        continue
                    if player.roundCompleted:
                        self._analyze_game_info(player)
                    if not player.gotSequence:
                        self._send_sequence(player)
                    if not player.checkingGameInfo:
                        self.__game.check_game_info(player.address)
                    if not player.gameOver:
                        game_over = False
                if game_over:
                    self.__gameOverTimer.start()
                    self.__gameOver = True
                    self.__playing = False
            if self.__gameOver and not self.__gameOverTimer.is_started():
                for player in self.get_players():
                    was_online = player.online
                    player.reset()
                    player.online = was_online
                self.__acceptingJoins = True
                self.__gameOver = False

    def _send_sequence(self, player):
        # TODO: Add forced game over
        sequence = []
        for i in range(0, player.roundNumber):
            sequence.append(self.__sequence[i])
        player.gotSequence = True
        self.__game.send_sequence(player.address, sequence)
        self.__game.start_game(player.address)

    def _analyze_game_info(self, player):
        game_info = player.lastGameInfo
        # HACK: There's a timing issue somewhere in the code, but this works to correct it...
        if len(game_info) != player.roundNumber:
            print("Expecting " + str(player.roundNumber) + " but got " + str(len(game_info)))
            print("Game info doesn't match round number for player " + str(player.address) + ", ignoring data")
            player.roundCompleted = False  # We've now analyzed it
            return
        game_over = False
        total_score = 0.0
        total_time = 0
        max_bonus_time = POINTS_BONUS_THRESHOLD * len(game_info)
        for button in game_info:
            print("Button " + str(button.button) + " took " + str(button.time) + "ms to press")
            if button.time == 65535:
                game_over = True
                break
            else:
                if button.time < POINTS_TIME_THRESHOLD:
                    ms_under = POINTS_TIME_THRESHOLD - button.time
                    total_score += ms_under * POINTS_PER_MS
                total_time += button.time
        if total_time < max_bonus_time and not game_over:
            bonus_time = max_bonus_time - total_time
            total_score += bonus_time * (POINTS_PER_MS * 2)
        if not game_over:
            total_score += POINTS_PER_ROUND
            player.roundCompleted = False  # We've now analyzed it
            player.roundNumber += 1
            player.gotSequence = False  # Indicates new round start
            player.score += int(round(total_score))
        else:
            player.score += int(round(total_score))
            print("Player " + str(player.address) + " is in game over!")
            player.gameOver = True
            print("Recording player score...")
            self.__scoreTracker.record_score(player.score)
            matrix.send_event("m.room.message", {
                "msgtype": "m.text",
                "body": "Player score: %s" % player.score,
                "ca.ents.supersimon": {
                    "score": player.score,
                    "address": player.address,
                    "round_number": player.roundNumber,
                }
            })
            self._reload_leaderboard()
            print("Updating player ranks...")
            player_scores = []
            for player in self.get_players():
                if not player.online or not player.gameOver:
                    continue
                player_scores.append(player.score)
            for player in self.get_players():
                if not player.online or not player.gameOver:
                    continue
                scores_over = 0
                for score in player_scores:
                    if score > player.score:
                        scores_over += 1
                player.localRank = scores_over + 1
                player.globalRank = self.__scoreTracker.get_rank(player.score)
