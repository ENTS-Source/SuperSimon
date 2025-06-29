from abc import ABC, abstractmethod

class GameModeGame(ABC):
  @abstractmethod
  def get_sequence(self, player: int) -> list[int]:
    '''Increments the player's sequence and returns all the buttons the player needs to press.
    '''
    pass

  @abstractmethod
  def is_next(self, player: int, button: int) -> bool:
    '''Checks if what the player pressed was correct for the sequence.
    '''
    pass

  @abstractmethod
  def player_died(self, player: int) -> None:
    '''Records that the player failed the game.
    '''
    pass