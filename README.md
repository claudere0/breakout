# 🕹️ Breakout Game in Python & Pygame

A classic arcade-style Breakout game built from scratch using Python and the Pygame library. This project is specifically designed to be simple, lightweight, and easy to understand for beginners who are interested in game development.

---

## 📖 Table of Contents
1. [What is Breakout?](#-what-is-breakout)
2. [Project Architecture (How it Fits Together)](#-project-architecture-how-it-fits-together)
3. [Key Game Programming Concepts](#-key-game-programming-concepts)
4. [Getting Started (Installation)](#-getting-started-installation)
5. [How to Play & Game Controls](#-how-to-play--game-controls)
6. [Understanding the Code (Code Walkthrough)](#-understanding-the-code-code-walkthrough)
7. [Collision Detection Explained](#-collision-detection-explained)
8. [Modding Guide (Create Your Own Features!)](#%EF%B8%8F-modding-guide-create-your-own-features)
9. [Future Roadmap / Ideas](#-future-roadmap-ideas)
10. [License](#-license)

---

## 🧱 What is Breakout?
Breakout is a classic arcade game where the player controls a horizontal **paddle** at the bottom of the screen. A **ball** bounces around the screen, and the player must prevent it from falling off the bottom edge by bouncing it back up. The goal is to hit and destroy all the colored **bricks** at the top of the screen.

In this implementation:
- **No external image or sound files are needed!** All visuals are rendered in real-time using mathematical shapes (rectangles and circles) provided by Pygame.
- Bricks have different levels of durability (hit points) represented by their colors.
- The game comes with **8 handcrafted levels** of varying difficulty and patterns.

---

## 📂 Project Architecture (How it Fits Together)
The project is divided into four main Python files. This keeps the code clean and organized:

```
breakout/
│
├── config.py         # ⚙️ Game settings, screen size, colors, and game states
├── objects.py        # 🧱 Blueprints (Classes) for the Paddle, Ball, and Bricks
├── levels.py         # 🗺️ Level designs represented as simple grid arrays (matrices)
└── breakout.py       # 🧠 The "brain" / main controller that runs the game loop
```

### File Breakdown:
- **[config.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/config.py)**: Contains global variables and configuration constants like the screen width/height, frames per second (FPS), RGB colors, and numerical constants for the game states (`MENU`, `PLAYING`, `WIN`, `LOSE`).
- **[levels.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/levels.py)**: Defines the layout grids for all 8 levels. Each level is an $8 \times 8$ grid of numbers where `0` means empty space and `1-4` represents brick durability.
- **[objects.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/objects.py)**: Defines the three key interactive components: `Paddle`, `Ball`, and `Brick`. Each contains its own state (position, size, speed) and code to update its state or draw itself on the screen.
- **[breakout.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/breakout.py)**: Initializes Pygame, creates the window, handles keyboard inputs, handles collisions between objects, and controls transitions between the menus, gameplay, winning, and losing states.

---

## 💡 Key Game Programming Concepts
If you are new to game programming, here are the most important concepts used in this codebase:

### 1. The Game Loop
A game is essentially a program that runs a continuous loop. Every single frame (60 times per second), the game performs three actions in order:
1. **Handle Events**: Checks if the player pressed a key, moved the mouse, or clicked the close window button.
2. **Update**: Calculates new positions, checks for collisions, and updates game states.
3. **Draw (Render)**: Clears the screen and draws the updated objects.

### 2. Delta Time (`dt`)
Computers run at different speeds. If we moved the paddle by a fixed number of pixels every frame, it would move faster on a high-end computer than on a slow one. 
To prevent this, the game calculates **Delta Time** (`dt`)—the time in seconds that passed since the last frame. By multiplying speeds (like `paddle.speed`) by `dt`, the movement becomes time-dependent rather than frame-dependent, ensuring smooth gameplay on all systems:
$$\text{New Position} = \text{Old Position} + \text{Speed} \times dt$$

### 3. Rectangles (`pygame.Rect`)
Pygame provides a powerful `Rect` object to represent 2D rectangular areas. Rectangles make it extremely easy to handle positioning and collision detection using built-in methods like `.colliderect()`.

---

## 🚀 Getting Started (Installation)

### Prerequisites
Make sure you have **Python 3** installed on your computer. You can download it from the [Official Python Website](https://www.python.org/downloads/).

### 1. Clone or Download the Project
Download the project files or clone the repository using Git:
```bash
git clone https://github.com/claudere0/breakout.git
cd breakout
```

### 2. Install Pygame
Pygame is the library used to handle window creation, rendering, and inputs. Install it via pip:
```bash
pip install pygame
```

### 3. Run the Game
Execute the main file using Python:
```bash
python breakout.py
```

---

## 🎮 How to Play & Game Controls

### Game Flow:
1. **Menu**: When the game starts, you will see a level selection screen. Press a number key from `1` to `8` to load that level.
2. **Playing**: Keep the ball bouncing. Break all the bricks to win the level!
3. **Win/Lose**: 
   - If the ball falls past the paddle, you lose. Press `R` to return to the selection menu.
   - If you break all bricks, you win! Press `N` to proceed to the next level, or `R` to return to the menu.

### Control Reference:
| Key | Action |
| :--- | :--- |
| `←` (Left Arrow) | Move paddle left |
| `→` (Right Arrow) | Move paddle right |
| `1` to `8` | Choose a level (from the selection menu) |
| `R` | Return to selection menu (when winning/losing) |
| `N` | Load the next level (when winning, if not on level 8) |
| `Q` | Quit the game |

---

## 🔍 Understanding the Code (Code Walkthrough)

### 🧱 Bricks & Durability
In [objects.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/objects.py), each brick has a `health` parameter. When the ball hits a brick, the `hit()` method decreases its health. The brick changes color based on how many hits it has remaining:

| Brick Color | Hits Needed to Destroy |
| :--- | :---: |
| 🔴 Red | 1 hit |
| 🟡 Yellow | 2 hits |
| 🟢 Green | 3 hits |
| 🔵 Blue | 4 hits |

### 🗺️ Designing Levels
Levels are stored in [levels.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/levels.py) as $8 \times 8$ matrices. Here is how the "Pyramid" level is structured:
```python
[
    [0,0,0,3,3,0,0,0],  # 3 = Green (3 hits)
    [0,0,3,3,3,3,0,0],
    [0,2,2,2,2,2,2,0],  # 2 = Yellow (2 hits)
    [0,2,2,2,2,2,2,0],
    [1,1,1,1,1,1,1,1],  # 1 = Red (1 hit)
    [1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0],  # 0 = Empty space
    [0,0,0,0,0,0,0,0],
]
```

---

## 💥 Collision Detection Explained
In standard games, collision detection checks if two rectangles overlap. However, if a fast-moving ball enters a brick, simple overlap checks don't tell us *which side* the ball hit. This can make the ball bounce in weird, glitchy directions.

To solve this, the game uses **previous-frame collision resolution**:
1. Every frame, before updating the ball's position, we store the ball's current rectangle in `self.prev_rect` ([objects.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/objects.py#L48)).
2. If the ball collides with a brick or the paddle, the `resolve_collision()` method in [breakout.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/breakout.py#L65) checks where the ball *used to be* in the previous frame:
   - If the ball's previous bottom was above the obstacle's top, it must have hit the **top**. We bounce it vertically (`bounce("y")`).
   - If the ball's previous top was below the obstacle's bottom, it must have hit the **bottom**. We bounce it vertically (`bounce("y")`).
   - If the ball's previous right was to the left of the obstacle's left edge, it hit the **left side**. We bounce it horizontally (`bounce("x")`).
   - If the ball's previous left was to the right of the obstacle's right edge, it hit the **right side**. We bounce it horizontally (`bounce("x")`).
3. This creates clean, predictable, and robust physics!

> [!TIP]
> **Paddle Steering**: When the ball hits the top of the paddle, the ball's horizontal speed is adjusted based on the paddle's movement speed ([breakout.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/breakout.py#L97)). Moving to the right while hitting the ball pushes the ball to bounce more to the right, allowing you to "steer" the ball!

---

## 🛠️ Modding Guide (Create Your Own Features!)
This codebase is an excellent playground for learning. Here are three simple modifications you can try:

### Challenge 1: Customize Colors and Window Size
Open [config.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/config.py) and change the constants:
- Adjust `WIDTH` and `HEIGHT` (e.g., set them to `600` or `800`).
- Create a new color by defining an RGB tuple, like `PURPLE = (128, 0, 128)`, and use it in [objects.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/objects.py) to change the paddle or ball color.

### Challenge 2: Make the Game Faster or Harder
Open [objects.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/objects.py):
- In `Paddle.reset()` (line 13), change `self.speed = 480` to make the paddle move faster or slower.
- In `Ball.reset()` (lines 43-44), change `self.speed_x` and `self.speed_y` to speed up the ball.

### Challenge 3: Create a Custom Level
Open [levels.py](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/levels.py):
- Edit one of the matrices in the `LEVELS` list.
- Use `0` for empty space, `1` for Red, `2` for Yellow, `3` for Green, and `4` for Blue.
- Try making a level in the shape of a smiley face, initials, or an obstacle pattern!

---

## 🌟 Future Roadmap (Ideas to Add)
Want to practice programming? Here are some features you can try adding to the game:
- 🔊 **Sound Effects**: Play a sound when the ball hits a brick or paddle using `pygame.mixer`.
- 💖 **Lives System**: Give the player 3 lives instead of ending the game immediately when the ball falls.
- 🏆 **Score System**: Gain points based on the brick color destroyed. Display the score at the top of the screen.
- ⚡ **Power-ups**: Drop random power-ups from destroyed bricks (e.g., extra balls, wider paddle, slow-motion ball).
- 🖱️ **Mouse Control**: Allow moving the paddle using the mouse cursor instead of just keys.

---

## 📝 License
This project is open-source and licensed under the [MIT License](file:///Users/amirkarataev/Desktop/Python3/projects/breakout/LICENSE).

## 👤 Author
Created with ❤️ by **claudere0**. If you enjoyed learning from this project, feel free to give it a ⭐ on GitHub!
