import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800  # Game window dimensions
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FRUIT_SIZE = 50
BOMB_SIZE = 50
ICE_SIZE = 50
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

# Resize all fruit images
for key in fruit_images:
    fruit_images[key] = pygame.transform.scale(fruit_images[key], (FRUIT_SIZE, FRUIT_SIZE))
    sliced_fruit_images[key] = pygame.transform.scale(sliced_fruit_images[key], (FRUIT_SIZE, FRUIT_SIZE))

# Load and resize bomb & ice images
bomb_image = pygame.image.load("images/bomb.png")
ice_image = pygame.image.load("images/ice.png")
bomb_image = pygame.transform.scale(bomb_image, (BOMB_SIZE, BOMB_SIZE))
ice_image = pygame.transform.scale(ice_image, (ICE_SIZE, ICE_SIZE))

# Load bomb sliced image
bomb_sliced_image = pygame.image.load("images/bomb_slice.png")
bomb_sliced_image = pygame.transform.scale(bomb_sliced_image, (BOMB_SIZE, BOMB_SIZE))

# Classes for game objects
class Fruit:
    def __init__(self):
        self.type = random.choice(list(fruit_images.keys()))  
        self.x = random.randint(FRUIT_SIZE // 2, WIDTH - FRUIT_SIZE // 2)
        self.y = HEIGHT - FRUIT_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.gravity = 0.1
        self.sliced = False
        self.sliced_time = 0 

    def update(self):
        self.x += self.speed_x
        self.speed_y += self.gravity
        self.y += self.speed_y

        # If sliced, wait before resetting
        if self.sliced and pygame.time.get_ticks() - self.sliced_time > SLICED_DISPLAY_TIME * 50:
            self.reset()

    def draw(self):
        if self.sliced:
            screen.blit(sliced_fruit_images[self.type], (self.x, self.y))  
        else:
            screen.blit(fruit_images[self.type], (self.x, self.y))  
            
    def reset(self):
        self.type = random.choice(list(fruit_images.keys()))  # New random fruit
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
        self.gravity = 0.1
        self.sliced = False  # To track if the bomb has been sliced

    def update(self):
        if not self.sliced:  # Only update if not sliced
            self.x += self.speed_x
            self.speed_y += self.gravity
            self.y += self.speed_y

    def draw(self):
        if self.sliced:
            screen.blit(bomb_sliced_image, (self.x, self.y))  # Draw sliced bomb
        else:
            screen.blit(bomb_image, (self.x, self.y))  # Draw regular bomb

    def reset(self):
        self.x = random.randint(0, WIDTH - BOMB_SIZE)
        self.y = HEIGHT - BOMB_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.sliced = False  # Reset sliced state when the bomb resets

class Ice:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ICE_SIZE)
        self.y = HEIGHT - ICE_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.gravity = 0.1

    def update(self):
        self.x += self.speed_x
        self.speed_y += self.gravity
        self.y += self.speed_y

    def draw(self):
        screen.blit(ice_image, (self.x, self.y))

    def reset(self):
        self.x = random.randint(0, WIDTH - ICE_SIZE)
        self.y = HEIGHT - ICE_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)

# Detect collisions
def detect_collision(obj_x, obj_y, obj_size, click_pos):
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
    fruits = [Fruit() for _ in range(3)]  
    bomb = Bomb()
    ice = Ice()
    score = 0
    lives = 3
    time_paused = False
    pause_timer = 0

    run = True
    while run:
        screen.fill(WHITE)  # Clear screen
        click_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()

        # Pause mechanics
        if time_paused:
            pause_timer -= 1
            if pause_timer <= 0:
                time_paused = False

        if not time_paused:
            # Update objects
            for fruit in fruits:
                fruit.update()
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
                
                if detect_collision(bomb.x, bomb.y, BOMB_SIZE, click_pos) and not bomb.sliced:
                    bomb.sliced = True  # Slice the bomb
                    score -= 5  # Penalize the player for slicing the bomb
                    print("Bomb Sliced!")  # Optional: Add some visual or audio feedback

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
