# TODO: CLEAN THIS ALL UP.
# Although it does kinda work as-is for a proof of concept?

print("Loading resources...")

import pygame
import random
import sys
import math
from shapes import * # shapes.py
from colors import * # colors.py
from time import sleep

# Set location on screen (0, 0)
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

# Init pygame stuff
pygame.init()

print("Getting screen information...")
displayInfo = pygame.display.Info()

size = width, height = displayInfo.current_w, displayInfo.current_h

print("Starting display with size " + str(width) + "x" + str(height) + " ...")
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ENTS Super Simon Game")
#pygame.display.toggle_fullscreen()

# Font definitions
regularFont = pygame.font.SysFont("monospace", 25)
largeFont = pygame.font.SysFont("monospace", 45)
extraLargeFont = pygame.font.SysFont("monospace", 90)

# ------ SCREEN INIT ------
print("Rendering major screen...")
players = 4 # TODO: Allow this to change (re-render display)
screen.fill(BACKGROUND_COLOR)

# Leaderboard section (boxes at top of screen)
lbPlayers = 5
lbMargin = 10
lbWidth = (width - (lbPlayers * lbMargin) - lbMargin) / lbPlayers
lbHeight = 75

for i in range(0, lbPlayers):
    # Rectangle
    x = i * lbWidth
    x += i * lbMargin
    rect = (x + lbMargin, lbMargin, lbWidth, lbHeight)
    AAfilledRoundedRect(screen, rect, WIDGET_BACKGROUND_COLOR1, 0.2)

    # Rank text
    rankLbl = regularFont.render("#" + str(i + 1), 1, MUTED_TEXT_COLOR)
    area = rankLbl.get_rect()
    rankX = (x + lbWidth + (lbMargin / 2)) - area.width
    rankY = (lbHeight + (lbMargin / 2)) - area.height
    screen.blit(rankLbl, (rankX, rankY))

    # Score text
    # TODO: Actual scores (and therefore not part of init routine)
    score = random.randint(5000, 90000)
    scoreLbl = largeFont.render(str(score), 1, SCORE_TEXT_COLOR)
    scoreX = x + lbMargin + (lbMargin / 2)
    scoreY = lbMargin
    screen.blit(scoreLbl, (scoreX, scoreY))

# Players section (boxes for player info)
# TODO: Dynamic
plMargin = 10
plMaxWidth = 0.50 # 50% of the screen
plStartX = plMargin
plX = plStartX
plY = lbMargin + lbMargin + lbHeight
availableWidth = (float)(width - plMargin) + 3.0
availabeHeight = (float)(height - plY - (plMargin * 2))
perRow = math.floor(plMaxWidth * players)
rows = players / (float)(perRow)
plWidth = (availableWidth - (plMargin * perRow) - (plMargin / 2)) / perRow
plHeight = (availabeHeight - (plMargin * rows) - (plMargin * 2)) / rows
playersDisplayed = 0
rowSize = 0
# TODO: Move this function?
def center_text(label, width):
    area = label.get_rect()
    remainder = width - area.width
    return math.floor(remainder / 2.0)
def center_text_y(label, height):
    area = label.get_rect()
    remainder = height - area.height
    return math.floor(remainder / 2.0)
while(playersDisplayed < players):
    # Backdrop for box
    rect = (plX, plY, plWidth, plHeight)
    AAfilledRoundedRect(screen, rect, WIDGET_BACKGROUND_COLOR2, 0.05)

    playerLabel = regularFont.render("Player " + str(playersDisplayed + 1), 1, MUTED_TEXT_COLOR)
    screen.blit(playerLabel, (plX + plMargin, plY + plMargin))

    # BEGIN HARDCODED STATES
    # States:
    # P1 = Not joined
    # P2 = Joined, waiting
    # P3 = Playing
    # P4 = Game Over
    subMessage = None
    scoreLbl = None
    if(playersDisplayed == 0):
        subMessage = regularFont.render("Press the center button to join", 1, PRIMARY_TEXT_COLOR)
    elif(playersDisplayed == 1):
        scoreLbl = extraLargeFont.render("Welcome!", 1, WHITE)
        subMessage = regularFont.render("Game starts in 5 seconds", 1, PRIMARY_TEXT_COLOR)
    elif(playersDisplayed == 2):
        subMessage = regularFont.render("Round 41", 1, PRIMARY_TEXT_COLOR)
        scoreLbl = extraLargeFont.render("112233", 1, SCORE_TEXT_COLOR)
    elif(playersDisplayed == 3):
        subMessage = regularFont.render("Final score: 9176 (98th/150)", 1, SCORE_TEXT_COLOR)
        scoreLbl = extraLargeFont.render("YOU WON!", 1, WINNER_TEXT_COLOR)
    if(subMessage is not None):
        x = plX + center_text(subMessage, plWidth)
        y = (plY + plHeight) - subMessage.get_rect().height - plMargin
        screen.blit(subMessage, (x, y))
    if(scoreLbl is not None):
        x = plX + center_text(scoreLbl, plWidth)
        y = plY + center_text_y(scoreLbl, plHeight)
        screen.blit(scoreLbl, (x, y))
    # END HARDCODED STATES

    # Control logic
    rowSize += 1
    plX += plWidth + plMargin
    if(rowSize >= perRow):
        plX = plStartX
        plY += plMargin + plHeight
        rowSize = 0
    playersDisplayed += 1


pygame.display.flip()
# ------ END SCREEN INIT ------

fps = 20 # Should be plenty for us

loopTime = fps / 60.0
print("Game loop starting at " + str(fps) + " fps (" + str(loopTime) + "s delay)...")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Close requested")
            running = False # Just in case sys.exit() doesn't work
            print("Shutting down display...")
            pygame.display.quit()
            print("Shutting down engine...")
            pygame.quit()
            print("Exiting...")
            sys.exit()
    #screen.fill((0, 255, 0))
    #pygame.display.flip()
    sleep(loopTime)
