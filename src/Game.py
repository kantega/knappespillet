from abc import ABC, abstractmethod

from Board import Board


class ExitCommand:
    def __init__(self, score: int | None):
        self.score = score


class GameInfo:
    def __init__(self, name: str, description: str, creator: str):
        self.name = name
        self.description = description
        self.creator = creator


class Game(ABC):
    @abstractmethod
    def info(self) -> GameInfo:
        """
        Return information about this game, to be used in the menu.
        """
        pass

    @abstractmethod
    def update(self, pressed_buttons: set[tuple[int, int]]) -> list:
        """
        Update the internal state and return a list of commands.
        This method is called every frame, just before the render() method.
        """
        pass

    @abstractmethod
    def render(self, pressed_buttons: set[tuple[int, int]]) -> Board:
        """
        Derive a board representation from the internal state.
        This method is called every frame, just after the update() method.
        """
        pass
