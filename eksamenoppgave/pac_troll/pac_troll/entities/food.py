from pac_troll.globals import FOOD_COLOR
from .entity import Entity


class Food(Entity):
    """
    Represents a food entity in the game.
    """

    _color = FOOD_COLOR
    _symbol = "M"

    def __init__(self):
        super().__init__()
