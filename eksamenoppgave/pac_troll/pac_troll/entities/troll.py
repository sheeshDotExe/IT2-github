from pac_troll.globals import TROLL_COLOR
from .entity import Entity


class Troll(Entity):
    """
    Represents a troll entity in the game.

    Attributes:
        _color (str): The color of the troll.
        _symbol (str): The symbol representing the troll.
        alive (bool): Indicates if the troll is alive.
        speed (float): The speed at which the troll moves.
        direction (str): The current direction of the troll.
        immune (bool): Indicates if the troll is immune to obsticles.
    """

    _color = TROLL_COLOR
    _symbol = "T"

    def __init__(self, speed: float, direction: str, immune: bool = False):
        super().__init__()

        self.alive, self.speed, self.direction, self.immune = (
            True,
            speed,
            direction,
            immune,
        )

    def set_direction(self, direction: str):
        """
        Sets the direction of the troll.

        Args:
            direction (str): The new direction of the troll.
        """
        self.direction = direction

    def move(self):
        """
        Moves the troll in the current direction.
        """
        if not self.alive:
            return

        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
