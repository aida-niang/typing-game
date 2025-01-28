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
font = pygame.font.Font(None, 40)
screen.fill(WHITE)

#load sounds :
sound_winner = pygame.mixer.Sound('sounds/You_Win_Perfect.wav')
sound_loser = pygame.mixer.Sound('sounds/you_lost.wav')

#load images
try :
    fruit_image = pygame.image.load('fruits/pasteque.png')
    fruit_slice = pygame.image.load('fruits/pasteque_slice.png')
except pygame.error as e:
    print(f"Error when loading image: {e}")
    pygame.quit()
    exit()

fruit_image = pygame.transform.scale(fruit_image, (50, 50))  # change the dimension of the image because, it is bigger than the screen size
fruit_slice = pygame.transform.scale(fruit_slice, (50, 50))

fruit_width, fruit_height = fruit_image.get_size()
fruit_x = (w - fruit_width) // 2  #Initial position of the image (bellow)
fruit_y = h - fruit_height
speed_x = random.uniform(-1.0, 1.0)  # displacement speed on x-axis
speed_y = random.uniform(-10.0, -5.0)  # displacement speed on y-axis
gravity = 0.1

#The target = circle (we can change it)
target_pos = None  
target_radius = 20

# function that detects collisions
def detect_collision(fruit_pos, fruit_size, target_pos, target_radius):
    if not target_pos:
        return False  

    fruit_center = (fruit_pos[0] + fruit_size[0] // 2, fruit_pos[1] + fruit_size[1] // 2)
    distance = ((fruit_center[0] - target_pos[0]) ** 2 + (fruit_center[1] - target_pos[1]) ** 2) ** 0.5 #the distance between the target and the image centers (sqrt((x2 - x1)² + (y2 - y1)²))
    return distance <= target_radius + fruit_size[0] // 2  # law : we have collision between 2 circles if d <= R1 + R2

def show_fruit_again() :
    global fruit_x, fruit_y, speed_x, speed_y
    
    speed_x = random.uniform(-1.0, 1.0)  # displacement speed on x-axis
    speed_y = random.uniform(-10.0, -5.0)
    gravity = 0.3
    fruit_x += speed_x #displacement of the fruit image in the x+
    speed_y += gravity # (v(y) = v0 + g*t) 
    fruit_y += speed_y  # (y(t) = y0 + vy*t + 1/2 g*t²) 


def play():
    global fruit_x, fruit_y, target_pos, speed_x, speed_y, fruit_image, score, player_name  #in order to change thel later
    # Here I added speed_y as a global variable because it is affected by the gravity
    player_name = get_player_name()
    score = 0
    run = True

    while run:
        screen.fill(WHITE) #clean the screen at each step (when updating the screen)
        draw_text(f"Player: {player_name}", font, BLACK, screen, w - 150, 30)
        draw_text(f"Score: {score}", font, BLACK, screen, h - 150, 70)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p :
                    target_pos = pygame.mouse.get_pos()
                    print(f"The postions of the target is : {target_pos}")
        
        fruit_x += speed_x #displacement of the fruit image in the x+
        speed_y += gravity # (v(y) = v0 + g*t) 
        fruit_y += speed_y  # (y(t) = y0 + vy*t + 1/2 g*t²) 
        #Here I used gravitational law : we have integrated the second law of Newton sum(F) = m*a
        if (fruit_x < fruit_width // 2) or (fruit_x > w - fruit_width) or (fruit_y > h) :
            show_fruit_again()


        screen.blit(fruit_image, (fruit_x, fruit_y)) #shiw the fruit_image


        if target_pos:
            pygame.draw.circle(screen, RED, target_pos, target_radius) #draw the circle when we press the choosen key (here it is 'p')


        if detect_collision((fruit_x, fruit_y), (fruit_width, fruit_height), target_pos, target_radius):
            sound_loser.play()
            pygame.time.wait(int(sound_winner.get_length() * 1000))
            print("Collision detected!")
            screen.blit(fruit_slice, (fruit_x, fruit_y)) #replace the full fruit by the sliced fruit
            run = False     #if there is collision, the program is closed

        pygame.display.flip()
        clock.tick(60) #the unit is FPS = frame per seconde 

    pygame.quit()


#This function allow to write on pygame screen :
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Function to get the player's name
def get_player_name():
    input_box = pygame.Rect(0, 0, 200, 40) 
    input_box.center = (w // 2, h// 2) 
    #input_box = pygame.Rect(w // 2 - 100, h // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    while True:
        screen.fill(WHITE)
        draw_text("Enter your name:", font, BLACK, screen, w // 2, h // 3)
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(text, font, BLACK, screen, w // 2, h // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    color = color_active
                else:
                    active = False
                    color = color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

def show_menu():
    screen.fill(WHITE)
    draw_text("--- Ninja Fruit ---", font, BLACK, screen, w // 2, h // 4)
    draw_text("1. Play", font, BLACK, screen, w // 2, h // 2 - 80)
    draw_text("2. View scores", font, BLACK, screen, w // 2, h // 2 - 40)
    draw_text("3. Delete scores", font, BLACK, screen, w // 2, h // 2)
    draw_text("4. Quit", font, BLACK, screen, w // 2, h // 2 + 40)
    
    pygame.display.update()

def choose_menu():
    score_file = "scores.txt"

    while True:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    play()
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    view_scores(score_file)
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    confirm_delete_scores(score_file)  
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5 or event.key == pygame.K_RETURN:
                    confirm_quit()  # Call the confirmation dialog function 
                else:
                    print("Choose a valid option")

#These functions allow to manage the score file : 
def update_score(score_file, player_name, score):# Read the existing scores from the file
    try:
        with open(score_file, 'r', encoding='utf-8') as f:
            scores = f.readlines()
    except FileNotFoundError:
        scores = []

    player_found = False
    for i, line in enumerate(scores):
        name, player_score = line.strip().split(": ")
        if name == player_name:
            # If the player is found, update their score
            new_score = int(player_score) + score
            scores[i] = f"{name}: {new_score}\n"
            player_found = True
            break

    # If the player is not found, add a new entry
    if not player_found:
        scores.append(f"{player_name}: {score}\n")

    # Write the updated scores back to the file
    with open(score_file, 'w', encoding='utf-8') as f:
        f.writelines(scores)

# Function to view the scores
def view_scores(score_file):
    screen.fill(WHITE)
    draw_text("Scores:", font, BLACK, screen, w // 2, 50)
    
    try:
        with open(score_file, 'r', encoding='utf-8') as f:
            scores = f.readlines()
            if not scores:
                draw_text("No scores available.", font, BLACK, screen, w // 2, h // 3)
            else:
                y_offset = 100
                for score in scores:
                    draw_text(score.strip(), font, BLACK, screen, w // 2, y_offset)
                    y_offset += 40
    except FileNotFoundError:
        draw_text(f"Error: {score_file} not found.", font, RED, screen, w // 2, h // 3)

    draw_text("Press any key to return.", font, BLACK, screen, w // 2, h - 50)
    pygame.display.update()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False

# Function to display the delete scores confirmation screen
def confirm_delete_scores(score_file):
    screen.fill(WHITE)
    draw_text("Do you really want to delete all scores?", font, BLACK, screen, w // 2, h // 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, w // 2, h // 2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # User confirms delete
                    with open(score_file, 'w', encoding='utf-8') as f:
                        f.truncate(0)  # Empty the file
                    screen.fill(WHITE)
                    draw_text("All scores deleted!", font, BLACK, screen, w // 2, h // 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return
                elif event.key == pygame.K_n:  # User cancels delete
                    screen.fill(WHITE)
                    draw_text("Scores not deleted.", font, RED, screen, w // 2, h // 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return

# Function to delete all scores
def delete_scores(score_file):
    print("Do you really want to delete all scores? (y/n): ")
    confirm = input().strip().lower()  # Ask for confirmation from the user
    
    if confirm == 'y':
        with open(score_file, 'w', encoding='utf-8') as f:
            f.truncate(0)  # Empty the file
        print("All scores deleted.")
    elif confirm == 'n':
        print("Scores not deleted.")
    else:
        print("Invalid choice. Please enter 'y' or 'n'.")

# Function to display the delete scores confirmation screen
def confirm_delete_scores(score_file):
    screen.fill(WHITE)
    draw_text("Do you really want to delete all scores?", font, BLACK, screen, w // 2, h // 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, w // 2, h // 2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # User confirms delete
                    with open(score_file, 'w', encoding='utf-8') as f:
                        f.truncate(0)  # Empty the file
                    screen.fill(WHITE)
                    draw_text("All scores deleted!", font, BLACK, screen, w // 2, h // 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return
                elif event.key == pygame.K_n:  # User cancels delete
                    screen.fill(WHITE)
                    draw_text("Scores not deleted.", font, RED, screen, h // 2, h // 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return
                
def confirm_quit():
    screen.fill(WHITE)
    draw_text("Do you really want to quit?", font, BLACK, screen, w // 2, h // 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, w // 2, h // 2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # User confirms quit
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_n:  # User cancels quit
                    return  # Exit the confirmation screen and return to the menu
                
try :
    if __name__ == '__main__':
        score_file = "score.txt"
        choose_menu()
except KeyboardInterrupt :
    print(f"Exiting ....... ")