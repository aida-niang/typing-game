# Pokémon Game in Python

![preview main](./frame_2.png)

## Project Description

This is a fun and interactive Typing Game inspired by Fruit Ninja. The game challenges players to type the words on falling fruits or click on them with the mouse to slice them. The faster and more accurately you type, the higher your score!
The game mechanics include:
- 3 Lives: You lose a life if you fail to slice a fruit.
- Game Over: Instantly lose if you slice a bomb.
- Freeze Power-up: Time pauses when you slice an ice.
This game is designed to improve typing speed and accuracy while providing an exciting gaming experience!

## Demo

Playing the game: [Live Demo](https://www.youtube.com/watch?v=XTXSr6LRkes)

## 🎮 Features

- Fruit Slicing Mechanics: Slice fruits by typing the words that appear on them or clicking with the mouse.
- Typing Challenge: The faster you type, the more fruits you slice.
- Multiple Levels:
  - Easy: Slow fruit movement and fewer fruits (2).
  - Medium: Faster fruit movement and increased number of fruits (4).
  - Difficult: Fastest speed with the most fruits appearing (8).
- Score Tracking: Keep track of your current and best scores.
- Sound Effects: Enjoy immersive fruit-slicing sounds.
- Visual Effects: Beautiful fruit animations upon slicing.
- Lives Counter: Start with 3 lives—lose one if you miss a fruit.
- Randomly Generated Fruits: Each fruit carries different letters/words.
- Physics-based Movement: Fruits fall realistically using physics-based animation.


## Technologies and tools Used

- Python: Main programming language.
- Pygame: Library for game development.
- Canva: Used for designing game images and assets.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.x
- The following Python libraries:
  - `pygame`

## Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/aida-niang/pokemon.git
   ```
2. Install dependencies:
   ```bash
   pip install pygame 
   ```

## Usage

Run the game with:
```bash
python3 main.py
```

## Project Structure

```
📂 typing-game  
├── 📁 assets/            # Graphics and sound resources  
│   ├── 📁 fonts/         # Fonts used in the game (e.g., for text rendering)  
│   ├── 📁 images/        # Graphics for fruits, ice, bomb, and UI elements  
│   ├── 📁 sounds/        # Sound effects (slice, bomb, ice freeze, loss, background music)  
├── game.py               # Main game logic, handling player interactions and game mechanics  
├── main.py               # Entry point for the game, starts the game loop  
├── objects.py            # Defines fruit, bomb, and ice classes with movement and slicing mechanics  
├── scores.txt            # Saves player scores based on the number of fruits sliced  
├── settings.py           # Stores game settings (e.g., screen size, speed, colors)  
├── utils.py              # Utility functions (e.g., loading assets, animations)  
├── .gitignore            # Excludes unnecessary files (e.g., local score data)  
└── README.md             # Project documentation  


```

## Detailed File Descriptions
- game.py : Manages the game loop, updating game objects, and handling user input.
- main.py : Entry point that initializes game settings and starts the main loop.
- objects.py : Defines the Fruit, Bomb, and Ice classes with their properties (e.g., movement speed, effects on the game).
- scores.txt : Stores high scores based on the number of fruits sliced.
- settings.py : Contains game settings such as screen resolution, colors, and fruits adjustments.
- utils.py : Includes helper functions for animations.
- assets/ : Folder containing all visual and audio elements used in the game (images, sounds, fonts).

## Contributing

This project was developed by:
- [Aida NIANG](https://github.com/aida-niang/)
- Amina TALEB
- Yannis MESSADIA

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thanks to everyone who contributed to the development of this game!

## Built With

- Python 3.8
- Pygame
- Canva

## Contact

**Aida NIANG** 
- I'm in : [LinkedIn](https://linkedin.com/in/aidabenhamathniang)
- Contact me : [Email](mailto:aidam.niang@gmail.com  )
- Project Link: [Portfolio](https://aida-niang.students-laplateforme.io)

