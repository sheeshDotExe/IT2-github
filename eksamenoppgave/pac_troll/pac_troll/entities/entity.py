from pac_troll.globals import (
    BASE_ENTITY_COLOR,
    GAME_OBJECT_WIDTH,
    GAME_OBJECT_HEIGHT,
    BASE_FONT,
    ENTITY_TEXT_COLOR,
)

import pygame as pg


class Entity:
    """
    Represents a game entity.

    Attributes:
        _color (tuple): The color of the entity.
        _symbol (str): The symbol representing the entity / the text displayed.
        image (Surface): The image of the entity.
        rect (Rect): The rectangular area occupied by the entity.
    """

    _color = BASE_ENTITY_COLOR
    _symbol = "N/A"

    def __init__(self):
        """
        Initializes a new instance of the Entity class.
        """
        self.image = pg.Surface((GAME_OBJECT_WIDTH, GAME_OBJECT_HEIGHT))
        self.rect = self.image.get_rect()

        self.image.fill(self._color)

        text = BASE_FONT.render(self._symbol, True, ENTITY_TEXT_COLOR)
        self.image.blit(
            text,
            text.get_rect(center=self.rect.center),
        )

    def set_position(self, x: int, y: int):
        """
        Sets the position of the entity.

        Args:
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.
        """
        self.rect.x, self.rect.y = x, y

    def draw(self, screen):
        """
        Draws the entity on the screen.

        Args:
            screen: The screen to draw on.
        """
        screen.blit(self.image, self.rect)
