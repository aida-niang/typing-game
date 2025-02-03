import pygame
from game import play, choose_menu, loading_screen

# Main function to handle game flow (menu, difficulty selection)
def main():
    loading_screen()  # Show loading screen first
    difficulty = choose_menu()  # Show main menu and get difficulty
    play(difficulty)  # Start the game loop with the chosen difficulty

# Start the game
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
