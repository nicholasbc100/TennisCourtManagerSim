"""Tennis court model."""

from enum import Enum


class Surface(Enum):
    HARD = "Hard"
    CLAY = "Clay"
    GRASS = "Grass"
    CARPET = "Carpet"


class Court:
    """Represents a single tennis court."""

    def __init__(self, court_id: int, name: str, surface: Surface = Surface.HARD):
        self.court_id = court_id
        self.name = name
        self.surface = surface
        self._available = True

    @property
    def is_available(self) -> bool:
        return self._available

    def book(self) -> None:
        if not self._available:
            raise ValueError(f"Court '{self.name}' is already booked.")
        self._available = False

    def release(self) -> None:
        self._available = True

    def __repr__(self) -> str:
        status = "Available" if self._available else "Booked"
        return f"Court({self.court_id}, '{self.name}', {self.surface.value}, {status})"
