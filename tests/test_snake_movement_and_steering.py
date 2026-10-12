from __future__ import annotations

import unittest
from src.snake_game import SnakeGame
from src.types import Coordinate, Direction, MoveResult


class SnakeMovementAndSteeringTest(unittest.TestCase):
    def test_snake_advances_head_and_maintains_length(self) -> None:
        # Given a new game on a 20x20 board with a snake facing Right
        game = SnakeGame(width=20, height=20, initial_direction=Direction.RIGHT)
        initial_head = game.head
        initial_length = len(game.snake)

        # When the game advances 1 tick
        result = game.step()

        # Then the snake's head advances by 1 cell to the right
        self.assertEqual(result, MoveResult.MOVED)
        self.assertEqual(
            game.head, Coordinate(initial_head.x + 1, initial_head.y)
        )
        # And the snake length remains unchanged
        self.assertEqual(len(game.snake), initial_length)

    def test_immediate_180_degree_reversal_is_ignored(self) -> None:
        # Given a snake moving Right
        game = SnakeGame(width=20, height=20, initial_direction=Direction.RIGHT)
        self.assertEqual(game.direction, Direction.RIGHT)

        # When the player attempts to steer Left
        accepted = game.change_direction(Direction.LEFT)

        # Then the heading remains Right (180-degree reversal is ignored)
        self.assertFalse(accepted)
        self.assertEqual(game.direction, Direction.RIGHT)
        game.step()
        self.assertEqual(game.direction, Direction.RIGHT)


if __name__ == "__main__":
    unittest.main()
