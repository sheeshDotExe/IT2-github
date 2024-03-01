from __future__ import annotations
import pygame as pg
import random

pg.font.init()
BASE_FONT = pg.font.Font(pg.font.get_default_font(), 32)

# constants
WIDTH, HEIGHT = 800, 600
GAME_OBJECT_WIDTH, GAME_OBJECT_HEIGHT = 30, 30
PLAYER_START_SPEED = 2
PLAYER_SPEED_INCREMENT = 0.15
FRAME_RATE = 60
NUMBER_OF_FOOD = 3

# colors
SCORE_TEXT_COLOR = (255, 255, 255)
GAME_OVER_TEXT_COLOR = (255, 0, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)

ENTITY_TEXT_COLOR = (0, 0, 0)
TROLL_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
OBSTICLE_COLOR = (0, 0, 255)
BASE_ENTITY_COLOR = (255, 255, 255)


class Game:
    """
    The Game class represents the main game loop and controls the game logic.

    Attributes:
        screen (pygame.Surface): The game screen surface.
        screen_rect (pygame.Rect): The rectangle representing the game screen.
        clock (pygame.time.Clock): The game clock for controlling the frame rate.
        running (bool): Flag indicating if the game is running.
        board (Board): The game board.
        player (Troll): The player character.
        score (int): The player's score.
    """

    __player_base_speed = PLAYER_START_SPEED

    def __init__(self):
        """
        Initializes the Game object.
        """
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.running = False

    def __setup_game(self):
        """
        Sets up the game by creating the board, player character, and initializing game variables.
        """
        self.board = Board(width=WIDTH, height=HEIGHT)
        self.board._setup_board()

        self.player = Troll(speed=self.__player_base_speed, direction="right")
        self.running = True
        self.score = 0

    def _draw_game_info(self):
        """
        Draws the game information on the screen, such as the score and game over text.
        """
        score_text = BASE_FONT.render(f"Score: {self.score}", True, SCORE_TEXT_COLOR)

        # function to offset the center of the screen to fit the text
        def offset_center(x, y):
            return x, y + score_text.get_height()

        self.screen.blit(
            score_text,
            score_text.get_rect(center=offset_center(*self.screen_rect.midtop)),
        )

        # if the player is still alive we don't need to draw the game over text
        if self.player.alive:
            return

        game_over_text = BASE_FONT.render("Game Over", True, GAME_OVER_TEXT_COLOR)
        self.screen.blit(
            game_over_text,
            game_over_text.get_rect(center=self.screen_rect.center),
        )

    def __update(self):
        """
        Updates the game state, including player movement, collisions, and event handling.
        """
        self.board.draw(self.screen)
        self.player.move()
        self.player.draw(self.screen)

        if not self.board.in_bounds(self.player.rect):
            self.player.alive = False

        if self.board.food_collision(self.player.rect, is_player=True):
            self.score += 1
            self.player.speed += PLAYER_SPEED_INCREMENT
            self.player.immune = True

        # when a player collides with an obsticle they die, unless it's the obticle created when colliding with the food
        if self.board.obsticle_collision(self.player.rect) and not self.player.immune:
            self.player.alive = False

        # remove immunety when the player is no longer colliding with the obsticle
        if self.player.immune and not self.board.obsticle_collision(self.player.rect):
            self.player.immune = False

        self._draw_game_info()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.set_direction("up")
                elif event.key == pg.K_DOWN:
                    self.player.set_direction("down")
                elif event.key == pg.K_LEFT:
                    self.player.set_direction("left")
                elif event.key == pg.K_RIGHT:
                    self.player.set_direction("right")

        pg.display.flip()

    def start_game(self):
        """
        Starts the game by setting up the game and entering the game loop.
        """
        self.__setup_game()

        while self.running:
            self.__update()
            self.clock.tick(FRAME_RATE)


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


class Food(Entity):
    """
    Represents a food entity in the game.
    """

    _color = FOOD_COLOR
    _symbol = "M"

    def __init__(self):
        super().__init__()


class Obsticle(Entity):
    """
    Represents an obstacle in the game.
    """

    _color = OBSTICLE_COLOR
    _symbol = "H"

    def __init__(self, x: int, y: int):
        super().__init__()
        self.rect.x, self.rect.y = x, y


def main() -> None:
    """
    ☆*: .｡. o(≧▽≦)o .｡.:*☆
    """
    game = Game()
    game.start_game()


if __name__ == "__main__":
    main()
