import pygame as pg
from typing import Optional

PADDLE_COLOR = (0, 255, 0)
PADDLE_VELOCITY = 5  # pixels per frame


class Paddle:
    def __init__(self, position: tuple[int, int], dimensions: tuple[int, int]) -> None:
        self.width, self.height = dimensions

        self.image = pg.Surface((self.width, self.height))
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect(center=position)

    def move(self, direction: Optional[str], border_rect: pg.Rect) -> None:
        if direction == "up" and self.rect.top > border_rect.top:
            self.rect.y -= PADDLE_VELOCITY
        elif direction == "down" and self.rect.bottom < border_rect.bottom:
            self.rect.y += PADDLE_VELOCITY

    def draw(self, window) -> None:
        window.blit(self.image, self.rect)
