# This is in it's own file because it is very long. I should really move this out
# to other methods, but instead I won't bother just yet.

import pygame
from colors import *
from shapes import *
from fonts import *

# Renderables
logo = pygame.image.load("images/logo.png").convert_alpha()
headerLbl = HEADER_FONT.render("ENTS SuperSimon", 1, PRIMARY_HEADER_TEXT_COLOR)
leaderboardLbl = SUBTITLE_FONT.render("Top scores:", 1, HEADER_TEXT_COLOR)

# General sizing
margin = 10
headerHeight = 160 # Calculated - change if header code changes
leaderboardHeight = 75 + leaderboardLbl.get_rect().height + margin # Calculated - change if leaderboard code changes
# player area is the rest of the height

def render(screen, gameManager):
    screen.fill(BACKGROUND_COLOR)
    blit_header(screen)
    blit_leaderboard(screen, gameManager)
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
