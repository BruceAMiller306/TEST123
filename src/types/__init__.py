"""Shared types for the whole application. Define each type once, here."""

from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def delta_x(self) -> int:
        return self.value[0]

    @property
    def delta_y(self) -> int:
        return self.value[1]

    def is_opposite(self, other: Direction) -> bool:
        return (self.delta_x + other.delta_x == 0) and (
            self.delta_y + other.delta_y == 0
        )


class Coordinate(NamedTuple):
    x: int
    y: int

    def translate(self, direction: Direction) -> Coordinate:
        return Coordinate(self.x + direction.delta_x, self.y + direction.delta_y)


class GameStatus(str, Enum):
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    GAME_OVER = "game_over"

    def __str__(self) -> str:
        return self.value


class MoveResult(str, Enum):
    MOVED = "moved"
    ATE_FOOD = "ate_food"
    COLLIDED_WALL = "collided_wall"
    COLLIDED_SELF = "collided_self"


class InvalidMoveError(ValueError):
    """Raised when an invalid game move or state transition is requested."""
