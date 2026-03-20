"""Tests for the Player model."""

import pytest

from src.player import Player


def test_player_creation():
    player = Player(1, "Alice", skill_level=8.0)
    assert player.player_id == 1
    assert player.name == "Alice"
    assert player.skill_level == 8.0
    assert player.wins == 0
    assert player.losses == 0


def test_player_default_skill():
    player = Player(1, "Bob")
    assert player.skill_level == 5.0


def test_player_invalid_skill_low():
    with pytest.raises(ValueError):
        Player(1, "X", skill_level=0.5)


def test_player_invalid_skill_high():
    with pytest.raises(ValueError):
        Player(1, "X", skill_level=10.5)


def test_player_skill_boundary():
    p1 = Player(1, "Low", skill_level=1.0)
    p2 = Player(2, "High", skill_level=10.0)
    assert p1.skill_level == 1.0
    assert p2.skill_level == 10.0


def test_player_record_win():
    player = Player(1, "Alice")
    player.record_win()
    assert player.wins == 1
    assert player.losses == 0
    assert player.matches_played == 1


def test_player_record_loss():
    player = Player(1, "Alice")
    player.record_loss()
    assert player.losses == 1
    assert player.wins == 0


def test_player_win_rate_no_matches():
    player = Player(1, "Alice")
    assert player.win_rate == 0.0


def test_player_win_rate():
    player = Player(1, "Alice")
    player.record_win()
    player.record_win()
    player.record_loss()
    assert player.win_rate == pytest.approx(2 / 3)


def test_player_repr():
    player = Player(1, "Alice", skill_level=7.0)
    r = repr(player)
    assert "Alice" in r
    assert "7.0" in r
