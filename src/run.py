from time import perf_counter, sleep

from adafruit_mcp230xx.mcp23017 import MCP23017
from board import D18, SCL, SDA
from busio import I2C
from digitalio import Direction, Pull
from neopixel import NeoPixel, GRB

from Board import Board
from interrupt import is_interrupted, handle_interrupts
from cli import select_game

# Position and rotation
LIGHT_MAPPING = [
    [(34, 8), (33, 8), (32, 3), (31, 4), (30, 0), (29, 5), (28, 6)],
    [(21, 3), (22, 5), (23, 11), (24, 5), (25, 9), (26, 10), (27, 11)],
    [(20, 8), (19, 8), (18, 10), (17, 1), (16, 7), (15, 6), (14, 9)],
    [(7, 8), (8, 11), (9, 5), (10, 8), (11, 1), (12, 9), (13, 0)],
    [(6, 4), (5, 8), (4, 6), (3, 0), (2, 3), (1, 1), (0, 10)],
]


def draw_board(pixels: NeoPixel, board: Board):
    for row in range(board.num_rows):
        for col in range(board.num_cols):
            button = board.buttons[(row, col)]
            (position, rotation) = LIGHT_MAPPING[row][col]
            for index, light in enumerate(button.lights):
                pixels[position * 12 + (index + rotation) % 12] = (
                    int(light.red * 255),
                    int(light.green * 255),
                    int(light.blue * 255)
                )


def get_pressed_buttons(extender_boards: list[MCP23017]) -> set[(int, int)]:
    pressed_buttons = set()
    for row in range(5):
        gpio = extender_boards[row].gpio
        for col in range(7):
            # Equivalent to get_pin(col).value, but faster since we only read gpio once
            if gpio & (1 << col) > 0:
                pressed_buttons.add((row, col))
    return pressed_buttons


def to_ms(sec: float) -> int:
    return int(sec * 1000)


def run(game, debug):
    pixels = NeoPixel(pin=D18, n=7 * 5 * 12, brightness=0.1, auto_write=False, pixel_order=GRB)

    i2c = I2C(SCL, SDA)
    extender_boards = [
        MCP23017(i2c, address=0x24),
        MCP23017(i2c, address=0x23),
        MCP23017(i2c, address=0x22),
        MCP23017(i2c, address=0x21),
        MCP23017(i2c, address=0x20),
    ]

    for row in range(5):
        for col in range(7):
            button = extender_boards[row].get_pin(col)
            button.direction = Direction.INPUT
            button.pull = Pull.UP

    target_framerate = 30

    handle_interrupts()

    running = True
    while running:
        if is_interrupted():
            running = False

        t0 = perf_counter()
        pressed_buttons = get_pressed_buttons(extender_boards)
        t1 = perf_counter()
        game.update(pressed_buttons)
        t2 = perf_counter()
        board = game.render(pressed_buttons)
        t3 = perf_counter()
        draw_board(pixels, board)
        t4 = perf_counter()
        pixels.show()
        t5 = perf_counter()

        time = (t5 - t0)
        target_time = 1 / target_framerate
        if target_time > time:
            sleep(target_time - time)

        if debug:
            print(
                f"buttons {to_ms(t1 - t0)}, "
                f"update {to_ms(t2 - t1)}, "
                f"render {to_ms(t3 - t2)}, "
                f"draw {to_ms(t4 - t3)}, "
                f"show {to_ms(t5 - t4)}, "
                f"total {to_ms(t5 - t0)}, "
                f"sleep {to_ms(target_time - time)}"
            )

    pixels.fill((0, 0, 0))
    pixels.show()


if __name__ == "__main__":
    run(select_game(), False)
