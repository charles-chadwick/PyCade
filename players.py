from pygame import sprite, rect
from pygame.sprite import Group
from consts import PlayerKind, PlayerMovement, PlayerState, PlayerShape

class Player(sprite.Sprite):

    @property
    def colors(self) -> dict:
        return self._colors

    @colors.setter
    def colors(self, value: dict):
        self._colors = value

        # Get the colors based on state
        for state in PlayerState:
            rgb_codes = str(self.colors[state.value]).split(',')
            self.colors[state.value] = tuple(int(num) for num in rgb_codes)

    @health.setter
    def health(self, value: int):
        self._health = value

    @property
    def kind(self) -> PlayerKind:
        return self._kind

    @kind.setter
    def kind(self, value: PlayerKind):
        self._kind = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def shape(self) -> PlayerShape:
        return self._shape

    @shape.setter
    def shape(self, value: PlayerShape):
        self._shape = value

    @property
    def size(self) -> tuple:
        return self._size

    @size.setter
    def size(self, value: str):
        self._size = tuple(int(num) for num in value.split(','))

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = value

    def __init__(self, kind: PlayerKind, *groups: Group):
        super().__init__(*groups)
        self._kind = kind

        self._colors = {}
        self._health = 0
        self._name = ""
        self._shape = None
        self._size = ()
        self._speed = 0

    def load(self, data : dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


