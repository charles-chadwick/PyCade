from typing import Any

from pygame import rect, sprite
from pygame.sprite import Group

class Weapon(sprite.Sprite):

    @property
    def damage(self) -> int:
        return self._damage

    @damage.setter
    def damage(self, value: str | int):

        if value is str:
            value = int(value)

        self._damage = value

    @property
    def size(self) -> tuple:
        return self._size

    @size.setter
    def size(self, value: str | tuple):

        if value is str:
            value = tuple(int(num) for num in value.split(','))

        self._size = value
        self.rect.size = self._size

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = value

    def __init__(self, *groups: Group):
        super().__init__(*groups)

        self._damage = None
        self._size = None
        self._speed = None