from random import randint

from Board import Board
from Game import Game, GameInfo, ExitCommand
from Light import Light, WHITE, CYAN, MAGENTA, YELLOW, RED
from utils import rotate


class TapDance(Game):
    def __init__(self):
        self.state = 'playing'
        self.time = 0
        self.score = 0
        self.waves = []
        self.next = ['up', 'down', 'right', 'left']
        self.fail_buttons = []

    def info(self) -> GameInfo:
        return GameInfo(
            name="TapDance",
            description="Keep at least one button pushed while avoiding the lights",
            image_path="src/images/tux.png",
            creator="Per Thomas",
        )

    def update(self, pressed_buttons: set[tuple[int, int]]) -> list:
        if self.state == 'playing':

            # Must hold at least one button
            if len(pressed_buttons) == 0:
                self.state = 'score'
                self.score = self.time // 30
                self.time = 0
                return []

            # Must not touch wave
            for row in range(5):
                for col in range(7):
                    for wave in self.waves:
                        if wave.is_deadly(row, col) and (row, col) in pressed_buttons:
                            self.fail_buttons.append((row, col))

            if len(self.fail_buttons) > 0:
                self.state = 'score'
                self.score = self.time // 30
                self.time = 0
                return []

            # Update all waves and keep relevant ones
            if self.time % 2 == 0:
                self.waves = [wave for wave in self.waves if wave.update()]

            spawn_period = max(1, 3 - self.time // (30 * 20))

            # Spawn new waves
            if self.time % (12 * 2 * spawn_period) == 0:
                self.next = rotate(self.next, randint(1, 3))
                self.waves.append(Wave(self.next[0]))

        elif self.state == 'score':
            if self.time >= 30 * 2:
                return [ExitCommand(score=self.score)]

        self.time += 1
        return []

    def render(self, pressed_buttons: set[tuple[int, int]]) -> Board:
        board = Board()

        if self.state == 'playing':
            for row in range(board.num_rows):
                for col in range(board.num_cols):
                    button = board.buttons[(row, col)]

                    # Waves
                    for wave in self.waves:
                        lights = wave.get_lights(row, col)
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

                    # Waves
                    for wave in self.waves:
                        lights = wave.get_lights(row, col)
                        if lights is not None:
                            for i in range(12):
                                button.lights[i] = (button.lights[i] + lights[i]) * play_intensity

            for (row, col) in self.fail_buttons:
                board.buttons[(row, col)].set_all_lights(RED * play_intensity)

        for (row, col) in pressed_buttons:
            board.buttons[(row, col)].set_all_lights(WHITE)

        return board


class Wave:
    def __init__(self, direction: str):
        self.direction = direction  # left, right, up, down
        self.time = 0

    def update(self) -> bool:
        self.time += 1
        return self.time < 100

    def is_deadly(self, row: int, col: int) -> bool:
        position = self.time // 12
        sub_position = self.time % 12
        grace_frames = 3

        if self.direction == 'right':
            if position == col:
                return grace_frames <= sub_position <= 12 - grace_frames - 1
        if self.direction == 'left':
            if self.time // 12 == 7 - col - 1:
                return grace_frames <= sub_position <= 12 - grace_frames - 1
        if self.direction == 'down':
            if self.time // 12 == row:
                return grace_frames <= sub_position <= 12 - grace_frames - 1
        if self.direction == 'up':
            if self.time // 12 == 5 - row - 1:
                return grace_frames <= sub_position <= 12 - grace_frames - 1

        return False

    def get_light(self) -> Light:
        if self.direction == 'right':
            return CYAN
        if self.direction == 'left':
            return MAGENTA
        if self.direction == 'down':
            return YELLOW
        if self.direction == 'up':
            return Light(0.66, 0.66, 0.66)
        raise RuntimeError(f"Invalid direction {self.direction}")

    def get_lights(self, row: int, col: int) -> list[Light] | None:
        if self.direction == 'right':
            if self.time // 12 == col:
                return rotate(self.light_pattern(self.time % 12), 3)
        if self.direction == 'left':
            if self.time // 12 == 7 - col - 1:
                return rotate(self.light_pattern(self.time % 12), 9)
        if self.direction == 'down':
            if self.time // 12 == row:
                return rotate(self.light_pattern(self.time % 12), 0)
        if self.direction == 'up':
            if self.time // 12 == 5 - row - 1:
                return rotate(self.light_pattern(self.time % 12), 6)
        return None

    def light_pattern(self, n):
        half = [self.get_light() if i < n < i + 6 else Light(0, 0, 0) for i in range(6)]
        return half + half[::-1]
