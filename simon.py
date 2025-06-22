import pygame
import db

# ---- SuperSimon Constants ----

GS_INTRO = 1
GS_STARTING = 2
GS_PLAYING_SHOW = 3
GS_PLAYING_TELL = 4
GS_FINISH = 5

GM_NORMAL = 1
GM_CHASE = 2
GM_MUSIC = 3
GAME_MODES = [GM_NORMAL, GM_CHASE, GM_MUSIC]  # used for cycling

# ---- SuperSimon Variables ----

CURRENT_GAME_MODE = GM_NORMAL
CURRENT_GAME_STATE = GS_INTRO

ACTIVE_MUSIC = {}  # used in music game mode
MUSIC_SOUNDS = [
  sounds.c4,
  sounds.d4,
  sounds.e4,
  sounds.g4,
  sounds.a4,
  sounds.c5,
  sounds.d5,
  sounds.e5,
  sounds.g5,
  sounds.a5,
]

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
    stop_all_tones()

  key_char = key.name[-1]
  if key_char.isdigit():
    num = int(key_char)
    if CURRENT_GAME_MODE == GM_MUSIC:
      play_tone(num)
    elif CURRENT_GAME_STATE == GS_INTRO:
      start_game()

def on_key_up(key):
  key_char = key.name[-1]
  if key_char.isdigit():
    num = int(key_char)
    if CURRENT_GAME_MODE == GM_MUSIC:
      stop_tone(num)

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

def play_tone(tone_id):
  if tone_id not in ACTIVE_MUSIC:
    ACTIVE_MUSIC[tone_id] = MUSIC_SOUNDS[tone_id]
    ACTIVE_MUSIC[tone_id].play(-1)  # loop forever

def stop_tone(tone_id):
  if tone_id in ACTIVE_MUSIC:
    ACTIVE_MUSIC[tone_id].stop()
    del ACTIVE_MUSIC[tone_id]

def stop_all_tones():
  for i in range(10):
    stop_tone(i)

def start_game():
  print("Start game")
