import random
import db

from game_mode_game import GameModeGame

class GameModeNormal(GameModeGame):
  sequence: list[int] = []
  player_positions = [-1, -1]  # first round increments to zero

  def __init__(self):
    print("Debug: created normal game")

  def get_sequence(self, player):
    self.player_positions[player] += 1
    pos = self.player_positions[player]
    if pos >= len(self.sequence):
      print("Debug: extending sequence")
      self.sequence.append(random.randint(0, 4))
    return self.sequence[:pos + 1]

  def is_next(self, player, button):
    return self.sequence[self.player_positions[player]] == button

  def player_died(self, player):
    db.save_score('normal', self.player_positions[player])
    # TODO: Play sound
