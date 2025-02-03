import pygame
import random
from settings import *

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Fruit")
clock = pygame.time.Clock()

# Load fruit images (Normal & Sliced)
fruit_images = {
    "apple": pygame.image.load("assets/images/apple.png"),
    "banana": pygame.image.load("assets/images/banana.png"),
    "orange": pygame.image.load("assets/images/orange.png"),  
    "pasteque": pygame.image.load("assets/images/pasteque.png"),  
    "strawberry": pygame.image.load("assets/images/strawberry.png"), 
}

sliced_fruit_images = {
    "apple": pygame.image.load("assets/images/apple_slice.png"),
    "banana": pygame.image.load("assets/images/banana_slice.png"),
    "orange": pygame.image.load("assets/images/orange_slice.png"),
    "pasteque": pygame.image.load("assets/images/pasteque_slice.png"),
    "strawberry": pygame.image.load("assets/images/strawberry_slice.png"),
}

# Resize all fruit images
for key in fruit_images:
    fruit_images[key] = pygame.transform.scale(fruit_images[key], (FRUIT_SIZE, FRUIT_SIZE))
    sliced_fruit_images[key] = pygame.transform.scale(sliced_fruit_images[key], (FRUIT_SIZE, FRUIT_SIZE))

# Load and resize bomb & ice images
bomb_image = pygame.image.load("assets/images/bomb.png")
ice_image = pygame.image.load("assets/images/ice.png")
bomb_image = pygame.transform.scale(bomb_image, (BOMB_SIZE, BOMB_SIZE))
ice_image = pygame.transform.scale(ice_image, (ICE_SIZE, ICE_SIZE))

#images : boom and ice break
bomb_image_sliced = pygame.image.load("assets/images/bomb_slice.png")
bomb_image_sliced = pygame.transform.scale(bomb_image_sliced, (BOMB_SIZE, BOMB_SIZE))
ice_image_sliced = pygame.image.load("assets/images/ice_sliced.png")
ice_image_sliced = pygame.transform.scale(ice_image_sliced, (ICE_SIZE, ICE_SIZE))

# Classes for game objects
class Fruit:
    def __init__(self, letter):
        self.type = random.choice(list(fruit_images.keys()))  
        self.letter = letter  # Add letter to each fruit
        self.x = random.randint(FRUIT_SIZE // 2, WIDTH - FRUIT_SIZE // 2)
        self.y = HEIGHT - FRUIT_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.gravity = 0.1
        self.sliced = False
        self.sliced_time = 0 

    def update(self, time_paused):
        if not time_paused:  # If not paused, apply regular gravity and movement
            self.x += self.speed_x
            self.speed_y += self.gravity
            self.y += self.speed_y
        else:  # If time is paused, slow down the fruit's movement
            self.speed_x *= 0.1  # Slow down horizontal movement
            self.speed_y *= 0.1  # Slow down vertical movement
            self.y += self.speed_y  # Only apply vertical movement for "slowed-down" effect

        # If sliced, wait before resetting
        if self.sliced and pygame.time.get_ticks() - self.sliced_time > SLICED_DISPLAY_TIME * 50:
            self.reset()

    def draw(self):
        if self.sliced:
            screen.blit(sliced_fruit_images[self.type], (self.x, self.y))  
        else:
            screen.blit(fruit_images[self.type], (self.x, self.y))  
            
        # Draw the letter on the fruit
        font = pygame.font.Font(None, 36)
        letter_text = font.render(self.letter, True, WHITE)
        screen.blit(letter_text, (self.x + FRUIT_SIZE // 2, self.y + FRUIT_SIZE // 2))

    def reset(self):
        self.type = random.choice(list(fruit_images.keys()))  # New random fruit
        self.letter = random.choice("ABCDEFGHIJKLMNOP")  # Assign new random letter
        self.x = random.randint(FRUIT_SIZE // 2, WIDTH - FRUIT_SIZE // 2)
        self.y = HEIGHT - FRUIT_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.sliced = False  # Reset slice state

class Bomb:
    def __init__(self):
        self.x = random.randint(0, WIDTH - BOMB_SIZE)
        self.y = HEIGHT - BOMB_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.gravity = 0.1  # Ajout de la gravité
        self.letter = random.choice("QRSTU")
        self.sliced = False

    def update(self, time_paused=False):  # Ajout de time_paused
        if not time_paused:
            self.x += self.speed_x
            self.speed_y += self.gravity
            self.y += self.speed_y
        else:
            self.speed_x *= 0.1  # Ralentir le mouvement horizontal
            self.speed_y *= 0.1  # Ralentir la chute
            self.y += self.speed_y

    def draw(self):
        if self.sliced:
            screen.blit(bomb_image_sliced, (self.x,self.y))
        else:
            screen.blit(bomb_image, (self.x, self.y))


        #Draw the letter on the bomb
        font = pygame.font.Font(None, 36)
        letter_text = font.render(self.letter, True, WHITE)
        screen.blit(letter_text, (self.x + BOMB_SIZE // 2, self.y + BOMB_SIZE // 2))

    def reset(self):
        self.x = random.randint(0, WIDTH - BOMB_SIZE)
        self.y = HEIGHT - BOMB_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)


class Ice:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ICE_SIZE)
        self.y = HEIGHT - ICE_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.gravity = 0.1
        self.letter = random.choice("VWXYZ")
        self.sliced = False
        self.active = True
        self.reset_time = None 

    def update(self):
        if self.active:
            self.x += self.speed_x
            self.speed_y += self.gravity
            self.y += self.speed_y

        if not self.active and self.reset_time is not None:
            if pygame.time.get_ticks() - self.reset_time >= 4000:
                self.relaunch()

    def draw(self):
        if self.active:
            if self.sliced:
                scaled_broken_ice = pygame.transform.scale(ice_image_sliced, (WIDTH, HEIGHT))
                screen.blit(ice_image_sliced, (0,0))
            else:
                screen.blit(ice_image, (self.x, self.y))
                font = pygame.font.Font(None, 36)
                letter_text= font.render(self.letter, True, BLACK)
                screen.blit(letter_text, (self.x + ICE_SIZE //4, self.y + ICE_SIZE //4))
        

    def reset(self):
        self.active = False
        self.sliced = False
        self.reset_time = pygame.time.get_ticks()

    def relaunch(self):    
        self.x = random.randint(0, WIDTH - ICE_SIZE)
        self.y = HEIGHT - ICE_SIZE + 200
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.letter = random.choice("VWXYZ")
        self.sliced = False
        self.active = True
        self.reset_time = None
        #self.visible = True