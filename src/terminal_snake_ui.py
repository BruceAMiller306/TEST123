from __future__ import annotations

import select
import sys
import time
from typing import TextIO
from src.snake_game import SnakeGame
from src.types import Coordinate, Direction, GameStatus


def render_board(game: SnakeGame) -> str:
    lines: list[str] = []
    lines.append(f"+{'-' * game.width}+")
    snake_set = set(game.snake)
    snake_head = game.head

    for y in range(game.height):
        row_chars: list[str] = ["|"]
        for x in range(game.width):
            coord = Coordinate(x, y)
            if coord == snake_head:
                row_chars.append("O")
            elif coord in snake_set:
                row_chars.append("o")
            elif game.food is not None and coord == game.food:
                row_chars.append("*")
            else:
                row_chars.append(" ")
        row_chars.append("|")
        lines.append("".join(row_chars))

    lines.append(f"+{'-' * game.width}+")
    lines.append(f"Score: {game.score} | Status: {game.status.value.upper()}")
    return "\n".join(lines)


class TerminalSnakeUI:
    def __init__(
        self,
        game: SnakeGame | None = None,
        output_stream: TextIO = sys.stdout,
    ) -> None:
        self._game: SnakeGame = game if game is not None else SnakeGame()
        self._output_stream: TextIO = output_stream

    @property
    def game(self) -> SnakeGame:
        return self._game

    def render(self) -> str:
        return render_board(self._game)

    def draw(self) -> None:
        # Clear screen and draw
        self._output_stream.write("\033[H\033[J")
        self._output_stream.write(self.render() + "\n")
        self._output_stream.write("Controls: [W/A/S/D] Steer | [R] Restart | [Q] Quit\n")
        if self._game.is_game_over:
            self._output_stream.write("*** GAME OVER! Press [R] to restart or [Q] to quit ***\n")
        self._output_stream.flush()

    def run(self, tick_seconds: float = 0.15) -> None:
        if not sys.stdin.isatty():
            self._output_stream.write("Snake Game: Ready.\n")
            self._output_stream.write(self.render() + "\n")
            return

        try:
            import termios
            import tty
        except ImportError:
            # Fallback for systems without termios
            self._output_stream.write("Interactive terminal controls require termios support.\n")
            return

        old_settings = termios.tcgetattr(sys.stdin.fileno())
        try:
            tty.setcbreak(sys.stdin.fileno())
            self.draw()

            while True:
                rlist, _, _ = select.select([sys.stdin], [], [], tick_seconds)
                if rlist:
                    ch = sys.stdin.read(1)
                    if ch in ("q", "Q", "\x03"):  # q or Ctrl+C
                        break
                    elif ch in ("r", "R"):
                        self._game.restart()
                    elif ch in ("w", "W"):
                        self._game.change_direction(Direction.UP)
                    elif ch in ("s", "S"):
                        self._game.change_direction(Direction.DOWN)
                    elif ch in ("a", "A"):
                        self._game.change_direction(Direction.LEFT)
                    elif ch in ("d", "D"):
                        self._game.change_direction(Direction.RIGHT)
                    elif ch == "\x1b":  # Arrow escape sequence
                        next_two = sys.stdin.read(2)
                        if next_two == "[A":
                            self._game.change_direction(Direction.UP)
                        elif next_two == "[B":
                            self._game.change_direction(Direction.DOWN)
                        elif next_two == "[C":
                            self._game.change_direction(Direction.RIGHT)
                        elif next_two == "[D":
                            self._game.change_direction(Direction.LEFT)

                if not self._game.is_game_over:
                    self._game.step()
                self.draw()
        finally:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)
            self._output_stream.write("\nThanks for playing Snake!\n")
            self._output_stream.flush()
