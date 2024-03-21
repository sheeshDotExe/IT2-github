from .components import (
    Board,
    connect,
    send_packet,
    receive_packet,
    Packet,
    PLAYER_NAME,
    ROLE,
)
import pygame as pg
import time

GAME_FPS = 24
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 650
BOARD_WIDTH, BOARD_HEIGHT = 900, 450

PACKET_SEND_RATE = 0.05


def mirror_position(position: tuple[int, int]) -> tuple[int, int]:
    return (WINDOW_WIDTH - position[0], position[1])


def mirror_velocity(velocity: tuple[int, int]) -> tuple[int, int]:
    return (-velocity[0], velocity[1])


class Game:
    def __init__(self) -> None:
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.window.fill((0, 0, 0))
        self.__board = Board(window=self.window, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.clock = pg.time.Clock()
        self.last_sent = time.time()
        self.input_queue, self.output_queue = connect()

    def _draw_scores(self, scores: list[int]) -> None: ...

    def update(self) -> None:

        if time.time() - self.last_sent > PACKET_SEND_RATE:
            send_packet(
                self.input_queue,
                Packet(
                    sender=PLAYER_NAME,
                    paddle_y=(self.__board._paddles[0].rect.y),
                    ball_position=mirror_position(self.__board._ball.position),
                    ball_velocity=mirror_velocity(self.__board._ball.velocity),
                    score=self.__board._scores,
                ),
            )
            self.last_sent = time.time()

        if not self.output_queue.empty():
            packet = receive_packet(self.output_queue)
            self.__board._paddles[1].rect.y = packet.paddle_y
            if ROLE != "HOST":
                self.__board._ball.position = packet.ball_position
                self.__board._ball.velocity = packet.ball_velocity
                self.__board._scores = packet.score

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        keys = pg.key.get_pressed()
        direction = None

        if keys[pg.K_w]:
            direction = "up"
        elif keys[pg.K_s]:
            direction = "down"

        self.window.fill((0, 0, 0))
        self.__board.update(direction=direction)
        self.__board.draw(window=self.window)
        self._draw_scores(self.__board.scores)

        pg.display.flip()

    def start(self) -> None:
        self.running = True

        while self.running:
            self.update()
            self.clock.tick(GAME_FPS)
