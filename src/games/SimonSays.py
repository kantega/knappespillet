import math
import random
from typing import List

from Board import Board
from HighScoreDisplay import display_high_scores
from HighScoreManager import read_high_scores, write_high_score
from Light import BLUE, GREEN, RED, WHITE, YELLOW, Light
from utils import clamp

QUIT_GAME_BUTTON_COORD = (0, 6)
START_GAME_BUTTON_COORD = (2, 3)  # Middle button in a 5x7 grid

class SimonSays:
    def __init__(self):
        self.name = "Simon Says"
        self.desc = "Repeat the sequence of lights!"
        self.file_name = "simon_says_high_scores.txt"

        self.state = 'waiting'
        self.sequence: List[tuple[int, int]] = []
        self.player_input: List[tuple[int, int]] = []
        self.time = 0
        self.current_step = 0
        self.scene_change_time = 30  # 1 second at 30 fps (adjust this value based on actual frame rate)
        self.display_delay = 20  # Number of frames to wait between displaying each button (slower display)
        self.light_on_time = 10  # Time each light stays on during the sequence display
        self.correct_blink_time = 5  # Time to blink the correct button in blue before the next sequence

        self.button_colors = [BLUE, GREEN, RED, YELLOW]

    def start_game(self):
        self.state = 'scene_change'
        self.sequence.clear()
        self.player_input.clear()
        self.current_step = 0
        self._add_to_sequence()

    def _add_to_sequence(self):
        # Add a random button to the sequence, excluding quit and start buttons
        while True:
            new_move = (random.randint(0, 4), random.randint(0, 6))
            if new_move != QUIT_GAME_BUTTON_COORD and new_move != START_GAME_BUTTON_COORD:
                self.sequence.append(new_move)
                break

    def update(self, pressed_buttons: set[tuple[int, int]], **kwargs):
        try:
            if self.state == 'waiting':
                if QUIT_GAME_BUTTON_COORD in pressed_buttons:
                    self.state = "quit"
                    self.time = 0
                elif START_GAME_BUTTON_COORD in pressed_buttons:
                    self.start_game()
                    return
                
            elif self.state == "quit":
                self.time += 1
                if QUIT_GAME_BUTTON_COORD not in pressed_buttons:
                    self.state = "waiting"
                    self.time = 0
                    return

                if self.time > 60:
                    go_to_main_menu = kwargs['go_to_main_menu']
                    return go_to_main_menu()

            elif self.state == 'scene_change':
                self.time += 1
                if self.time >= self.scene_change_time:
                    self.time = 0
                    self.state = 'display_sequence'
                    return

            elif self.state == 'display_sequence':
                # Show the current light in the sequence
                if self.current_step == 0:
                    required_time = self.light_on_time * 2
                else:
                    required_time = self.light_on_time
                
                if self.time < required_time:
                    self.time += 1
                else:
                    self.time = 0
                    self.current_step += 1
                    if self.current_step >= len(self.sequence):
                        self.current_step = 0
                        self.state = 'player_turn'
                        return
            elif self.state == 'player_turn':
                if QUIT_GAME_BUTTON_COORD in pressed_buttons:
                    self.state = "quit"
                    self.time = 0
                if len(pressed_buttons) > 0:
                    button_press = assert_single_button_press(pressed_buttons)

                    # Ignore quit button during sequence input
                    if button_press == QUIT_GAME_BUTTON_COORD:
                        return

                    self.player_input.append(button_press)

                    if self.player_input[self.current_step] == self.sequence[self.current_step]:
                        self.state = 'correct_guess'
                        self.blink_time = 0
                    else:
                        self.state = 'game_over'

            elif self.state == 'correct_guess':
                self.blink_time += 1
                if self.blink_time < self.correct_blink_time:
                    pass  # Blink effect handled in the render method
                else:
                    self.current_step += 1
                    if self.current_step == len(self.sequence):
                        self.player_input.clear()
                        self.state = 'scene_change'
                        self.time = 0
                        self.current_step = 0
                        self._add_to_sequence()
                    else:
                        self.state = 'player_turn'

            elif self.state == 'game_over':
                self.time += 1
                if self.time > 100:  # Show "Game Over" for a short time
                    # Write the high score to file
                    write_high_score(len(self.sequence), self.file_name)
                    
                    # Display high scores
                    high_scores = read_high_scores(self.file_name)
                    print(f"High scores: {high_scores}")
                    display_high_scores(high_scores) 
                    self.state = 'waiting'
                    self.time = 0
                    self.sequence.clear()
                    self.player_input.clear()

        except NotSingleButtonPressException:
            return

    def render(self, pressed_buttons: set[tuple[int, int]]) -> Board:
        board = Board()
        
        # Always set the quit button to red
        board.buttons[QUIT_GAME_BUTTON_COORD].set_all_lights(RED)
    
        if self.state == 'waiting':
            # Light up all buttons in GREEN to indicate readiness
            for row in range(5):
                for col in range(7):
                    if (row, col) != QUIT_GAME_BUTTON_COORD:
                        board.buttons[(row, col)].set_all_lights(GREEN)
            # Set the middle button to BLUE
            board.buttons[START_GAME_BUTTON_COORD].set_all_lights(BLUE)

        elif self.state == "quit":
            button = board.buttons[QUIT_GAME_BUTTON_COORD]
            hold_progress = clamp(1, self.time, 60) / 60
            number_of_lights = math.ceil(hold_progress * button.num_lights)
            button.set_n_lights(number_of_lights, YELLOW)
            return board

        elif self.state == 'scene_change':
            # Scene transition: turn off all lights or show a pattern
            for row in range(5):
                for col in range(7):
                    if (row, col) != QUIT_GAME_BUTTON_COORD:
                        board.buttons[(row, col)].set_all_lights(Light(0, 0, 0))

        elif self.state == 'display_sequence':
            if self.current_step < len(self.sequence):
                # Light stays on for light_on_time frames
                row, col = self.sequence[self.current_step]
                board.buttons[(row, col)].set_all_lights(YELLOW)

        elif self.state == 'player_turn':

            # Highlight the player's current input in BLUE
            for move in self.player_input:
                board.buttons[move].set_all_lights(BLUE)

        elif self.state == 'correct_guess':
            # Blink the last pressed button in BLUE to indicate correct guess
            last_move = self.player_input[-1]
            if self.blink_time % 2 == 0:
                board.buttons[last_move].set_all_lights(BLUE)
            else:
                board.buttons[last_move].set_all_lights(WHITE)

        elif self.state == 'game_over':
            # Flash all buttons in RED to indicate the game is over
            for row in range(5):
                for col in range(7):
                    if (row, col) != QUIT_GAME_BUTTON_COORD:
                        board.buttons[(row, col)].set_all_lights(RED)

        return board

# Utility function for handling single button press
def assert_single_button_press(pressed_buttons: set[tuple[int, int]]):
    if len(pressed_buttons) is None or len(pressed_buttons) == 0:
        raise NotSingleButtonPressException("No pressed buttons")
    if len(pressed_buttons) > 1:
        raise NotSingleButtonPressException("Multiple pressed buttons")
    return pressed_buttons.pop()

# Exception for handling incorrect button presses
class NotSingleButtonPressException(Exception):
    def __init__(self, msg: str): 
        self.msg = msg