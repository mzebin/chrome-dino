# Importing required modules.
from itertools import cycle
import random
import sys

import pygame

# Initializing pygame.
pygame.init()

# Creating a Screen.
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Defining Colours.
WHITE = (255, 255, 255)
GREY = (83, 83, 83)

# Creating fonts.
font_path = "fonts/PressStart-2P-Regular.ttf"

FONT_1 = pygame.font.Font(font_path, 48)
FONT_2 = pygame.font.Font(font_path, 16)


class Game:

    def __init__(self):
        pass


if __name__ == "__main__":
    Game()

