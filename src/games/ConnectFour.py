import math
from Board import Board
from Light import Light, WHITE, CYAN, MAGENTA, YELLOW, GREEN, RED
from utils import clamp, rotate

P1_COLOR = WHITE
P2_COLOR = RED
KEY_PRESS_TIMEOUT = 12

QUIT_GAME_BUTTON_COORD = (0,6)

GAME_STATE_MENU = "menu"
GAME_STATE_QUITTING = "quit"
GAME_STATE_PLAYING = "playing"
GAME_STATE_P1_WIN = "winner1"
GAME_STATE_P2_WIN = "winner2"


class ConnectFour:
    def get_image(self):
        return "img1.png"
    def __init__(self):
        self.name = "ConnectFour"
        self.desc = "Get four in a row. 2 player game."

        self.num_rows = 5
        self.num_cols = 7
        
        self.resetEverything()

    def resetBoardState(self):        
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.virtualBoard[(row, col)] = 0

    def resetEverything(self):
        self.virtualBoard = dict()
        self.gameState = GAME_STATE_MENU
        self.time = 0
        self.lastKeyPress = 0
        self.currentPlayer = 1 # Players 1 and 2
        self.gamePieceDrops = []
        self.cleanUpWave = None
        self.resetBoardState()

    def keyPressTimeout(self): 
        return (self.time - self.lastKeyPress) < KEY_PRESS_TIMEOUT

    # Returns next empty row in the column, descending. 
    # Returns -1 if all rows are taken. 
    def getNextEmptyRow(self, col):
        for row in range(self.num_rows-1, -1, -1):
            if self.virtualBoard[(row, col)] == 0:
                return row
            
        return -1
    

    # Returns false if no one has won. If there is a winner, returns
    # @Returns 
    # winner: The winning player
    # row: the row if the first winning piece
    # col: the columns of the first winning piece
    # deltaRow: helper value to determine which direction the winning line is 
    # deltaCol: helper value to determine which direction the winning line is 
    def checkIfGameIsWon(self): 

        # Helper function to check consecutive pieces in a given direction
        def checkDirection(row, col, deltaRow, deltaCol):
            start_value = self.virtualBoard.get((row, col))
            if start_value == 0:
                return False
            for i in range(1, 4):
                r = row + i * deltaRow
                c = col + i * deltaCol
                if self.virtualBoard.get((r, c)) != start_value:
                    return False
            return True

        # Check all cells for possible winning positions.
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                boardPiece = self.virtualBoard.get((row, col))
                if (boardPiece != 0):
                    if col + 3 < self.num_cols and checkDirection(row, col, 0, 1):
                        return boardPiece, row, col, 0, 1
                    if row + 3 < self.num_rows and checkDirection(row, col, 1, 0):
                        return boardPiece, row, col, 1, 0
                    if row + 3 < self.num_rows and col + 3 < self.num_cols and checkDirection(row, col, 1, 1):
                        return boardPiece, row, col, 1, 1
                    if row + 3 < self.num_rows and col - 3 >= 0 and checkDirection(row, col, 1, -1):
                        return boardPiece, row, col, 1, -1
                    
        return False
    
    # Sets game state according to winner, then resets virtual board state 
    def gameIsWon(self, gameWinner, row, col, deltaRow, deltaCol):
        if gameWinner == 1:
            self.gameState = GAME_STATE_P1_WIN
        else:
            self.gameState = GAME_STATE_P2_WIN

        self.time = 0
        self.resetBoardState()
        self.gamePieceDrops = []
        for i in range(0, 4):
                r = row + i * deltaRow
                c = col + i * deltaCol
                
                self.virtualBoard[(r, c)] = gameWinner

    
    """
    This is the main update function. It updates board state each frame.
    """
    def update(self, pressed_buttons: set[(int, int)], **kwargs):

        if self.gameState == GAME_STATE_MENU:
                if QUIT_GAME_BUTTON_COORD in pressed_buttons:
                    self.gameState = GAME_STATE_QUITTING
                    self.time = 0
                
                elif len(pressed_buttons) > 0:
                    self.gameState = GAME_STATE_PLAYING
                    self.time = 0
                    self.resetBoardState()
                    return
        

        elif self.gameState == GAME_STATE_QUITTING:
                self.time += 1
                if QUIT_GAME_BUTTON_COORD not in pressed_buttons:
                    self.gameState = GAME_STATE_MENU
                    self.time = 0
                    return

                if self.time > 60:
                    go_to_main_menu = kwargs['go_to_main_menu']
                    return go_to_main_menu()

        elif self.gameState == GAME_STATE_PLAYING:

            gameWin = self.checkIfGameIsWon()
            if gameWin:
                self.gameIsWon(*gameWin)
                
        
            for (_, col) in pressed_buttons:
                if not self.keyPressTimeout():
                    self.lastKeyPress = self.time

                    nextEmptyRow = self.getNextEmptyRow(col)
                    if nextEmptyRow > -1:
                        # Update board state
                        self.virtualBoard[(nextEmptyRow, col)] = self.currentPlayer

                        # Start falling piece animation 
                        self.gamePieceDrops.append(GamePieceDrop(finalRow=nextEmptyRow, column=col,  player=self.currentPlayer))

                        # Switch player
                        self.currentPlayer = 2 if self.currentPlayer == 1 else 1
                
                
            # Update all drop animtations and keep relevant ones
            self.gamePieceDrops = [drop for drop in self.gamePieceDrops if drop.update()]
        

        if self.gameState == GAME_STATE_P1_WIN or self.gameState == GAME_STATE_P2_WIN:
            # if winner animation is done, set game state to menu
            if self.time > 180: 
                self.resetEverything()
                return
            
            # After 3 seconds, start cleanup animation 
            if self.time == 90: 
                self.cleanUpWave = Wave(1 if self.gameState == GAME_STATE_P1_WIN else 2)

            if self.cleanUpWave:
                self.cleanUpWave.update()

        self.time += 1
        

    """
    This is the main render function. It determines the look of the board, and returns it. 
    """
    def render(self, pressed_buttons: set[(int, int)]) -> Board:
        board = Board()
            
        if self.gameState == GAME_STATE_MENU:
            board.buttons[(1, 1)].set_all_lights(GREEN)
            board.buttons[(2, 2)].set_all_lights(GREEN)
            board.buttons[(3, 3)].set_all_lights(GREEN)
            board.buttons[(4, 4)].set_all_lights(GREEN)
            board.buttons[QUIT_GAME_BUTTON_COORD].set_all_lights(RED)

        elif self.gameState == GAME_STATE_QUITTING:
            button = board.buttons[QUIT_GAME_BUTTON_COORD]
            hold_progress = clamp(1, self.time, 60) / 60
            number_of_lights = math.ceil(hold_progress * button.num_lights)
            button.set_n_lights(number_of_lights, YELLOW)
            return board            
        
        else:
            for row in range(5):
                for col in range(7):
                    button = board.buttons[(row, col)]

                    # Render dropped game pieces
                    for drop in self.gamePieceDrops:
                        lights = drop.get_lights(row, col)
                        if lights is not None:
                            for i in range(12):
                                button.lights[i] = (button.lights[i] + lights[i])

                    # Render cleanup wave
                    if self.cleanUpWave:
                        lights = self.cleanUpWave.get_lights(row, col)
                        if lights is not None:
                            for i in range(12):
                                button.lights[i] = (button.lights[i] + lights[i])

            for (row, col), boardState in self.virtualBoard.items():
                if boardState == 1:
                    board.buttons[(row, col)].set_all_lights(P1_COLOR)
                elif boardState == 2:
                    board.buttons[(row, col)].set_all_lights(P2_COLOR)

        return board


class GamePieceDrop:
    def __init__(self, finalRow, column, player):
        self.finalRow = finalRow
        self.column = column
        self.player = player 

        self.time = 0
        self.currentRow = 0

    def update(self) -> bool:
        self.time += 1
        self.currentRow = self.time // 8
        return self.currentRow < self.finalRow


    def get_color(self) -> Light:
        if self.player == 1:
            return P1_COLOR
        if self.player == 2:
            return P2_COLOR

    def get_lights(self, row: int, col: int) -> list[Light] | None:
        if self.currentRow == row and self.column == col:
            return rotate(self.light_pattern(self.time % 8), 0)

    def light_pattern(self, n):
        half = [self.get_color() if i < n < i + 6 else Light(0, 0, 0) for i in range(6)]
        return half + half[::-1]


class Wave:
    def __init__(self, winner):
        self.winningPlayer = winner
        self.time = 0

    def update(self) -> bool:
        self.time += 1
        return self.time < 100

    def get_color(self) -> Light:
        if self.winningPlayer == 1:
            return P1_COLOR
        elif self.winningPlayer == 2:
            return P2_COLOR
        else: 
            raise RuntimeError("Wrong winner format", self.winningPlayer)

    def get_lights(self, row: int, col: int) -> list[Light] | None:
        if self.time // 12 == 5 - row - 1:
            return rotate(self.light_pattern(self.time % 12), 6)
        if self.time // 12 > 5 - row - 1:
            return [self.get_color() for i in range(12)] 

    def light_pattern(self, n):
        half = [self.get_color() if i < n < i + 6 else Light(0, 0, 0) for i in range(6)]
        return half + half[::-1]