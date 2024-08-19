from typing import Optional

from Board import Board
from Light import  MAGENTA, YELLOW, GREEN, RED
from enum import Enum

from games.TapDance import TapDance
from games.TapTendrils import TapTendrils
import math

from utils import clamp

class MENU_STATES(Enum):
    WAITING = "WAITING" # When waiting for games to be selected
    HOLDING = "HOLDING" # While holding a game to be selecting
    ANIMATE_START = "ANIMATE_START"     # While animating into the new game
    ANIMATE_QUIT = "ANIMATE_QUIT"     # While animating into the new game
    PLAYING = "PLAYING" # While the game is playing


class Menu:
    """ 
    Main menu: A game that loads other games.
    Select the game you want to play by holding one of the buttons
    """
    def __init__(self):
        self.games = {
            (0,0): TapDance(),
            (0,1): TapTendrils(),
        }
        self.game_coords = self._get_game_coords()
        self.playing_game = None

        self.name = "Menu"
        self.desc = f"Select game to play ({len(self.games)} games available ⬇️)"

        self.state: MENU_STATES = MENU_STATES.WAITING 

        self.time: int = 0

        self.n_time_ticks_for_selection = 30
        self.n_time_ticks_for_start_animation =  10

        self.holding_game: Optional[tuple[int, int]]  = None

    def update(self, pressed_buttons: set[(int, int)]):
        if self.state == MENU_STATES.WAITING:
            if len(pressed_buttons) == 0:
                return
            pressed_button = pressed_buttons.copy().pop()
            if pressed_button in self._get_game_coords():
                self.holding_game = pressed_button
                self.state = MENU_STATES.HOLDING
                self.time = 0

        elif self.state == MENU_STATES.HOLDING:
            if self.holding_game not in pressed_buttons:
                self.state =MENU_STATES.WAITING
                self.time = 0
                self.holding_game = None
                return

            if self.time > self.n_time_ticks_for_selection:
                self.state = MENU_STATES.ANIMATE_START
                self.time = 0
                return

            self.time += 1

        elif self.state == MENU_STATES.ANIMATE_START:
            self.time += 1
            if self.time > self.n_time_ticks_for_start_animation:
                self.state = MENU_STATES.PLAYING
                self.playing_game = self.games[self.holding_game]
                self.time = 0
                self.holding_game = None
        
        elif self.state == MENU_STATES.ANIMATE_QUIT:
            self.time += 1
            if self.time > self.n_time_ticks_for_start_animation:
                self.state = MENU_STATES.WAITING
                self.time = 0
                self.holding_game = None

        elif self.state == MENU_STATES.PLAYING:
            return self.playing_game.update(pressed_buttons, go_to_main_menu=self.stop_game)

    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()

        match self.state:
            case MENU_STATES.PLAYING:
                return self.playing_game.render(pressed_buttons)
            case MENU_STATES.WAITING:
                for coord in self.game_coords:
                    board.buttons[coord].set_all_lights(GREEN)
                for coord in pressed_buttons:
                    if coord not in self.game_coords:
                        board.buttons[coord].set_all_lights(RED)

            case MENU_STATES.HOLDING:
                for coord in self.game_coords:
                    button = board.buttons[coord]
                    if coord == self.holding_game:
                        hold_progress = clamp(1, self.time, self.n_time_ticks_for_selection) / self.n_time_ticks_for_selection                        
                        number_of_lights = math.ceil(hold_progress * button.num_lights)
                        button.set_n_lights(number_of_lights, YELLOW)
                    else:
                        button.set_all_lights(GREEN)

                for coord in pressed_buttons:
                    if coord not in self.game_coords:
                        board.buttons[coord].set_all_lights(RED)

            case MENU_STATES.ANIMATE_START:
                cols_to_light = int(self.time / (
                    self.n_time_ticks_for_start_animation / board.num_cols
                ))
                for col in range(cols_to_light):
                    board.light_column(col, MAGENTA)

            case MENU_STATES.ANIMATE_QUIT:
                pass


        for row, col in pressed_buttons:
            if (row, col) not in self.game_coords:
                board.buttons[(row, col)].set_all_lights(RED)

        return board
    
    def stop_game(self):
        if self.state == MENU_STATES.PLAYING:
            self.time = 0
            self.state = MENU_STATES.ANIMATE_QUIT
            self.start_holding = None
            self.holding_game = None
            self.playing_game = None

    def _get_game_coords(self):
        return self.games.keys()
