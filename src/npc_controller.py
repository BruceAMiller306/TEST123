from __future__ import annotations

from src.types import Coordinate, Direction


class NPCController:
    @staticmethod
    def choose_attack_direction(
        current_head: Coordinate,
        current_direction: Direction,
        target_head: Coordinate,
        board_width: int,
        board_height: int,
        occupied_cells: set[Coordinate] | None = None,
    ) -> Direction:
        occupied = occupied_cells if occupied_cells is not None else set()
        candidates: list[Direction] = [
            d for d in Direction if not current_direction.is_opposite(d)
        ]

        def distance_to_target(d: Direction) -> float:
            next_coord = current_head.translate(d)
            # Heavy penalty if moving out of bounds or into occupied cell
            is_out_of_bounds = (
                next_coord.x < 0
                or next_coord.x >= board_width
                or next_coord.y < 0
                or next_coord.y >= board_height
            )
            is_occupied = next_coord in occupied
            penalty = 1000.0 if (is_out_of_bounds or is_occupied) else 0.0
            manhattan = abs(next_coord.x - target_head.x) + abs(
                next_coord.y - target_head.y
            )
            return penalty + manhattan

        candidates.sort(key=distance_to_target)
        return candidates[0]
