from __future__ import annotations

import unittest
from src.food_spawner import FoodSpawner
from src.snake_game import SnakeGame
from src.types import Coordinate, Direction, MoveResult


class EatingFoodAndGrowingTest(unittest.TestCase):
    def test_eating_food_increases_score_and_grows_snake(self) -> None:
        # Given a snake with head at (5, 5) moving Right and food at (6, 5)
        body = [Coordinate(5, 5), Coordinate(4, 5), Coordinate(3, 5)]
        next_food_location = Coordinate(10, 10)
        spawner = FoodSpawner(deterministic_positions=[next_food_location])
        game = SnakeGame(
            width=20,
            height=20,
            initial_body=body,
            initial_direction=Direction.RIGHT,
            initial_food=Coordinate(6, 5),
            food_spawner=spawner,
        )
        initial_length = len(game.snake)
        initial_score = game.score

        # When the game advances 1 tick
        result = game.step()

        # Then the snake eats the food
        self.assertEqual(result, MoveResult.ATE_FOOD)
        self.assertEqual(game.head, Coordinate(6, 5))

        # And the player score increases by 1
        self.assertEqual(game.score, initial_score + 1)

        # And the snake length increases by 1
        self.assertEqual(len(game.snake), initial_length + 1)

        # And new food spawns on an unoccupied board cell
        self.assertEqual(game.food, next_food_location)
        self.assertNotIn(game.food, game.snake)


if __name__ == "__main__":
    unittest.main()
