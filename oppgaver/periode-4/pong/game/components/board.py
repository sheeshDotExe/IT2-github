from typing import Optional
import pygame as pg
import random
from .ball import Ball, BALL_Y_MOVEMENT_VELOCITIES, BALL_RADIUS
from .paddle import Paddle

NUMBER_OF_PLAYERS = 2
BORDER_COLOR = (0, 255, 0)

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100


class Board:
    def __init__(self, window, width, height) -> None:
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(center=window.get_rect().center)

        self._ball = Ball(
            position=self.rect.center,
            initial_velocity=(10, random.choice(BALL_Y_MOVEMENT_VELOCITIES)),
        )

        paddle_positions = [
            (self.rect.left + 30, self.rect.centery),
            (self.rect.right - 30, self.rect.centery),
        ]

        self._paddles = [
            Paddle(
                position=paddle_positions[i], dimensions=(PADDLE_WIDTH, PADDLE_HEIGHT)
            )
            for i in range(NUMBER_OF_PLAYERS)
        ]
        self._scores = [0 for _ in range(NUMBER_OF_PLAYERS)]

    @property
    def scores(self) -> list[int]:
        return self._scores

    def check_collision(self):
        # check if ball collides with the top or bottom of the board
        if (
            self._ball.position[1] <= self.rect.top + BALL_RADIUS
            or self._ball.position[1] >= self.rect.bottom - BALL_RADIUS
        ):
            self._ball.velocity = (self._ball.velocity[0], -self._ball.velocity[1])

        # check if ball collides with the paddles
        for i, paddle in enumerate(self._paddles):
            if paddle.rect.collidepoint(*self._ball.position):
                self._ball.velocity = (
                    -self._ball.velocity[0],
                    random.choice(BALL_Y_MOVEMENT_VELOCITIES),
                )

        # check if ball collides with the left or right of the board
        if (
            self._ball.position[0] <= self.rect.left
            or self._ball.position[0] >= self.rect.right
        ):
            if self._ball.position[0] <= self.rect.left:
                self._scores[1] += 1
            else:
                self._scores[0] += 1

            self._ball.position = self.rect.center

    def update(self, direction: Optional[str]) -> None:
        self.check_collision()

        # update the ball
        self._ball.update()

        # update the paddles
        self._paddles[0].move(direction, border_rect=self.rect)

    def draw(self, window) -> None:
        # draw the border of the board
        pg.draw.rect(window, BORDER_COLOR, self.rect, width=2)

        # draw the middle line splitting the board
        pg.draw.line(
            window, BORDER_COLOR, self.rect.midtop, self.rect.midbottom, width=2
        )

        # draw the ball
        self._ball.draw(window)

        # draw the paddles
        for paddle in self._paddles:
            paddle.draw(window)
