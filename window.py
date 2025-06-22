import pygame

is_fullscreen = False
def make_fullscreen():
  global is_fullscreen
  if is_fullscreen:
    return
  screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
  is_fullscreen = True
