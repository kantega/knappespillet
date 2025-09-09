from random import randint

from Board import Board
from Game import Game, ExitCommand, GameInfo
from Light import Light, GREEN, WHITE
from utils import clamp


class TapTendrils(Game):

    def __init__(self):
        self.state = 'playing'
        self.time = 0
        self.score = 0
        self.tendrils = [Tendril(i) for i in range(7)]
        self.lives = [True for _ in range(7)]

    def info(self) -> GameInfo:
        return GameInfo(
            name="TapTendrils",
            description="Tap the tendrils to prevent them from reaching the bottom. You have a guard in each column.",
            creator="Per Thomas",
        )

    def update(self, pressed_buttons: set[tuple[int, int]]) -> list:
        if self.state == 'playing':
            # Update tendrils
            for tendril in self.tendrils:
                tendril.update()

            # Increase grow rate over time
            grow_period = max(0, 20 - self.time // 60)

            # Grow tendrils
            if self.time % grow_period == 0:
                n = randint(0, 6)
                for i in range(7):
                    k = (n + i + 3) % 7
                    if self.tendrils[k].size == 0:
                        self.tendrils[k].growing = True
                        break

            # Tap tendrils to stop growth
            for row in range(5):
                for col in range(7):
                    for tendril in self.tendrils:
                        if tendril.get_lights(row, col) is not None and (row, col) in pressed_buttons:
                            tendril.growing = False

            # Tendrils eat lives and cause failure
            for i in range(7):
                if self.tendrils[i].is_deadly():
                    if self.lives[i]:
                        self.lives[i] = False
                        self.tendrils[i].growing = False
                    else:
                        self.state = 'score'
                        self.score = self.time // 30
                        self.time = 0
                        return []

        elif self.state == 'score':
            if self.time >= 30 * 2:
                return [ExitCommand(score=self.score)]

        self.time += 1
        return []

    def render(self, pressed_buttons: set[tuple[int, int]]) -> Board:
        board = Board()

        if self.state == 'playing':
            if self.time < 30:
                life_intensity = self.time / 30
            else:
                life_intensity = 1

            for row in range(5):
                for col in range(7):
                    button = board.buttons[(row, col)]

                    # Lives
                    if self.lives[col] and row == 4:
                        button.set_all_lights(GREEN * life_intensity)

                    # Tendrils
                    for tendril in self.tendrils:
                        lights = tendril.get_lights(row, col)
                        if lights is not None:
                            for i in range(12):
                                button.lights[i] = button.lights[i] + lights[i]

        if self.state == 'score':
            if self.time < 30:
                play_intensity = 1
            elif self.time < 60:
                play_intensity = 1 - (self.time - 30) / 30
            else:
                play_intensity = 0

            for row in range(5):
                for col in range(7):
                    button = board.buttons[(row, col)]

                    # Lives
                    if self.lives[col] and row == 4:
                        button.set_all_lights(GREEN * play_intensity)

                    # Tendrils
                    for tendril in self.tendrils:
                        lights = tendril.get_lights(row, col)
                        if lights is not None:
                            for i in range(12):
                                button.lights[i] = (button.lights[i] + lights[i]) * play_intensity

        for (row, col) in pressed_buttons:
            board.buttons[(row, col)].set_all_lights(WHITE)

        return board


class Tendril:
    def __init__(self, col):
        self.col = col
        self.size = 0
        self.growing = False

    def update(self):
        if self.growing:
            self.size = clamp(0, self.size + 1, 5 * 6)
        else:
            self.size = clamp(0, self.size - 2, 5 * 6)

    def is_deadly(self) -> bool:
        return self.size >= 5 * 6

    def get_light(self) -> Light:
        if self.growing:
            return Light(1, 0, 1)
        else:
            return Light(0.66, 0.33, 0.66)

    def get_lights(self, row, col) -> list[Light] | None:
        if self.size < row * 6 or self.col != col:
            return None
        if self.growing:
            return self.light_pattern(self.size - row * 6)
        else:
            return self.light_pattern(self.size - row * 6)

    def light_pattern(self, n):
        half = [self.get_light() if i < n else Light(0, 0, 0) for i in range(6)]
        return half + half[::-1]
