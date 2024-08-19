import imageio

from Button import Button
from Light import Light

FONT_5x3 = imageio.v3.imread("./font-5x3.png")


class Board:
    def __init__(self):
        self.num_rows = 5
        self.num_cols = 7
        self.buttons = dict()
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.buttons[(row, col)] = Button()

    def show_char(self, offset_row: int, offset_col: int, char: str, light: Light):
        codepoint = ord(char)
        font_row = (codepoint // 32) * (5 + 1)
        font_col = (codepoint % 32) * (3 + 1)

        for char_row in range(5):
            for char_col in range(3):
                light_on = FONT_5x3[font_row + char_row][font_col + char_col][0] == 255
                row = char_row + offset_row
                col = char_col + offset_col
                if light_on and 0 <= row < self.num_rows and 0 <= col < self.num_cols:
                    self.buttons[(row, col)].set_all_lights(light)

    def show_two_digit_number(self, n: int, light: Light):
        n1 = (n // 10) % 10
        n2 = n % 10
        self.show_char(0, 0, str(n1), light)
        self.show_char(0, 4, str(n2), light)
    
    def light_column(self, col: int, light: Light):
        for i in range(self.num_rows):
            self.buttons[(i, col)].set_all_lights(light)