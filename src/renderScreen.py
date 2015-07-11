# This is in it's own file because it is very long. I should really move this out
# to other methods, but instead I won't bother just yet.

PLAYER_STATE_NOT_JOINED = 1
PLAYER_STATE_JOINED = 2
PLAYER_STATE_PLAYING = 4
PLAYER_STATE_GAME_OVER = 5
PLAYER_STATE_OFFLINE = 6

import pygame
from colors import *
from shapes import *
from fonts import *
from renderUtils import *

# Renderables
logo = pygame.image.load("images/logo.png").convert_alpha()
headerLbl = HEADER_FONT.render("ENTS SuperSimon", 1, PRIMARY_HEADER_TEXT_COLOR)
leaderboardLbl = SUBTITLE_FONT.render("Top scores:", 1, HEADER_TEXT_COLOR)
playersLbl = SUBTITLE_FONT.render("Participants:", 1, HEADER_TEXT_COLOR)
noPlayersLbl = REGULAR_FONT.render("No game pads found", 1, DEEP_RED)

# General sizing
margin = 10
headerHeight = 160 # Calculated - change if header code changes
leaderboardHeight = 75 + leaderboardLbl.get_rect().height + margin # Calculated - change if leaderboard code changes
# player area is the rest of the height

def render(screen, gameManager):
    screen.fill(BACKGROUND_COLOR)
    blit_header(screen)
    blit_leaderboard(screen, gameManager)
    blit_players(screen, gameManager)
    pygame.display.flip() # Actually render things to the screen

def blit_header(screen):
    x = margin
    y = margin
    w = 119
    h = 150
    screen.blit(logo, (x, y, w, h))
    screen.blit(headerLbl, (x + w + margin, -margin)) # negative because of the font

def blit_leaderboard(screen, gameManager):
    x = margin
    y = headerHeight + margin
    screen.blit(leaderboardLbl, (x, y))
    y += leaderboardLbl.get_rect().height + margin
    h = 75
    w = (screen.get_rect().width - margin - margin) / (float)(len(gameManager.leaderboard))
    for i in range(0, len(gameManager.leaderboard)):
        rx = (i * w) + x
        rect = (rx, y, w - margin, h)
        AAfilledRoundedRect(screen, rect, WIDGET_BACKGROUND_COLOR1, 0.2)

        lbl = LEADERBOARD_RANK_FONT.render("#" + str(i + 1), 1, MUTED_TEXT_COLOR)
        area = lbl.get_rect()
        lx = (rx + w) - area.width - margin - (margin / 2)
        ly = (y + h) - area.height
        screen.blit(lbl, (lx, ly))

        score = gameManager.leaderboard[i]
        lbl = LEADERBOARD_SCORE_FONT.render(str(score), 1, SCORE_TEXT_COLOR)
        lx = rx + margin + (margin / 2)
        ly = y
        screen.blit(lbl, (lx, ly))

def blit_players(screen, gameManager):
    x = margin
    y = headerHeight + margin + leaderboardHeight + margin
    screen.blit(playersLbl, (x, y))
    y += playersLbl.get_rect().height + margin
    players = gameManager.getPlayers()
    if len(players) <= 0:
        screen.blit(noPlayersLbl, (x, y))
        return # Nothing else to do
    w = (screen.get_rect().width - margin - margin) / (float)(len(players))
    h = screen.get_rect().height - y - margin
    for i in range(0, len(players)):
        player = players[i]
        rx = (i * w) + x
        rect = (rx, y, w - margin, h)
        AAfilledRoundedRect(screen, rect, WIDGET_BACKGROUND_COLOR2, 0.05)

        lbl = PLAYER_NUMBER_FONT.render("Player " + str(i + 1), 1, MUTED_TEXT_COLOR)
        lx = rx + margin
        ly = y + margin
        screen.blit(lbl, (lx, ly))

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

        message = None
        subMessage1 = None
        subMessage2 = None
        if state == PLAYER_STATE_NOT_JOINED:
            subMessage1 = PLAYER_SUBTEXT1_FONT.render("not yet joined", 1, PRIMARY_TEXT_COLOR)
            subMessage2 = PLAYER_SUBTEXT2_FONT.render("press the center button to join", 1, PRIMARY_TEXT_COLOR)
        elif state == PLAYER_STATE_JOINED:
            subMessage2 = PLAYER_SUBTEXT1_FONT.render("starting in " + str(gameManager.getTimeToStart()) + "s", 1, PRIMARY_TEXT_COLOR)
        elif state == PLAYER_STATE_PLAYING:
            message = PLAYER_MAJOR_FONT.render(str(player.score), 1, SCORE_TEXT_COLOR)
            subMessage2 = PLAYER_SUBTEXT1_FONT.render("Round " + str(player.roundNumber))
        elif state == PLAYER_STATE_GAME_OVER:
            color = LOSER_TEXT_COLOR
            if player.localRank == 1:
                color = WINNER_TEXT_COLOR
            message = PLAYER_MAJOR_FONT.render(rankStr(player.localRank), 1, color)
            subMessage2 = PLAYER_SUBTEXT1_FONT.render(str(player.score) + " (" + rankStr(player.globalRank) + ")")
        elif state == PLAYER_STATE_OFFLINE:
            message = PLAYER_MAJOR_FONT.render("OFFLINE", 1, DEEP_RED)

        if message is not None:
            lx = rx + center_text_x(message, w)
            ly = y + center_text_y(message, h)
            screen.blit(message, (lx, ly))

        if subMessage2 is not None:
            lx = rx + center_text_x(subMessage2, w)
            ly = (y + h) - margin - subMessage2.get_rect().height
            screen.blit(subMessage2, (lx, ly))
            if subMessage1 is not None:
                lx = rx + center_text_x(subMessage1, w)
                ly -= subMessage1.get_rect().height + margin
                screen.blit(subMessage1, (lx, ly))
