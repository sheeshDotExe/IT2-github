from .globals import *
from .board import Board
from .entities import Troll


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
