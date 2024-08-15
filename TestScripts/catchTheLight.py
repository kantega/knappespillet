import random
import time
from config import GameBoard

#Author: Magnus Kråbøl
# Simple game about catching the light

#Setup colors
magenta = (255, 0, 255)
blue = (0, 0, 255)

#Initialize game board
game_board = GameBoard()

#Variables to hold active button position
active_button_row = None
active_button_column = None

#Points counter
points = 0

def light_up_random_button(game_board: GameBoard):
    global active_button_row
    active_button_row = random.randint(0,4)
    global active_button_column
    active_button_column = random.randint(0,6)
    game_board.color_single_ring(active_button_column, active_button_row, (magenta))
    game_board.paint()
    time.sleep(0.5)

light_up_random_button(game_board)
game_board.color_all_rings(blue)

while True:
    if game_board.is_button_pressed(active_button_column, active_button_row):
        game_board.clear_all_pixels()
        points += 1
        print(f"Button pressed! Score: {points}")
        light_up_random_button(game_board)
    else:
        print(f"Button not pressed! Score: {points}")
        time.sleep(0.5)

