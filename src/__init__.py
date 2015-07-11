# ENTS SuperSimon Raspberry Pi
# ------------------------------------------------------------------------------
# Master game controller for game pad coordination and functionality.

# Start by spinning up the configuration
from config import Configuration
config = Configuration()

print("Game fullscreen = " + str(config.game.fullscreen))
print("Serial device = " + config.protocol.device)
print("Discover maximum devices = " + str(config.protocol.discoverMaximum))

# Now we can start by setting up pygame
print("Preparing game setup...")
import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0" # Starts window at (0, 0)
pygame.init()
displayInfo = pygame.display.Info()
offset = 0
# Just so that the bottom of the screen can be seen
if not config.game.fullscreen:
    offset = 100
screenSize = sWidth, sHeight = displayInfo.current_w, displayInfo.current_h - offset

# Creation of the screen object
print("Setting up graphical interface...")
screen = pygame.display.set_mode(screenSize, pygame.DOUBLEBUF, 32)
screen.set_alpha(None)
pygame.display.set_caption("ENTS SuperSimon Game")
if config.game.fullscreen:
    pygame.display.toggle_fullscreen()

# Start loading the actual game
print("Starting communications...")
from communication.simon import SuperSimon
game = SuperSimon(config.protocol)

# Now we can start up the display with a disover sequence
print("Discovering initial clients...")
game.discoverClients()

# Prepare for game loop
import sys
from time import sleep
from screenRenderer import ScreenRenderer
from gameManager import GameManager
manager = GameManager(game)
renderer = ScreenRenderer(screen, manager)

# State variables for game stuffs
from communication.utils import *
lastTick = millis()

# Start game loop
print("Starting game loop...")
gameRunning = True
maxRenderTime = 0
timesOver1s = 0
while(gameRunning):
    start = millis()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Close requested")
            gameRunning = False
            print("Shutting down display...")
            pygame.display.quit()
            print("Shutting down engine...")
            pygame.quit()
            print("Shutting down communication...")
            game.exit()
            print("Exiting...")
            sys.exit()
    renderer.tick()
    now = millis()
    if now - lastTick >= 200:
        manager.tick(now - lastTick)
        lastTick = now
    end = millis()
    rtime = end - start
    if rtime > maxRenderTime:
        if rtime > 1000:
            timesOver1s += 1
        else:
            maxRenderTime = rtime
        print("!! NEW MAXIMUM RENDER TIME: " + str(maxRenderTime) + "ms")
    print("Took " + str(end - start) + "ms (max (<1000ms) = " + str(maxRenderTime) + "ms, times over 1s = " + str(timesOver1s) + ") to do game loop. Sleeping for 100ms...")
    sleep(0.1)
