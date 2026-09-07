import json

import consts
import sqlite3
from pygments.lexers import spice
from pygame import sprite, rect

class Map(sprite.Sprite):

    @property
    def boundaries(self) -> list:
        return self._boundaries

    @boundaries.setter
    def boundaries(self, value: str):
        self._boundaries = json.loads(value)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int):
        self._level = value

    def __init__(self, *groups: sprite.Group):
        super().__init__(*groups)

        self._conn = sqlite3.connect(consts.Paths.DATABASE)
        self._conn.row_factory = sqlite3.Row

        self._boundaries = []
        self._name = None
        self._level = None

    def load(self, name, level):

        cursor = self._conn.execute("SELECT * FROM maps WHERE game = ? AND level = ?", (name, level,))
        map_data = dict(cursor.fetchone())
        self.boundaries = map_data["boundaries"]
        self.name = name
        self.level = level

