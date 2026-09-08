import json

import pygame.sprite

import consts
import sqlite3
from pygments.lexers import spice
from pygame import sprite, rect

import items
import players


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

    def automateEnemies(self, surface : pygame.Surface, enemies):

        # Handle enemy stuff
        for enemy in enemies:
            enemy.handleInput()
            enemy.draw(surface)
            self.enforceBoundaries(enemy)

            new_direction = enemy.direction

            if enemy.rect.right >= consts.SCREEN_SIZE[0]:
                enemy.move(consts.PlayerDirection.DOWN, enemy.size[1])
                new_direction = consts.PlayerDirection.LEFT
            elif enemy.rect.left <= 0:
                enemy.move(consts.PlayerDirection.DOWN, enemy.size[1])
                new_direction = consts.PlayerDirection.RIGHT

            enemy.direction = new_direction

    def enforceBoundaries(self, player: players.Player):

        # Check the boundary for the player type
        for boundary in self.boundaries:
            if boundary["kind"] == player.kind:
                boundary_rect = rect.Rect(boundary["x"], boundary["y"], boundary["width"], boundary["height"])
                player.rect.clamp_ip(boundary_rect)
                break

    def checkForCollisions(self, *human : players.Human, enemies: list):

        whole_board = pygame.rect.Rect(0, 0, consts.SCREEN_SIZE[0], consts.SCREEN_SIZE[1])

        # Cycle through human weapons
        for weapon in human.weapons:

            for enemy in enemies:
                if pygame.sprite.collide_rect(weapon.rect, enemy.rect):
                    # enemy takes damage if the weapon hits
                    enemy.takeDamage(weapon.damage)
                    human.weapons.remove(weapon)
                elif pygame.sprite.collide_rect(enemy.rect, human.rect):
                    # human takes damage if they collide with the enemy
                    # @todo: change this so the enemy has damange points
                    human.takeDamage(1)
                    human.weapons.remove(weapon)

            # Now if the weapon is off the board, nuke it
            if not whole_board.colliderect(weapon.rect):
                human.weapons.remove(weapon)


    def load(self, name, level):

        cursor = self._conn.execute("SELECT * FROM maps WHERE game = ? AND level = ?", (name, level,))
        map_data = dict(cursor.fetchone())
        self.boundaries = map_data["boundaries"]
        self.name = name
        self.level = level