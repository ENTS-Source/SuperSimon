import pygame
from colors import *
from shapes import *
from fonts import *
from renderUtils import *

PLAYER_STATE_NOT_JOINED = 1
PLAYER_STATE_JOINED = 2
PLAYER_STATE_PLAYING = 4
PLAYER_STATE_GAME_OVER = 5
PLAYER_STATE_OFFLINE = 6


class ScreenRenderer:
    def __init__(self, screen, game_manager):
        self.__screen = screen
        self.__gameManager = game_manager
        self._register_components()
        self.__margin = 10
        self.__headerHeight = 160  # Calculated - change if header code changes
        self.__leaderboardHeight = 125 + self.__margin + self.__leaderboardLbl.get_rect().height  # Calculated - change if leaderboard code changes
        self.__leaderboard = ScreenLeaderboard()
        self.__players = ScreenPlayers()
        self.__totals = ScreenTotal()
        self._render_all()

    def _register_components(self):
        self.__logo = pygame.image.load("images/logo.png").convert_alpha()
        self.__headerLbl = HEADER_FONT.render("ENTS SuperSimon", 1, PRIMARY_HEADER_TEXT_COLOR)
        self.__leaderboardLbl = SUBTITLE_FONT.render("Top scores:", 1, HEADER_TEXT_COLOR)
        self.__playersLbl = SUBTITLE_FONT.render("Participants:", 1, HEADER_TEXT_COLOR)
        self.__noPlayersLbl = REGULAR_FONT.render("No game pads found", 1, DEEP_RED)

    # Renders the entire scene
    def _render_all(self):
        self.__screen.fill(BACKGROUND_COLOR)
        self._render_header()
        self._render_totals()
        self._render_leaderboard_background()
        self._render_player_background()
        self._render_players()
        pygame.display.flip()

    def _render_totals(self):
        dirty = []
        if self.__totals.lastLbl is not None:
            dirty.append(self.__totals.lastLbl)
            pygame.draw.rect(self.__screen, BACKGROUND_COLOR, self.__totals.lastLbl)
        lbl = TOTALS_FONT.render("Total players: " + str(self.__gameManager.get_total_players()), 1, MUTED_TEXT_COLOR)
        r = lbl.get_rect()
        sr = self.__screen.get_rect()
        pos = (sr.width - r.width - self.__margin, self.__margin)
        rect = (pos[0], pos[1], r.width, r.height)
        dirty.append(rect)
        self.__screen.blit(lbl, pos)
        self.__totals.lastLbl = rect
        return dirty

    def _render_header(self):
        x = self.__margin
        y = self.__margin
        w = 119
        h = 150
        self.__screen.blit(self.__logo, (x, y, w, h))
        self.__screen.blit(self.__headerLbl, (x + w + self.__margin, -self.__margin))  # Negative because of the font

    def _render_leaderboard_background(self):
        x = self.__margin
        y = self.__headerHeight + self.__margin
        self.__screen.blit(self.__leaderboardLbl, (x, y))
        for i in range(0, len(self.__gameManager.leaderboard)):
            r = self._get_label_rect()
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]
            rx = (i * w) + x
            rect = (rx, y, w - self.__margin, h)
            aa_filled_rounded_rectangle(self.__screen, rect, WIDGET_BACKGROUND_COLOR1, 0.2)

            lbl = LEADERBOARD_RANK_FONT.render("#" + str(i + 1), 1, MUTED_TEXT_COLOR)
            area = lbl.get_rect()
            lx = (rx + w) - area.width - self.__margin - (self.__margin / 2)
            ly = (y + h) - area.height
            self.__screen.blit(lbl, (lx, ly))

            # We pre-render the score so that it is updated for when we do ticking
            self._draw_leaderboard_score(i, rx, y)

    def _render_player_background(self):
        x = self.__margin
        y = self.__headerHeight + self.__margin + self.__leaderboardHeight + self.__margin
        self.__screen.blit(self.__playersLbl, (x, y))

    def _get_label_rect(self):
        x = self.__margin
        y = self.__headerHeight + self.__margin + self.__leaderboardLbl.get_rect().height + self.__margin
        w = (self.__screen.get_rect().width - self.__margin - self.__margin) / float(
            len(self.__gameManager.leaderboard))
        h = 75
        return x, y, w, h

    def _draw_leaderboard_score(self, i, rx, y):
        dirty = []
        score = self.__gameManager.leaderboard[i]
        local_lb = self.__leaderboard
        if not local_lb.has_changed(i, score):
            return dirty  # Nothing to draw
        lbl = LEADERBOARD_SCORE_FONT.render(str(score), 1, SCORE_TEXT_COLOR)
        lx = rx + self.__margin + (self.__margin / 2)
        ly = y
        old_label = local_lb.get_old_label(i)
        if old_label is not None:
            olr = self._get_rect(old_label.get_rect(), (lx, ly), True)
            dirty.append(olr)
            pygame.draw.rect(self.__screen, WIDGET_BACKGROUND_COLOR1, olr)
        self.__screen.blit(lbl, (lx, ly))
        local_lb.set_label(i, score, lbl)
        dirty.append(self._get_rect(lbl.get_rect(), (lx, ly)))
        return dirty

    def _render_players(self):
        x = self.__margin
        y = self.__headerHeight + self.__margin + self.__leaderboardHeight + self.__margin + self.__playersLbl.get_rect().height + self.__margin
        players = self.__gameManager.get_players()
        player_count = len(players)
        if self.__players.hadNoPlayersLbl and player_count <= 0:
            return []  # Already rendered
        dirty = []
        if player_count <= 0:
            self.__screen.blit(self.__noPlayersLbl, (x, y))
            dirty.append(self._get_rect(self.__noPlayersLbl.get_rect(), (x, y)))
            self.__players.hadNoPlayersLbl = True
            return []
        self.__players.hadNoPlayersLbl = False
        w = (self.__screen.get_rect().width - self.__margin - self.__margin) / float(player_count)
        h = self.__screen.get_rect().height - y - self.__margin
        rerendering = False
        if player_count > self.__players.pastPlayers:
            rerendering = True
            r = (x, y, w * player_count, h)
            dirty.append(r)
            pygame.draw.rect(self.__screen, BACKGROUND_COLOR, r)
            self.__players.reset_past_players()
        self.__players.pastPlayers = player_count
        for i in range(0, player_count):
            player = players[i]
            rx = (i * w) + x
            if rerendering:
                rect = (rx, y, w - self.__margin, h)
                aa_filled_rounded_rectangle(self.__screen, rect, WIDGET_BACKGROUND_COLOR2, 0.05)

                lbl = PLAYER_NUMBER_FONT.render("Player " + str(i + 1), 1, MUTED_TEXT_COLOR)
                lx = rx + self.__margin
                ly = y + self.__margin
                self.__screen.blit(lbl, (lx, ly))

            # Get current player state
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
            sub_message_1 = None
            sub_message_2 = None
            if state == PLAYER_STATE_NOT_JOINED and self.__gameManager.is_game_in_progress():
                sub_message_2 = PLAYER_SUBTEXT1_FONT.render("not playing", 1, MUTED_TEXT_COLOR)
            elif state == PLAYER_STATE_NOT_JOINED and not self.__gameManager.is_game_in_progress():
                sub_message_1 = PLAYER_SUBTEXT1_FONT.render("not yet joined", 1, PRIMARY_TEXT_COLOR)
                sub_message_2 = PLAYER_SUBTEXT2_FONT.render("press the center button to join", 1, PRIMARY_TEXT_COLOR)
            elif state == PLAYER_STATE_JOINED:
                sub_message_2 = PLAYER_SUBTEXT1_FONT.render(
                    "starting in " + str(self.__gameManager.get_time_to_start()) + "s", 1, PRIMARY_TEXT_COLOR)
            elif state == PLAYER_STATE_PLAYING:
                message = PLAYER_MAJOR_FONT.render(str(player.score), 1, SCORE_TEXT_COLOR)
                sub_message_2 = PLAYER_SUBTEXT1_FONT.render("Round " + str(player.roundNumber), 1, PRIMARY_TEXT_COLOR)
            elif state == PLAYER_STATE_GAME_OVER:
                color = LOSER_TEXT_COLOR
                if player.localRank == 1:
                    color = WINNER_TEXT_COLOR
                message = PLAYER_MAJOR_FONT.render(self._rank_str(player.localRank), 1, color)
                sub_message_2 = PLAYER_SUBTEXT1_FONT.render(
                    str(player.score) + " (" + self._rank_str(player.globalRank) + ")", 1, SCORE_TEXT_COLOR)
            elif state == PLAYER_STATE_OFFLINE:
                message = PLAYER_MAJOR_FONT.render("OFFLINE", 1, DEEP_RED)

            # Start calculating blitting
            past_player = self.__players.get_player(i)

            if past_player.primaryMessage is not None:
                pygame.draw.rect(self.__screen, WIDGET_BACKGROUND_COLOR2, past_player.primaryMessage)
                dirty.append(past_player.primaryMessage)
            if past_player.subMessage2 is not None:
                pygame.draw.rect(self.__screen, WIDGET_BACKGROUND_COLOR2, past_player.subMessage2)
                dirty.append(past_player.subMessage2)
            if past_player.subMessage1 is not None:
                pygame.draw.rect(self.__screen, WIDGET_BACKGROUND_COLOR2, past_player.subMessage1)
                dirty.append(past_player.subMessage1)

            if message is not None:
                lx = rx + center_text_x(message, w)
                ly = y + center_text_y(message, h)
                self.__screen.blit(message, (lx, ly))
                r = self._get_rect(message.get_rect(), (lx, ly))
                dirty.append(r)
                past_player.primaryMessage = r

            if sub_message_2 is not None:
                lx = rx + center_text_x(sub_message_2, w)
                ly = (y + h) - self.__margin - sub_message_2.get_rect().height
                self.__screen.blit(sub_message_2, (lx, ly))
                r = self._get_rect(sub_message_2.get_rect(), (lx, ly))
                dirty.append(r)
                past_player.subMessage2 = r
                if sub_message_1 is not None:
                    lx = rx + center_text_x(sub_message_1, w)
                    ly -= sub_message_1.get_rect().height + self.__margin
                    self.__screen.blit(sub_message_1, (lx, ly))
                    r = self._get_rect(sub_message_1.get_rect(), (lx, ly))
                    dirty.append(r)
                    past_player.subMessage1 = r
        return dirty

    @staticmethod
    def _rank_str(rank):
        str_rank = str(rank)
        # "eleventh", etc are special cases
        if str_rank.endswith("11"):
            return str_rank + "th"
        if str_rank.endswith("12"):
            return str_rank + "th"
        if str_rank.endswith("13"):
            return str_rank + "th"
        # ... otherwise we can use the normal if statements
        if str_rank.endswith("1"):
            return str_rank + "st"
        if str_rank.endswith("2"):
            return str_rank + "nd"
        if str_rank.endswith("3"):
            return str_rank + "rd"
        # ... default to 'th' though
        return str_rank + "th"

    def _get_rect(self, r, d, tbuff=False):
        o = 0
        if tbuff:
            o = self.__margin
        return r[0] + d[0], r[1] + d[1], r[2], r[3] - o

    # Renders only applicable parts
    def tick(self):
        dirty = []
        for i in range(0, len(self.__gameManager.leaderboard)):
            r = self._get_label_rect()
            d = self._draw_leaderboard_score(i, (i * r[2]) + r[0], r[1])
            for a in d:
                dirty.append(a)
        d = self._render_players()
        for a in d:
            dirty.append(a)
        d = self._render_totals()
        for a in d:
            dirty.append(a)
        pygame.display.update(dirty)


class ScreenLeaderboard:
    def __init__(self):
        self.__pastValues = []
        self.__pastLabels = []

    def has_changed(self, i, score):
        if len(self.__pastValues) <= i:
            return True
        if self.__pastValues[i] != score:
            return True
        return False

    def get_old_label(self, i):
        if len(self.__pastLabels) <= i:
            return None
        return self.__pastLabels[i]

    def set_label(self, i, val, lbl):
        if len(self.__pastLabels) <= i:
            self.__pastLabels.append(lbl)
            self.__pastValues.append(val)
        else:
            self.__pastLabels[i] = lbl
            self.__pastValues[i] = val


class ScreenTotal:
    def __init__(self):
        self.lastLbl = None


class ScreenPlayers:
    def __init__(self):
        self.pastPlayers = 0
        self.hadNoPlayersLbl = False
        self.__pastPlayers = []

    def get_player(self, i):
        if len(self.__pastPlayers) <= i:
            p = ScreenPlayer()
            self.__pastPlayers.append(p)
        return self.__pastPlayers[i]

    def reset_past_players(self):
        self.__pastPlayers = []


class ScreenPlayer:
    def __init__(self):
        self.primaryMessage = None
        self.subMessage1 = None
        self.subMessage2 = None
