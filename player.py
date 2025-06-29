from consts import GS_INTRO, GS_PLAYING_SHOW, GS_PLAYING_TELL, GS_PLAYING_FINISH, BUTTON_IDLE_TIME, BUTTON_SHOW_TIME
from pgzero.clock import clock

class Player:
  state = GS_INTRO

  _index = 0
  _game = None
  _button_functions = []

  def __init__(self, index):
    self._index = index

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
    sequence = self._game.get_sequence(self._index)
    print("Debug: player sequence ", self._index, sequence)
    clock.schedule_unique(lambda: self._show_sequence(sequence), BUTTON_IDLE_TIME)

  def _show_sequence(self, sequence):
    for i in range(len(sequence)):
      print("Debug: sequence ", self._index, i, sequence[i])
      clock.schedule_unique(lambda i=i: self._button_functions[sequence[i]](True), i * (BUTTON_SHOW_TIME + BUTTON_IDLE_TIME))
      clock.schedule_unique(lambda i=i: self._button_functions[sequence[i]](False), (i * (BUTTON_SHOW_TIME + BUTTON_IDLE_TIME)) + BUTTON_SHOW_TIME)
    clock.schedule_unique(self._set_state_to_tell, (len(sequence) - 1) * (BUTTON_SHOW_TIME + BUTTON_IDLE_TIME) + BUTTON_SHOW_TIME)

  def _set_state_to_tell(self):
    print("Debug: -> tell ", self._index)
    self.state = GS_PLAYING_TELL
