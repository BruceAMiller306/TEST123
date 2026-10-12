from __future__ import annotations

from typing import Sequence
from src.food_spawner import FoodSpawner
from src.types import Coordinate, Direction, GameStatus, MoveResult


class SnakeGame:
    def __init__(
        self,
        width: int = 20,
        height: int = 20,
        initial_body: Sequence[Coordinate] | None = None,
        initial_direction: Direction = Direction.RIGHT,
        food_spawner: FoodSpawner | None = None,
        initial_food: Coordinate | None = None,
    ) -> None:
        self._width: int = width
        self._height: int = height
        self._direction: Direction = initial_direction
        self._pending_direction: Direction = initial_direction
        self._status: GameStatus = GameStatus.READY
        self._score: int = 0
        self._food_spawner: FoodSpawner = (
            food_spawner if food_spawner is not None else FoodSpawner()
        )

        if initial_body is not None:
            self._snake: list[Coordinate] = list(initial_body)
        else:
            mid_x = width // 2
            mid_y = height // 2
            self._snake = [
                Coordinate(mid_x, mid_y),
                Coordinate(mid_x - 1, mid_y),
                Coordinate(mid_x - 2, mid_y),
            ]

        if initial_food is not None:
            self._food: Coordinate | None = initial_food
        else:
            self._food = self._food_spawner.spawn(
                self._width, self._height, set(self._snake)
            )

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def snake(self) -> list[Coordinate]:
        return list(self._snake)

    @property
    def head(self) -> Coordinate:
        return self._snake[0]

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def food(self) -> Coordinate | None:
        return self._food

    @property
    def score(self) -> int:
        return self._score

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def is_game_over(self) -> bool:
        return self._status == GameStatus.GAME_OVER

    def change_direction(self, new_direction: Direction) -> bool:
        if self._status == GameStatus.GAME_OVER:
            return False
        if self._direction.is_opposite(new_direction):
            return False
        self._pending_direction = new_direction
        return True

    def step(self) -> MoveResult:
        if self._status == GameStatus.READY:
            self._status = GameStatus.RUNNING

        if self._status == GameStatus.GAME_OVER:
            return MoveResult.COLLIDED_WALL

        self._direction = self._pending_direction
        new_head = self.head.translate(self._direction)

        if (
            new_head.x < 0
            or new_head.x >= self._width
            or new_head.y < 0
            or new_head.y >= self._height
        ):
            self._status = GameStatus.GAME_OVER
            return MoveResult.COLLIDED_WALL

        ate_food = self._food is not None and new_head == self._food
        body_to_check = self._snake if ate_food else self._snake[:-1]
        if new_head in body_to_check:
            self._status = GameStatus.GAME_OVER
            return MoveResult.COLLIDED_SELF

        self._snake.insert(0, new_head)
        if ate_food:
            self._score += 1
            self._food = self._food_spawner.spawn(
                self._width, self._height, set(self._snake)
            )
            return MoveResult.ATE_FOOD

        self._snake.pop()
        return MoveResult.MOVED

    def restart(self) -> None:
        mid_x = self._width // 2
        mid_y = self._height // 2
        self._snake = [
            Coordinate(mid_x, mid_y),
            Coordinate(mid_x - 1, mid_y),
            Coordinate(mid_x - 2, mid_y),
        ]
        self._direction = Direction.RIGHT
        self._pending_direction = Direction.RIGHT
        self._status = GameStatus.READY
        self._score = 0
        self._food = self._food_spawner.spawn(
            self._width, self._height, set(self._snake)
        )
