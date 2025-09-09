import math

from Board import Board
from Game import Game, GameInfo, ExitCommand
from Light import BLUE, YELLOW, WHITE, Light
from utils import clamp

class Player:
    def __init__(self, light: Light):
        self.light = light
        self.moves: set[tuple[int, int]] = set()

    def place_move(self, move: tuple[int, int]):
        self.moves.add(move)

class TickTackToe(Game):
    def __init__(self):
        self.state = 'playing'
        self.game_board_coords = [(1,2), (1,3), (1,4),
                                  (2,2), (2,3), (2,4),
                                  (3,2), (3,3), (3,4)]

        self.non_game_board_coords = set()
        for col in range(7):
            for row in range(5):
                if (row, col) not in self.game_board_coords:
                    self.non_game_board_coords.add((row, col))

        self.players = [Player(BLUE), Player(YELLOW)]
        self.current_player_index = 0

        self._possible_winning_combos = self._get_winning_combos()
        self.winning_combo = None

        self._winner = None

        self.moves = set()

        self.time = 0

    def info(self) -> GameInfo:
        return GameInfo(
            name="TickTackToe",
            description="The classic two player game.",
            creator="Erik M",
        )

    def update(self, pressed_buttons: set[tuple[int, int]]) -> list:
        try:
            if self.state == 'playing':
                self.time += 1

                button_press = assert_single_button_press(pressed_buttons)
                if self._is_valid_move(button_press):
                    self._current_player().place_move(button_press)
                    self.time = 0
                    self.state = "check_score"
                    return []

            elif self.state == "check_score":
                self.time += 1
                if self._check_if_done():
                    self.state = "score"
                    self.time = 0
                    return []

                if self.time > 10:
                    self._next_player()
                    self.time = 0
                    self.state = "playing"

            elif self.state == "score":
                self.time += 1
                if self.time > 4 * 30:
                    return [ExitCommand(score=0)]

            return []

        except NotSingleButtonPressException:
            return []

    def render(self, pressed_buttons: set[tuple[int, int]]) -> Board:
        board = Board()

        if self.state in ['playing',  "check_score"]:
            for coord in self.non_game_board_coords:
                board.buttons[coord].set_all_lights(WHITE)
            for player in self.players:
                for move in player.moves:
                    board.buttons[move].set_all_lights(player.light)

        elif self.state == "score":
            animation_progress = clamp(0, self.time, 2 * 30) / (2 * 30) # 100max
            number_of_lights = math.floor((1-animation_progress) * 12)
            for player in self.players:
                for move in player.moves:
                    lights = []
                    for i in range(number_of_lights):
                        lights.append(player.light)
                    for i in range(number_of_lights, 12):
                        lights.append(Light(0, 0, 0))
                    board.buttons[move].set_lights(lights)
            if self._winner != None:
                for coords in self.winning_combo:
                    board.buttons[coords].set_all_lights(self._winner.light)

                for coord in self.non_game_board_coords:
                    board.buttons[coord].set_all_lights(WHITE)

        for coord in pressed_buttons:
            button = board.buttons[coord]
            button.set_all_lights(WHITE)

        return board

    def _check_if_done(self):
        n_player1_moves = len(self.players[0].moves)
        n_player2_moves = len(self.players[1].moves)
        total_moves = n_player1_moves + n_player2_moves
        max_moves = len(self.game_board_coords)
        if total_moves == max_moves:
            return True
        for player in self.players:
            for winning_combo in self._possible_winning_combos:
                overlap = player.moves.intersection(winning_combo)
                if len(overlap) == 3:
                    self.winning_combo = winning_combo
                    self._winner = player
                    return True
        return False

    def _get_winning_combos(self):
        return [
            #all combos on the horizontal board
            set([(1,2), (1,3), (1,4)]),
            set([(2,2), (2,3), (2,4)]),
            set([(3,2), (3,3), (3,4)]),

            #all combos on the vertical board
            set([(1,2), (2,2), (3,2)]),
            set([(1,3), (2,3), (3,3)]),
            set([(1,4), (2,4), (3,4)]),

            #all combos on the diagonal board
            set([(1,2), (2,3), (3,4)]),
            set([(3,2), (2,3), (1,4)]),
        ]

    def _is_valid_move(self, move: tuple[int, int]) -> bool:
        is_on_board = move in self.game_board_coords
        all_moves = self.players[0].moves.union(self.players[1].moves)
        move_was_not_played = move not in all_moves
        return is_on_board  and move_was_not_played

    def _current_player(self)->Player:
        return self.players[self.current_player_index]

    def _next_player(self):
        self.current_player_index = (self.current_player_index + 1) % 2

def assert_single_button_press(pressed_buttons: set([int, int])):
    if len(pressed_buttons) == 0:
        raise NotSingleButtonPressException("No pressed buttons")
    if len(pressed_buttons) > 1:
        raise NotSingleButtonPressException("Multiple pressed buttons")
    (row, col) = pressed_buttons.copy().pop()
    return (row, col)

class NotSingleButtonPressException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
