# Simple Text-Based Game on a 5x5 Grid
import random

# Player starts at position (0, 0)
player_row = 0
player_col = 0
grid_size = 5
score = 0
win_score = 10


def spawn_collectible():
    """Spawn collectible at a random position not occupied by the player or hazard."""
    while True:
        row = random.randint(0, grid_size - 1)
        col = random.randint(0, grid_size - 1)
        if (row != player_row or col != player_col) and (row != hazard_row or col != hazard_col):
            return row, col


def spawn_hazard():
    """Spawn hazard at a random position not occupied by the player or collectible."""
    while True:
        row = random.randint(0, grid_size - 1)
        col = random.randint(0, grid_size - 1)
        if (row != player_row or col != player_col) and (row != collectible_row or col != collectible_col):
            return row, col


# Initial spawn: collectible first (only checks player), then hazard (checks both)
while True:
    collectible_row = random.randint(0, grid_size - 1)
    collectible_col = random.randint(0, grid_size - 1)
    if collectible_row != player_row or collectible_col != player_col:
        break

hazard_row, hazard_col = spawn_hazard()

# Main game loop
while True:
    # Clear the screen (works on most terminals)
    print("\n" * 50)

    # Draw the grid
    for row in range(grid_size):
        for col in range(grid_size):
            if row == player_row and col == player_col:
                print(" @ ", end="")  # Player position
            elif row == collectible_row and col == collectible_col:
                print(" * ", end="")  # Collectible
            elif row == hazard_row and col == hazard_col:
                print(" K ", end="")  # Hazard
            else:
                print(" . ", end="")  # Empty cell
        print()  # New line after each row

    print("\nScore: " + str(score) + " / " + str(win_score))
    print("Player is at (" + str(player_row) + ", " + str(player_col) + ")")
    print("Type 'quit' to exit.")

    # Wait for user input
    user_input = input("\n> ")

    if user_input == "quit":
        print("Thanks for playing!")
        break

    # Handle WASD movement
    if user_input == "w":
        if player_row > 0:
            player_row = player_row - 1
    elif user_input == "s":
        if player_row < grid_size - 1:
            player_row = player_row + 1
    elif user_input == "a":
        if player_col > 0:
            player_col = player_col - 1
    elif user_input == "d":
        if player_col < grid_size - 1:
            player_col = player_col + 1

    # Check if player hit the hazard
    if player_row == hazard_row and player_col == hazard_col:
        print("\n" + "=" * 40)
        print("  GAME OVER!")
        print("=" * 40)
        break

    # Check if player collected the item
    if player_row == collectible_row and player_col == collectible_col:
        score = score + 1
        if score >= win_score:
            print("\n" + "=" * 40)
            print("  YOU WIN! Final Score: " + str(score))
            print("=" * 40)
            break
        collectible_row, collectible_col = spawn_collectible()
