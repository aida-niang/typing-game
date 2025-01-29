import pygame
import random

pygame.init()
#In order to control the speed of updating the images in pygame screen, we have to insert this function :
clock = pygame.time.Clock()

w = 800
h = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Ninja Fruit')
screen.fill(WHITE)

#load images with alphabets
image_abc = []
for i in range(65, 91) :
    list_letters = [chr(i)] 

    for letter in list_letters:
        try:
            image = pygame.image.load(f'alphabets/{letter}.png')  
            image = pygame.transform.scale(image, (50, 50))  
            image_abc.append(image) 
        except pygame.error:
            print(f"Erreur in charging the image {letter}.png")

#load sounds :
sound_winner = pygame.mixer.Sound('sounds/You_Win_Perfect.wav')
sound_loser = pygame.mixer.Sound('sounds/you_lost.wav')

#load images :
fruit_image = pygame.image.load('fruits/pasteque.png')
fruit_slice = pygame.image.load('fruits/pasteque_slice.png')
bomb_image = pygame.image.load('fruits/bomb.png')

fruit_image = pygame.transform.scale(fruit_image, (50, 50))  # change the dimension of the image because, it is bigger than the screen size
fruit_slice = pygame.transform.scale(fruit_slice, (50, 50))
bomb_image = pygame.transform.scale(bomb_image, (50, 50))

fruit_width, fruit_height = fruit_image.get_size() #it's the same size as for all the images
fruit_x = random.uniform(fruit_width // 2, w - fruit_width // 2)  #Initial position of the image (bellow)
fruit_y = h - fruit_height
speed_x_f = random.uniform(-1.0, 1.0)  # displacement speed on x-axis of the fruit
speed_y_f = random.uniform(-10.0, -5.0)  # displacement speed on y-axis of the fruit
gravity = 0.1

bomb_x = random.uniform(fruit_width // 2, w - fruit_width // 2)   #Initial position of the image (bellow)
bomb_y = h + fruit_height
speed_x_b = random.uniform(-1.0, 1.0)  # displacement speed on x-axis of the bomb
speed_y_b = random.uniform(-10.0, -5.0)  # displacement speed on y-axis of the bomb

#The target = circle (we can change it)
target_pos = None  
target_radius = 20

# function that detects collisions
def detect_collision_fruit(fruit_pos, fruit_size, target_pos, target_radius):
    if not target_pos:
        return False  

    fruit_center = (fruit_pos[0] + fruit_size[0] // 2, fruit_pos[1] + fruit_size[1] // 2)
    distance = ((fruit_center[0] - target_pos[0]) ** 2 + (fruit_center[1] - target_pos[1]) ** 2) ** 0.5 #the distance between the target and the image centers (sqrt((x2 - x1)² + (y2 - y1)²))
    return distance <= target_radius + fruit_size[0] // 2  # law : we have collision between 2 circles if d <= R1 + R2

def detect_collision_bomb(bomb_pos, bomb_size, target_pos, target_radius):
    if not target_pos:
        return False  

    bomb_center = (bomb_pos[0] + bomb_size[0] // 2, bomb_pos[1] + bomb_size[1] // 2)
    distance = ((bomb_center[0] - target_pos[0]) ** 2 + (bomb_center[1] - target_pos[1]) ** 2) ** 0.5 #the distance between the target and the image centers (sqrt((x2 - x1)² + (y2 - y1)²))
    return distance <= target_radius + bomb_size[0] // 2  # law : we have collision between 2 circles if d <= R1 + R2


def show_fruit_again() :
    global fruit_x, fruit_y, speed_x_f, speed_y_f
    
    speed_x_f = random.uniform(-1.0, 1.0)  # displacement speed on x-axis
    speed_y_f = random.uniform(-10.0, -5.0)
    gravity = 0.3
    fruit_x += speed_x_f #displacement of the fruit image in the x+
    speed_y_f += gravity # (v(y) = v0 + g*t) 
    fruit_y += speed_y_f  # (y(t) = y0 + vy*t + 1/2 g*t²) 

def show_bomb_again() :
    global bomb_x, bomb_y, speed_x_b, speed_y_b
    
    speed_x_b = random.uniform(-1.0, 1.0)  # displacement speed on x-axis
    speed_y_b = random.uniform(-10.0, -5.0)
    gravity = 0.3
    bomb_x += speed_x_b #displacement of the fruit image in the x+
    speed_y_b += gravity # (v(y) = v0 + g*t) 
    bomb_y += speed_y_b  # (y(t) = y0 + vy*t + 1/2 g*t²) 


def play():
    global fruit_x, fruit_y, bomb_x, bomb_y, target_pos, speed_x_f, speed_y_f, speed_x_b, speed_y_b, fruit_image  #in order to change thel later
    # Here I added speed_y as a global variable because it is affected by the gravity
    run = True

    while run:
        screen.fill(WHITE) #clean the screen at each step (when updating the screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p :
                    target_pos = pygame.mouse.get_pos()
                    print(f"The postions of the target is : {target_pos}")
        
        fruit_x += speed_x_f #displacement of the fruit image in the x+
        speed_y_f += gravity # (v(y) = v0 + g*t) 
        fruit_y += speed_y_f  # (y(t) = y0 + vy*t + 1/2 g*t²) 

        bomb_x += speed_x_b #displacement of the fruit image in the x+
        speed_y_b += gravity # (v(y) = v0 + g*t) 
        bomb_y += speed_y_b  # (y(t) = y0 + vy*t + 1/2 g*t²) 
        #Here I used gravitational law : we have integrated the second law of Newton sum(F) = m*a
        if (fruit_x < fruit_width // 2) or (fruit_x > w - fruit_width) or (fruit_y > h) :
            show_fruit_again()

        if (bomb_x < fruit_width // 2) or (bomb_x > w - fruit_width) or (bomb_y > h) :
            show_bomb_again()

        for i in range(len(image_abc)) :
            space = 50  #space between two images
            screen.blit(image_abc[i], (fruit_x + i * space, fruit_y)) #shiw the fruit_images

        screen.blit(bomb_image, (bomb_x, bomb_y))  #show the bomb image


        if target_pos:
            pygame.draw.circle(screen, RED, target_pos, target_radius) #draw the circle when we press the choosen key (here it is 'p')


        if detect_collision_fruit((fruit_x, fruit_y), (fruit_width, fruit_height), target_pos, target_radius):
            print("Collision detected!")
            screen.blit(fruit_slice, (fruit_x, fruit_y)) #replace the full fruit by the sliced fruit
            sound_loser.play()
            pygame.time.wait(int(sound_loser.get_length() * 1000))
            run = False     #if there is collision, the program is closed
        

        pygame.display.flip()
        clock.tick(60) #the unit is FPS = frame per seconde 

    pygame.quit()

try :
    if __name__ == '__main__':
        play()
except KeyboardInterrupt :
    print(f"Exiting ....... ")
