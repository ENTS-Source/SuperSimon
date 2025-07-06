from consts import BUTTON_DEBOUNCE

from gpiozero import Button, LED
import time

class LocalButton:
  def __init__(self, btn: Button):
    self._btn = btn
    self._activate_time = time.time()
    self._state = False
    self.press_event = 1

  def is_newly_pressed(self):
    event = self.press_event
    return self.is_pressed() and event != self.press_event

  def is_pressed(self):
    if (time.time() - self._activate_time) <= BUTTON_DEBOUNCE:
      return self._state
    if self._btn.is_pressed:
      self._activate_time = time.time()
      self._state = True
    else:
      self._state = False
      self.press_event *= -1
    return self._state


buttons = [
  LocalButton(Button(2)),
  LocalButton(Button(3)),
  LocalButton(Button(4)),
  LocalButton(Button(17)),
  LocalButton(Button(27)),
]

lights = [
  LED(22),
  LED(10),
  LED(9),
  LED(11),
  LED(0),
]

def is_newly_pressed(player: int, button: int) -> bool:
  if player == 1:
    return True  # TODO: Remove

  btn = buttons[(player * 5) + button]
  return btn.is_newly_pressed()

def set_led(player: int, button: int, on: bool):
  if player == 1:
    return  # TODO: Remove

  led = lights[(player * 5) + button]
  led.value = on
