import math
from random import randint

from Board import Board
from Light import WHITE, CYAN, MAGENTA, YELLOW, GREEN, RED
from utils import clamp 

QUIT_GAME_BUTTON_COORD = (0,6)

class CatchTheLight:
    def __init__(self):
        self.name = "CatchTheLight"
        self.desc = "Rush to catch the light as many times as you can before the time runs out"
        self.game_dev = "Magnus K"
        self.state = 'waiting'
        self.time = 0
        self.inactive_time = 0
        self.score = 0
        self.active_button = 0
        
    def update(self, pressed_buttons: set[(int, int)],  **kwargs):
        if self.state == 'waiting':
            if QUIT_GAME_BUTTON_COORD in pressed_buttons and "go_to_main_menu" in kwargs:
                self.state = "quit"
                self.time = 0
            if (2, 3) in pressed_buttons:
                self.state = 'playing'
                self.time = 0
                self.score = 0
                self.inactive_time = 0
                self.active_button = (randint(0, 4), randint(0, 6))
                return
        
        elif self.state == "quit":
            if QUIT_GAME_BUTTON_COORD not in pressed_buttons:
                self.state = "waiting"
                self.time = 0
                return

            if self.time > 30:
                go_to_main_menu = kwargs["go_to_main_menu"]
                return go_to_main_menu()


        elif self.state == 'playing':            
            if self.active_button in pressed_buttons:
                self.score += 1
                self.inactive_time = 0
                self.active_button = (randint(0, 4), randint(0, 6))
            else:
                self.inactive_time += 1
                if self.inactive_time > 5 * 30:
                    self.state = 'score'
                    self.time = 0

            if self.time > 30 * 30:
                self.state = 'score'
                self.time = 0

        elif self.state == 'score':
            if self.time > 90:
                self.state = 'waiting'
                self.time = 0     

        self.time += 1

    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()

        if self.state == 'waiting':
            board.buttons[(2, 3)].set_all_lights(GREEN)
            board.buttons[QUIT_GAME_BUTTON_COORD].set_all_lights(RED)

        if self.state == 'playing':
            board.buttons[self.active_button].set_all_lights(MAGENTA)

        if self.state == 'score':

            if self.time < 30:

                for row in range(5):
                    for col in range(7):
                        board.buttons[(row, col)].set_all_lights(WHITE)
                
            else:
                board.show_two_digit_number(self.score, CYAN)

        elif self.state == "quit":
            button = board.buttons[QUIT_GAME_BUTTON_COORD]
            hold_progress = clamp(1, self.time, 60) / 60
            number_of_lights = math.ceil(hold_progress * button.num_lights)
            button.set_n_lights(number_of_lights, YELLOW)
            return board

        for (row, col) in pressed_buttons:
            board.buttons[(row, col)].set_all_lights(WHITE)

        return board