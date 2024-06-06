import time
from config import GameBoard

print("STARTING testConfig script")

pink_color = (255, 0, 255)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
blue_color = (0, 255, 255)
white_color = (255, 255, 255)
no_color = (0, 0, 0)

""" 
5 Rows x 7 Columns = 35 buttons
Coordinates written as if facing the board with the buttons

Coordinates for the buttons and lights are as follows:

4,0    4,1    4,2    4,3    4,4    4,5    4,6  
3,0    3,1    3,2    3,3    3,4    3,5    3,6  
2,0    2,1    2,2    2,3    2,4    2,5    2,6  
1,0    1,1    1,2    1,3    1,4    1,5    1,6  
0,0    0,1    0,2    0,3    0,4    0,5    0,6  
"""
game_board = GameBoard()

def blink():
    for i in range(game_board.NUM_COLS):
        for j in range(game_board.NUM_ROWS):
            game_board.color_single_ring(j,i,white_color)
    game_board.paint()
    time.sleep(0.04)

def whole_board_reset():
    game_board.color_all_rings(pink_color)
    game_board.color_single_ring(1, 3, blue_color)
    game_board.color_single_ring(3, 3, blue_color)
    game_board.color_single_ring(2, 2, red_color)
    game_board.color_single_ring(2, 4, blue_color)
    game_board.paint()

print("INITIALIZING pixels with color green")
game_board.color_all_rings(no_color)
game_board.paint()

i=0
j=0

while True:
    i = i % game_board.NUM_ROWS
    j = j % game_board.NUM_COLS
    game_board.color_single_ring(i, j, green_color)
    game_board.paint()
    time.sleep(0.5)
    game_board.color_single_ring(i, j, no_color)
    game_board.paint()
    i+=1
    if (i>= game_board.NUM_ROWS):
        j+=1
    #if game_board.is_button_pressed(2, 4):  # right_button
    #    blink()
    #    time.sleep(0.05)
    #else:
    #    whole_board_reset() 
    #    time.sleep(0.005)
