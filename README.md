# 🎮 Breakout

A classic **Breakout** arcade game built with **Python** and **Pygame**. Control the paddle, keep the ball in play, and destroy every brick to complete each level.

This project recreates the original Breakout gameplay while adding multiple handcrafted levels with varying layouts and brick durability.

---

## Features

* 🎮 Classic Breakout gameplay
* 🧱 8 unique handcrafted levels
* ❤️ Brick durability system (1–4 hit points)
* ⚡ Dynamic ball reflection from the paddle
* 🎯 Accurate collision detection using previous-frame collision resolution
* 📋 Level selection menu
* 🏆 Win/Lose game states
* 🚀 Lightweight and beginner-friendly codebase
* 📦 No assets required—everything is rendered with Pygame primitives

---

## Gameplay

* Move the paddle to keep the ball in play.
* Break every brick to clear the level.
* Bricks require different numbers of hits depending on their color.
* If the ball falls below the screen, the level is lost.

---

## Controls

| Key     | Action                             |
| ------- | ---------------------------------- |
| ←       | Move paddle left                   |
| →       | Move paddle right                  |
| **1–8** | Select level from the menu         |
| **N**   | Next level (after winning)         |
| **R**   | Return to the level selection menu |
| **Q**   | Quit the game                      |

---

## Brick Colors

| Color     | Durability |
| --------- | ---------: |
| 🔴 Red    |      1 hit |
| 🟡 Yellow |     2 hits |
| 🟢 Green  |     3 hits |
| 🔵 Blue   |     4 hits |

---

## Project Structure

```
.
├── breakout.py      # Main game loop and state management
├── config.py        # Game constants and settings
├── levels.py        # Level layouts
├── objects.py       # Paddle, Ball, and Brick classes
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/claudere0/breakout.git
cd breakout
```

### Install dependencies

```bash
pip install pygame
```

---

## Running the Game

```bash
python breakout.py
```

---

## Game Architecture

### Game (`breakout.py`)

The `Game` class manages:

* Window creation
* Event handling
* Game states
* Collision detection
* Level loading
* Rendering
* Update loop

---

### Objects (`objects.py`)

Contains three core game objects:

* **Paddle**

  * Keyboard movement
  * Direction tracking for ball deflection

* **Ball**

  * Movement
  * Bouncing physics
  * Previous-frame position tracking for accurate collision handling

* **Brick**

  * Health system
  * Color based on durability
  * Destruction when health reaches zero

---

### Levels (`levels.py`)

Levels are represented as 8×8 integer grids.

Each number corresponds to brick durability:

```
0 = Empty
1 = Red
2 = Yellow
3 = Green
4 = Blue
```

This makes creating new levels as simple as editing a matrix.

---

## Collision System

Instead of relying only on overlapping rectangles, the game stores the ball's previous position every frame.

This allows collisions to determine whether the ball hit the:

* Top
* Bottom
* Left
* Right

of an object, producing more consistent and realistic bounces.

---

## Current Levels

1. Chessboard
2. Pyramid
3. Columns
4. Invader
5. Fortress
6. Hourglass
7. Maze
8. Final Challenge

Each level introduces different layouts and durability patterns.

---

## Technologies

* Python 3
* Pygame

---

## Future Improvements

Possible enhancements include:

* Sound effects
* Background music
* Particle effects
* Power-ups
* Multiple balls
* Score system
* Lives
* High score saving
* Pause menu
* Mouse support
* Animated bricks
* Sprite graphics
* Fullscreen mode

---

## Learning Goals

This project demonstrates:

* Object-oriented programming
* Game loops
* Collision detection
* State machines
* Basic game physics
* Pygame rendering
* Event-driven programming
* Level design using data structures

---

## License

This project is open source and available under the MIT License.

---

## Author

Created by **claudere0**.

If you found this project helpful, consider giving it a ⭐ on GitHub.
