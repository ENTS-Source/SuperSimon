import pygame
import db

# ---- SuperSimon Constants ----

GS_INTRO = 1
GS_STARTING = 2
GS_PLAYING = 3
GS_FINISH = 4

GM_NORMAL = 1
GM_CHASE = 2
GM_MUSIC = 3
GAME_MODES = [GM_NORMAL, GM_CHASE, GM_MUSIC]  # used for cycling

# ---- SuperSimon Variables ----

CURRENT_GAME_MODE = GM_NORMAL
CURRENT_GAME_STATE = GS_INTRO

# ---- Pygame Zero Setup/Game Start ----

TITLE = "SuperSimon 2.0"
WIDTH = 1920
HEIGHT = 1080

PADDING = 20
LOGO_R = 150 + PADDING

db.init()

def draw():
  window_setup()  # internally handles duplicate calls

  # Base setup
  screen.clear()
  screen.fill((0, 0, 128))
  screen.blit('logo', (0, 10))
  screen.draw.text("ENTS SuperSimon 2.0", (LOGO_R, PADDING), fontsize=100, shadow=(2, 2), scolor="#202020", color="#FFFFFF")

  # Render game objects
  draw_game_mode()
  draw_game_state()

  # Draw assets
  # TODO

def update():
  # TODO
  pass

def on_key_down(key):
  if key == keys.M:
    global CURRENT_GAME_MODE
    if CURRENT_GAME_STATE != GS_INTRO:
      return
    idx = GAME_MODES.index(CURRENT_GAME_MODE)
    idx += 1
    if idx >= len(GAME_MODES):
      idx = 0
    CURRENT_GAME_MODE = GAME_MODES[idx]

DID_WINDOW_SETUP = False
def window_setup():
  global DID_WINDOW_SETUP
  if DID_WINDOW_SETUP:
    return
  screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
  pygame.mouse.set_visible(False)
  DID_WINDOW_SETUP = True

def draw_game_mode():
  gm_text = "UNKNOWN"
  if CURRENT_GAME_MODE == GM_NORMAL:
    gm_text = "Normal"
  elif CURRENT_GAME_MODE == GM_CHASE:
    gm_text = "Chase"
  elif CURRENT_GAME_MODE == GM_MUSIC:
    gm_text = "Music"

  screen.draw.text("Game mode: " + gm_text, (LOGO_R, 75 + PADDING), fontsize=30, color="orange")

def draw_game_state():
  # TODO
  pass
