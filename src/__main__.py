"""Entry point: `python -m src` runs the application."""

from __future__ import annotations

import sys
from src.terminal_snake_ui import TerminalSnakeUI


def main() -> None:
    ui = TerminalSnakeUI()
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Snake Game: Ready.")
        print(ui.render())
        return

    ui.run()


if __name__ == "__main__":
    main()
