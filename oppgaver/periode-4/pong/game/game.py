from .components import Board
import pygame as pg

GAME_FPS = 24
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 650
BOARD_WIDTH, BOARD_HEIGHT = 900, 450


class Game:
    def __init__(self) -> None:
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.window.fill((0, 0, 0))
        self.__board = Board(window=self.window, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.clock = pg.time.Clock()

    def _draw_scores(self, scores: list[int]) -> None: ...

    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        keys = pg.key.get_pressed()
        directions = [None, None]

        if keys[pg.K_w]:
            directions[0] = "up"
        elif keys[pg.K_s]:
            directions[0] = "down"

        if keys[pg.K_UP]:
            directions[1] = "up"
        elif keys[pg.K_DOWN]:
            directions[1] = "down"

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
