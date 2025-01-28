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

#speed and gravity
gravity = 0.1



#ajout d'une classe pour les fruits
class Fruit:
    def __init__(self, x, y, image, letter):
        self.x = x
        self.y = y
        self.image = image
        self.letter = letter
        self.speed_x = -random.uniform(-2, 2)  # Mouvement horizontal aléatoire
        self.speed_y = random.uniform(0.5, 1)  # Vitesse initiale vers le haut
        self.gravity = 0.1  # Effet de gravité constant
        

    def draw(self, screen):
        # Dessiner le fruit
        a=screen.blit(self.image, (self.x, -(self.y)))
        # Dessiner la lettre associée
        text = font.render(self.letter, True, RED)
        screen.blit(text, a)

    def move(self):
        # Appliquer la gravité
        self.speed_y += self.gravity

        # Mettre à jour la position
        self.x += self.speed_x
        self.y += self.speed_y

    #     # Si le fruit tombe en bas de l'écran, le repositionner
    #     if self.y > 500:  # Supposons que 500 soit la hauteur de l'écran
    #         self.reset_position()
    
    # def reset_position(self):
    #     """
    #     Réinitialiser la position du fruit en haut de l'écran
    #     avec une vitesse aléatoire.
    #     """
    #     self.x = random.randint(0, 800)  # Supposons que 800 soit la largeur de l'écran
    #     self.y = random.randint(-50, -10)  # Réapparaît légèrement au-dessus de l'écran
    #     self.speed_x = random.uniform(-2, 2)  # Réinitialiser la vitesse horizontale
    #     self.speed_y = random.randint(-10, -5)  # Réinitialiser la vitesse verticale



    def spawn():
        x = random.randint(50, w - 50)
        y = -500  # Commence en haut de l'écran
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