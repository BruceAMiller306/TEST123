from __future__ import annotations

import unittest
from src.snake_game import SnakeGame
from src.types import Coordinate, Direction, GameStatus, MoveResult


class SnakeCollisionsAndGameOverTest(unittest.TestCase):
    def test_wall_collision_triggers_game_over(self) -> None:
        # Given a snake head at the right boundary (19, 10) moving Right
        body = [Coordinate(19, 10), Coordinate(18, 10), Coordinate(17, 10)]
        game = SnakeGame(
            width=20,
            height=20,
            initial_body=body,
            initial_direction=Direction.RIGHT,
        )

        # When the game advances 1 tick
        result = game.step()

        # Then the snake collides with the wall
        self.assertEqual(result, MoveResult.COLLIDED_WALL)
        # And the game status is Game Over
        self.assertEqual(game.status, GameStatus.GAME_OVER)
        self.assertTrue(game.is_game_over)

    def test_self_collision_triggers_game_over(self) -> None:
        # Given a snake curled such that moving Down hits its own body
        # Head at (5, 5), body at (5, 6), (4, 6), (4, 5)
        # Moving Down from (5, 5) will step into (5, 6)
        body = [
            Coordinate(5, 5),
            Coordinate(4, 5),
            Coordinate(4, 6),
            Coordinate(5, 6),
            Coordinate(6, 6),
        ]
        game = SnakeGame(
            width=20,
            height=20,
            initial_body=body,
            initial_direction=Direction.DOWN,
        )

        # When the game advances 1 tick
        result = game.step()

        # Then the snake collides with itself
        self.assertEqual(result, MoveResult.COLLIDED_SELF)
        # And the game status is Game Over
        self.assertEqual(game.status, GameStatus.GAME_OVER)
        self.assertTrue(game.is_game_over)


if __name__ == "__main__":
    unittest.main()
