from gpiozero import Button, LED
from time import sleep

buttons = [
  # Player 1
  Button(2),
  Button(3),
  Button(4),
  Button(17),
  Button(27),

  # Player 2
  Button(14),
  Button(15),
  Button(18),
  Button(23),
  Button(25),  # not 24 because the screw went missing
]

leds = [
  # Player 1
  LED(22),
  LED(10),
  LED(9),
  LED(11),
  LED(0),

  # Player 2
  LED(1),
  LED(12),
  LED(16),
  LED(20),
  LED(21),
]

def set_press(i):
  buttons[i].when_pressed = lambda: do_press(i, True)
  buttons[i].when_released = lambda: do_press(i, False)

def do_press(i: int, on: bool):
  leds[i].value = on
  print(f"Button {i} pressed? {on}")

for i in range(len(buttons)):
  set_press(i)

print("Sleeping forever - Ctrl+C to exit")
sleep(99999999)