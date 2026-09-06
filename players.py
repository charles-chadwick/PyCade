import json
import sys
from abc import ABC, abstractmethod

import pygame
from pygame import sprite, rect, draw, Surface
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

    def draw(self, screen: Surface):
        """
        Draw the player on the screen
        :param screen:
        :return:
        """
        # Get the color
        color = self.colors[self.state]

        # @TODO: Change the color based on if the player is being wounded in the moment

        # Get the shape, fill it
        if self.shape == PlayerShape.SQUARE:
            draw.rect(screen, color, self.rect, border_radius=4)
        elif self.shape == PlayerShape.CIRCLE:
            draw.circle(screen, color, self.rect.center, self.rect.width // 2)

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

    def move(self, direction):
        """
        Move the player
        :param direction:
        :return: None
        """

        new_x = self.rect.x
        new_y = self.rect.y

        if direction == PlayerDirection.LEFT:
            new_x = new_x - self.speed
        elif direction == PlayerDirection.RIGHT:
            new_x = new_x + self.speed
        elif direction == PlayerDirection.UP:
            new_y = new_y - self.speed
        elif direction == PlayerDirection.DOWN:
            new_y = new_y + self.speed

        self.rect.x = new_x
        self.rect.y = new_y

class Human(Player):

    def __init__(self, *groups: Group):
        super().__init__(PlayerKind.HUMAN, *groups)

    def handleInput(self):

        # Check for quit and space bar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

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
        self.move(PlayerDirection.RIGHT)
