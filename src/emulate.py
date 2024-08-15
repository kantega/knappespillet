import pygame
from pygame import Surface, Vector2, Color
from pygame.freetype import Font, SysFont
from pygame.time import Clock

from Board import Board
from Button import Button
from Light import Light
from cli import select_game, select
from interrupt import is_interrupted, handle_interrupts

KEYBOARD_LAYOUTS = {
    "qwerty": [
        [None, None, None, None, None, None, None],
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
        [None, None, None, None, None, None, None],
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
    ]
}


def draw_board(surface: Surface, font: Font, keyboard_layout: list[list[str]], board: Board):
    surface.fill((60, 20, 60))
    for row in range(board.num_rows):
        for col in range(board.num_cols):
            button = board.buttons[(row, col)]
            key_char = keyboard_layout[row][col]
            center = Vector2(100 + col * 100, 100 + row * 100)
            draw_button(surface, font, center, key_char, button)


def draw_button(surface: Surface, font: Font, center: Vector2, key_char: str, button: Button):
    average_light = Light(0, 0, 0)
    for light in button.lights:
        average_light += light * (1 / 12)
    background_light = average_light * (1 / 2)
    pygame.draw.circle(surface, to_color(background_light), center, 20)

    pygame.draw.circle(surface, (100, 100, 100), center, 20, 1)
    for index, light in enumerate(button.lights):
        offset = Vector2(0, -12).rotate(15).rotate(index * 30)
        pygame.draw.circle(surface, to_color(background_light | light), center + offset, 2)

    if key_char is not None:
        key_light = background_light + Light(0.7, 0.7, 0.7)
        font.render_to(surface, center + Vector2(-4, -4), key_char.upper(), to_color(key_light))


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


def emulate(game, keyboard_layout):
    pygame.init()
    screen = pygame.display.set_mode(size=(800, 600), vsync=1)
    pygame.display.set_caption(game.name)
    font = SysFont(name="Monospace", size=11)
    clock = Clock()
    handle_interrupts()

    running = True
    while running:
        if is_interrupted():
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed_buttons = get_pressed_buttons(keyboard_layout)
        game.update(pressed_buttons)
        board = game.render(pressed_buttons)
        draw_board(screen, font, keyboard_layout, board)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def select_keyboard_layout() -> str:
    options = list(KEYBOARD_LAYOUTS)
    index = select("Select keyboard layout:", options)
    return KEYBOARD_LAYOUTS[options[index]]


if __name__ == "__main__":
    emulate(select_game(), select_keyboard_layout())
