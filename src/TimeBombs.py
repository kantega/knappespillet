import math
import random
from typing import Literal

from Board import Board
from Game import GameInfo, Game, ExitCommand
from Light import CYAN, MAGENTA, RED, WHITE, Light
from utils import clamp


class TimeBombs(Game):
    def __init__(self):
        self.state = 'playing'
        self.failure_buttons = set()
        self.time = 0
        self.score = 0
        self.bombs = [Bomb(2,2, "BLUE"), Bomb(2,3, "YELLOW"), Bomb(2,4, "RED")]

    def info(self) -> GameInfo:
        return GameInfo(
            name="TimeBombs",
            description="Click all the rings before their time goes out",
            creator="Erik M",
        )

    def update(self, pressed_buttons: set[tuple[int, int]]) -> list:
        if self.state == 'playing':
            bomb_coords = set(bomb.get_coord() for bomb in self.bombs)
            bombs_coords_pressed = bomb_coords.intersection(pressed_buttons)
            bombs_pressed: list[Bomb] = []
            for bomb in self.bombs:
                if bomb.get_coord() in bombs_coords_pressed:
                    bombs_pressed.append(bomb)

            for bomb in bombs_pressed:
                self.score +=1

            self.bombs = [bomb for bomb in self.bombs if bomb.get_coord() not in bombs_coords_pressed]

            for bomb in self.bombs:
                if bomb.is_expired():
                    self.failure_buttons.add(bomb.get_coord())

            if len(self.failure_buttons):
                self.state = "score"
                self.time = 0
                return []

            for bomb in self.bombs:
                bomb.update()

            spawn_period = max(1, 3 - self.time // (30 * 10))
            n_new_boms = clamp(1, self.time // 30 *60 ,3)

            if self.time % (15 * spawn_period) == 0:
                possible_new_bomb_coords= set((int(random.random()*5), int(random.random()*7)) for _ in range(10))
                for _ in range(n_new_boms):
                    (row, col)= possible_new_bomb_coords.difference(bomb_coords).pop()
                    new_bomb = Bomb(row, col, random.choice(["RED", "YELLOW", "BLUE"]))
                    self.bombs.append(new_bomb)

        elif self.state == 'score':
            if self.time >= 30 * 2:
                return [ExitCommand(score=self.score)]

        self.time += 1
        return []

    def render(self, pressed_buttons: set[tuple[int, int]]) -> Board:
        board = Board()
        if self.state == 'playing':
            for bomb in self.bombs:
                board.buttons[bomb.get_coord()].set_lights(bomb.get_lights())

        elif self.state == "score":
            if self.time < 30:
                play_intensity = 1
            elif self.time < 60:
                play_intensity = 1 - (self.time - 30) / 30
            else:
                play_intensity = 0

            for row in range(5):
                for col in range(7):
                    button = board.buttons[(row, col)]
                    # Bombs
                    for bomb in self.bombs:
                        lights = bomb.get_lights()
                        if lights is not None:
                            for i in range(12):
                                button.lights[i] = (button.lights[i] + lights[i]) * play_intensity

            for (row, col) in self.failure_buttons:
                board.buttons[(row, col)].set_all_lights(RED * play_intensity)

        for (row, col) in pressed_buttons:
            board.buttons[(row, col)].set_all_lights(WHITE)

        return board

class Bomb:
    def __init__(self,row: int, col: int, type: Literal["RED", "BLUE", "YELLOW"]):
        self.row = row
        self.col = col
        self.type = type
        self.progress = 0
        self.time = 0

    def update(self):
        self.time += 1
        max_time = self._get_max_time()
        self.progress = clamp(0, self.time, max_time) / max_time # 100max

    def is_expired(self) -> bool:
        return self.progress>=1

    def get_light(self) -> Light:
        match self.type:
            case "RED":
                return RED
            case "BLUE":
                return CYAN
            case "YELLOW":
                return MAGENTA

    def get_lights(self) -> list[Light] | None:
        number_of_lights = math.floor((1-self.progress) * 12)
        lights = []
        for _ in range(number_of_lights):
            lights.append(self.get_light())
        for _ in range(number_of_lights, 12):
            lights.append(Light(0, 0, 0))
        return lights

    def get_coord(self) -> tuple[int,int]:
        return (self.row, self.col)

    def _get_max_time(self) -> int:
        match self.type:
            case "RED":
                return 50
            case "BLUE":
                return 100
            case "YELLOW":
                return 120
