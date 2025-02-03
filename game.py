import pygame
import random
import os
from settings import *
from utils import load_gif_frames
from objects import Fruit, Bomb, Ice, bomb_image_sliced, ice_image_sliced

# Initialize pygame and its modules
pygame.init()
pygame.font.init()  
pygame.mixer.init() 

#load sounds :
sound_start = pygame.mixer.Sound('assets/sounds/game.wav')
sound_end = pygame.mixer.Sound('assets/sounds/you_lost.wav')

# Font setup
font_game = pygame.font.Font("assets/fonts/arcade.ttf", 18)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Fruit")
clock = pygame.time.Clock()

#Load background 
background=pygame.image.load("assets/images/background_yin.jpeg")
#background_ice = pygame.image.load("assets/images/background_ice.jpg").convert_alpha()
background=background.convert()
start_screen_bg = pygame.image.load("assets/images/start.png")
start_screen_bg = pygame.transform.scale(start_screen_bg, (WIDTH, HEIGHT))
easy_bg = pygame.image.load("assets/images/easy.png")
easy_bg = pygame.transform.scale(easy_bg, (WIDTH, HEIGHT))
medium_bg = pygame.image.load("assets/images/medium.png")
medium_bg = pygame.transform.scale(medium_bg, (WIDTH, HEIGHT))
hard_bg = pygame.image.load("assets/images/hard.png")
hard_bg = pygame.transform.scale(hard_bg, (WIDTH, HEIGHT))


#load GIF frames
loading_frames = load_gif_frames("assets/images/loading")
easy_gif_frames = load_gif_frames("assets/images/easy")
medium_gif_frames = load_gif_frames("assets/images/medium")
hard_gif_frames = load_gif_frames("assets/images/hard")
scores_gif_frames = load_gif_frames("assets/images/scores")
quit_gif_frames = load_gif_frames("assets/images/quit")

def loading_screen():
    frame_index = 0
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.blit(start_screen_bg, (0, 0))

        # Display text "Loading..."
        font = font_game
        loading_text = font.render("Loading...", True, WHITE)
        screen.blit(loading_text, (620, 700))

        # Display animation gif
        screen.blit(loading_frames[frame_index], (600, 730))
        frame_index = (frame_index + 1) % len(loading_frames)  # Change frame

        pygame.display.flip()
        clock.tick(10)  # speed (~10 FPS)

        # Stop after 3 seconds
        if pygame.time.get_ticks() - start_time > 3000:
            running = False

        # Handle events (close window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def choose_menu(): 
    score_file = "scores.txt"
    frame_index_easy = 0
    frame_index_medium = 0
    frame_index_hard = 0
    clock = pygame.time.Clock()

    # Define the position and size of the areas
    easy_rect = pygame.Rect(50, 20, 400, 380)  
    medium_rect = pygame.Rect(500, 200, 400, 400)
    hard_rect = pygame.Rect(950, 20, 400, 380)
    scores_rect = pygame.Rect(50, 400, 400, 380)
    quit_rect = pygame.Rect(950, 400, 400, 380)

    while True:
        screen.blit(background, (0, 0))

        font = font_game
        loading_text = font.render("Start playing...", True, WHITE)
        screen.blit(loading_text, (600, 50))

        # Draw clickable areas
        pygame.draw.rect(screen, (255, 0, 0), easy_rect, 2)  
        pygame.draw.rect(screen, (0, 255, 0), medium_rect, 2)  
        pygame.draw.rect(screen, (0, 0, 255), hard_rect, 2) 
        pygame.draw.rect(screen, (255, 0, 0), scores_rect, 2)  
        pygame.draw.rect(screen, (0, 255, 0), quit_rect, 2)   

        # Display animations
        screen.blit(easy_gif_frames[frame_index_easy], (50, 20))
        screen.blit(medium_gif_frames[frame_index_medium], (500, 200))
        screen.blit(hard_gif_frames[frame_index_hard], (950, 20))
        screen.blit(scores_gif_frames[frame_index_medium], (50, 400))
        screen.blit(quit_gif_frames[frame_index_hard], (950, 400))

        # Change frames for GIF animation
        frame_index_easy = (frame_index_easy + 1) % len(easy_gif_frames)
        frame_index_medium = (frame_index_medium + 1) % len(medium_gif_frames)
        frame_index_hard = (frame_index_hard + 1) % len(hard_gif_frames)

        pygame.display.flip()
        clock.tick(10)  

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    play('easy')  
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    play('medium')  
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    play('hard')  
                elif event.key == pygame.K_4 or event.key == pygame.K_KP3 :
                    view_scores(score_file)
                elif event.key == pygame.K_5 or event.key == pygame.K_KP4 or event.key == pygame.K_RETURN:
                    confirm_quit() 

            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
            
                    if easy_rect.collidepoint(mouse_x, mouse_y):
                        play('easy')  
                    elif medium_rect.collidepoint(mouse_x, mouse_y):
                        play('medium')  
                    elif hard_rect.collidepoint(mouse_x, mouse_y):
                        play('hard')  
                    elif scores_rect.collidepoint(mouse_x, mouse_y):
                        view_scores ()
                        #if delete_score_rect.collidepoint(mouse_x, mouse_y):
                            #confirm_delete_scores
                    elif quit_rect.collidepoint(mouse_x, mouse_y):
                        confirm_quit ()

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

def get_player_name(difficulty):
    input_box = pygame.Rect(0, 0, 200, 40) 
    input_box.center = (700, 430) 
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 48)

    # Choose background based on difficulty
    if difficulty == "easy":
        background = easy_bg
    elif difficulty == "medium":
        background = medium_bg
    elif difficulty == "hard":
        background = hard_bg

    while True:
        # Apply the selected background
        screen.blit(background, (0, 0)) 
        go_back_text = font.render("Press 'ESCAPE' to go back", True, RED)  
        screen.blit(go_back_text, (100, 100))
        draw_text("Enter your name", font_game, WHITE, screen, 700, 380)
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(text, font_game, WHITE, screen, 700, 430)
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
                    choose_menu()

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
def play(difficulty):
    score_file = 'scores.txt'
    player_name = get_player_name(difficulty)

    # Définir num_fruits en fonction de la difficulté
    if difficulty == "easy":
        num_fruits = 2
    elif difficulty == "medium":
        num_fruits = 6
    elif difficulty == "hard":
        num_fruits = 10
    else:
        num_fruits = 4  # Par défaut, choisir une difficulté "medium"

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
    sound_start.play()

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
                    #display boom
                    screen.blit(bomb_image_sliced, (bomb.x, bomb.y))
                    pygame.display.flip()
                    pygame.time.delay(500) #update display and leaving a bit of time to see the boom
                    font = pygame.font.Font(None, 48)
                    game_over_text = font.render("Game Over!", True, RED)
                    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    sound_end.play()
                    pygame.time.wait(int(sound_end.get_length() * 1000))
                    run = False
                    choose_menu()
                
                if ice.letter == key_pressed:
                    time_paused = True
                    screen.blit(ice_image_sliced, (ice.x, ice.y))
                    pygame.display.flip()
                    pause_timer = clock.get_fps() * random.randint(3, 5)
                    pygame.time.delay(int(pause_timer))
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
                screen.blit(bomb_image_sliced, (bomb.x, bomb.y))
                sound_start.stop()
                pygame.display.flip()
                pygame.time.delay(500) #update display and leaving a bit of time to see the boom    
                font = pygame.font.Font(None, 48)
                game_over_text = font.render("Game Over!", True, RED)
                screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                pygame.display.flip()
                pygame.time.delay(2000)
                sound_end.play()
                run = False
                choose_menu()

            if detect_collision(ice.x, ice.y, ICE_SIZE, click_pos):
                time_paused = True
                screen.blit(ice_image_sliced, (ice.x,ice.y))
                pygame.display.flip()
                pause_timer = clock.get_fps() * random.randint(3, 5)
                pygame.time.delay(int(pause_timer))
                ice.reset()
                

        # Handle fruits falling off the screen (if paused, they still drop)
        for fruit in fruits:
            if fruit.y > HEIGHT and not fruit.sliced:
                lives -= 1
                if lives == 0:
                    sound_start.stop()
                    font = pygame.font.Font(None, 48)
                    game_over_text = font.render("Game Over!", True, RED)
                    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    sound_end.play()
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