from __future__ import annotations

import unittest
from src.arena_game import ArenaGame
from src.types import Coordinate, Dot, GameStatus, SnakeColor


class SnakeEliminationTest(unittest.TestCase):
    def test_snake_with_length_one_is_eliminated_when_eating_matching_dot(self) -> None:
        # Given a green snake with length 1 and a green dot directly ahead
        green_dot = Dot(coordinate=Coordinate(6, 10), color=SnakeColor.GREEN)
        game = ArenaGame(
            width=20,
            height=20,
            player_body=[Coordinate(5, 10)],
            dots=[green_dot],
        )

        player_snake = game.player_snake
        self.assertEqual(player_snake.length, 1)
        self.assertTrue(player_snake.is_alive)

        # When a snake moves through a dot matching its color
        game.step()

        # Then that snake has no squares remaining and is eliminated
        self.assertEqual(player_snake.length, 0)
        self.assertFalse(player_snake.is_alive)
        self.assertEqual(game.status, GameStatus.GAME_OVER)


if __name__ == "__main__":
    unittest.main()
