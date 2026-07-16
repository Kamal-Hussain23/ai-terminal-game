# Danger Dragon

A terminal-based Python game where you guide the Dragon Rider across a dangerous 5x5 grid to collect dragon eggs while avoiding volcanic hazards.

## Story

> *Navigate the Dragon Rider to collect eggs.*

You are the Dragon Rider (🤠). Eggs (🥚) are scattered across the grid, but so are deadly volcanoes (🌋). Collect 10 eggs to win. Step on a volcano and it's game over.

## Features

- **WASD Movement** — Move with `W` (up), `A` (left), `S` (down), `D` (right)
- **Collectible System** — Pick up eggs to increase your score; each egg respawns at a new random location
- **Hazard Tiles** — Volcanoes appear at random positions; stepping on one ends the game
- **Win/Lose Conditions** — Reach score 10 to win; hit a volcano to lose
- **Replay Support** — After each round, choose to play again or exit cleanly
- **Boundary Protection** — Player cannot move off the grid
- **Themed UI** — Custom emojis and story-driven intro

## How to Run

### Play the Game

```bash
python game.py
```

### Run the Tests

```bash
pytest test_game.py -v
```

The test suite includes 27 tests covering:

| Test Class | Tests | What's Covered |
|---|---|---|
| TestInitGame | 5 | Spawning logic and grid boundaries |
| TestHandleMovement | 8 | WASD input and boundary checks |
| TestPlayRound | 3 | Quit, game over, play again |
| TestGameLoop | 2 | Multi-round restart flow |
| TestConstants | 2 | Grid size and win score |
| TestTheme | 7 | Game name, emojis, and messages |

## Project Structure

```
ai-terminal-game/
├── game.py          # Main game logic and entry point
├── test_game.py     # Pytest test suite
├── .gitignore       # Excludes __pycache__, .pytest_cache
└── README.md        # This file
```

## What I Learned

### Iterative Development

This project was built step by step, starting with a bare grid and adding features one at a time: movement, collectibles, hazards, scoring, win/lose conditions, restart, and finally theming. Each step was tested before moving to the next. This approach made it easy to isolate bugs and understand how each piece of the system fit together.

### Engineering Prompts to Prevent Regression

Every time a new feature was added, existing tests were re-run to make sure nothing broke. When refactoring the code into functions, the tests were rewritten to match the new structure rather than relying on the old module-level variables. This discipline caught issues like the `NameError` that appeared when spawn functions referenced variables that hadn't been initialized yet — a classic regression that automated tests surfaced immediately.

### The Value of Automated Tests

Writing tests alongside the game forced clearer function design. Functions like `handle_movement()` and `init_game()` were naturally shaped to be testable — taking inputs and returning outputs rather than relying on global state. The test suite now serves as both a safety net for future changes and living documentation of how every feature is supposed to behave.

## Built With

- **Python 3.11** — Core language
- **pytest** — Test framework
- **unittest.mock** — Test isolation via input/output mocking
