from Board import Board
from Light import GREEN


class TestMarquee:
    def __init__(self):
        self.name = "[Test] Marquee"
        self.desc = "Scolling text"

        self.time = 0
        self.text = "HELLO WORLD"

    def update(self, pressed_buttons: set[(int, int)], **kwargs):
        self.time += 1

    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()

        offset = 7 - (self.time // 6) % (len(self.text) * (3 + 1) + 7)

        for index, char in enumerate(self.text):
            board.show_char(0, index * (3 + 1) + offset, char, GREEN)

        return board
