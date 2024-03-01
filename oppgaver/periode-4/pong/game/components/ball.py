import pygame as pg

BALL_RADIUS = 10
BALL_COLOR = (0, 255, 0)
BALL_Y_MOVEMENT_VELOCITIES = [-8, 8]


class Ball:
    def __init__(
        self, position: tuple[int, int], initial_velocity: tuple[int, int]
    ) -> None:
        self.position = position
        self.velocity = initial_velocity

    def set_velocity(self, velocity: tuple[int, int]) -> None:
        self.velocity = velocity

    def update(self) -> None:
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )

    def draw(self, window) -> None:
        pg.draw.circle(window, BALL_COLOR, self.position, BALL_RADIUS)
