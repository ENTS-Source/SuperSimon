class Player:
    def __init__(self, address):
        self.address = address
        self.online = False
        self.joined = False
        self.roundNumber = 0
        self.roundCompleted = False
        self.playing = False
        self.gameOver = False
        self.localRank = 0
        self.globalRank = 0
