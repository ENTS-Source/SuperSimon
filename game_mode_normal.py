import random
import db

from game_mode_game import GameModeGame

class GameModeNormal(GameModeGame):
  def __init__(self, death_sound):
    print("Debug: created normal game")
    self._sequence: list[int] = []
    self._player_positions = [0, 0]
    self._player_tell_positions = [0, 0]
    self._death_sound = death_sound

  def get_sequence(self, player):
    self._player_positions[player] += 1
    pos = self._player_positions[player]
    if pos >= len(self._sequence):
      print("Debug: extending sequence")
      self._sequence.append(random.randint(0, 4))
      print("Debug: total sequence: ", self._sequence)
    self._player_tell_positions[player] = 0
    return self._sequence[:pos]

  def is_next(self, player, button):
    pos = self._player_tell_positions[player]
    self._player_tell_positions[player] += 1
    print("Debug: CHECK ", player, button, pos, self._sequence[pos])
    return self._sequence[pos] == button

  def can_advance(self, player):
    return self._player_tell_positions[player] >= self._player_positions[player]

  def player_died(self, player):
    db.save_score('normal', self._player_positions[player])
    self._death_sound.play()

  def get_sequence_len(self, player):
    return self._player_positions[player]
