import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800  # Game window dimensions
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FRUIT_SIZE = 100
BOMB_SIZE = 100
ICE_SIZE = 100
SLICED_DISPLAY_TIME = 10  # Time to show sliced fruit before resetting

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
        letter_text = font.render(self.letter, True, BLACK)
        screen.blit(letter_text, (self.x + FRUIT_SIZE // 2, self.y + FRUIT_SIZE // 2))

    def reset(self):
        self.type = random.choice(list(fruit_images.keys()))  # New random fruit
        self.letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Assign new random letter
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
        self.letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

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
        self.letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

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
def draw_score_and_lives(score, lives):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

# Main game loop
def play():
    fruits = [Fruit(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")) for _ in range(2)]  # Only 2 fruits with letters
    bomb = Bomb()
    ice = Ice()
    score = 0
    lives = 3
    time_paused = False
    pause_timer = 0

    run = True
    while run:
        screen.blit(background, (0,0))  # yin yang background for an authentic fruit ninja experience
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
                    run = False
                if ice.letter == key_pressed:
                    time_paused = True
                    pause_timer = clock.get_fps() * random.randint(3, 5)
                    ice.reset()

        # Pause mechanics
        if time_paused:
            pause_timer -= 1
            if pause_timer <= 0:
                time_paused = False

        if not time_paused:
            # Update objects
            for fruit in fruits:
                fruit.update(time_paused)
            bomb.update()
            ice.update()

        
            # Check for clicks and calculate combo
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
                
                if detect_collision(bomb.x, bomb.y, BOMB_SIZE, click_pos):
                    font = pygame.font.Font(None, 48)
                    game_over_text = font.render("Game Over!", True, RED)
                    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    run = False

                if detect_collision(ice.x, ice.y, ICE_SIZE, click_pos):
                    time_paused = True
                    pause_timer = clock.get_fps() * random.randint(3, 5)
                    ice.reset()

            for fruit in fruits:
                if fruit.y > HEIGHT and not fruit.sliced:
                    lives -= 1
                    if lives == 0:
                        font = pygame.font.Font(None, 48)
                        game_over_text = font.render("Game Over!", True, RED)
                        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        run = False
                    fruit.reset()

        # Draw objects
        for fruit in fruits:
            fruit.draw()
        bomb.draw()
        ice.draw()
        draw_score_and_lives(score, lives)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    play()
