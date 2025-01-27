import pygame
import random
import string


pygame.init()
#In order to control the speed of updating the images in pygame screen, we have to insert this function (fps) :
clock = pygame.time.Clock()


#colors
w = 500
h = 500
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#game window settings
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Ninja Fruit')
screen.fill(WHITE)


#images
fruit_image = pygame.image.load('fruits/pasteque.png')
fruit_slice = pygame.image.load('fruits/pasteque_slice.png')

fruit_image = pygame.transform.scale(fruit_image, (50, 50))  # change the dimension of the image because, it is bigger than the screen size
fruit_slice = pygame.transform.scale(fruit_slice, (50, 50))

#fonts for letters with the fruit
font = pygame.font.Font(None, 36)

#score
score = 0

#list of fruits
fruits = []

#Running the game
RUNNING = True


#ajout d'une classe pour les fruits
class Fruit:
    def __init__(self, x, y, image, letter):
        self.x = x
        self.y = y
        self.image = image
        self.letter = letter
        self.speed = random.randint(3,8)

    def draw(self, screen):
        # Dessiner le fruit
        screen.blit(self.image, (self.x, self.y))
        # Dessiner la lettre associée
        text = font.render(self.letter, True, WHITE)
        screen.blit(text, (self.x + 10, self.y + 10))

    def move(self):
        self.y += self.speed



    def spawn():
        x = random.randint(50, w - 50)
        y = -50  # Commence en haut de l'écran
        letter = random.choice(string.ascii_uppercase)  # Lettre aléatoire
        fruit = Fruit(x, y, fruit_image, letter)
        fruits.append(fruit)

    def cut(letter):
        global score
        for fruit in fruits:
            if fruit.letter == letter:
                fruits.remove(fruit)  # Supprime le fruit
                score += 10  # Augmente le score
                break

# Temps pour générer des fruits
FRUIT_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FRUIT_SPAWN_EVENT, 1000)  # Un fruit par seconde

while RUNNING:
    screen.fill(WHITE)

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == FRUIT_SPAWN_EVENT:
            Fruit.spawn()
        if event.type == pygame.KEYDOWN:
            Fruit.cut(event.unicode.upper())

    # Mettre à jour les fruits
    for fruit in fruits[:]:
        fruit.move()
        if fruit.y > h:  # Si le fruit dépasse l'écran, il est perdu
            fruits.remove(fruit)
        fruit.draw(screen)

    # Afficher le score
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))

    # Rafraîchir l'écran
    pygame.display.flip()
    clock.tick(60)

pygame.quit()