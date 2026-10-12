from __future__ import annotations

import random
from typing import Sequence
from src.arena_snake import ArenaSnake
from src.npc_controller import NPCController
from src.types import Coordinate, Direction, Dot, GameStatus, SnakeColor, SnakeRole


class ArenaGame:
    def __init__(
        self,
        width: int = 20,
        height: int = 20,
        player_body: Sequence[Coordinate] | None = None,
        red_npc_body: Sequence[Coordinate] | None = None,
        orange_npc_body: Sequence[Coordinate] | None = None,
        dots: Sequence[Dot] | None = None,
        random_generator: random.Random | None = None,
        wrap_around: bool = True,
    ) -> None:
        self._width: int = width
        self._height: int = height
        self._wrap_around: bool = wrap_around
        self._random: random.Random = (
            random_generator if random_generator is not None else random.Random()
        )

        # Initialize Green Player snake (length 5)
        if player_body is not None:
            p_body = list(player_body)
        else:
            p_body = [
                Coordinate(5, 10),
                Coordinate(4, 10),
                Coordinate(3, 10),
                Coordinate(2, 10),
                Coordinate(1, 10),
            ]
        self._player_snake: ArenaSnake = ArenaSnake(
            color=SnakeColor.GREEN,
            role=SnakeRole.PLAYER,
            initial_body=p_body,
            initial_direction=Direction.RIGHT,
        )

        # Initialize Red NPC snake (length 5)
        if red_npc_body is not None:
            r_body = list(red_npc_body)
        else:
            r_body = [
                Coordinate(15, 5),
                Coordinate(15, 4),
                Coordinate(15, 3),
                Coordinate(15, 2),
                Coordinate(15, 1),
            ]
        self._npc_red: ArenaSnake = ArenaSnake(
            color=SnakeColor.RED,
            role=SnakeRole.NPC,
            initial_body=r_body,
            initial_direction=Direction.DOWN,
        )

        # Initialize Orange NPC snake (length 5)
        if orange_npc_body is not None:
            o_body = list(orange_npc_body)
        else:
            o_body = [
                Coordinate(15, 15),
                Coordinate(15, 16),
                Coordinate(15, 17),
                Coordinate(15, 18),
                Coordinate(15, 19),
            ]
        self._npc_orange: ArenaSnake = ArenaSnake(
            color=SnakeColor.ORANGE,
            role=SnakeRole.NPC,
            initial_body=o_body,
            initial_direction=Direction.UP,
        )

        self._dots: list[Dot] = []
        if dots is not None:
            self._dots = list(dots)
        else:
            self._spawn_initial_dots()

        self._status: GameStatus = GameStatus.READY

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def player_snake(self) -> ArenaSnake:
        return self._player_snake

    @property
    def npc_red(self) -> ArenaSnake:
        return self._npc_red

    @property
    def npc_orange(self) -> ArenaSnake:
        return self._npc_orange

    @property
    def snakes(self) -> list[ArenaSnake]:
        return [self._player_snake, self._npc_red, self._npc_orange]

    @property
    def dots(self) -> list[Dot]:
        return list(self._dots)

    @property
    def status(self) -> GameStatus:
        return self._status

    def get_snake(self, color: SnakeColor) -> ArenaSnake | None:
        for snake in self.snakes:
            if snake.color == color:
                return snake
        return None

    def add_dot(self, dot: Dot) -> None:
        self._dots.append(dot)

    def _spawn_initial_dots(self) -> None:
        for color in (SnakeColor.GREEN, SnakeColor.RED, SnakeColor.ORANGE):
            dot = self._spawn_dot(color)
            if dot is not None:
                self._dots.append(dot)

    def _spawn_dot(self, color: SnakeColor) -> Dot | None:
        occupied = set()
        for snake in self.snakes:
            occupied.update(snake.body)
        for d in self._dots:
            occupied.add(d.coordinate)

        empty_coords = [
            Coordinate(x, y)
            for x in range(self._width)
            for y in range(self._height)
            if Coordinate(x, y) not in occupied
        ]
        if not empty_coords:
            return None
        chosen = self._random.choice(empty_coords)
        return Dot(coordinate=chosen, color=color)

    def steer_player(self, direction: Direction) -> bool:
        return self._player_snake.steer(direction)

    def step(self) -> None:
        if self._status == GameStatus.READY:
            self._status = GameStatus.RUNNING

        # 1. NPCs make decisions attacking green snake
        if self._player_snake.is_alive:
            target = self._player_snake.head
            occupied = set()
            for s in self.snakes:
                occupied.update(s.body)

            if self._npc_red.is_alive:
                next_dir = NPCController.choose_attack_direction(
                    self._npc_red.head,
                    self._npc_red.direction,
                    target,
                    self._width,
                    self._height,
                    occupied,
                )
                self._npc_red.steer(next_dir)

            if self._npc_orange.is_alive:
                next_dir = NPCController.choose_attack_direction(
                    self._npc_orange.head,
                    self._npc_orange.direction,
                    target,
                    self._width,
                    self._height,
                    occupied,
                )
                self._npc_orange.steer(next_dir)

        # 2. Advance alive snakes
        for snake in self.snakes:
            if snake.is_alive:
                raw_head = snake.head.translate(snake.direction)
                if self._wrap_around:
                    wrapped_head = Coordinate(
                        raw_head.x % self._width, raw_head.y % self._height
                    )
                else:
                    wrapped_head = raw_head
                snake.advance(wrapped_head)

        # 3. Check dot collisions
        remaining_dots: list[Dot] = []
        for dot in self._dots:
            consumed = False
            for snake in self.snakes:
                if snake.is_alive and snake.head == dot.coordinate:
                    consumed = True
                    # The snake with that dot's color loses a square
                    matching_snake = self.get_snake(dot.color)
                    if matching_snake is not None:
                        matching_snake.lose_square()
                    break

            if not consumed:
                remaining_dots.append(dot)
            else:
                replacement = self._spawn_dot(dot.color)
                if replacement is not None:
                    remaining_dots.append(replacement)

        self._dots = remaining_dots

        # 4. Check game status
        if not self._player_snake.is_alive:
            self._status = GameStatus.GAME_OVER
        elif not self._npc_red.is_alive and not self._npc_orange.is_alive:
            self._status = GameStatus.PLAYER_WON
        else:
            self._status = GameStatus.RUNNING
