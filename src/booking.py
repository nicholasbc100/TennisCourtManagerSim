"""Booking model for a tennis court reservation."""

from datetime import datetime

from .court import Court
from .player import Player


class Booking:
    """Represents the reservation of a court for a match between two players."""

    def __init__(
        self,
        booking_id: int,
        court: Court,
        player1: Player,
        player2: Player,
        start_time: datetime,
        duration_minutes: int = 60,
    ):
        if player1 is player2:
            raise ValueError("A player cannot book a court against themselves.")
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be a positive integer.")
        self.booking_id = booking_id
        self.court = court
        self.player1 = player1
        self.player2 = player2
        self.start_time = start_time
        self.duration_minutes = duration_minutes

    @property
    def end_time(self) -> datetime:
        from datetime import timedelta
        return self.start_time + timedelta(minutes=self.duration_minutes)

    def __repr__(self) -> str:
        return (
            f"Booking({self.booking_id}, "
            f"court='{self.court.name}', "
            f"{self.player1.name} vs {self.player2.name}, "
            f"{self.start_time.strftime('%Y-%m-%d %H:%M')})"
        )
