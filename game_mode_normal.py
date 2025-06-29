import random
import db

from game_mode_game import GameModeGame

class GameModeNormal(GameModeGame):
  _sequence: list[int] = []
  _player_positions = [0, 0]

  def __init__(self):
    print("Debug: created normal game")

  def get_sequence(self, player):
    self._player_positions[player] += 1
    pos = self._player_positions[player]
    if pos >= len(self._sequence):
      print("Debug: extending sequence")
      self._sequence.append(random.randint(0, 4))
      print("Debug: total sequence: ", self._sequence)
    return self._sequence[:pos]

  def is_next(self, player, button):
    return self._sequence[self._player_positions[player]] == button

  def player_died(self, player):
    db.save_score('normal', self._player_positions[player])
    # TODO: Play sound
