import random
import pytest
from unittest.mock import patch
from io import StringIO


class TestInitGame:
    def test_player_starts_at_origin(self):
        """Player should start at position (0, 0)."""
        from game import init_game
        pr, pc, score, cr, cc, hr, hc = init_game()
        assert pr == 0
        assert pc == 0
        assert score == 0

    def test_collectible_not_on_player(self):
        """Collectible should not spawn on the player."""
        from game import init_game
        for seed in range(20):
            random.seed(seed)
            pr, pc, score, cr, cc, hr, hc = init_game()
            assert not (cr == 0 and cc == 0), f"Failed with seed {seed}"

    def test_hazard_not_on_player(self):
        """Hazard should not spawn on the player."""
        from game import init_game
        for seed in range(20):
            random.seed(seed)
            pr, pc, score, cr, cc, hr, hc = init_game()
            assert not (hr == 0 and hc == 0), f"Failed with seed {seed}"

    def test_hazard_not_on_collectible(self):
        """Hazard and collectible should not overlap."""
        from game import init_game
        for seed in range(20):
            random.seed(seed)
            pr, pc, score, cr, cc, hr, hc = init_game()
            assert not (hr == cr and hc == cc), f"Failed with seed {seed}"

    def test_all_on_grid(self):
        """All entities should be within grid boundaries."""
        from game import init_game, GRID_SIZE
        for seed in range(20):
            random.seed(seed)
            pr, pc, score, cr, cc, hr, hc = init_game()
            assert 0 <= pr < GRID_SIZE
            assert 0 <= pc < GRID_SIZE
            assert 0 <= cr < GRID_SIZE
            assert 0 <= cc < GRID_SIZE
            assert 0 <= hr < GRID_SIZE
            assert 0 <= hc < GRID_SIZE


class TestHandleMovement:
    def test_move_right(self):
        from game import handle_movement
        r, c = handle_movement("d", 0, 0)
        assert r == 0
        assert c == 1

    def test_move_left(self):
        from game import handle_movement
        r, c = handle_movement("a", 0, 1)
        assert r == 0
        assert c == 0

    def test_move_down(self):
        from game import handle_movement
        r, c = handle_movement("s", 0, 0)
        assert r == 1
        assert c == 0

    def test_move_up(self):
        from game import handle_movement
        r, c = handle_movement("w", 1, 0)
        assert r == 0
        assert c == 0

    def test_cannot_move_left_from_edge(self):
        from game import handle_movement
        r, c = handle_movement("a", 0, 0)
        assert c == 0

    def test_cannot_move_up_from_edge(self):
        from game import handle_movement
        r, c = handle_movement("w", 0, 0)
        assert r == 0

    def test_cannot_move_right_from_edge(self):
        from game import handle_movement, GRID_SIZE
        r, c = handle_movement("d", 0, GRID_SIZE - 1)
        assert c == GRID_SIZE - 1

    def test_cannot_move_down_from_edge(self):
        from game import handle_movement, GRID_SIZE
        r, c = handle_movement("s", GRID_SIZE - 1, 0)
        assert r == GRID_SIZE - 1


class TestPlayRound:
    def test_quit_exits_round(self):
        """Typing 'quit' should return False (don't play again)."""
        from game import play_round
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print"):
                assert play_round() is False

    def test_game_over_then_play_again(self):
        """Game over should prompt and accept play again."""
        from game import play_round
        import game as game_mod
        random.seed(0)
        # Seed 0 places hazard at (0, 2), so d d hits it
        with patch("builtins.input", side_effect=["d", "d", "y"]):
            with patch("builtins.print") as mp:
                assert play_round() is True
                calls = [str(c) for c in mp.call_args_list]
                assert any("GAME OVER" in c for c in calls)

    def test_game_over_then_decline(self):
        """Game over should prompt and accept decline."""
        from game import play_round
        import game as game_mod
        random.seed(0)
        with patch("builtins.input", side_effect=["d", "d", "n"]):
            with patch("builtins.print") as mp:
                assert play_round() is False
                calls = [str(c) for c in mp.call_args_list]
                assert any("GAME OVER" in c for c in calls)


class TestGameLoop:
    def test_single_round_quit(self):
        """Main loop should exit cleanly on quit."""
        from game import play_round
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print"):
                assert play_round() is False

    def test_play_again_then_quit(self):
        """Play again then quit should work."""
        from game import play_round
        import game as game_mod
        random.seed(0)
        # Game over, play again, then quit in second round
        with patch("builtins.input", side_effect=["d", "d", "y", "quit"]):
            with patch("builtins.print"):
                # First round: game over + play again = True
                assert play_round() is True
                # Second round: quit = False
                assert play_round() is False


class TestConstants:
    def test_grid_size(self):
        from game import GRID_SIZE
        assert GRID_SIZE == 5

    def test_win_score(self):
        from game import WIN_SCORE
        assert WIN_SCORE == 10
