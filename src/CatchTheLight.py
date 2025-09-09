from random import randint

from Board import Board
from Game import Game, ExitCommand, GameInfo
from Light import WHITE, MAGENTA


class CatchTheLight(Game):
    def __init__(self):
        self.time = 0
        self.inactive_time = 0
        self.score = 0
        self.active_button = (randint(0, 4), randint(0, 6))

    def info(self) -> GameInfo:
        return GameInfo(
            name="CatchTheLight",
            description="Rush to catch the light as many times as you can before the time runs out",
            creator="Magnus K",
        )

    def update(self, pressed_buttons: set[tuple[int, int]]) -> list:
        if self.active_button in pressed_buttons:
            self.score += 1
            self.inactive_time = 0
            self.active_button = (randint(0, 4), randint(0, 6))
        else:
            self.inactive_time += 1
            if self.inactive_time > 5 * 30:
                return [ExitCommand(score=self.score)]

        if self.time > 30 * 30:
            return [ExitCommand(score=self.score)]

        self.time += 1
        return []

    def render(self, pressed_buttons: set[tuple[int, int]]) -> Board:
        board = Board()

        board.buttons[self.active_button].set_all_lights(MAGENTA)

        for (row, col) in pressed_buttons:
            board.buttons[(row, col)].set_all_lights(WHITE)

        return board
