"""Tests for the CourtManager orchestration class."""

from datetime import datetime

import pytest

from src.court import Surface
from src.manager import CourtManager


@pytest.fixture
def manager():
    return CourtManager()


@pytest.fixture
def populated_manager():
    m = CourtManager()
    m.add_court("Court 1", Surface.HARD)
    m.add_court("Court 2", Surface.CLAY)
    m.add_player("Alice", skill_level=8.0)
    m.add_player("Bob", skill_level=6.0)
    return m


# ---- Court management ----

def test_add_court(manager):
    court = manager.add_court("Court 1", Surface.GRASS)
    assert court.name == "Court 1"
    assert court.surface == Surface.GRASS
    assert len(manager.list_courts()) == 1


def test_add_multiple_courts(manager):
    manager.add_court("C1")
    manager.add_court("C2")
    assert len(manager.list_courts()) == 2


def test_get_court(manager):
    court = manager.add_court("Center Court")
    fetched = manager.get_court(court.court_id)
    assert fetched is court


def test_get_court_not_found(manager):
    with pytest.raises(KeyError):
        manager.get_court(999)


def test_available_courts(populated_manager):
    courts = populated_manager.available_courts()
    assert len(courts) == 2


# ---- Player management ----

def test_add_player(manager):
    player = manager.add_player("Alice", skill_level=7.5)
    assert player.name == "Alice"
    assert player.skill_level == 7.5
    assert len(manager.list_players()) == 1


def test_get_player(manager):
    player = manager.add_player("Bob")
    fetched = manager.get_player(player.player_id)
    assert fetched is player


def test_get_player_not_found(manager):
    with pytest.raises(KeyError):
        manager.get_player(999)


# ---- Booking management ----

def test_book_court(populated_manager):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t = datetime(2026, 4, 1, 10, 0)
    booking = m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t)
    assert booking.court is courts[0]
    assert not courts[0].is_available
    assert len(m.list_bookings()) == 1


def test_book_court_reduces_available_courts(populated_manager):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t = datetime(2026, 4, 1, 10, 0)
    m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t)
    assert len(m.available_courts()) == 1


def test_cancel_booking(populated_manager):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t = datetime(2026, 4, 1, 10, 0)
    booking = m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t)
    m.cancel_booking(booking.booking_id)
    assert courts[0].is_available
    assert len(m.list_bookings()) == 0


def test_cancel_nonexistent_booking(manager):
    with pytest.raises(KeyError):
        manager.cancel_booking(999)


def test_bookings_for_player(populated_manager):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t1 = datetime(2026, 4, 1, 10, 0)
    t2 = datetime(2026, 4, 1, 12, 0)
    m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t1)
    m.book_court(courts[1].court_id, players[0].player_id, players[1].player_id, t2)
    bookings = m.bookings_for_player(players[0].player_id)
    assert len(bookings) == 2


def test_list_bookings_sorted_by_time(populated_manager):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t_late = datetime(2026, 4, 1, 14, 0)
    t_early = datetime(2026, 4, 1, 9, 0)
    b_late = m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t_late)
    # Release and rebook second court earlier
    b_early = m.book_court(courts[1].court_id, players[0].player_id, players[1].player_id, t_early)
    bookings = m.list_bookings()
    assert bookings[0].start_time < bookings[1].start_time


# ---- Match simulation ----

def test_simulate_match_via_manager(populated_manager):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t = datetime(2026, 4, 1, 10, 0)
    booking = m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t)
    result = m.simulate_match(booking.booking_id, best_of=3, seed=1)
    assert result.winner in players
    # Booking should be removed after simulation
    assert len(m.list_bookings()) == 0
    # Court released
    assert courts[0].is_available


def test_simulate_match_recorded(populated_manager):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t = datetime(2026, 4, 1, 10, 0)
    booking = m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t)
    m.simulate_match(booking.booking_id, seed=42)
    assert len(m.match_results()) == 1


def test_simulate_nonexistent_booking(manager):
    with pytest.raises(KeyError):
        manager.simulate_match(999)


# ---- Display methods (smoke tests) ----

def test_print_schedule_empty(manager, capsys):
    manager.print_schedule()
    captured = capsys.readouterr()
    assert "No upcoming" in captured.out


def test_print_player_stats_empty(manager, capsys):
    manager.print_player_stats()
    captured = capsys.readouterr()
    assert "No players" in captured.out


def test_print_match_results_empty(manager, capsys):
    manager.print_match_results()
    captured = capsys.readouterr()
    assert "No matches" in captured.out


def test_print_schedule_with_booking(populated_manager, capsys):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t = datetime(2026, 4, 1, 10, 0)
    m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t)
    m.print_schedule()
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out


def test_print_player_stats_with_match(populated_manager, capsys):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t = datetime(2026, 4, 1, 10, 0)
    booking = m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t)
    m.simulate_match(booking.booking_id, seed=1)
    m.print_player_stats()
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out


def test_print_match_results_after_simulation(populated_manager, capsys):
    m = populated_manager
    courts = m.list_courts()
    players = m.list_players()
    t = datetime(2026, 4, 1, 10, 0)
    booking = m.book_court(courts[0].court_id, players[0].player_id, players[1].player_id, t)
    m.simulate_match(booking.booking_id, seed=1)
    m.print_match_results()
    captured = capsys.readouterr()
    assert "Winner" in captured.out
