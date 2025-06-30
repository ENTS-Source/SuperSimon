import pygame
import db

from consts import GM_NORMAL, GM_CHASE, GM_MUSIC, GS_PLAYING_NONSPECIFIC, GS_INTRO, GAME_MODES, GS_PLAYING_FINISH, GS_STARTING
from player import Player
from game_mode_normal import GameModeNormal

# ---- SuperSimon Variables ----

CURRENT_GAME_MODE = GM_NORMAL

PLAYERS = [
  Player(0),
  Player(1),
]

def set_global_game_state(new_state):
  for player in PLAYERS:
    player.state = new_state

def get_global_game_state():
  state = PLAYERS[0].state
  return min(GS_PLAYING_NONSPECIFIC, state)

ACTIVE_MUSIC = {}  # used in music game mode
MUSIC_SOUNDS = [
  sounds.ddr_0,
  sounds.ddr_1,
  sounds.ddr_2,
  sounds.ddr_3,
  sounds.ddr_4,
  sounds.ddr_5,
  sounds.ddr_6,
  sounds.ddr_7,
  sounds.ddr_8,
  sounds.ddr_9,
]

BUTTON_SOUNDS = [
  sounds.red,     # top
  sounds.blue,    # left
  sounds.white,   # center
  sounds.green,   # right
  sounds.yellow,  # bottom
]

BUTTON_FUNCTIONS = [
  # Player 1
  lambda show: set_button_state(0, 0, show),
  lambda show: set_button_state(0, 1, show),
  lambda show: set_button_state(0, 2, show),
  lambda show: set_button_state(0, 3, show),
  lambda show: set_button_state(0, 4, show),

  # Player 2
  lambda show: set_button_state(1, 0, show),
  lambda show: set_button_state(1, 1, show),
  lambda show: set_button_state(1, 2, show),
  lambda show: set_button_state(1, 3, show),
  lambda show: set_button_state(1, 4, show),
]

def set_button_state(player, button, show):
  if show:
    BUTTON_SOUNDS[button].play()
    # TODO: Button LED
  else:
    BUTTON_SOUNDS[button].stop()
    # TODO: Button LED

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
  check_all_dead()

# ---- game functions ----

def check_all_dead():
  for player in PLAYERS:
    if player.state != GS_PLAYING_FINISH:
      return
  print("Debug: all players dead -> end_game soon")
  clock.schedule_unique(end_game, 5.0)

def end_game():
  print("Debug: Game end -> INTRO")
  set_global_game_state(GS_INTRO)

def try_game_mode_cycle():
  global CURRENT_GAME_MODE

  if get_global_game_state() != GS_INTRO:
      return  # not allowed to switch right now

  idx = (GAME_MODES.index(CURRENT_GAME_MODE) + 1) % len(GAME_MODES)
  CURRENT_GAME_MODE = GAME_MODES[idx]

  # Clean up after previous game modes
  music.stop()
  for i in range(10):
    stop_tone(i)

  # Enable things depending on game mode
  if CURRENT_GAME_MODE == GM_MUSIC:
    music.play('backing_track')
    music.set_volume(0.45)

def try_button_press(player, button):
    if get_global_game_state() == GS_INTRO:
      begin_countdown()
    elif get_global_game_state() == GS_PLAYING_NONSPECIFIC:
      record_player_button(player, button)

def record_player_button(player, button):
  if CURRENT_GAME_MODE == GM_MUSIC:
    play_tone((player * 5) + button)
  elif get_global_game_state() == GS_INTRO:
    begin_countdown()
  else:
    PLAYERS[player].try_record_button_down(button)

def try_button_release(player, button):
  PLAYERS[player].try_record_button_up(button)

def begin_countdown():
  print("Debug: countdown")
  set_global_game_state(GS_STARTING)
  sounds.countdown.play()
  clock.schedule_unique(start_game, 3.1)  # 3 seconds plus a bit for lag

def start_game():
  print("Debug: start game")
  if CURRENT_GAME_MODE == GM_NORMAL:
    game = GameModeNormal()
    for i in range(len(PLAYERS)):
      player = PLAYERS[i]
      player.start_game(game, BUTTON_FUNCTIONS[i*5:(i*5)+5])

# ---- music mode functions ----

def play_tone(tone_id):
  print("Debug: play tone ", tone_id)
  if tone_id not in ACTIVE_MUSIC:
    ACTIVE_MUSIC[tone_id] = MUSIC_SOUNDS[tone_id]
    ACTIVE_MUSIC[tone_id].play(-1)  # loop forever

def stop_tone(tone_id):
  print("Debug: stop tone ", tone_id)
  if tone_id in ACTIVE_MUSIC:
    ACTIVE_MUSIC[tone_id].stop()
    del ACTIVE_MUSIC[tone_id]

# ---- game render ----

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

# ---- pygame keyboard interface ----

def on_key_down(key):
  if key == keys.M:
    try_game_mode_cycle()

  key_char = key.name[-1]
  if key_char.isdigit():
    num = int(key_char)
    if num == 0:
      num = 10
    player = 0 if num <= 5 else 1
    button = (num - 1) % 5
    try_button_press(player, button)

def on_key_up(key):
  key_char = key.name[-1]
  if key_char.isdigit():
    num = int(key_char)
    if num == 0:
      num = 10
    player = 0 if num <= 5 else 1
    button = (num - 1) % 5
    try_button_press(player, button)

# ---- pygame setup ----

DID_WINDOW_SETUP = False
def window_setup():
  global DID_WINDOW_SETUP
  if DID_WINDOW_SETUP:
    return
  screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
  pygame.mouse.set_visible(False)
  DID_WINDOW_SETUP = True