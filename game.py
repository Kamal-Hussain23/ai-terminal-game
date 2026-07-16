# Simple Text-Based Game on a 5x5 Grid

# Player starts at position (0, 0)
player_row = 0
player_col = 0
grid_size = 5

# Main game loop
while True:
    # Clear the screen (works on most terminals)
    print("\n" * 50)

    # Draw the grid
    for row in range(grid_size):
        for col in range(grid_size):
            if row == player_row and col == player_col:
                print(" @ ", end="")  # Player position
            else:
                print(" . ", end="")  # Empty cell
        print()  # New line after each row

    print("\nPlayer is at (" + str(player_row) + ", " + str(player_col) + ")")
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
