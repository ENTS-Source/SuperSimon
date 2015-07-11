class Player:
    def __init__(self, address):
        self.address = address
        self.reset()

    def reset(self):
        self.online = False
        self.joined = False
        self.roundNumber = 0
        self.roundCompleted = False
        self.playing = False
        self.gameOver = False
        self.localRank = 0
        self.globalRank = 0
        self.score = 0
