"""Central CourtManager that orchestrates courts, players, bookings and matches."""

from datetime import datetime
from typing import Dict, List, Optional

from .booking import Booking
from .court import Court, Surface
from .match import MatchResult, simulate_match
from .player import Player


class CourtManager:
    """Manages tennis courts, players, bookings and match simulation."""

    def __init__(self):
        self._courts: Dict[int, Court] = {}
        self._players: Dict[int, Player] = {}
        self._bookings: Dict[int, Booking] = {}
        self._match_results: List[MatchResult] = []
        self._next_court_id = 1
        self._next_player_id = 1
        self._next_booking_id = 1

    # ------------------------------------------------------------------
    # Court management
    # ------------------------------------------------------------------

    def add_court(self, name: str, surface: Surface = Surface.HARD) -> Court:
        """Register a new court and return it."""
        court = Court(self._next_court_id, name, surface)
        self._courts[court.court_id] = court
        self._next_court_id += 1
        return court

    def get_court(self, court_id: int) -> Court:
        if court_id not in self._courts:
            raise KeyError(f"Court with id {court_id} not found.")
        return self._courts[court_id]

    def list_courts(self) -> List[Court]:
        return list(self._courts.values())

    def available_courts(self) -> List[Court]:
        return [c for c in self._courts.values() if c.is_available]

    # ------------------------------------------------------------------
    # Player management
    # ------------------------------------------------------------------

    def add_player(self, name: str, skill_level: float = 5.0) -> Player:
        """Register a new player and return them."""
        player = Player(self._next_player_id, name, skill_level)
        self._players[player.player_id] = player
        self._next_player_id += 1
        return player

    def get_player(self, player_id: int) -> Player:
        if player_id not in self._players:
            raise KeyError(f"Player with id {player_id} not found.")
        return self._players[player_id]

    def list_players(self) -> List[Player]:
        return list(self._players.values())

    # ------------------------------------------------------------------
    # Booking management
    # ------------------------------------------------------------------

    def book_court(
        self,
        court_id: int,
        player1_id: int,
        player2_id: int,
        start_time: datetime,
        duration_minutes: int = 60,
    ) -> Booking:
        """Book a court for two players at the given time slot."""
        court = self.get_court(court_id)
        p1 = self.get_player(player1_id)
        p2 = self.get_player(player2_id)
        court.book()
        booking = Booking(
            self._next_booking_id, court, p1, p2, start_time, duration_minutes
        )
        self._bookings[booking.booking_id] = booking
        self._next_booking_id += 1
        return booking

    def cancel_booking(self, booking_id: int) -> None:
        """Cancel a booking and release the court."""
        if booking_id not in self._bookings:
            raise KeyError(f"Booking with id {booking_id} not found.")
        booking = self._bookings.pop(booking_id)
        booking.court.release()

    def get_booking(self, booking_id: int) -> Booking:
        if booking_id not in self._bookings:
            raise KeyError(f"Booking with id {booking_id} not found.")
        return self._bookings[booking_id]

    def list_bookings(self) -> List[Booking]:
        return sorted(self._bookings.values(), key=lambda b: b.start_time)

    def bookings_for_player(self, player_id: int) -> List[Booking]:
        player = self.get_player(player_id)
        return [
            b for b in self._bookings.values()
            if b.player1 is player or b.player2 is player
        ]

    # ------------------------------------------------------------------
    # Match simulation
    # ------------------------------------------------------------------

    def simulate_match(
        self,
        booking_id: int,
        best_of: int = 3,
        seed: Optional[int] = None,
    ) -> MatchResult:
        """Simulate the match for the given booking and record the result.

        The booking is removed from the active schedule after simulation.
        """
        booking = self.get_booking(booking_id)
        result = simulate_match(booking, best_of=best_of, seed=seed)
        self._match_results.append(result)
        # Remove the booking and release the court
        self._bookings.pop(booking_id)
        booking.court.release()
        return result

    def match_results(self) -> List[MatchResult]:
        return list(self._match_results)

    # ------------------------------------------------------------------
    # Schedule / statistics display
    # ------------------------------------------------------------------

    def print_schedule(self) -> None:
        """Print upcoming bookings sorted by start time."""
        bookings = self.list_bookings()
        if not bookings:
            print("No upcoming bookings.")
            return
        print(f"{'ID':<5} {'Court':<12} {'Player 1':<20} {'Player 2':<20} "
              f"{'Start':<18} {'Duration':>10}")
        print("-" * 90)
        for b in bookings:
            print(
                f"{b.booking_id:<5} {b.court.name:<12} {b.player1.name:<20} "
                f"{b.player2.name:<20} "
                f"{b.start_time.strftime('%Y-%m-%d %H:%M'):<18} "
                f"{b.duration_minutes:>8} min"
            )

    def print_player_stats(self) -> None:
        """Print win/loss statistics for all registered players."""
        players = self.list_players()
        if not players:
            print("No players registered.")
            return
        print(f"{'ID':<5} {'Name':<20} {'Skill':>6} {'W':>5} {'L':>5} {'Win%':>8}")
        print("-" * 55)
        for p in players:
            print(
                f"{p.player_id:<5} {p.name:<20} {p.skill_level:>6.1f} "
                f"{p.wins:>5} {p.losses:>5} {p.win_rate:>7.1%}"
            )

    def print_match_results(self) -> None:
        """Print results of all simulated matches."""
        if not self._match_results:
            print("No matches simulated yet.")
            return
        for i, result in enumerate(self._match_results, 1):
            print(f"{i:>3}. {result}")
