import busio
import digitalio
import board
import neopixel
from adafruit_mcp230xx.mcp23017 import MCP23017

"""
5 Rows x 7 Columns = 35 buttons
Coordinates written as if facing the board with the buttons

Using A pins 0-6 on each MCP23017 extender board
Coordinates for the buttons are as follows:

4,0    4,1    4,2    4,3    4,4    4,5    4,6  mcp4
3,0    3,1    3,2    3,3    3,4    3,5    3,6  mcp3
2,0    2,1    2,2    2,3    2,4    2,5    2,6  mcp2
1,0    1,1    1,2    1,3    1,4    1,5    1,6  mcp1
0,0    0,1    0,2    0,3    0,4    0,5    0,6  mcp0
"""

""" 
Order written as if facing the board with the buttons
Order of how the NeoPixel lightrings are serially connected (0-indexed):

28    29    30    31    32    33    34
27    26    25    24    23    22    21
14    15    16    17    18    19    20
13    12    11    10     9     8     7
0      1     2     3     4     5     6
"""


class GameBoard:
    extender_boards = []
    buttons: dict[str, digitalio.DigitalInOut] = {}

    def __init__(self):
        self.NUM_ROWS = 5
        self.NUM_COLS = 7
        self.NUMBER_OF_CONNECTED_NEOPIXEL_RINGS = 35
        self.PIXELS_PER_RING = 12
        self.TOTAL_NUMBER_OF_PIXELS = (
            self.NUMBER_OF_CONNECTED_NEOPIXEL_RINGS * self.PIXELS_PER_RING
        )

        self.__NEOPIXEL_DATA_IN_PIN = (
            board.D18
        )  # GPIO18 yellow # TODO: find out why docs say that we need to use GPIO 10

        self.__init_buttons()
        self.__init_neopixels()

    def __init_buttons(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.extender_boards = [
            MCP23017(self.i2c, address=0x20),
            MCP23017(self.i2c, address=0x21),
            MCP23017(self.i2c, address=0x22),
            MCP23017(self.i2c, address=0x23),
            MCP23017(self.i2c, address=0x24),
        ]
        for columns in range(self.NUM_COLS):
            for row in range(self.NUM_ROWS):
                self.buttons[f"x{row}y{columns}"] = self.extender_boards[row].get_pin(
                    columns
                )

        for button in self.buttons.values():
            button.direction = digitalio.Direction.INPUT
            button.pull = digitalio.Pull.UP

    def __init_neopixels(self):
        self.pixels = neopixel.NeoPixel(
            self.__NEOPIXEL_DATA_IN_PIN,
            self.TOTAL_NUMBER_OF_PIXELS,
            brightness=0.2,
            auto_write=False,
            pixel_order=neopixel.GRB,
        )

    def __get_all_buttons(self):
        return self.buttons.values()

    def is_any_button_pressed(self):
        all_buttons_values = [button.value for button in self.__get_all_buttons()]
        return any(all_buttons_values)

    def __get_button(self, row: int, column: int):
        return self.buttons[f"x{row}y{column}"]

    def is_button_pressed(self, row: int, column: int) -> bool:
        button = self.__get_button(row, column)
        return button.value

    def clear_all_pixels(self):
        self.pixels.fill((0, 0, 0))

    def color_ring_by_physical_mapping(self, pixel_ring_index: int, color: tuple):
        if (
            pixel_ring_index < 0
            or pixel_ring_index >= self.NUMBER_OF_CONNECTED_NEOPIXEL_RINGS
        ):
            raise ValueError("pixel_ring_index out of range")
        for j in range(self.PIXELS_PER_RING):
            self.pixels[pixel_ring_index * self.PIXELS_PER_RING + j] = color

    def color_ring_pixel_by_physical_mapping(
        self, pixel_ring_index: int, sub_pixel: int, color: tuple
    ):
        if (
            pixel_ring_index < 0
            or pixel_ring_index >= self.NUMBER_OF_CONNECTED_NEOPIXEL_RINGS
        ):
            raise ValueError("pixel_ring_index out of range")
        if sub_pixel < 0 or sub_pixel >= self.PIXELS_PER_RING:
            raise ValueError("sub_pixel out of range")
        self.pixels[pixel_ring_index * self.PIXELS_PER_RING + sub_pixel] = color

    def __map_pixel_ring_to_coordinates(
        self, physical_index_in_ring_chain: int
    ) -> tuple[int, int]:
        if (
            physical_index_in_ring_chain < 0
            or physical_index_in_ring_chain >= self.NUMBER_OF_CONNECTED_NEOPIXEL_RINGS
        ):
            raise ValueError("physical_index_in_ring_chain out of range")
        is_even_row = physical_index_in_ring_chain % 14 < 7
        row = physical_index_in_ring_chain // self.NUM_COLS
        column = physical_index_in_ring_chain % self.NUM_COLS
        if not is_even_row:
            column = self.NUM_COLS - (physical_index_in_ring_chain % self.NUM_COLS) - 1
        return row, column

    def __map_coordinates_to_pixel_ring(self, row: int, column: int) -> int:
        if row < 0 or row >= self.NUM_ROWS:
            raise ValueError("row out of range")
        if column < 0 or column >= self.NUM_COLS:
            raise ValueError("column out of range")
        is_even_row = row % 2 == 0
        if is_even_row:
            return row * self.NUM_COLS + column
        else:
            return row * self.NUM_COLS + (self.NUM_COLS - column - 1)

    def color_single_ring(self, row: int, column: int, color: tuple):
        self.color_ring_by_physical_mapping(
            self.__map_coordinates_to_pixel_ring(row, column), color
        )

    def color_all_rings(self, color: tuple):
        self.pixels.fill(color)

    def color_ring_pixel(self, row: int, column: int, pixel_num: int, color: tuple):
        self.color_ring_pixel_by_physical_mapping(
            self.__map_coordinates_to_pixel_ring(row, column), pixel_num, color
        )

    def paint(self):
        self.pixels.show()
