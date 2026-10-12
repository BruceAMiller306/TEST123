from __future__ import annotations

import unittest
from src.npc_controller import NPCController
from src.types import Coordinate, Direction


class NPCAttacksGreenSnakeTest(unittest.TestCase):
    def test_npc_chooses_direction_closing_distance_to_green_snake(self) -> None:
        # Given an NPC snake at (10, 5) heading Down and a green snake at (10, 10)
        npc_head = Coordinate(10, 5)
        npc_dir = Direction.DOWN
        target_head = Coordinate(10, 10)

        # When the NPC snake makes a move decision
        chosen_dir = NPCController.choose_attack_direction(
            current_head=npc_head,
            current_direction=npc_dir,
            target_head=target_head,
            board_width=20,
            board_height=20,
        )

        # Then it chooses a direction that moves its head closer towards the green snake (Down)
        self.assertEqual(chosen_dir, Direction.DOWN)

    def test_npc_turns_towards_green_snake_when_misaligned(self) -> None:
        # Given an NPC snake at (5, 5) heading Down and a green snake at (10, 5)
        npc_head = Coordinate(5, 5)
        npc_dir = Direction.DOWN
        target_head = Coordinate(10, 5)

        chosen_dir = NPCController.choose_attack_direction(
            current_head=npc_head,
            current_direction=npc_dir,
            target_head=target_head,
            board_width=20,
            board_height=20,
        )

        # Moving Right closes horizontal distance to target (10, 5)
        self.assertEqual(chosen_dir, Direction.RIGHT)


if __name__ == "__main__":
    unittest.main()
