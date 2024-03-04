from pac_troll.globals import OBSTICLE_COLOR
from .entity import Entity


class Obsticle(Entity):
    """
    Represents an obstacle in the game.
    """

    _color = OBSTICLE_COLOR
    _symbol = "H"

    def __init__(self, x: int, y: int):
        super().__init__()
        self.rect.x, self.rect.y = x, y
