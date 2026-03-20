"""Tests for match simulation."""

import pytest

from src.booking import Booking
from src.court import Court, Surface
from src.match import MatchResult, SetResult, simulate_match
from src.player import Player


@pytest.fixture
def court():
    return Court(1, "Court 1", Surface.HARD)


@pytest.fixture
def strong_player():
    return Player(1, "Strong", skill_level=9.0)


@pytest.fixture
def weak_player():
    return Player(2, "Weak", skill_level=2.0)


@pytest.fixture
def equal_players():
    p1 = Player(1, "P1", skill_level=5.0)
    p2 = Player(2, "P2", skill_level=5.0)
    return p1, p2


@pytest.fixture
def booking(court, strong_player, weak_player):
    from datetime import datetime
    return Booking(1, court, strong_player, weak_player, datetime(2026, 4, 1, 10, 0))


def test_simulate_match_returns_result(booking):
    result = simulate_match(booking, best_of=3, seed=1)
    assert isinstance(result, MatchResult)
    assert result.winner in (booking.player1, booking.player2)


def test_simulate_match_best_of_3(booking):
    result = simulate_match(booking, best_of=3, seed=42)
    p1_wins = sum(1 for s in result.sets if s.player1_games > s.player2_games)
    p2_wins = sum(1 for s in result.sets if s.player2_games > s.player1_games)
    sets_to_win = 2
    assert max(p1_wins, p2_wins) == sets_to_win
    assert len(result.sets) in (2, 3)


def test_simulate_match_best_of_5(booking):
    result = simulate_match(booking, best_of=5, seed=10)
    p1_wins = sum(1 for s in result.sets if s.player1_games > s.player2_games)
    p2_wins = sum(1 for s in result.sets if s.player2_games > s.player1_games)
    assert max(p1_wins, p2_wins) == 3
    assert len(result.sets) in (3, 4, 5)


def test_simulate_match_updates_player_stats(booking):
    p1 = booking.player1
    p2 = booking.player2
    result = simulate_match(booking, best_of=3, seed=5)
    assert p1.wins + p1.losses == 1
    assert p2.wins + p2.losses == 1
    assert result.winner.wins == 1
    loser = p2 if result.winner is p1 else p1
    assert loser.losses == 1


def test_simulate_match_strong_wins_more_often(court):
    """Over many trials, the stronger player should win most matches."""
    from datetime import datetime
    wins = 0
    trials = 100
    for seed in range(trials):
        p1 = Player(1, "Strong", skill_level=9.0)
        p2 = Player(2, "Weak", skill_level=1.0)
        booking = Booking(1, court, p1, p2, datetime(2026, 1, 1))
        result = simulate_match(booking, best_of=3, seed=seed)
        if result.winner is p1:
            wins += 1
    assert wins > trials * 0.85, f"Expected >85% wins, got {wins}/{trials}"


def test_simulate_match_invalid_best_of(booking):
    with pytest.raises(ValueError, match="odd"):
        simulate_match(booking, best_of=2)


def test_set_result_str():
    s = SetResult(6, 3)
    assert str(s) == "6-3"


def test_match_result_score_string(booking):
    result = simulate_match(booking, best_of=3, seed=42)
    score = result.score_string()
    # Each set should be in the format "X-Y"
    for part in score.split(", "):
        assert "-" in part


def test_simulate_match_is_reproducible(booking):
    from datetime import datetime
    def make_booking():
        p1 = Player(1, "P1", skill_level=7.0)
        p2 = Player(2, "P2", skill_level=6.0)
        return Booking(1, Court(1, "C"), p1, p2, datetime(2026, 1, 1))

    r1 = simulate_match(make_booking(), best_of=3, seed=123)
    r2 = simulate_match(make_booking(), best_of=3, seed=123)
    assert r1.score_string() == r2.score_string()
    assert r1.winner.name == r2.winner.name
