# Importing required modules.
from itertools import cycle
import os
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
font_path = os.path.join("fonts", "PressStart2P-Regular.ttf")

FONT_1 = pygame.font.Font(font_path, 48)
FONT_2 = pygame.font.Font(font_path, 16)


class Game:
    DINO_START_IMAGE = pygame.image.load("images/dino/dino_start.png")

    def __init__(self):
        # Scores.
        self.score = 0
        self.high_score = 0

        # Pygame clock.
        self.clock = pygame.time.Clock()

    def update_score(self):
        # Updating the score.
        self.score += 1

        # Updating the high score.
        self.high_score = max(self.high_score, self.score)

    def display_score(self):
        score_text = "High Score: {} Score: {}".format(
            self.high_score,
            self.score,
        )

        score = FONT_2.render(score_text, True, GREY)
        score_rect = score.get_rect()
        score_rect.center = (950, 50)
        SCREEN.blit(score, score_rect)

    def start_screen(self, restart=True):
        while True:
            # Filling the screen with white colour.
            SCREEN.fill(WHITE)

            if restart:
                # Creating restart message.
                message = FONT_1.render("Press any key to restart", True, GREY)
            else:
                # Creating start message.
                message = FONT_2.render("Press any key to start", True, GREY)

            # Displaying Score.
            self.display_score()

            # Showing the image of the dino.
            dino_image_rect = self.DINO_START_IMAGE.get_rect()
            dino_image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            SCREEN.blit(self.DINO_START_IMAGE, dino_image_rect)

            # Showing the message.
            message_rect = message.get_rect()
            message_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(message, message_rect)

            # Checking for events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Getting mouse button clicks.
                clicks = pygame.mouse.get_pressed(3)
                if event.type == pygame.KEYDOWN or clicks[0]:
                    # Reset the score.
                    self.score = 0

                    # Running the mainloop
                    self.mainloop()

            # Updating the display.
            pygame.display.update()

    def mainloop(self):
        while True:
            # Filling the screen with white colour.
            SCREEN.fill(WHITE)

            # Displaying the score.
            self.update_score()
            self.display_score()

            # Checking for events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Updating the display.
            self.clock.tick(30)
            pygame.display.update()


if __name__ == "__main__":
    Game().start_screen()

