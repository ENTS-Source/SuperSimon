from consts import GS_INTRO, GS_PLAYING_SHOW, GS_PLAYING_TELL, GS_PLAYING_FINISH, BUTTON_IDLE_TIME, BUTTON_SHOW_TIME
from pgzero.clock import clock
from functools import partial

class Player:
  def __init__(self, index):
    self.state = GS_INTRO
    self._index = index
    self._game = None
    self._button_functions = []

  def try_record_button_down(self, button):
    if self.state != GS_PLAYING_TELL:
      return  # not in a game

    self._button_functions(button)

    if self._game.is_next(self._index, button):
      self._show()
    else:
      self._game.player_died(self._index)
      self.state = GS_PLAYING_FINISH

    return

  def try_record_button_up(self, button):
    return

  def start_game(self, game, button_functions):
    self._game = game
    self._button_functions = button_functions
    self._show()

  def _show(self):
    print("Debug: -> show ", self._index)
    self.state = GS_PLAYING_SHOW
    self._sequence = self._game.get_sequence(self._index)
    print("Debug: player sequence ", self._index, self._sequence)
    clock.schedule(self._show_sequence, BUTTON_IDLE_TIME)

  def _go_to_tell(self):
      print("Debug: -> tell ", self._index)
      self.state = GS_PLAYING_TELL

  def _show_sequence(self):
    sequence = self._sequence
    print("Debug: show sequence ", self._index)

    for i in range(len(sequence)):
      print("Debug: sequence ", self._index, i, sequence[i])
      clock.schedule_oschedulence(lambda i=i: self._button_functions[sequence[i]](True), i * (BUTTON_SHOW_TIME + BUTTON_IDLE_TIME))
      clock.schedule(lambda i=i: self._button_functions[sequence[i]](False), (i * (BUTTON_SHOW_TIME + BUTTON_IDLE_TIME)) + BUTTON_SHOW_TIME)

    clock.schedule(self._go_to_tell, (len(sequence) - 1) * (BUTTON_SHOW_TIME + BUTTON_IDLE_TIME) + BUTTON_SHOW_TIME)