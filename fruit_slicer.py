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

# Load images
fruit_image = pygame.image.load("fruits/pasteque.png")
fruit_slice = pygame.image.load("fruits/pasteque_slice.png")
bomb_image = pygame.image.load("fruits/bomb.png")
ice_image = pygame.image.load("fruits/ice.png")

# Scale images
fruit_image = pygame.transform.scale(fruit_image, (FRUIT_SIZE, FRUIT_SIZE))
fruit_slice = pygame.transform.scale(fruit_slice, (FRUIT_SIZE, FRUIT_SIZE))
bomb_image = pygame.transform.scale(bomb_image, (BOMB_SIZE, BOMB_SIZE))
ice_image = pygame.transform.scale(ice_image, (ICE_SIZE, ICE_SIZE))

# Classes for game objects
class Fruit:
    def __init__(self):
        self.x = random.randint(FRUIT_SIZE // 2, WIDTH - FRUIT_SIZE // 2)
        self.y = HEIGHT - FRUIT_SIZE
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.randint(-12, -8)
        self.gravity = 0.1
        self.sliced = False
        self.sliced_time = 0  # Timer for sliced fruit

    def update(self):
        self.x += self.speed_x
        self.speed_y += self.gravity
        self.y += self.speed_y

        # If sliced, wait a few frames before resetting
        if self.sliced and pygame.time.get_ticks() - self.sliced_time > SLICED_DISPLAY_TIME * 50:
            self.reset()

    def draw(self):
        if self.sliced:
            screen.blit(fruit_slice, (self.x, self.y))  # Show sliced fruit
        else:
            screen.blit(fruit_image, (self.x, self.y))  # Show normal fruit

    def reset(self):
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

    def update(self):
        self.x += self.speed_x
        self.speed_y += self.gravity
        self.y += self.speed_y

    def draw(self):
        screen.blit(bomb_image, (self.x, self.y))

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
    fruits = [Fruit() for _ in range(5)]
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

            # Reset fruits that go off-screen
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

            if bomb.y > HEIGHT or bomb.x < 0 or bomb.x > WIDTH:
                bomb.reset()
            if ice.y > HEIGHT or ice.x < 0 or ice.x > WIDTH:
                ice.reset()

        # Draw objects
        for fruit in fruits:
            fruit.draw()
        bomb.draw()
        ice.draw()

        # Draw score and lives
        draw_score_and_lives(score, lives)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    play()
