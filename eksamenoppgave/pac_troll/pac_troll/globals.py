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
