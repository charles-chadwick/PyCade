from enum import StrEnum

class Paths(StrEnum):
    DATABASE = "res/pygame.sqlite3"

class PlayerKind(StrEnum):
    ENEMY = "Enemy"
    HUMAN = "Human"

class PlayerDirection(StrEnum):
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"

class PlayerShape(StrEnum):
    CIRCLE = "Circle"
    SQUARE = "Square"

class PlayerState(StrEnum):
    ALIVE = "Alive"
    DEAD = "Dead"
    WOUNDED = "Wounded"

BACKGROUND_COLOR = (50, 50, 50)
SCOREBOARD_COLOR = (65,65,65)
SCREEN_SIZE = (1280, 968)
SCOREBOARD_RECT = (0, 896, 1280, 960)