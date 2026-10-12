from __future__ import annotations

import random
from typing import Sequence
from src.types import Coordinate


class FoodSpawner:
    def __init__(
        self,
        deterministic_positions: Sequence[Coordinate] | None = None,
        random_generator: random.Random | None = None,
    ) -> None:
        self._positions_queue: list[Coordinate] = (
            list(deterministic_positions)
            if deterministic_positions is not None
            else []
        )
        self._random: random.Random = (
            random_generator if random_generator is not None else random.Random()
        )

    def spawn(
        self,
        board_width: int,
        board_height: int,
        occupied_positions: set[Coordinate],
    ) -> Coordinate | None:
        if self._positions_queue:
            return self._positions_queue.pop(0)

        all_empty_positions = [
            Coordinate(x, y)
            for x in range(board_width)
            for y in range(board_height)
            if Coordinate(x, y) not in occupied_positions
        ]
        if not all_empty_positions:
            return None
        return self._random.choice(all_empty_positions)
