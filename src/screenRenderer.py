import pygame
from colors import *
from shapes import *
from fonts import *
from renderUtils import *
from communication.utils import *

PLAYER_STATE_NOT_JOINED = 1
PLAYER_STATE_JOINED = 2
PLAYER_STATE_PLAYING = 4
PLAYER_STATE_GAME_OVER = 5
PLAYER_STATE_OFFLINE = 6

class ScreenRenderer:
    def __init__(self, screen, gameManager):
        self.__screen = screen
        self.__gameManager = gameManager
        self.__registerComponents()
        self.__margin = 10
        self.__headerHeight = 160 # Calculated - change if header code changes
        self.__leaderboardHeight = 75 + self.__margin + self.__leaderboardLbl.get_rect().height # Calculated - change if leaderboard code changes
        self.__leaderboard = ScreenLeaderboard()
        self.__players = ScreenPlayers()
        self.__renderAll()

    def __registerComponents(self):
        self.__logo = pygame.image.load("images/logo.png").convert_alpha()
        self.__headerLbl = HEADER_FONT.render("ENTS SuperSimon", 1, PRIMARY_HEADER_TEXT_COLOR)
        self.__leaderboardLbl = SUBTITLE_FONT.render("Top scores:", 1, HEADER_TEXT_COLOR)
        self.__playersLbl = SUBTITLE_FONT.render("Participants:", 1, HEADER_TEXT_COLOR)
        self.__noPlayersLbl = REGULAR_FONT.render("No game pads found", 1, DEEP_RED)

    # Renders the entire scene
    def __renderAll(self):
        self.__screen.fill(BACKGROUND_COLOR)
        self.__renderHeader()
        self.__renderLeaderboardBackground()
        self.__renderPlayerBackground()
        self.__renderPlayers()
        pygame.display.flip()

    def __renderHeader(self):
        x = self.__margin
        y = self.__margin
        w = 119
        h = 150
        self.__screen.blit(self.__logo, (x, y, w, h))
        self.__screen.blit(self.__headerLbl, (x + w + self.__margin, -self.__margin)) # Negative because of the font

    def __renderLeaderboardBackground(self):
        x = self.__margin
        y = self.__headerHeight + self.__margin
        self.__screen.blit(self.__leaderboardLbl, (x, y))
        for i in range(0, len(self.__gameManager.leaderboard)):
            r = self.__getLbRect(i)
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]
            rx = (i * w) + x
            rect = (rx, y, w - self.__margin, h)
            AAfilledRoundedRect(self.__screen, rect, WIDGET_BACKGROUND_COLOR1, 0.2)

            lbl = LEADERBOARD_RANK_FONT.render("#" + str(i + 1), 1, MUTED_TEXT_COLOR)
            area = lbl.get_rect()
            lx = (rx + w) - area.width - self.__margin - (self.__margin / 2)
            ly = (y + h) - area.height
            self.__screen.blit(lbl, (lx, ly))

            # We pre-render the score so that it is updated for when we do ticking
            self.__drawLeaderboardScore(i, rx, y)

    def __renderPlayerBackground(self):
        x = self.__margin
        y = self.__headerHeight + self.__margin + self.__leaderboardHeight + self.__margin
        self.__screen.blit(self.__playersLbl, (x, y))

    def __getLbRect(self, i):
        x = self.__margin
        y = self.__headerHeight + self.__margin + self.__leaderboardLbl.get_rect().height + self.__margin
        w = (self.__screen.get_rect().width - self.__margin - self.__margin) / (float)(len(self.__gameManager.leaderboard))
        h = 75
        return (x, y, w, h)

    def __drawLeaderboardScore(self, i, rx, y):
        dirty = []
        score = self.__gameManager.leaderboard[i]
        localLb = self.__leaderboard
        if not localLb.hasChanged(i, score):
            return dirty # Nothing to draw
        lbl = LEADERBOARD_SCORE_FONT.render(str(score), 1, SCORE_TEXT_COLOR)
        lx = rx + self.__margin + (self.__margin / 2)
        ly = y
        oldLbl = localLb.getOldLabel(i)
        if oldLbl is not None:
            olr = self.__getRect(oldLbl.get_rect(), (lx, ly), True)
            dirty.append(olr)
            pygame.draw.rect(self.__screen, WIDGET_BACKGROUND_COLOR1, olr)
        self.__screen.blit(lbl, (lx, ly))
        localLb.setLabel(i, score, lbl)
        dirty.append(self.__getRect(lbl.get_rect(), (lx, ly)))
        return dirty

    def __renderPlayers(self):
        x = self.__margin
        y = self.__headerHeight + self.__margin + self.__leaderboardHeight + self.__margin + self.__playersLbl.get_rect().height + self.__margin
        players = self.__gameManager.getPlayers()
        playerCount = len(players)
        if self.__players.hadNoPlayersLbl and playerCount <= 0:
            return # Already rendered
        dirty = []
        if playerCount <= 0:
            self.__screen.blit(self.__noPlayersLbl, (x, y))
            dirty.append(self.__getRect(self.__noPlayersLbl.get_rect(), (x, y)))
            self.__players.hadNoPlayersLbl = True
            return
        self.__players.hadNoPlayersLbl = False
        w = (self.__screen.get_rect().width - self.__margin - self.__margin) / (float)(playerCount)
        h = self.__screen.get_rect().height - y - self.__margin
        reRendering = False
        if playerCount > self.__players.pastPlayers:
            reRendering = True
            r = (x, y, w * playerCount, h)
            dirty.append(r)
            pygame.draw.rect(self.__screen, BACKGROUND_COLOR, r)
            self.__players.resetPastPlayers()
        self.__players.pastPlayers = playerCount
        for i in range(0, playerCount):
            player = players[i]
            rx = (i * w) + x
            if reRendering:
                rect = (rx, y, w - self.__margin, h)
                AAfilledRoundedRect(self.__screen, rect, WIDGET_BACKGROUND_COLOR2, 0.05)

                lbl = PLAYER_NUMBER_FONT.render("Player " + str(i + 1), 1, MUTED_TEXT_COLOR)
                lx = rx + self.__margin
                ly = y + self.__margin
                self.__screen.blit(lbl, (lx, ly))

            # Get current player state
            state = 0 # Unknown state
            if player.joined:
                state = PLAYER_STATE_JOINED
            else:
                state = PLAYER_STATE_NOT_JOINED
            if player.playing:
                state = PLAYER_STATE_PLAYING
            if player.gameOver:
                state = PLAYER_STATE_GAME_OVER
            if not player.online:
                state = PLAYER_STATE_OFFLINE

            # Render the player state
            message = None
            subMessage1 = None
            subMessage2 = None
            if state == PLAYER_STATE_NOT_JOINED and self.__gameManager.isGameInProgress():
                subMessage2 = PLAYER_SUBTEXT1_FONT.render("not playing", 1, MUTED_TEXT_COLOR)
            elif state == PLAYER_STATE_NOT_JOINED and not self.__gameManager.isGameInProgress():
                subMessage1 = PLAYER_SUBTEXT1_FONT.render("not yet joined", 1, PRIMARY_TEXT_COLOR)
                subMessage2 = PLAYER_SUBTEXT2_FONT.render("press the center button to join", 1, PRIMARY_TEXT_COLOR)
            elif state == PLAYER_STATE_JOINED:
                subMessage2 = PLAYER_SUBTEXT1_FONT.render("starting in " + str(self.__gameManager.getTimeToStart()) + "s", 1, PRIMARY_TEXT_COLOR)
            elif state == PLAYER_STATE_PLAYING:
                message = PLAYER_MAJOR_FONT.render(str(player.score), 1, SCORE_TEXT_COLOR)
                subMessage2 = PLAYER_SUBTEXT1_FONT.render("Round " + str(player.roundNumber), 1, PRIMARY_TEXT_COLOR)
            elif state == PLAYER_STATE_GAME_OVER:
                color = LOSER_TEXT_COLOR
                if player.localRank == 1:
                    color = WINNER_TEXT_COLOR
                message = PLAYER_MAJOR_FONT.render(self.__rankStr(player.localRank), 1, color)
                subMessage2 = PLAYER_SUBTEXT1_FONT.render(str(player.score) + " (" + self.__rankStr(player.globalRank) + ")", 1, SCORE_TEXT_COLOR)
            elif state == PLAYER_STATE_OFFLINE:
                message = PLAYER_MAJOR_FONT.render("OFFLINE", 1, DEEP_RED)

            # Start calculating blitting
            pastPlayer = self.__players.getPlayer(i)

            if pastPlayer.primaryMessage is not None:
                pygame.draw.rect(self.__screen, WIDGET_BACKGROUND_COLOR2, pastPlayer.primaryMessage)
                dirty.append(pastPlayer.primaryMessage)
            if pastPlayer.subMessage2 is not None:
                pygame.draw.rect(self.__screen, WIDGET_BACKGROUND_COLOR2, pastPlayer.subMessage2)
                dirty.append(pastPlayer.subMessage2)
            if pastPlayer.subMessage1 is not None:
                pygame.draw.rect(self.__screen, WIDGET_BACKGROUND_COLOR2, pastPlayer.subMessage1)
                dirty.append(pastPlayer.subMessage1)

            if message is not None:
                lx = rx + center_text_x(message, w)
                ly = y + center_text_y(message, h)
                self.__screen.blit(message, (lx, ly))
                r = self.__getRect(message.get_rect(), (lx, ly))
                dirty.append(r)
                pastPlayer.primaryMessage = r

            if subMessage2 is not None:
                lx = rx + center_text_x(subMessage2, w)
                ly = (y + h) - self.__margin - subMessage2.get_rect().height
                self.__screen.blit(subMessage2, (lx, ly))
                r = self.__getRect(subMessage2.get_rect(), (lx, ly))
                dirty.append(r)
                pastPlayer.subMessage2 = r
                if subMessage1 is not None:
                    lx = rx + center_text_x(subMessage1, w)
                    ly -= subMessage1.get_rect().height + self.__margin
                    self.__screen.blit(subMessage1, (lx, ly))
                    r = self.__getRect(subMessage1.get_rect(), (lx, ly))
                    dirty.append(r)
                    pastPlayer.subMessage1 = r
        return dirty

    def __rankStr(self, rank):
        return str(rank) # TODO: Actually implement this

    def __getRect(self, r, d, tbuff = False):
        o = 0
        if tbuff: o = self.__margin
        return (r[0] + d[0], r[1] + d[1], r[2] , r[3] - o)

    # Renders only applicable parts
    def tick(self):
        start = millis()
        dirty = []
        for i in range(0, len(self.__gameManager.leaderboard)):
            r = self.__getLbRect(i)
            d = self.__drawLeaderboardScore(i, (i * r[2]) + r[0], r[1])
            for a in d: dirty.append(a)
        e1 = millis()
        #print("Took " + str(e1 - start) + "ms to render leaderboard")
        d = self.__renderPlayers()
        for a in d: dirty.append(a)
        e2 = millis()
        #print("Took " + str(e2 - e1) + "ms to render player area")
        s1 = millis()
        pygame.display.update(dirty)
        end = millis()
        #print("Took " + str(end - s1) + "ms do update")
        #print("Took " + str(end - start) + "ms to render scene")

class ScreenLeaderboard:
    def __init__(self):
        self.__pastValues = []
        self.__pastLabels = []

    def hasChanged(self, i, score):
        if len(self.__pastValues) <= i: return True
        if self.__pastValues[i] != score: return True
        return False

    def getOldLabel(self, i):
        if len(self.__pastLabels) <= i: return None
        return self.__pastLabels[i]

    def setLabel(self, i, val, lbl):
        if len(self.__pastLabels) <= i:
            self.__pastLabels.append(lbl)
            self.__pastValues.append(val)
        else:
            self.__pastLabels[i] = lbl
            self.__pastValues[i] = val

class ScreenPlayers:
    def __init__(self):
        self.pastPlayers = 0
        self.hadNoPlayersLbl = False
        self.__pastPlayers = []

    def getPlayer(self, i):
        if len(self.__pastPlayers) <= i:
            p = ScreenPlayer()
            self.__pastPlayers.append(p)
        return self.__pastPlayers[i]

    def resetPastPlayers(self):
        self.__pastPlayers = []

class ScreenPlayer:
    def __init__(self):
        self.primaryMessage = None
        self.subMessage1 = None
        self.subMessage2 = None
