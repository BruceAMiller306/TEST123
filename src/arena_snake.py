from __future__ import annotations

from typing import Sequence
from src.types import Coordinate, Direction, SnakeColor, SnakeRole


class ArenaSnake:
    def __init__(
        self,
        color: SnakeColor,
        role: SnakeRole,
        initial_body: Sequence[Coordinate],
        initial_direction: Direction,
    ) -> None:
        self._color: SnakeColor = color
        self._role: SnakeRole = role
        self._body: list[Coordinate] = list(initial_body)
        self._direction: Direction = initial_direction
        self._is_alive: bool = len(self._body) > 0

    @property
    def color(self) -> SnakeColor:
        return self._color

    @property
    def role(self) -> SnakeRole:
        return self._role

    @property
    def body(self) -> list[Coordinate]:
        return list(self._body)

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @property
    def length(self) -> int:
        return len(self._body)

    @property
    def head(self) -> Coordinate:
        if not self._body:
            raise IndexError("Snake has no body segments.")
        return self._body[0]

    def steer(self, new_direction: Direction) -> bool:
        if not self._is_alive or self._direction.is_opposite(new_direction):
            return False
        self._direction = new_direction
        return True

    def advance(self, new_head: Coordinate) -> None:
        if not self._is_alive:
            return
        self._body.insert(0, new_head)
        self._body.pop()

    def lose_square(self) -> None:
        if not self._is_alive:
            return
        if self._body:
            self._body.pop()
        if len(self._body) == 0:
            self._is_alive = False
