from enum import StrEnum, Enum

class Paths(StrEnum):
    DATABASE = "res/pygame.sqlite3"

class PlayerKind(StrEnum):
    HUMAN = "Human"
    ENEMY = "Enemy"

class PlayerDirection(StrEnum):
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"

class PlayerShape(StrEnum):
    SQUARE = "Square"
    CIRCLE = "Circle"

class PlayerState(StrEnum):
    ALIVE = "Alive"
    WOUNDED = "Wounded"
    DEAD = "Dead"

BACKGROUND_COLOR = (50, 50, 50)
SCOREBOARD_COLOR = (65,65,65)
SCREEN_SIZE = (1280, 968)
SCOREBOARD_RECT = (0, 896, 1280, 960)