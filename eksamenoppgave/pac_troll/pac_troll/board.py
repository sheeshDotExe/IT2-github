import random
import pygame as pg
from .globals import (
    BOARD_BACKGROUND_COLOR,
    GAME_OBJECT_HEIGHT,
    GAME_OBJECT_WIDTH,
    NUMBER_OF_FOOD,
)
from .entities import Food
from .entities import Obsticle


class Board:
    """
    Represents the game board.

    Attributes:
        width (int): The width of the board.
        height (int): The height of the board.
        image (pygame.Surface): The surface representing the board.
        obsticles (list): List of obsticles on the board.
        food (list): List of food items on the board.

    Methods:
        __init__(self, width: int, height: int): Initializes the Board object.
        _setup_board(self): Sets up the board by creating obsticles and food items.
        _get_random_position(self): Returns a random position on the board.
        in_bounds(self, rect: pygame.Rect): Checks if a rectangle is within the bounds of the board.
        food_collision(self, rect, is_player: bool = False): Checks if there is a collision with food items.
        obsticle_collision(self, rect): Checks if there is a collision with obsticles.
        draw(self, screen): Draws the board, food items, and obsticles on the screen.
    """

    __number_of_food = NUMBER_OF_FOOD

    def __init__(self, width: int, height: int):
        """
        Initializes the Board class.

        Args:
            width (int): The width of the PacTroll image.
            height (int): The height of the PacTroll image.
        """
        self.width, self.height = width, height
        self.image = pg.Surface((width, height))
        self.image.fill(BOARD_BACKGROUND_COLOR)

    def _setup_board(self):
        """
        Set up the game board by initializing obstacles and food items.
        """
        self.obsticles = []
        self.food = [Food() for _ in range(self.__number_of_food)]
        for food in self.food:
            food.set_position(*self._get_random_position())

    def _get_random_position(self):
        """
        Get a random position within the game boundaries,
        that doesn't collide with any food or obsticles.

        Returns:
            tuple: A tuple containing the x and y coordinates of the random position.
        """
        while True:
            x = random.randint(0, self.width - GAME_OBJECT_WIDTH)
            y = random.randint(0, self.height - GAME_OBJECT_HEIGHT)
            rect = pg.Rect(x, y, GAME_OBJECT_WIDTH, GAME_OBJECT_HEIGHT)

            if not self.food_collision(rect) and not self.obsticle_collision(rect):
                return (x, y)

    def in_bounds(self, rect: pg.Rect):
        """
        Check if the given rectangle is within the bounds of the game screen.

        Args:
            rect (pg.Rect): The rectangle to check.

        Returns:
            bool: True if the rectangle is within the bounds, False otherwise.
        """
        return (
            rect.x >= 0
            and rect.y >= 0
            and rect.x + rect.width <= self.width
            and rect.y + rect.height <= self.height
        )

    def food_collision(self, rect, is_player: bool = False):
        """
        Checks for collision between the given rectangle and the food objects.
        If a collision occurs, it performs the following actions:
        - If the collision involves the player, it spawns an obstacle at the food's position and moves the food to a random position.
        - If the collision does not involve the player, no additional actions are performed.

        Parameters:
        - rect: The rectangle to check for collision.
        - is_player: A boolean flag indicating whether the collision involves the player. Default is False.

        Returns:
        - True if a collision occurs, False otherwise.
        """
        for food in self.food:
            if food.rect.colliderect(rect):
                if is_player:
                    self.obsticles.append(Obsticle(food.rect.x, food.rect.y))
                    food.rect.x, food.rect.y = self._get_random_position()
                return True
        return False

    def obsticle_collision(self, rect):
        """
        Checks if the given rectangle collides with any obstacles.

        Args:
            rect (pygame.Rect): The rectangle to check collision with.

        Returns:
            bool: True if collision occurs, False otherwise.
        """
        for obsticle in self.obsticles:
            if obsticle.rect.colliderect(rect):
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

        for food in self.food:
            food.draw(screen)

        for obsticle in self.obsticles:
            obsticle.draw(screen)
