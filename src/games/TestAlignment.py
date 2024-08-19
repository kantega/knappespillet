from Board import Board
from Light import RED, GREEN, BLUE, WHITE


class TestAlignment:
    def __init__(self):
        self.name = "[Test] Alignment"
        self.desc = "Test pattern to adjust alignment. Should have red top, green sides and blue bottom."

    def update(self, pressed_buttons: set[(int, int)], **kwargs):
        pass

    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()

        for row in range(5):
            for col in range(7):
                button = board.buttons[(row, col)]

                button.lights[11] = RED
                button.lights[0] = RED

                button.lights[2] = GREEN
                button.lights[3] = GREEN

                button.lights[5] = BLUE
                button.lights[6] = BLUE

                button.lights[8] = GREEN
                button.lights[9] = GREEN

                if (row, col) in pressed_buttons:
                    button.lights[1] = WHITE
                    button.lights[4] = WHITE
                    button.lights[7] = WHITE
                    button.lights[10] = WHITE

        return board
