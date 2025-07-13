import pygame
import db

from consts import GM_NORMAL, GM_CHASE, GM_MUSIC, GS_PLAYING_NONSPECIFIC, GS_INTRO, GAME_MODES, GS_PLAYING_FINISH, GS_STARTING, GS_PLAYING_END, BTN_ON_NO_SOUND, BTN_ON
from player import Player
from game_mode_normal import GameModeNormal
from gpio import set_led, is_newly_pressed

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
  lambda state: set_button_state(0, 0, state),
  lambda state: set_button_state(0, 1, state),
  lambda state: set_button_state(0, 2, state),
  lambda state: set_button_state(0, 3, state),
  lambda state: set_button_state(0, 4, state),

  # Player 2
  lambda state: set_button_state(1, 0, state),
  lambda state: set_button_state(1, 1, state),
  lambda state: set_button_state(1, 2, state),
  lambda state: set_button_state(1, 3, state),
  lambda state: set_button_state(1, 4, state),
]

def set_button_state(player, button, state):
  set_led(player, button, state == BTN_ON or state == BTN_ON_NO_SOUND)
  if state == BTN_ON:
    BUTTON_SOUNDS[button].play()
  else:
    BUTTON_SOUNDS[button].stop()

# ---- Pygame Zero Setup/Game Start ----

TITLE = "SuperSimon 2.0"
WIDTH = 1080
HEIGHT = 720

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

  # Draw assets
  # TODO

def update():
  check_all_dead()
  check_all_buttons()

# ---- game functions ----

def check_all_dead():
  for player in PLAYERS:
    if player.state != GS_PLAYING_FINISH:
      return
  print("Debug: all players dead -> end_game soon")
  set_global_game_state(GS_PLAYING_END)
  clock.schedule_unique(end_game, 5.0)

def end_game():
  print("Debug: -> intro")
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

def check_all_buttons():
  # TODO: Check mode button
  for player in range(2):
    for button in range(5):
      if is_newly_pressed(player, button):
        if get_global_game_state() == GS_INTRO:
          begin_countdown()
          return
        elif get_global_game_state() == GS_PLAYING_NONSPECIFIC:
          record_player_button(player, button)

def record_player_button(player, button):
  if CURRENT_GAME_MODE == GM_MUSIC:
    play_tone((player * 5) + button)
  else:
    PLAYERS[player].check_button(button)

def begin_countdown():
  print("Debug: countdown")
  set_global_game_state(GS_STARTING)
  sounds.countdown.play()
  clock.schedule_unique(start_game, 3.1)  # 3 seconds plus a bit for lag

def start_game():
  print("Debug: start game")
  if CURRENT_GAME_MODE == GM_NORMAL:
    game = GameModeNormal(sounds.game_over)
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
    draw_normal_game_state()
  elif CURRENT_GAME_MODE == GM_CHASE:
    gm_text = "Chase"
  elif CURRENT_GAME_MODE == GM_MUSIC:
    gm_text = "Music"

  screen.draw.text("Game mode: " + gm_text, (LOGO_R, 75 + PADDING), fontsize=30, color="orange")

def draw_normal_game_state():
  y_start = 75 + PADDING + (PADDING * 4)
  if get_global_game_state() == GS_INTRO:
    r = Rect((PADDING, y_start), (WIDTH - (PADDING * 2), HEIGHT - y_start - PADDING))
    screen.draw.filled_rect(r, (191, 66, 245))

# ---- pygame setup ----

DID_WINDOW_SETUP = False
def window_setup():
  global DID_WINDOW_SETUP
  if DID_WINDOW_SETUP:
    return
  screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
  pygame.mouse.set_visible(False)
  DID_WINDOW_SETUP = True