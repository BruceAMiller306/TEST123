from __future__ import annotations

import unittest
from src.arena_game import ArenaGame
from src.html_game_generator import generate_html_game
from src.types import SnakeColor, SnakeRole


class SnakesInitializationAndAppearanceTest(unittest.TestCase):
    def test_three_snakes_initialized_with_length_five(self) -> None:
        # Given a new game on a 4-inch by 4-inch black board
        game = ArenaGame(width=20, height=20)

        # When the game starts
        # Then there are 3 snakes: one green player snake, one red NPC snake, and one orange NPC snake
        self.assertEqual(len(game.snakes), 3)

        player_snake = game.get_snake(SnakeColor.GREEN)
        self.assertIsNotNone(player_snake)
        assert player_snake is not None
        self.assertEqual(player_snake.role, SnakeRole.PLAYER)
        self.assertEqual(player_snake.color, SnakeColor.GREEN)

        npc_red = game.get_snake(SnakeColor.RED)
        self.assertIsNotNone(npc_red)
        assert npc_red is not None
        self.assertEqual(npc_red.role, SnakeRole.NPC)
        self.assertEqual(npc_red.color, SnakeColor.RED)

        npc_orange = game.get_snake(SnakeColor.ORANGE)
        self.assertIsNotNone(npc_orange)
        assert npc_orange is not None
        self.assertEqual(npc_orange.role, SnakeRole.NPC)
        self.assertEqual(npc_orange.color, SnakeColor.ORANGE)

        # And each snake has an initial length of 5 squares
        self.assertEqual(player_snake.length, 5)
        self.assertEqual(npc_red.length, 5)
        self.assertEqual(npc_orange.length, 5)

    def test_html_specifies_four_inch_dimensions_and_black_background(self) -> None:
        # Given the HTML-based game generator
        html = generate_html_game()

        # Then the board container is 4in by 4in with a black background
        self.assertIn("width: 4in;", html)
        self.assertIn("height: 4in;", html)
        self.assertIn("background-color: #000000;", html)


if __name__ == "__main__":
    unittest.main()
