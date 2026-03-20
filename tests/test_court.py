"""Tests for the Court model."""

import pytest

from src.court import Court, Surface


def test_court_creation():
    court = Court(1, "Court 1", Surface.HARD)
    assert court.court_id == 1
    assert court.name == "Court 1"
    assert court.surface == Surface.HARD
    assert court.is_available is True


def test_court_default_surface():
    court = Court(1, "Center Court")
    assert court.surface == Surface.HARD


def test_court_book():
    court = Court(1, "Court 1")
    court.book()
    assert court.is_available is False


def test_court_release():
    court = Court(1, "Court 1")
    court.book()
    court.release()
    assert court.is_available is True


def test_court_book_already_booked():
    court = Court(1, "Court 1")
    court.book()
    with pytest.raises(ValueError, match="already booked"):
        court.book()


def test_court_repr():
    court = Court(2, "Court 2", Surface.CLAY)
    assert "Court 2" in repr(court)
    assert "Clay" in repr(court)
    assert "Available" in repr(court)
