#!/usr/bin/env python3
import time
from config import GameBoard

print("STARTING ExecStop script")

off_color = (0, 0, 0)
pink_color = (255, 0, 255)
red_color = (255, 0, 0)
green_color = (0, 255, 0)
blue_color = (0, 255, 255)

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


def animate_wave_from_left_to_right(game_board: GameBoard, color: tuple):
    for i in range(game_board.NUM_COLS - 1, -1, -1):
        for j in range(game_board.NUM_ROWS):
            game_board.color_single_ring(j, i, color)
        game_board.paint()
        time.sleep(0.04)


def animate_wave_from_bottom_to_top(game_board: GameBoard, color: tuple):
    for i in range(game_board.NUM_ROWS):
        for j in range(game_board.NUM_COLS):
            game_board.color_single_ring(i, j, color)
        game_board.paint()
        time.sleep(0.04)


def animate_wave_from_top_to_bottom(game_board: GameBoard, color: tuple):
    for i in range(game_board.NUM_ROWS - 1, -1, -1):
        for j in range(game_board.NUM_COLS):
            game_board.color_single_ring(i, j, color)
        game_board.paint()
        time.sleep(0.04)


def animate_wave_from_right_to_left(game_board: GameBoard, color: tuple):
    for i in range(game_board.NUM_COLS):
        for j in range(game_board.NUM_ROWS):
            game_board.color_single_ring(j, i, color)
        game_board.paint()
        time.sleep(0.04)


def animate_physical_pixel_ring_filling(game_board: GameBoard):
    for i in range(game_board.NUMBER_OF_CONNECTED_NEOPIXEL_RINGS):
        game_board.color_ring_pixel_by_physical_mapping(i, 2, green_color)
        game_board.color_ring_pixel_by_physical_mapping(i, 6, red_color)
        game_board.color_ring_pixel_by_physical_mapping(i, 10, blue_color)
        game_board.paint()
        time.sleep(0.04)


animate_physical_pixel_ring_filling(game_board)

game_board.color_all_rings(off_color)
game_board.paint()

