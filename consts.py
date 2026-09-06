from enum import StrEnum, Enum


class Paths(StrEnum):
    DATABASE = "res/pygame.sqlite3"

class PlayerKind(StrEnum):
    HUMAN = "Human"
    ENEMY = "Enemy"

class Screen(Enum):
    BACKGROUND_COLOR = (61,56,70)
    WIDTH = 1280
    HEIGHT = 1024