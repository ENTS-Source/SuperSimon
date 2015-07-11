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
screenSize = sWidth, sHeight = displayInfo.current_w, displayInfo.current_h

# Creation of the screen object
print("Setting up graphical interface...")
screen = pygame.display.set_mode(screenSize, 0, 32)
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
from renderScreen import render
from gameManager import GameManager
manager = GameManager(game)
fps = 20

# State variables for game stuffs
from communication.utils import *
lastTick = millis()

# Start game loop
print("Starting game loop...")
gameRunning = True
while(gameRunning):
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
    render(screen, manager)
    now = millis()
    if now - lastTick >= 500:
        manager.tick(now - lastTick)
        lastTick = now
    sleep(fps / 60.0)
