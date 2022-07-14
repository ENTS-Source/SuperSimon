# ENTS SuperSimon Raspberry Pi
# ------------------------------------------------------------------------------
# Master game controller for game pad coordination and functionality.
#import RPi.GPIO as GPIO
import subprocess

# Start by spinning up the configuration
from config import Configuration

config = Configuration()

# print("Setting up buttons")
# GPIO.setmode(GPIO.BOARD);
# GPIO.setup(config.buttons.btn1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(config.buttons.btn2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

pygame.mouse.set_visible(False)

# Start loading the actual game
print("Starting communications...")
from communication.simon import SuperSimon

game = SuperSimon(config.protocol)

# Begin score tracking
print("Starting score tracker...")
from scoreTracker import ScoreTracker

scoreTracker = ScoreTracker()

# Now we can start up the display with a disover sequence
print("Discovering initial clients...")
game.discover_clients()

# Prepare for game loop
import sys
from time import sleep
from screenRenderer import ScreenRenderer
from gameManager import GameManager

manager = GameManager(game, scoreTracker)
renderer = ScreenRenderer(screen, manager)

# State variables for game stuffs
from communication.utils import *

lastTick = millis()

# Start game loop
print("Starting game loop...")
gameRunning = True
maxRenderTime = 0
timesOver1s = 0

def closeAll():
    print("Close requested")
    gameRunning = False
    print("Shutting down display...")
    pygame.display.quit()
    print("Shutting down engine...")
    pygame.quit()
    print("Shutting down communication...")
    game.exit()
    print("Shutting down score tracker...")
    scoreTracker.close()
    print("Exiting...")
    sys.exit()

forceExit = False
while gameRunning:
    start = millis()
    if forceExit:
        closeAll()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            closeAll()
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
    # print("Took " + str(end - start) + "ms (max (<1000ms) = " + str(maxRenderTime) + "ms, times over 1s = " + str(timesOver1s) + ") to do game loop. Sleeping for 100ms...")
    sleep(0.1)

    # check for shutdown buttons
    # if(GPIO.input(config.buttons.btn1_pin) == 1):
    #     print("Shutdown button pressed, forcing exit on next loop")
    #     forceExit = True
