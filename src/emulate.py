import pygame
from pygame import Surface, Vector2, Color
from pygame.freetype import Font
from pygame.time import Clock

from Board import Board
from Button import Button
from Controller import Controller
from Light import Light
from interrupt import is_interrupted, handle_interrupts

KEYBOARD_LAYOUTS = {
    "qwerty": [
        ["1", "2", "3", "4", "5", "6", "7"],
        ["q", "w", "e", "r", "t", "y", "u"],
        ["a", "s", "d", "f", "g", "h", "j"],
        ["z", "x", "c", "v", "b", "n", "m"],
        [None, None, None, None, None, None, None],
    ],
    "qwerty-centered": [
        [None, None, None, None, None, None, None],
        [None, "q", "w", "e", "r", "t", None],
        [None, "a", "s", "d", "f", "g", None],
        [None, "z", "x", "c", "v", "b", None],
        [None, None, None, None, None, None, None],
    ],
    "colemak": [
        ["1", "2", "3", "4", "5", "6", "7"],
        ["q", "w", "f", "p", "g", "j", "u"],
        ["a", "r", "s", "t", "d", "h", "n"],
        ["z", "x", "c", "v", "b", "k", "m"],
        [None, None, None, None, None, None, None],
    ],
    "colemak-centered": [
        [None, None, None, None, None, None, None],
        [None, "q", "w", "f", "p", "g", None],
        [None, "a", "r", "s", "t", "d", None],
        [None, "z", "x", "c", "v", "b", None],
        [None, None, None, None, None, None, None],
    ],
}


def draw_board(
        surface: Surface, font: Font, keyboard_layout: list[list[str]], board: Board
):
    surface.fill((60, 20, 60))
    for row in range(board.num_rows):
        for col in range(board.num_cols):
            button = board.buttons[(row, col)]
            key_char = keyboard_layout[row][col]
            center = Vector2(100 + col * 100, 100 + row * 100)
            draw_button(surface, font, center, key_char, button)


def draw_button(
        surface: Surface, font: Font, center: Vector2, key_char: str, button: Button
):
    average_light = Light(0, 0, 0)
    for light in button.lights:
        average_light += light * (1 / 12)
    background_light = average_light * (1 / 2)
    pygame.draw.circle(surface, to_color(background_light), center, 20)

    pygame.draw.circle(surface, (100, 100, 100), center, 20, 1)
    for index, light in enumerate(button.lights):
        offset = Vector2(0, -12).rotate(15).rotate(index * 30)
        pygame.draw.circle(
            surface, to_color(background_light | light), center + offset, 2
        )

    if key_char is not None:
        key_light = background_light + Light(0.7, 0.7, 0.7)
        font.render_to(
            surface, center + Vector2(-4, -4), key_char.upper(), to_color(key_light)
        )


def to_color(light: Light) -> Color:
    return Color(
        int(light.red * 175 + 80),
        int(light.green * 175 + 80),
        int(light.blue * 175 + 80),
    )


def get_pressed_buttons(keyboard_layout: list[list[str]]) -> set[(int, int)]:
    pressed_buttons = set()
    pressed_keys = pygame.key.get_pressed()

    for row in range(5):
        for col in range(7):
            key_char = keyboard_layout[row][col]
            if key_char is not None and pressed_keys[ord(key_char)]:
                pressed_buttons.add((row, col))

    return pressed_buttons


def emulate(keyboard_layout):
    pygame.init()
    menu_window = pygame.Window(title="Menu", size=(640, 360), position=(80, 0))
    menu_surface = menu_window.get_surface()
    board_window = pygame.Window(title="Board", size=(800, 600), position=(0, 440))
    board_surface = board_window.get_surface()

    font = Font(file="src/fonts/Space_Mono/SpaceMono-Regular.ttf", size=12)
    clock = Clock()
    handle_interrupts()

    controller = Controller()

    running = True
    while running:
        if is_interrupted():
            running = False

        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False

        pressed_buttons = get_pressed_buttons(keyboard_layout)
        controller.update(pressed_buttons)
        board = controller.render_board(pressed_buttons)
        menu = controller.render_menu(pressed_buttons)

        draw_board(board_surface, font, keyboard_layout, board)

        menu_surface.fill((0, 0, 0))
        menu_surface.blit(pygame.transform.scale_by(menu, 0.5))

        menu_window.flip()
        board_window.flip()
        clock.tick(30)

    pygame.quit()


def select(header: str, options: list[str]) -> int:
    while True:
        print()
        print(header)
        for index, option in enumerate(options):
            print(f"{index + 1}. {option}")
        print()
        s = input("Enter a number: ")
        if s.isdigit() and 1 <= int(s) <= len(options):
            return int(s) - 1


def select_keyboard_layout():
    options = list(KEYBOARD_LAYOUTS)
    index = select("Select keyboard layout:", options)
    return KEYBOARD_LAYOUTS[options[index]]


if __name__ == "__main__":
    emulate(select_keyboard_layout())
