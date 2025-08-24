import pygame
from pygame import Surface
from pygame.freetype import Font

from Board import Board
from Game import Game, ExitCommand
from Light import GREEN, YELLOW, WHITE, CYAN, BLACK
from TapDance import TapDance
from TapTendrils import TapTendrils


# TODO: Display game info nicely
# TODO: High scores
# TODO: Adapt remaining games
# TODO: Make it run on the wall
class Controller:
    def __init__(self):
        self.state: str = "select_game"
        self.games: list[Game] = [
            TapDance(),
            TapTendrils(),
        ]
        self.index: int = 0
        self.time: int = 0
        self.score: int = 0
        self.last_pressed_buttons: set[tuple[int, int]] = set()
        self.large_font: Font = Font(file="src/fonts/Space_Mono/SpaceMono-Regular.ttf", size=32)
        self.small_font: Font = Font(file="src/fonts/Space_Mono/SpaceMono-Regular.ttf", size=20)
        self.image: Surface = pygame.image.load("src/images/tux.png")

    def update(self, pressed_buttons: set[tuple[int, int]]) -> None:

        if self.state == "select_game":
            if (2, 2) in pressed_buttons and (2, 2) not in self.last_pressed_buttons:
                self.index = (self.index + len(self.games) - 1) % len(self.games)
            if (2, 3) in pressed_buttons and (2, 3) not in self.last_pressed_buttons:
                self.state = "play_game"
                self.games[self.index].__init__()
            if (2, 4) in pressed_buttons and (2, 4) not in self.last_pressed_buttons:
                self.index = (self.index + len(self.games) + 1) % len(self.games)

        if self.state == "play_game":
            commands = self.games[self.index].update(pressed_buttons)
            for command in commands:
                if isinstance(command, ExitCommand):
                    self.state = "show_score"
                    self.time = 0
                    self.score = command.score

        if self.state == "show_score":

            if self.time > 30 * 4:
                self.state = "select_game"

        self.time += 1
        self.last_pressed_buttons = pressed_buttons

    def render_board(self, pressed_buttons: set[tuple[int, int]]) -> Board:
        if self.state == "select_game":
            board = Board()

            board.buttons[(2, 2)].lights = [YELLOW if i >= 6 else BLACK for i in range(12)]
            board.buttons[(2, 3)].set_all_lights(GREEN)
            board.buttons[(2, 4)].lights = [YELLOW if i < 6 else BLACK for i in range(12)]

            for (row, col) in pressed_buttons:
                board.buttons[(row, col)].set_all_lights(WHITE)

            return board

        if self.state == "play_game":
            return self.games[self.index].render(pressed_buttons)

        if self.state == "show_score":
            if self.time < 30 * 3:
                intensity = 1
            elif self.time < 30 * 4:
                intensity = 1 - (self.time - 30 * 6) / 30
            else:
                intensity = 0

            board = Board()
            board.show_two_digit_number(self.score, CYAN * intensity)
            return board

        raise RuntimeError(f"Unhandled state {self.state}")

    def render_menu(self, pressed_buttons: set[tuple[int, int]]) -> Surface:
        surface = Surface(size=(1280, 720))
        game_info = self.games[self.index].info()

        self.large_font.render_to(surface, dest=(20, 20), text=game_info.name, fgcolor=(255, 0, 0))
        self.small_font.render_to(surface, dest=(20, 80), text=game_info.description, fgcolor=(0, 255, 0))

        surface.blit(self.image, dest=(100,200))

        return surface
