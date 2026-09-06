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

class Screen(Enum):
    BACKGROUND_COLOR = (61,56,70)
    WIDTH = 1280
    HEIGHT = 1024