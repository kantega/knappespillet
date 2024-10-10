import math
import random
from Board import Board
from Light import BLACK, CYAN, MAGENTA, YELLOW, GREEN, RED, BLUE
from utils import clamp, rotate

KEY_PRESS_TIMEOUT = 10 # frames
SHOW_SCORE_DURATION = 180 # frames

QUIT_GAME_BUTTON_COORD = (0,6)
SHOW_LAST_SCORE_BUTTON_COORD = (4,6)
SHOW_HIGH_SCORE_BUTTON_COORD = (4,0)

ROUND_INCREMENT = 1

GAME_STATE_MENU = "menu"
GAME_STATE_QUITTING = "quit"
GAME_STATE_PLAYING = "playing"
GAME_STATE_TRANSITION_ANIMATION = "animating transition"
GAME_STATE_TASK_ANIMATION = "animating task"
GAME_STATE_GAME_OVER = "game over"
GAME_STATE_LAST_SCORE = "last score"
GAME_STATE_HIGH_SCORE = "high score"

class PatternMemory:
    def get_image(self):
        return "img1.png"
    def __init__(self):
        self.name = "Pattern Memory"
        self.desc = "Memorize the pattern."

        self.num_rows = 5
        self.num_cols = 7

        self.high_score = 0
        self.last_score = 0
        
        self.reset_everything()


    def populate_random(self, current_round):
        n = (current_round * ROUND_INCREMENT) + 4
        
        # Get all possible (row, col) positions on the board
        all_positions = [(row, col) for row in range(self.num_rows) for col in range(self.num_cols)]
        
        self.task_board = random.sample(all_positions, n)

    def reset_everything(self):
        self.game_state = GAME_STATE_MENU
        self.time = 0
        self.current_round = 0
        self.score = 0

        self.lastKeyPress = 0

        self.input_board = []
        self.populate_random(current_round=self.current_round)

        self.animation = None


    def keyPressTimeout(self): 
        return (self.time - self.lastKeyPress) < KEY_PRESS_TIMEOUT
    

    def check_for_wrong_inputs(self): 
        for input in self.input_board:
            if not (input in self.task_board):
                return input
                    
        return False
    
    def check_if_correct_pattern(self):
        if len(self.input_board) != len(self.task_board):
            return False
        
        for input in self.input_board:
            if not (input in self.task_board):
                return False
            
        return True

    def start_transition_animation(self, next_game_state):
        self.game_state = GAME_STATE_TRANSITION_ANIMATION
        self.animation = TransitionAnimation()
        self.next_game_state = next_game_state

    """
    This is the main update function. It updates board state each frame.
    """
    def update(self, pressed_buttons: set[(int, int)], **kwargs):

        if self.game_state == GAME_STATE_MENU:
                if QUIT_GAME_BUTTON_COORD in pressed_buttons:
                    self.game_state = GAME_STATE_QUITTING
                    self.time = 0

                elif SHOW_HIGH_SCORE_BUTTON_COORD in pressed_buttons:
                    self.game_state = GAME_STATE_HIGH_SCORE
                    self.time = 0

                elif SHOW_LAST_SCORE_BUTTON_COORD in pressed_buttons:
                    self.game_state = GAME_STATE_LAST_SCORE
                    self.time = 0
                
                elif len(pressed_buttons) > 0:
                    self.time = 0
                    self.input_board = []

                    self.populate_random(current_round=self.current_round)

                    self.start_transition_animation(GAME_STATE_TASK_ANIMATION)
                    return
        

        elif self.game_state == GAME_STATE_QUITTING:
                self.time += 1
                if QUIT_GAME_BUTTON_COORD not in pressed_buttons:
                    self.game_state = GAME_STATE_MENU
                    self.time = 0
                    return

                if self.time > 60:
                    go_to_main_menu = kwargs['go_to_main_menu']
                    return go_to_main_menu()

        elif self.game_state == GAME_STATE_GAME_OVER:
            if self.time > SHOW_SCORE_DURATION:
                self.reset_everything()
                return
            
        elif self.game_state == GAME_STATE_LAST_SCORE or self.game_state == GAME_STATE_HIGH_SCORE:
            if self.time > SHOW_SCORE_DURATION:
                self.game_state = GAME_STATE_MENU
                
            

        elif self.game_state == GAME_STATE_TRANSITION_ANIMATION:
            self.animation.update()
            if self.animation.check_if_done():
                if self.next_game_state == GAME_STATE_TASK_ANIMATION:
                    self.next_game_state = GAME_STATE_PLAYING
                    self.game_state = GAME_STATE_TASK_ANIMATION
                    self.animation = TaskAnimation(self.task_board)
                else:
                    self.game_state = self.next_game_state
                    self.animation = None

        elif self.game_state == GAME_STATE_TASK_ANIMATION:
            self.animation.update()
            if self.animation.check_if_done():
                self.start_transition_animation(GAME_STATE_PLAYING)


        elif self.game_state == GAME_STATE_PLAYING:
            for (row, col) in pressed_buttons:
                if not self.keyPressTimeout():
                    self.lastKeyPress = self.time
                    self.input_board.append((row, col))
                    self.score = self.score + 1

                wrong_input = self.check_for_wrong_inputs()
                if wrong_input:
                    self.time = 0
                    self.last_score = self.score - 1 # Remove the point from the incorrect button press  
                    self.high_score = self.last_score if self.last_score > self.high_score else self.high_score
                    self.start_transition_animation(GAME_STATE_GAME_OVER)
                
                correct_pattern = self.check_if_correct_pattern()
                if correct_pattern:
                    self.current_round = self.current_round + 1
                    self.input_board = []
                    self.populate_random(current_round=self.current_round)

                    self.start_transition_animation(GAME_STATE_TASK_ANIMATION)
                
                
        self.time += 1
        

    """
    This is the main render function. It determines the look of the board, and returns it. 
    """
    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()
            
        if self.game_state == GAME_STATE_MENU:
            board.buttons[(1, 2)].set_all_lights(GREEN)
            board.buttons[(3, 2)].set_all_lights(GREEN)
            board.buttons[(1, 4)].set_all_lights(GREEN)
            board.buttons[(3, 4)].set_all_lights(GREEN)
            board.buttons[QUIT_GAME_BUTTON_COORD].set_all_lights(RED)
            board.buttons[SHOW_HIGH_SCORE_BUTTON_COORD].set_all_lights(BLUE)
            board.buttons[SHOW_LAST_SCORE_BUTTON_COORD].set_all_lights(YELLOW)

        elif self.game_state == GAME_STATE_QUITTING:
            button = board.buttons[QUIT_GAME_BUTTON_COORD]
            hold_progress = clamp(1, self.time, 60) / 60
            number_of_lights = math.ceil(hold_progress * button.num_lights)
            button.set_n_lights(number_of_lights, YELLOW)
            return board            
        
        elif self.game_state == GAME_STATE_TRANSITION_ANIMATION or self.game_state == GAME_STATE_TASK_ANIMATION:
            for row in range(5):
                for col in range(7):
                    board.buttons[(row, col)].set_all_lights(self.animation.get_light_color(row, col))

        elif self.game_state == GAME_STATE_GAME_OVER or self.game_state == GAME_STATE_LAST_SCORE:
            board.show_two_digit_number(self.last_score, CYAN)


        elif self.game_state == GAME_STATE_HIGH_SCORE:
            board.show_two_digit_number(self.high_score, CYAN)
            
        elif self.game_state == GAME_STATE_PLAYING:
            for (row, col) in self.input_board:
                    board.buttons[(row, col)].set_all_lights(GREEN)
            
        return board

    

class TransitionAnimation: 
    def __init__(self):
        self.time = 0
        self.is_done = False
        self.phase = 'horizontal'  # 'horizontal' or 'vertical'
        self.board_width = 7        # Assume board is 7 columns
        self.board_height = 5       # Assume board is 5 rows
        self.speed = 6              # Frames it takes for one "step" outward from center
        self.max_horizontal_steps = max(self.board_width // 2, self.board_width - (self.board_width // 2) - 1)
        self.max_vertical_steps = max(self.board_height // 2, self.board_height - (self.board_height // 2) - 1)
        
    def update(self):
        if self.is_done:
            return
        
        self.time += 1
        
        # Horizontal phase complete, start vertical phase
        if self.phase == 'horizontal' and self.time >= (self.max_horizontal_steps + 1) * self.speed:
            self.phase = 'vertical'
            self.time = 0  # Reset time for vertical phase
        
        # Vertical phase complete, animation is done
        elif self.phase == 'vertical' and self.time >= (self.max_vertical_steps + 1) * self.speed:
            self.is_done = True

    def get_light_color(self, row, col):
        if self.phase == 'horizontal':
            # Center is column 3 (0-indexed), propagate outwards
            center_col = self.board_width // 2
            steps_out = self.time // self.speed
            left_bound = max(center_col - steps_out, 0)
            right_bound = min(center_col + steps_out, self.board_width - 1)
            
            # Light columns within bounds
            if left_bound <= col <= right_bound:
                return MAGENTA

        elif self.phase == 'vertical':
            # Center is row 2 (0-indexed), propagate outwards
            center_row = self.board_height // 2
            steps_out = self.time // self.speed
            upper_bound = max(center_row - steps_out, 0)
            lower_bound = min(center_row + steps_out, self.board_height - 1)
            
            # Light rows within bounds
            if upper_bound <= row <= lower_bound:
                return CYAN

        return BLACK

    def check_if_done(self):
        return self.is_done


class TaskAnimation:
    def __init__(self, task):
        self.is_done = False
        self.time = 0
        self.speed = 15 # number of frames per light
        self.task = task # list of (row, col) touples
        
    def update(self):
        if self.is_done:
            return
        
        self.time += 1
        
        if self.time >= len(self.task) * self.speed + self.speed * 4:
            self.is_done = True


    def get_light_color(self, row, col):
        
        n = min(len(self.task), self.time // self.speed)
        if (row, col) in self.task[:n]:
            return GREEN

        return BLACK

    def check_if_done(self):
        return self.is_done
    

