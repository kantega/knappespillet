from Menu import Menu
from games.TimeBombs import TimeBombs
from games.TapDance import TapDance
from games.TapTendrils import TapTendrils
from games.TestAlignment import TestAlignment
from games.TestCounter import TestCounter
from games.TestMarquee import TestMarquee
from games.CatchTheLight import CatchTheLight


def select_game() -> any:
    games = [
        Menu(),
        TapDance(),
        TapTendrils(),
        TimeBombs(),
        CatchTheLight(),
        TestAlignment(),
        TestCounter(),
        TestMarquee(),
    ]
    options = [f"{game.name} - {game.desc}" for game in games]
    index = select("Select game:", options)
    return games[index]


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
