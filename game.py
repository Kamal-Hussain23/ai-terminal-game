# Simple Text-Based Game on a 5x5 Grid
import random

GRID_SIZE = 5
WIN_SCORE = 10


def spawn_collectible(player_row, player_col, hazard_row, hazard_col):
    """Spawn collectible at a random position not occupied by the player or hazard."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if (row != player_row or col != player_col) and (row != hazard_row or col != hazard_col):
            return row, col


def spawn_hazard(player_row, player_col, collectible_row, collectible_col):
    """Spawn hazard at a random position not occupied by the player or collectible."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if (row != player_row or col != player_col) and (row != collectible_row or col != collectible_col):
            return row, col


def init_game():
    """Reset all game state for a new game."""
    player_row, player_col = 0, 0
    score = 0

    # Spawn collectible first (only needs to avoid player)
    while True:
        collectible_row = random.randint(0, GRID_SIZE - 1)
        collectible_col = random.randint(0, GRID_SIZE - 1)
        if collectible_row != player_row or collectible_col != player_col:
            break

    # Spawn hazard (avoids player and collectible)
    hazard_row, hazard_col = spawn_hazard(player_row, player_col, collectible_row, collectible_col)

    return player_row, player_col, score, collectible_row, collectible_col, hazard_row, hazard_col


def draw_grid(player_row, player_col, collectible_row, collectible_col, hazard_row, hazard_col, score):
    """Draw the grid with all entities."""
    print("\n" * 50)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if row == player_row and col == player_col:
                print(" @ ", end="")
            elif row == collectible_row and col == collectible_col:
                print(" * ", end="")
            elif row == hazard_row and col == hazard_col:
                print(" K ", end="")
            else:
                print(" . ", end="")
        print()
    print("\nScore: " + str(score) + " / " + str(WIN_SCORE))
    print("Player is at (" + str(player_row) + ", " + str(player_col) + ")")
    print("Type 'quit' to exit.")


def handle_movement(user_input, player_row, player_col):
    """Process WASD input and return new position."""
    if user_input == "w" and player_row > 0:
        player_row = player_row - 1
    elif user_input == "s" and player_row < GRID_SIZE - 1:
        player_row = player_row + 1
    elif user_input == "a" and player_col > 0:
        player_col = player_col - 1
    elif user_input == "d" and player_col < GRID_SIZE - 1:
        player_col = player_col + 1
    return player_row, player_col


def play_round():
    """Play a single round of the game. Returns True to play again, False to quit."""
    player_row, player_col, score, collectible_row, collectible_col, hazard_row, hazard_col = init_game()
    game_active = True

    while game_active:
        draw_grid(player_row, player_col, collectible_row, collectible_col, hazard_row, hazard_col, score)

        user_input = input("\n> ")

        if user_input == "quit":
            return False

        # Handle movement
        player_row, player_col = handle_movement(user_input, player_row, player_col)

        # Check hazard collision
        if player_row == hazard_row and player_col == hazard_col:
            print("\n" + "=" * 40)
            print("  GAME OVER!")
            print("=" * 40)
            game_active = False

        # Check collectible pickup
        if game_active and player_row == collectible_row and player_col == collectible_col:
            score = score + 1
            if score >= WIN_SCORE:
                print("\n" + "=" * 40)
                print("  YOU WIN! Final Score: " + str(score))
                print("=" * 40)
                game_active = False
            else:
                collectible_row, collectible_col = spawn_collectible(
                    player_row, player_col, hazard_row, hazard_col
                )

    # Ask to play again
    while True:
        choice = input("\nPlay again? (y/n) > ").strip().lower()
        if choice == "y":
            return True
        if choice == "n":
            return False


# Main game loop
if __name__ == "__main__":
    print("Welcome to the Grid Game!")
    print("Collect * items. Avoid K hazards.")
    print("Reach score " + str(WIN_SCORE) + " to win!\n")

    while True:
        if not play_round():
            print("Thanks for playing!")
            break
