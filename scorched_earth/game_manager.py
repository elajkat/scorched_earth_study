import pygame

from scorched_earth import game_constants
from scorched_earth import game_menu


def scorched_earth():
    pygame.init()

    size = [game_constants.SCREEN_WIDTH, game_constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('Scorched Earth remastered :-)')

    clock = pygame.time.Clock()
    menu = game_menu.ScorchedEarthMenu(screen, clock)
    menu.menu_loop()

    pygame.quit()
