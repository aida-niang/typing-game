import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800  # Game window dimensions
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0,128,0)
BLUE = (12,152,186)
FRUIT_SIZE = 100
BOMB_SIZE = 100
ICE_SIZE = 100
SLICED_DISPLAY_TIME = 10  # Time to show sliced fruit before resetting

#load sounds :
sound_winner = pygame.mixer.Sound('sounds/You_Win_Perfect.wav')
sound_loser = pygame.mixer.Sound('sounds/you_lost.wav')

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Fruit")
clock = pygame.time.Clock()

# Load fruit images (Normal & Sliced)
fruit_images = {
    "apple": pygame.image.load("images/apple.png"),
    "banana": pygame.image.load("images/banana.png"),
    "orange": pygame.image.load("images/orange.png"),  
    "pasteque": pygame.image.load("images/pasteque.png"),  
    "strawberry": pygame.image.load("images/strawberry.png"), 
}

sliced_fruit_images = {
    "apple": pygame.image.load("images/apple_slice.png"),
    "banana": pygame.image.load("images/banana_slice.png"),
    "orange": pygame.image.load("images/orange_slice.png"),
    "pasteque": pygame.image.load("images/pasteque_slice.png"),
    "strawberry": pygame.image.load("images/strawberry_slice.png"),
}

#background yin-yang
background=pygame.image.load("images/background_yin.jpeg")
background_ice = pygame.image.load("images/background_ice.jpg").convert_alpha()
background=background.convert()

# Resize all fruit images
for key in fruit_images:
    fruit_images[key] = pygame.transform.scale(fruit_images[key], (FRUIT_SIZE, FRUIT_SIZE))
    sliced_fruit_images[key] = pygame.transform.scale(sliced_fruit_images[key], (FRUIT_SIZE, FRUIT_SIZE))

# Load and resize bomb & ice images
bomb_image = pygame.image.load("images/bomb.png")
ice_image = pygame.image.load("images/ice.png")
bomb_image = pygame.transform.scale(bomb_image, (BOMB_SIZE, BOMB_SIZE))
ice_image = pygame.transform.scale(ice_image, (ICE_SIZE, ICE_SIZE))

#images : boom and ice break
bomb_image_sliced = pygame.image.load("images/bomb_slice.png")
# ice_image_sliced = pygame.image.load("images/")

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
        screen.blit(bomb_image, (self.x, self.y))
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

    def update(self):
        self.x += self.speed_x
        self.speed_y += self.gravity
        self.y += self.speed_y

    def draw(self):
        screen.blit(ice_image, (self.x, self.y))
        # Draw the letter on the ice
        font = pygame.font.Font(None, 36)
        letter_text = font.render(self.letter, True, BLACK)
        screen.blit(letter_text, (self.x + ICE_SIZE // 2, self.y + ICE_SIZE // 2))

    def reset(self):
        self.x = random.randint(0, WIDTH - ICE_SIZE)
        self.y = HEIGHT - ICE_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)

# Detect collisions
def detect_collision(obj_x, obj_y, obj_size, click_pos):
    if click_pos is None:
        return False  # No click, no collision
    return (
        obj_x <= click_pos[0] <= obj_x + obj_size and
        obj_y <= click_pos[1] <= obj_y + obj_size
    )

# Draw score and lives
def draw_score_lives_player(score, lives, player_name):
    font = pygame.font.Font(None, 36)
    players_text = font.render(f"Player's name : {player_name}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

#This function allow to write on pygame screen :
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def show_menu():
    screen.blit(background, (0,0))
    font = pygame.font.Font(None, 48)
    draw_text("--- Ninja Fruit ---", font, BLACK, screen, WIDTH// 2, HEIGHT// 4)
    draw_text("1. Play", font, BLACK, screen, WIDTH// 2, HEIGHT// 2 - 80)
    draw_text("2. Scores", font, BLACK, screen, WIDTH// 2, HEIGHT// 2 - 40)
    draw_text("3. Delete scores", font, BLACK, screen, WIDTH// 2, HEIGHT// 2)
    draw_text("4. Quit", font, BLACK, screen, WIDTH// 2, HEIGHT// 2 + 40)
    
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
                    play(score_file)
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    view_scores(score_file)
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    confirm_delete_scores(score_file)  
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4 or event.key == pygame.K_RETURN:
                    confirm_quit()  # Call the confirmation dialog function 
                else:
                    print("Choose a valid option")


def choose_difficulty():
    menu_run = True
    selected_difficulty = None  # Stocke la difficulté choisie
    font = pygame.font.Font(None, 48)

    while menu_run:
        screen.blit(background, (0,0))
        title_text = font.render("Choose difficulty level", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - 250, HEIGHT // 4))
        go_back_text = font.render("Press 'ESCAPE' to go back", True, RED)  
        screen.blit(go_back_text, (100, 100))
        

        # Options 
        easy_text = font.render("1. Easy", True, BLACK)
        medium_text = font.render("2. Midium", True, BLACK)
        hard_text = font.render("3. Difficult", True, BLACK)

        screen.blit(easy_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(medium_text, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(hard_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE :
                    choose_menu()
                if event.key == pygame.K_1:
                    selected_difficulty = "easy"
                elif event.key == pygame.K_2:
                    selected_difficulty = "medium"
                elif event.key == pygame.K_3:
                    selected_difficulty = "hard"

        if selected_difficulty:
            menu_run = False  # Quitter le menu et commencer le jeu

    return selected_difficulty

def get_player_name():
    input_box = pygame.Rect(0, 0, 200, 40) 
    input_box.center = (WIDTH// 2, HEIGHT// 2) 
    #input_box = pygame.Rect(WIDTH// 2 - 100, h // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 48)

    while True:
        screen.blit(background, (0, 0))
        go_back_text = font.render("Press 'ESCAPE' to go back", True, RED)  
        screen.blit(go_back_text, (100, 100))
        draw_text("Enter your name:", font, BLACK, screen, WIDTH// 2, HEIGHT// 3)
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(text, font, BLACK, screen, WIDTH// 2, HEIGHT// 2)
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
                if event.key == pygame.K_ESCAPE :
                    choose_difficulty()

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
    font = pygame.font.Font(None, 48)
    screen.fill(WHITE)
    draw_text("Scores:", font, BLACK, screen, WIDTH// 2, 50)
    
    try:
        with open(score_file, 'r', encoding='utf-8') as f:
            scores = f.readlines()
            if not scores:
                draw_text("No scores available.", font, BLACK, screen, WIDTH// 2, HEIGHT// 3)
            else:
                y_offset = 100
                for score in scores:
                    draw_text(score.strip(), font, BLACK, screen, WIDTH// 2, y_offset)
                    y_offset += 40
    except FileNotFoundError:
        draw_text(f"Error: {score_file} not found.", font, RED, screen, WIDTH// 2, HEIGHT// 3)

    draw_text("Press any key to return.", font, BLACK, screen, WIDTH// 2, HEIGHT- 50)
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
    font = pygame.font.Font(None, 48)
    screen.fill(WHITE)
    draw_text("Do you really want to delete all scores?", font, BLACK, screen, WIDTH// 2, HEIGHT// 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, WIDTH// 2, HEIGHT// 2)
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
                    draw_text("All scores deleted!", font, BLACK, screen, WIDTH// 2, HEIGHT// 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return
                elif event.key == pygame.K_n:  # User cancels delete
                    screen.fill(WHITE)
                    draw_text("Scores not deleted.", font, RED, screen, WIDTH// 2, HEIGHT// 2)
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
    font = pygame.font.Font(None, 48)
    screen.fill(WHITE)
    draw_text("Do you really want to delete all scores?", font, BLACK, screen, WIDTH// 2, HEIGHT// 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, WIDTH// 2, HEIGHT// 2)
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
                    draw_text("All scores deleted!", font, BLACK, screen, WIDTH// 2, HEIGHT// 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # Show message for 2 seconds
                    return
                elif event.key == pygame.K_n:  # User cancels delete
                    screen.fill(WHITE)
                    draw_text("Scores not deleted.", font, RED, screen, HEIGHT// 2, HEIGHT// 2)
                    pygame.display.update()
                    pygame.time.delay(2000)  # ShoWIDTHmessage for 2 seconds
                    return
                
def confirm_quit():
    font = pygame.font.Font(None, 48)
    screen.fill(WHITE)
    draw_text("Do you really want to quit?", font, BLACK, screen, WIDTH// 2, HEIGHT// 3)
    draw_text("Press Y to confirm or N to cancel.", font, BLACK, screen, WIDTH// 2, HEIGHT// 2)
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


# Main game loop
def play(score_file):
    difficulty = choose_difficulty()
    player_name = get_player_name()
    
    # Définir le nombre initial de fruits en fonction du niveau
    if difficulty == "easy":
        num_fruits = 2
    elif difficulty == "medium":
        num_fruits = 4
    elif difficulty == "hard":
        num_fruits = 6


    fruits = [Fruit(random.choice("ABCDEFGHIJKLMNOP")) for _ in range(num_fruits)]  # Only 2 fruits with letters
    bomb = Bomb()
    ice = Ice()
    score = 0
    lives = 3
    time_paused = False
    pause_timer = 0
    frozen = False
    frozen_start = 0
    frozen_duration = 0
    run = True
    while run:
        screen.blit(background, (0, 0))  
        
        click_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key).upper()  # Get the pressed key
                for fruit in fruits:
                    if fruit.letter == key_pressed and not fruit.sliced:
                        fruit.sliced = True
                        fruit.sliced_time = pygame.time.get_ticks()  # Store slice time
                        score += 1  # Increase score when correct key is pressed
                        break
                
                # Detect Bomb or Ice key press
                if bomb.letter == key_pressed:
                    font = pygame.font.Font(None, 48)
                    game_over_text = font.render("Game Over!", True, RED)
                    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    sound_loser.play()
                    pygame.time.wait(int(sound_loser.get_length() * 1000))
                    run = False
                    show_menu()
                
                if ice.letter == key_pressed:
                    # ice_surface=background_ice.copy()
                    # ice_surface.set_alpha(80) #adding a transparency effect so the user can still see the fruits
                    # screen.blit(ice_surface, (0, 0))
                    # pygame.display.flip()
                    # pygame.time.delay(30)
                    time_paused = True
                    pause_timer = clock.get_fps() * random.randint(3, 5)
                    ice.reset()

                    

        # Pause mechanics
        if time_paused:
            pause_timer -= 1
            if pause_timer <= 0:
                time_paused = False

        # Update objects (skip the update if time is paused)
        if not time_paused:
            for fruit in fruits:
                fruit.update(time_paused)
            bomb.update()
            ice.update()

        # Check for clicks and calculate combo (works when time is paused as well)
        if click_pos:
            combo_count = 0
            for fruit in fruits:
                if detect_collision(fruit.x, fruit.y, FRUIT_SIZE, click_pos) and not fruit.sliced:
                    fruit.sliced = True
                    fruit.sliced_time = pygame.time.get_ticks()  # Store slice time
                    combo_count += 1

            if combo_count > 0:
                score += combo_count  # Base points
                score += combo_count - 1  # Bonus for combos

            # Check collision with bomb and ice (even when paused)
            if detect_collision(bomb.x, bomb.y, BOMB_SIZE, click_pos):
                font = pygame.font.Font(None, 48)
                game_over_text = font.render("Game Over!", True, RED)
                screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                pygame.display.flip()
                pygame.time.delay(2000)
                #sound_loser.play()
                #pygame.time.wait(int(sound_loser.get_length() * 1000))
                run = False
                choose_menu()

            if detect_collision(ice.x, ice.y, ICE_SIZE, click_pos):
                time_paused = True
                screen.blit(background_ice, (0,0))
                pygame.display.flip()
                pause_timer = clock.get_fps() * random.randint(3, 5)
                pygame.time.delay(int(pause_timer))
                ice.reset()
                

        # Handle fruits falling off the screen (if paused, they still drop)
        for fruit in fruits:
            if fruit.y > HEIGHT and not fruit.sliced:
                lives -= 1
                if lives == 0:
                    font = pygame.font.Font(None, 48)
                    game_over_text = font.render("Game Over!", True, RED)
                    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    sound_loser.play()
                    pygame.time.wait(int(sound_loser.get_length() * 1000))
                    run = False
                    choose_menu()
                fruit.reset()

        # Draw objects
        for fruit in fruits:
            fruit.draw()
        bomb.draw()
        ice.draw()
        draw_score_lives_player(score, lives, player_name)

        pygame.display.flip()
        clock.tick(60)
        update_score(score_file, player_name, score)

    pygame.quit()
try : 
    if __name__ == "__main__":
        choose_menu()
except KeyboardInterrupt :
    print(f"Exiting......")