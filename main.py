import pygame
import consts
import loader
import players

pygame.init()
pygame.display.set_caption("PyCade")
surface = pygame.display.set_mode(consts.SCREEN_SIZE)
clock = pygame.time.Clock()

loader_class = loader.Loader()
human = players.Human()
human.load(loader_class.loadHuman())

while True:

    # Fill the surface
    surface.fill(consts.BACKGROUND_COLOR)

    # Handle player stuff
    human.handleInput()
    human.draw(surface)

    # Update
    pygame.display.flip()
    clock.tick(60)