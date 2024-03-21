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
                    paddle_y=(
                        self.__board._paddles[0].rect.y
                        if ROLE == "HOST"
                        else self.__board._paddles[1].rect.y
                    ),
                    ball_position=self.__board._ball.position,
                    ball_velocity=self.__board._ball.velocity,
                    score=self.__board._scores,
                ),
            )
            self.last_sent = time.time()

        if not self.output_queue.empty():
            packet = receive_packet(self.output_queue)
            if ROLE != "HOST":
                self.__board._ball.position = packet.ball_position
                self.__board._ball.velocity = packet.ball_velocity
                self.__board._scores = packet.score
                self.__board._paddles[0].rect.y = packet.paddle_y
            else:
                self.__board._paddles[1].rect.y = packet.paddle_y

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        keys = pg.key.get_pressed()
        directions = [None, None]

        if keys[pg.K_w]:
            directions[0 if ROLE == "HOST" else 1] = "up"
        elif keys[pg.K_s]:
            directions[0 if ROLE == "HOST" else 1] = "down"

        self.window.fill((0, 0, 0))
        self.__board.update(directions=directions)
        self.__board.draw(window=self.window)
        self._draw_scores(self.__board.scores)

        pg.display.flip()

    def start(self) -> None:
        self.running = True

        while self.running:
            self.update()
            self.clock.tick(GAME_FPS)
