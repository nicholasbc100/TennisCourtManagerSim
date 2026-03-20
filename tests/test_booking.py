"""Tests for the Booking model."""

from datetime import datetime

import pytest

from src.booking import Booking
from src.court import Court, Surface
from src.player import Player


@pytest.fixture
def court():
    return Court(1, "Court 1", Surface.HARD)


@pytest.fixture
def p1():
    return Player(1, "Alice", skill_level=8.0)


@pytest.fixture
def p2():
    return Player(2, "Bob", skill_level=6.0)


def test_booking_creation(court, p1, p2):
    t = datetime(2026, 4, 1, 10, 0)
    booking = Booking(1, court, p1, p2, t, duration_minutes=90)
    assert booking.booking_id == 1
    assert booking.court is court
    assert booking.player1 is p1
    assert booking.player2 is p2
    assert booking.start_time == t
    assert booking.duration_minutes == 90


def test_booking_end_time(court, p1, p2):
    t = datetime(2026, 4, 1, 10, 0)
    booking = Booking(1, court, p1, p2, t, duration_minutes=60)
    assert booking.end_time == datetime(2026, 4, 1, 11, 0)


def test_booking_default_duration(court, p1, p2):
    t = datetime(2026, 4, 1, 10, 0)
    booking = Booking(1, court, p1, p2, t)
    assert booking.duration_minutes == 60


def test_booking_same_player_raises(court, p1):
    with pytest.raises(ValueError, match="themselves"):
        Booking(1, court, p1, p1, datetime.now())


def test_booking_invalid_duration(court, p1, p2):
    with pytest.raises(ValueError, match="positive"):
        Booking(1, court, p1, p2, datetime.now(), duration_minutes=0)


def test_booking_repr(court, p1, p2):
    t = datetime(2026, 4, 1, 10, 0)
    booking = Booking(1, court, p1, p2, t)
    r = repr(booking)
    assert "Alice" in r
    assert "Bob" in r
    assert "Court 1" in r
