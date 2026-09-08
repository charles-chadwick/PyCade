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

        # Built once instead of per frame in checkForCollisions
        self._whole_board = rect.Rect((0, 0), consts.SCREEN_SIZE)

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

    def checkForCollisions(self, human : players.Human, enemies: list):

        # Dead enemies can't be hit or do damage. The rects come out once so the checks below run
        # inside pygame's collidelist instead of a python loop per weapon
        live_enemies = [enemy for enemy in enemies if enemy.state != consts.PlayerState.DEAD]
        enemy_rects = [enemy.rect for enemy in live_enemies]

        # The human takes damage from touching an enemy, whether or not they have weapons in flight
        # @todo: change this so the enemy has damage points
        if human.rect.collidelist(enemy_rects) != -1:
            human.takeDamage(1)

        # Cycle through human weapons, keeping only the ones still in play. Rebuilding the list in a
        # single pass avoids mutating the list being iterated over (which skips entries) and the
        # repeated remove() scans
        surviving_weapons = []

        for weapon in human.weapons:

            # If the weapon is off the board, nuke it
            if not self._whole_board.colliderect(weapon.rect):
                weapon.kill()
                continue

            # The weapon is spent on the first enemy it hits
            hit_index = weapon.rect.collidelist(enemy_rects)
            if hit_index != -1:
                enemy = live_enemies[hit_index]
                enemy.takeDamage(weapon.damage)

                # Out of health, so take it out of play. Dropping it from the local lists too keeps
                # the rects in step with live_enemies so later weapons this frame can't hit a corpse
                if enemy.health <= 0:
                    enemy.kill()
                    enemies.remove(enemy)
                    del live_enemies[hit_index]
                    del enemy_rects[hit_index]

                weapon.kill()
                continue

            surviving_weapons.append(weapon)

        human.weapons = surviving_weapons


    def load(self, name, level):

        cursor = self._conn.execute("SELECT * FROM maps WHERE game = ? AND level = ?", (name, level,))
        map_data = dict(cursor.fetchone())
        self.boundaries = map_data["boundaries"]
        self.name = name
        self.level = level