from __future__ import annotations

import unittest
from src.arena_game import ArenaGame
from src.types import Coordinate, Dot, SnakeColor


class ColorDotsAndShrinkingTest(unittest.TestCase):
    def test_snake_passing_through_green_dot_shrinks_green_snake(self) -> None:
        # Given a green snake with length 5 and a green dot on the board directly in its path
        # Player head at (5, 10), moving Right towards (6, 10)
        green_dot = Dot(coordinate=Coordinate(6, 10), color=SnakeColor.GREEN)
        game = ArenaGame(
            width=20,
            height=20,
            dots=[green_dot],
        )

        player_snake = game.player_snake
        self.assertEqual(player_snake.length, 5)

        # When any snake moves through the green dot
        game.step()

        # Then the green snake loses a square and its length becomes 4
        self.assertEqual(player_snake.head, Coordinate(6, 10))
        self.assertEqual(player_snake.length, 4)

    def test_passing_through_red_and_orange_dots_shrinks_matching_snakes(self) -> None:
        # Given a red snake and orange snake with length 5
        # Red dot in path of green snake at (6, 10)
        red_dot = Dot(coordinate=Coordinate(6, 10), color=SnakeColor.RED)
        game = ArenaGame(
            width=20,
            height=20,
            dots=[red_dot],
        )

        red_snake = game.npc_red
        self.assertEqual(red_snake.length, 5)

        # When a snake moves through a red dot
        game.step()

        # Then the red snake loses a square
        self.assertEqual(red_snake.length, 4)

        # And when a snake moves through an orange dot
        # Next step: green snake head at (6, 10), moving Right towards (7, 10)
        orange_dot = Dot(coordinate=Coordinate(7, 10), color=SnakeColor.ORANGE)
        game.add_dot(orange_dot)
        orange_snake = game.npc_orange
        self.assertEqual(orange_snake.length, 5)

        game.step()

        # Then the orange snake loses a square
        self.assertEqual(orange_snake.length, 4)


if __name__ == "__main__":
    unittest.main()
