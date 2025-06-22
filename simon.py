import db

TITLE = "SuperSimon 2.0"
WIDTH = 800
HEIGHT = 600

db.init()

def draw():
  make_fullscreen()

def update():
  # TODO
  pass

# ------------------------------------------------------------------------------

is_fullscreen = False
def make_fullscreen():
  global is_fullscreen
  if is_fullscreen:
    return
  screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
  is_fullscreen = True
