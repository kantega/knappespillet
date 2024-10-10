from Board import Board
from Light import WHITE


class TestCounter:
    def get_image(self):
        return "img1.png"
    def __init__(self):
        self.name = "[Test] Counter"
        self.desc = "A two digit counter"

        self.time = 0

    def update(self, pressed_buttons: set[(int, int)], **kwargs):
        self.time += 1

    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()
        board.show_two_digit_number(self.time // 15, WHITE)
        return board
