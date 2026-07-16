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
        # Move to bottom edge first (row 4)
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
