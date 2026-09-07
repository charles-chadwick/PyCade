import sys

import pygame
import consts
import loader
import players
import logging
from map import Map
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s: %(message)s')

pygame.init()
pygame.display.set_caption("PyCade")
surface = pygame.display.set_mode(consts.SCREEN_SIZE)
clock = pygame.time.Clock()

# Load the game and map
game_map = Map()
game_map.load("Space Invaders", 1)

# Load the players
loader_class = loader.Loader()

# Human
human = players.Human()
human.load(loader_class.loadHuman())

# Enemies
enemies = []
for enemy_data in loader_class.loadEnemies():

    if enemy_data["name"] == "Ball Sack":
        for i in range(3):
            enemy = players.Enemy()
            enemy.load(enemy_data)
            enemy.rect.x += (enemy.rect.width * 2) * i
            enemy.move(consts.PlayerDirection.RIGHT)
            enemies.append(enemy)

while True:

    # Fill the surface
    surface.fill(consts.BACKGROUND_COLOR)

    # Handle player stuff
    human.handleInput()
    human.draw(surface)
    game_map.enforceBoundaries(human)

    # Handle enemy stuff
    for enemy in enemies:
        enemy.handleInput()
        enemy.draw(surface)
        game_map.enforceBoundaries(enemy)

    # Update
    pygame.display.flip()
    clock.tick(24)