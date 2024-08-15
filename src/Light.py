from typing import Self

from utils import clamp


class Light:
    def __init__(self, red: float = 0, green: float = 0, blue: float = 0):
        self.red = clamp(0, red, 1)
        self.green = clamp(0, green, 1)
        self.blue = clamp(0, blue, 1)

    def __add__(self, other: Self) -> Self:
        return Light(
            self.red + other.red,
            self.green + other.green,
            self.blue + other.blue,
        )

    def __mul__(self, other: float) -> Self:
        return Light(
            self.red * other,
            self.green * other,
            self.blue * other,
        )

    def __or__(self, other: Self) -> Self:
        return Light(
            max(self.red, other.red),
            max(self.green, other.green),
            max(self.blue, other.blue),
        )


RED = Light(1, 0, 0)
GREEN = Light(0, 1, 0)
BLUE = Light(0, 0, 1)
CYAN = Light(0, 1, 1)
MAGENTA = Light(1, 0, 1)
YELLOW = Light(1, 1, 0)
WHITE = Light(1, 1, 1)
