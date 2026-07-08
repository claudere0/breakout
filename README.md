# Breakout (Pygame)

![Gameplay](images/screenshot.png)

A classic Breakout game written in Python using Pygame.

This project was created to practice object-oriented programming, game loops, delta time movement, collision detection, and basic game architecture.

## Features

- Classic Breakout gameplay with 8 handcrafted levels
- Brick durability system (1–4 hits) with color coding
- Dynamic ball reflection from the paddle
- Precise collision resolution using previous-frame tracking
- Level selection menu
- Delta time based movement

## Controls

| Key | Action |
|-----|--------|
| ← | Move Paddle Left |
| → | Move Paddle Right |
| **1–8** | Select Level (from the menu) |
| **N** | Next Level (after winning) |
| **R** | Return to Level Selection |
| **Q** | Quit |

## Project Structure

```
project/
│
├── breakout.py
├── config.py
├── levels.py
├── objects.py
└── README.md
```

## Architecture

The project is built around the following files:

- **breakout.py** – Manages the game loop, events, level transition state, and collision resolution logic.
- **objects.py** – Defines the `Paddle`, `Ball`, and `Brick` classes.
- **levels.py** – Contains the layout matrices for the 8 levels.
- **config.py** – Stores game settings, colors, window sizes, and state definitions.

## Installation

```bash
pip install pygame
```

## Running the game

```bash
python breakout.py
```
