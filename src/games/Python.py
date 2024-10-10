import math
from random import randint

from Board import Board
from Light import Light, WHITE, CYAN, MAGENTA, YELLOW, GREEN, RED
from utils import clamp, rotate

QUIT_GAME_BUTTON_COORD = (0,6)
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"

class Python:
    def get_image(self):
        return "img1.png"
    def __init__(self):
        self.name = "Python"
        self.desc = "It's snake, but in python -_-'"

        self.state = 'waiting'
        self.snake = [(2,3), (2,2)]
        self.moving = RIGHT
        self.last_move = RIGHT
        self.fruit = None

        self.time = 0
        self.speed = 1

    def update(self, pressed_buttons: set[(int, int)], **kwargs):
        if self.state == 'waiting':
            if QUIT_GAME_BUTTON_COORD in pressed_buttons and "go_to_main_menu" in kwargs:
                self.state = "quit"
                self.time = 0
            if (2, 3) in pressed_buttons:
                self.state = 'playing'
                self.snake = [(2,3), (2,2)]
                self.moving = RIGHT
                self.last_move = RIGHT
                self.time = 0
                self.speed = 1
                self.fruit = None
                return
        
        elif self.state == "quit":
            if QUIT_GAME_BUTTON_COORD not in pressed_buttons:
                self.state = "waiting"
                self.time = 0
                return

            if self.time > 60:
                go_to_main_menu = kwargs["go_to_main_menu"]
                return go_to_main_menu()

            self.time += 1

        elif self.state == 'playing':
            self.select_direction(pressed_buttons)
            self.spawn_fruit()
            if self.time % 45 == 0:
                self.move_snake()
            self.time += 1

    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()

        if self.state == 'waiting':
            board.buttons[(2, 3)].set_all_lights(GREEN)
            board.buttons[QUIT_GAME_BUTTON_COORD].set_all_lights(RED)

        if self.state == 'playing':
            for snake_parts in self.snake:
                board.buttons[snake_parts].set_all_lights(GREEN)
            if self.fruit is not None:
                board.buttons[self.fruit].set_all_lights(RED)
                
        
        elif self.state == "quit":
            button = board.buttons[QUIT_GAME_BUTTON_COORD]
            hold_progress = clamp(1, self.time, 60) / 60
            number_of_lights = math.ceil(hold_progress * button.num_lights)
            button.set_n_lights(number_of_lights, YELLOW)
            return board
        
        for (row, col) in pressed_buttons:
            board.buttons[(row, col)].set_all_lights(WHITE)

        return board
    
    def select_direction(self, pressed_buttons: set[(int, int)]):
        snake_head = self.snake[0]
        if len(pressed_buttons) == 0:
            return
        if len(pressed_buttons) > 1:
            return
        pressed_button = next(iter(pressed_buttons))
        row_diff = pressed_button[0] - snake_head[0]
        column_diff =  pressed_button[1] - snake_head[1]

        if row_diff != 0:
            if row_diff > 0:
                if self.last_move != UP:
                    self.moving = DOWN
                    return
            elif self.last_move != DOWN:
                self.moving = UP
                return
            
        if column_diff == 0:
            return
        if column_diff > 0 and self.last_move != LEFT:
            self.moving = RIGHT
        elif self.last_move != RIGHT:
            self.moving = LEFT
    
    def move_snake(self):
        snake_head = self.snake[0]
        snake_length = len(self.snake) - 1

        for index in range(snake_length, 0, -1):
            self.snake[index] = self.snake[index - 1]
        if self.moving == RIGHT:
            self.snake[0] = add_to_index(snake_head, 1, 1)
            if self.snake[0][1] > 6:
                self.death()
        
        elif self.moving == LEFT:
            self.snake[0] = add_to_index(snake_head, 1, -1)
            if self.snake[0][1] < 0:
                self.death()

        elif self.moving == UP:
            self.snake[0] = add_to_index(snake_head, 0, -1)
            if self.snake[0][0] < 0:
                self.death()
        
        else:
            self.snake[0] = add_to_index(snake_head, 0, 1)
            if self.snake[0][0] > 4:
                self.death()
        
        self.last_move = self.moving

        if self.snake[0] in self.snake[1:]:
            self.death()

        if self.fruit is None:
            return
        if self.snake[0] == self.fruit:
            self.snake.append(self.snake[snake_length])
            self.fruit = None
    
    def death(self):
        self.state = "waiting"
        
        self.snake = [(2,3), (2,2)]
        self.moving = RIGHT

        self.time = 0
        self.speed = 1

    def spawn_fruit(self):
        if self.fruit is not None:
            return
        random_column = randint(0, 6)
        random_row = randint(0, 4)

        self.fruit = (random_row, random_column)

def add_to_index(tup, index, value):
    temp_list = list(tup)
    temp_list[index] += value
    
    return tuple(temp_list)
