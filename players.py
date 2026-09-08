import json
import sys
import pygame

import items
from items import Weapon
from abc import ABC, abstractmethod
from pygame import sprite, rect, draw, Surface, time
from pygame.sprite import Group

import consts
from consts import PlayerKind, PlayerDirection, PlayerState, PlayerShape

class Player(sprite.Sprite, ABC):

    @property
    def colors(self) -> dict:
        return self._colors

    @colors.setter
    def colors(self, value: str):
        self._colors = {
            state: tuple(int(num) for num in rgb.split(','))
            for state, rgb in json.loads(value).items()
        }

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: PlayerDirection):
        self._direction = value

    @property
    def health(self):
        return self._health

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
        self.rect.size = self._size

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = value

    @property
    def state(self) -> PlayerState:
        return self._state

    @state.setter
    def state(self, value: PlayerState):
        self._state = value

    @property
    def weapons(self) -> list:
        return self._weapons

    @weapons.setter
    def weapons(self, value: list):
        self._weapons = value

    rect: rect.Rect

    def __init__(self, kind: PlayerKind, *groups: Group):
        super().__init__(*groups)

        self._kind = kind

        self.rect = rect.Rect(0, 0, 0, 0)
        self._colors = {}
        self._direction = None
        self._health = 0
        self._name = ""
        self._shape = None
        self._size = ()
        self._speed = 0
        self._state = PlayerState.ALIVE
        self._weapons = []

        self._time_since_weapon_last_fired = 0
        self._time_since_wounded = 0

    def draw(self, screen: Surface):
        """
        Draw the player on the screen
        :param screen:
        :return:
        """
        # Get the color
        color = self.colors[self.state]

        """
        The color will change  based on their state
        """
        if self.state == PlayerState.WOUNDED:

            current_time = pygame.time.get_ticks()
            if current_time - self._time_since_wounded <= 200:
                # @todo fade colors
                color = (255, 0, 255)
            else:
                self.state = PlayerState.ALIVE
                self._time_since_wounded = current_time

        # Get the shape, fill it
        if self.shape == PlayerShape.SQUARE:
            draw.rect(screen, color, self.rect, border_radius=4)
        elif self.shape == PlayerShape.CIRCLE:
            draw.circle(screen, color, self.rect.center, self.rect.width // 2)

        # draw any weapons
        for weapon in self.weapons:
            current_time = pygame.time.get_ticks()
            draw.rect(screen, (255, 0, 0), weapon.rect)

            if self.kind == PlayerKind.ENEMY:
                weapon.rect.y += weapon.speed
            else:
                weapon.rect.y -= weapon.speed

    def fire(self):

        # check for existing weapons
        if len(self.weapons) > 2:
            return

        # check for time since last weapon was fired
        # @todo: fix the weapon class to load the data better
        current_time = pygame.time.get_ticks()
        time_since_last_fired = current_time - self._time_since_weapon_last_fired
        if time_since_last_fired >= 400:
            self._time_since_weapon_last_fired = current_time
            new_weapon = items.Weapon()
            new_weapon.damage = 2
            new_weapon.rect = pygame.rect.Rect(self.rect.centerx, self.rect.y, 8, 8)
            new_weapon.size = (8, 8)
            new_weapon.speed = 16
            self.weapons.append(new_weapon)

    @abstractmethod
    def handleInput(self):
        pass

    def load(self, data : dict):
        """
        Load the player data from a dict
        :param data:
        :return: None
        """
        # cycle over items and check if it exists. If so, set it.
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def move(self, direction : PlayerDirection, y_include: int = 0):
        """
        Move the player
        :param y_include:
        :param direction:
        :return: None
        """

        self._direction = direction

        new_x = self.rect.x
        new_y = self.rect.y

        if direction == PlayerDirection.LEFT:
            new_x = new_x - self.speed
        elif direction == PlayerDirection.RIGHT:
            new_x = new_x + self.speed
        elif direction == PlayerDirection.UP:
            new_y = new_y - y_include or self.speed
        elif direction == PlayerDirection.DOWN:
            new_y = new_y + y_include or self.speed

        self.rect.x = new_x
        self.rect.y = new_y

    def takeDamage(self, damage_points : int):

        self.state = PlayerState.WOUNDED
        self.health -= damage_points
        self._time_since_wounded = pygame.time.get_ticks()

        if self.health <= 0:
            self.state = PlayerState.DEAD

class Human(Player):

    def __init__(self, *groups: Group):
        super().__init__(PlayerKind.HUMAN, *groups)

    def handleInput(self):

        # Check for quit and space bar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.fire()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move(PlayerDirection.UP)
        elif keys[pygame.K_DOWN]:
            self.move(PlayerDirection.DOWN)
        elif keys[pygame.K_LEFT]:
            self.move(PlayerDirection.LEFT)
        elif keys[pygame.K_RIGHT]:
            self.move(PlayerDirection.RIGHT)

class Enemy(Player):

    def __init__(self, *groups: Group):
        super().__init__(PlayerKind.ENEMY, *groups)

    def handleInput(self):
        self.move(self.direction)
