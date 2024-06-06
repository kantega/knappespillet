import time
from config import GameBoard

print("STARTING testConfig script")

pink_color = (255, 0, 255)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
blue_color = (0, 255, 255)
color_white = (255, 255, 255)
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


while True:
    game_board.color_all_rings(color_white)
    game_board.paint()
    time.sleep(0.1)
