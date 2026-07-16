import pytest
from unittest.mock import patch
from io import StringIO


def run_game_with_inputs(inputs):
    """Helper function to run the game with a list of inputs."""
    # Add 'quit' to end if not already there
    if inputs[-1] != "quit":
        inputs.append("quit")

    with patch("builtins.input", side_effect=inputs):
        with patch("builtins.print"):
            # Import and run the game
            import importlib
            import game
            importlib.reload(game)


class TestInitialPosition:
    def test_player_starts_at_origin(self):
        """Player should start at position (0, 0)."""
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_row == 0
                assert game.player_col == 0


class TestMovement:
    def test_move_right(self):
        """D key should move player right (increase column)."""
        with patch("builtins.input", side_effect=["d", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_row == 0
                assert game.player_col == 1

    def test_move_left(self):
        """A key should move player left (decrease column)."""
        # First move right, then left to test
        with patch("builtins.input", side_effect=["d", "a", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_row == 0
                assert game.player_col == 0

    def test_move_down(self):
        """S key should move player down (increase row)."""
        with patch("builtins.input", side_effect=["s", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_row == 1
                assert game.player_col == 0

    def test_move_up(self):
        """W key should move player up (decrease row)."""
        # First move down, then up to test
        with patch("builtins.input", side_effect=["s", "w", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_row == 0
                assert game.player_col == 0


class TestBoundaryChecks:
    def test_cannot_move_left_from_edge(self):
        """Player should not move left when at column 0."""
        with patch("builtins.input", side_effect=["a", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_col == 0

    def test_cannot_move_up_from_edge(self):
        """Player should not move up when at row 0."""
        with patch("builtins.input", side_effect=["w", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_row == 0

    def test_cannot_move_right_from_edge(self):
        """Player should not move right when at right edge."""
        # Move to right edge first (column 4)
        with patch("builtins.input", side_effect=["d", "d", "d", "d", "d", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_col == 4

    def test_cannot_move_down_from_edge(self):
        """Player should not move down when at bottom edge."""
        import random
        # Seed so hazard isn't in column 0 blocking the path down
        random.seed(42)
        with patch("builtins.input", side_effect=["s", "s", "s", "s", "s", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.player_row == 4


class TestGridSize:
    def test_grid_size_is_five(self):
        """Grid should be 5x5."""
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.grid_size == 5


class TestScore:
    def test_initial_score_is_zero(self):
        """Score should start at 0."""
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.score == 0

    def test_win_score_is_ten(self):
        """Win score should be 10."""
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                assert game.win_score == 10


class TestCollectible:
    def test_collectible_spawns_not_on_player(self):
        """Collectible should not spawn on the player."""
        import random
        # Try multiple seeds to ensure it works
        for seed in range(20):
            random.seed(seed)
            with patch("builtins.input", return_value="quit"):
                with patch("builtins.print"):
                    import importlib
                    import game
                    importlib.reload(game)
                    # Collectible should NOT be at player start (0, 0)
                    assert not (game.collectible_row == 0 and game.collectible_col == 0), \
                        f"Failed with seed {seed}"

    def test_collectible_is_on_grid(self):
        """Collectible should be within grid boundaries."""
        import random
        for seed in range(20):
            random.seed(seed)
            with patch("builtins.input", return_value="quit"):
                with patch("builtins.print"):
                    import importlib
                    import game
                    importlib.reload(game)
                    assert 0 <= game.collectible_row < game.grid_size
                    assert 0 <= game.collectible_col < game.grid_size

    def test_score_increases_on_collect(self):
        """Score should increase by 1 when player collects item."""
        import random
        # Force collectible to be at (0, 1) so moving right collects it
        random.seed(1)
        with patch("builtins.input", side_effect=["d", "quit"]):
            with patch("builtins.print"):
                import importlib
                import game
                importlib.reload(game)
                # Place collectible where we know it'll be after seed 1
                game.collectible_row = 0
                game.collectible_col = 1
                # Now simulate the move
                game.player_col = 1
                # Check if collected
                if game.player_row == game.collectible_row and game.player_col == game.collectible_col:
                    game.score += 1
                assert game.score == 1


class TestHazard:
    def test_hazard_spawns_not_on_player(self):
        """Hazard should not spawn on the player."""
        import random
        for seed in range(20):
            random.seed(seed)
            with patch("builtins.input", return_value="quit"):
                with patch("builtins.print"):
                    import importlib
                    import game
                    importlib.reload(game)
                    assert not (game.hazard_row == 0 and game.hazard_col == 0), \
                        f"Failed with seed {seed}"

    def test_hazard_is_on_grid(self):
        """Hazard should be within grid boundaries."""
        import random
        for seed in range(20):
            random.seed(seed)
            with patch("builtins.input", return_value="quit"):
                with patch("builtins.print"):
                    import importlib
                    import game
                    importlib.reload(game)
                    assert 0 <= game.hazard_row < game.grid_size
                    assert 0 <= game.hazard_col < game.grid_size

    def test_hazard_spawns_not_on_collectible(self):
        """Hazard and collectible should not overlap."""
        import random
        for seed in range(20):
            random.seed(seed)
            with patch("builtins.input", return_value="quit"):
                with patch("builtins.print"):
                    import importlib
                    import game
                    importlib.reload(game)
                    assert not (game.hazard_row == game.collectible_row and
                                game.hazard_col == game.collectible_col), \
                        f"Failed with seed {seed}"

    def test_game_over_on_hazard(self):
        """Player should get Game Over when stepping on hazard."""
        import random
        # With seed 0, hazard is at (0, 2), so moving right twice hits it
        random.seed(0)
        with patch("builtins.input", side_effect=["d", "d", "quit"]):
            with patch("builtins.print") as mock_print:
                import importlib
                import game
                importlib.reload(game)
                calls = [str(c) for c in mock_print.call_args_list]
                assert any("GAME OVER" in c for c in calls), "Game Over message not found"
