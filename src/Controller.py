import math

from pygame import Surface
from pygame.freetype import Font

from Board import Board
from CatchTheLight import CatchTheLight
from ConnectFour import ConnectFour
from Game import Game, ExitCommand
from Light import GREEN, YELLOW, WHITE, CYAN, BLACK
from TapDance import TapDance
from TapTendrils import TapTendrils
from TickTackToe import TickTackToe
from TimeBombs import TimeBombs


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
            CatchTheLight(),
            TimeBombs(),
            ConnectFour(),
            TickTackToe(),
        ]
        self.index: int = 0
        self.time: int = 0
        self.score: int = 0
        self.last_pressed_buttons: set[tuple[int, int]] = set()
        self.large_font: Font = Font(file="src/fonts/Space_Mono/SpaceMono-Regular.ttf", size=96)
        self.small_font: Font = Font(file="src/fonts/Space_Mono/SpaceMono-Regular.ttf", size=64)
        self.large_font.origin = True
        self.small_font.origin = True

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
                    if command.score is not None:
                        self.state = "show_score"
                        self.time = 0
                        self.score = command.score
                    else:
                        self.state = "select_game"

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

        draw_text(surface, (32, 32), game_info.name, self.large_font, (255, 255, 255), 1280 - 64)
        draw_text(surface, (32, 64 + 96), game_info.description, self.small_font, (255, 255, 255), 1280 - 64)

        return surface


def draw_text(surface: Surface, dest: tuple[int, int], text: str, font: Font, color: tuple[int, int, int], max_width: int):
    (dest_x, dest_y) = dest
    char_bounds = font.get_rect('X')
    x = char_bounds.x
    y = char_bounds.y

    for word in text.split(' '):
        word_bounds = font.get_rect(word)
        if x + word_bounds.x + word_bounds.width >= max_width:
            x = 0
            y += math.floor(char_bounds.height * 1.5)
        if x + word_bounds.x + word_bounds.width >= max_width:
            raise RuntimeError("word is too long")
        font.render_to(surface, (dest_x + x, dest_y + y), word, color)
        x += word_bounds.width + char_bounds.width
