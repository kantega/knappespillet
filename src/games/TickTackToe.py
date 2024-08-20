import math
from random import randint
from typing import NamedTuple

from Board import Board
from Light import BLUE, RED, YELLOW, GREEN, WHITE, Light
from utils import clamp

class Move(NamedTuple): 
    row: int
    col: int
    label: Light 

    def get_coord(self):
        return (self.row, self.col)

class Player:
    def __init__(self, light: Light):
        self.light = light
        self.moves = set()

    def update(self, pressed_button: tuple[int, int]):
        pass

    def has_won():
        pass


QUIT_GAME_BUTTON_COORD = (0,6)

# TODO not done
class TickTackToe:
    def __init__(self):
        self.name = "TickTackToe"
        self.desc = "The classic Two player game"

        self.state = 'waiting'
        self.game_board_coords = [(1,2), (1,3), (1,4),
                                  (2,2), (2,3), (2,4),
                                  (3,2), (3,3), (3,4)]

        self.non_game_board_coords = set()
        for col in range(7):
            for row in range(5):
                if (row, col) not in self.game_board_coords:
                    self.non_game_board_coords.add((row, col))
        self.players: list[Player] = []
        self.current_player_index = 0

        self._has_winner = False

        self.moves = set()

        self.time = 0

    def update(self, pressed_buttons: set[(int, int)], **kwargs):
        try:
            if self.state == 'waiting':
                if QUIT_GAME_BUTTON_COORD in pressed_buttons:
                    self.state = "quit"
                    self.time = 0
                
                (row, col) = assert_single_button_press(pressed_buttons)
                if (row, col) in self.game_board_coords:
                    self.players.append(Player(BLUE))
                    self.players.append(Player(YELLOW))
                    self.current_player_index = 0

                    self.moves.add(Move(row, col, self.current_player().light))
                    self.state = 'playing'
                    self.time = 0
                    return
            
            elif self.state == "quit":
                if QUIT_GAME_BUTTON_COORD not in pressed_buttons:
                    self.state = "waiting"
                    self.time = 0
                    return

                if self.time > 60:
                    return go_to_main_menu()

                self.time += 1

            elif self.state == 'playing':
                if self._check_if_done():
                    self.players.clear()
                    self.state = "waiting"

                (row, col) = assert_single_button_press(pressed_buttons)
                move = Move(row, col, self.current_player())
                if self.is_valid_move(move):
                    self.moves.add(move)

                    self.time = 0
                    self.score = 0
                    return
        except Exception:
            return

            


    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()
        if self.state == 'waiting':
            for coord in self.game_board_coords:
                board.buttons[coord].set_all_lights(GREEN)
            
            board.buttons[QUIT_GAME_BUTTON_COORD].set_all_lights(RED)

        if self.state == 'playing':
            for coord in self.non_game_board_coords:
                board.buttons[coord].set_all_lights(WHITE)
            for player in self.players:
                for coord in player.moves:
                    board.buttons[coord].set_all_lights(player.light)

        elif self.state == "quit":
            button = board.buttons[QUIT_GAME_BUTTON_COORD]
            hold_progress = clamp(1, self.time, 60) / 60
            number_of_lights = math.ceil(hold_progress * button.num_lights)
            button.set_n_lights(number_of_lights, YELLOW)
            return board

        return board
    
    def _check_if_done(self):
        if len(self.player1_selected) + len(self.player2_selected) == len(self.game_board_coords):
            return True
        return False
    
    def is_valid_move(self, move: Move) -> bool:
        is_on_board = move.get_coord() in self.game_board_coords
        move_was_not_played = move not in self.moves
        no_winner = not self._has_winner
        return is_on_board and  no_winner and move_was_not_played 

    def current_player(self)->Player: 
        return self.players[self.current_player_index]
    
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]


    


def assert_single_button_press(pressed_buttons: set([int, int])):
    if len(pressed_buttons) == 0:
        raise Exception("No pressed buttons")
    if len(pressed_buttons) > 1:
        raise Exception("Multiple pressed buttons")
    (row, col) = pressed_buttons.copy().pop()
    return (row, col)