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
        #self.__renderPlayerArea()
        pygame.display.flip()

    def __renderHeader(self):
        x = self.__margin
        y = self.__margin
        w = 119
        h = 150
        self.__screen.blit(self.__logo, (x, y, w, h))
        self.__screen.blit(self.__headerLbl, (x + w + self.__margin, -self.__margin)) # Negative because of the font

    def __renderLeaderboardBackground(self):
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
        print("Took " + str(e1 - start) + "ms to render leaderboard")
        s1 = millis()
        pygame.display.update(dirty)
        end = millis()
        print("Took " + str(end - s1) + "ms do update")
        print("Took " + str(end - start) + "ms to render scene")

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
