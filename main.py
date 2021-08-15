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


class Track:
    # Image of the track.
    IMAGE = pygame.image.load("images/others/track.png")

    # Speed of the track.
    SPEED = 25

    def __init__(self):
        # Speed of the track.
        self.track_speed = self.SPEED

        # position of the track.
        self.x = 0
        self.y = 375

        # The width of the track.
        self.width = self.IMAGE.get_width()

    @property
    def positions(self):
        return [(self.x, self.y), (self.x + self.width, self.y)]
    
    def update(self):
        # Resetting the x position.
        if self.x <= -self.width:
            self.x = 0
        
        # Decrementing the x position.
        self.x -= self.track_speed
    
    def draw(self):
        SCREEN.blit(self.IMAGE, self.positions[0])
        SCREEN.blit(self.IMAGE, self.positions[1])


class Cloud:
    # Images of the cloud.
    IMAGES = [
        pygame.image.load("images/others/cloud_1.png"),
        pygame.image.load("images/others/cloud_2.png"),
    ]

    # Speed of the cloud.
    SPEED = 20

    def __init__(self):
        # Speed of the cloud.
        self.speed =  self.SPEED

        # Setting up a clouds.
        self.image = random.choice(self.IMAGES)
        self.width = self.image.get_width()
        self.x = SCREEN_WIDTH + random.randint(0, 250)
        self.y = random.randint(50, 250)
    
    def update(self):
        self.x -= self.speed
        if self.x < -self.width * random.randint(1, 3):
            # Resetting the cloud.
            self.image = random.choice(self.IMAGES)
            self.width = self.image.get_width()
            self.x = SCREEN_WIDTH + random.randint(0, 250)
            self.y = random.randint(50, 250)
    
    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))


class Dinosaur:
    # Images of Dinosaur running.
    RUNNING_IMAGES = [
        pygame.image.load("images/dino/dino_run_1.png"),
        pygame.image.load("images/dino/dino_run_2.png"),
    ]

    # Images of Dinosaur Ducking.
    DUCKING_IMAGES = [
        pygame.image.load("images/dino/dino_duck_1.png"),
        pygame.image.load("images/dino/dino_duck_2.png"),
    ]

    # Image of Dinosaur Jumping.
    JUMPING_IMAGE = pygame.image.load("images/dino/dino_jump.png")

    # The position of the dinosaur and the
    # velocity of the jumping dinosaur.
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 10

    def __init__(self):
        # Dinosaur images.
        self.dino_running_images = cycle(self.RUNNING_IMAGES)
        self.dino_ducking_images = cycle(self.DUCKING_IMAGES)

        # Setting the initial image.
        self.image = self.RUNNING_IMAGES[0]
        self.rect = self.image.get_rect()

        # Changing the position of the image.
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS

        # Jumping velocity.
        self.jump_velocity = self.JUMP_VEL

        # Flags.
        self.running = True
        self.ducking = False
        self.jumping = False

        self.change_image = False
    
    def update(self, keys_pressed):
        if not self.jumping:
            if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_SPACE]:
                self.running = False
                self.ducking = False
                self.jumping = True
            elif keys_pressed[pygame.K_DOWN]:
                self.running = False
                self.ducking = True
                self.jumping = False
            else:
                self.running = True
                self.ducking = False
                self.jumping = False

        if self.running:
            self.run()
        elif self.ducking:
            self.duck()
        elif self.jumping:
            self.jump()
    
    def run(self):
        if self.change_image:
            self.image = next(self.dino_running_images)

        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.change_image = not self.change_image
    
    def duck(self):
        if self.change_image:
            self.image = next(self.dino_ducking_images)

        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS + 35
        self.change_image = not self.change_image

    def jump(self):
        self.image = self.JUMPING_IMAGE
        if self.jumping:
            self.rect.y -= (self.jump_velocity * 4)
            self.jump_velocity -= 1
        
        if self.jump_velocity < -self.JUMP_VEL:
            self.jumping = False
            self.jump_velocity = self.JUMP_VEL

    def draw(self):
        SCREEN.blit(self.image, self.rect)


class Game:
    DINO_START_IMAGE = pygame.image.load("images/dino/dino_start.png")

    def __init__(self):
        # Scores.
        self.score = 0
        self.high_score = 0

        # Pygame clock.
        self.clock = pygame.time.Clock()

        # Game objects.
        self.track = Track()
        self.cloud = Cloud()

        self.dino = Dinosaur()

    def update_score(self):
        # Updating the score.
        self.score += 1

        # Updating the high score.
        self.high_score = max(self.high_score, self.score)
    
    @property
    def score_text(self):
        return "High Score: {} Score: {}".format(self.high_score, self.score)

    def display_score(self):
        # Creating score.
        score = FONT_2.render(self.score_text, True, GREY)

        # Changing the position of the score text.
        score_rect = score.get_rect()
        score_rect.center = (950, 50)

        # Displaying the score.
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

            # Displaying the track.
            self.track.update()
            self.track.draw()

            # Displaying the cloud.
            self.cloud.update()
            self.cloud.draw()

            # Displaying the score.
            self.update_score()
            self.display_score()

            # Displaying the dinosaur.
            self.dino.update(pygame.key.get_pressed())
            self.dino.draw()

            # Checking for events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Updating the display.
            self.clock.tick(30)
            pygame.display.update()


if __name__ == "__main__":
    Game().start_screen()

