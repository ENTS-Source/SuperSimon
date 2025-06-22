import pygame

is_fullscreen = False
def make_fullscreen(width, height):
  global is_fullscreen
  if is_fullscreen:
    return
  screen.surface = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
  is_fullscreen = True
