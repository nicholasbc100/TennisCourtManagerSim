"""Match simulation between two players."""

import random
from dataclasses import dataclass, field
from typing import List

from .booking import Booking
from .player import Player


@dataclass
class SetResult:
    player1_games: int
    player2_games: int

    def __str__(self) -> str:
        return f"{self.player1_games}-{self.player2_games}"


@dataclass
class MatchResult:
    booking: Booking
    sets: List[SetResult] = field(default_factory=list)
    winner: Player = None  # type: ignore[assignment]

    def score_string(self) -> str:
        return ", ".join(str(s) for s in self.sets)

    def __str__(self) -> str:
        return (
            f"{self.booking.player1.name} vs {self.booking.player2.name} | "
            f"Winner: {self.winner.name} | Score: {self.score_string()}"
        )


def _simulate_game(p1_win_prob: float) -> bool:
    """Return True if player 1 wins the game."""
    return random.random() < p1_win_prob


def _simulate_set(p1_win_prob: float) -> SetResult:
    """Simulate a single set of tennis (first to 6 games, must win by 2; tiebreak at 6-6)."""
    p1_games = 0
    p2_games = 0
    while True:
        if _simulate_game(p1_win_prob):
            p1_games += 1
        else:
            p2_games += 1
        if p1_games >= 6 and p1_games - p2_games >= 2:
            return SetResult(p1_games, p2_games)
        if p2_games >= 6 and p2_games - p1_games >= 2:
            return SetResult(p1_games, p2_games)
        if p1_games == 7:
            return SetResult(7, 6)
        if p2_games == 7:
            return SetResult(6, 7)


def simulate_match(booking: Booking, best_of: int = 3, seed: int = None) -> MatchResult:
    """Simulate a best-of-N sets match (N must be odd, default 3).

    Skill levels influence win probability per game via a logistic function.
    """
    if best_of % 2 == 0 or best_of < 1:
        raise ValueError("best_of must be a positive odd integer (e.g., 1, 3, 5).")

    if seed is not None:
        random.seed(seed)

    p1 = booking.player1
    p2 = booking.player2

    # Logistic transform: probability p1 wins a game
    skill_diff = p1.skill_level - p2.skill_level
    p1_win_prob = 1.0 / (1.0 + 10 ** (-skill_diff / 4.0))

    sets_to_win = (best_of + 1) // 2
    p1_sets = 0
    p2_sets = 0
    sets: List[SetResult] = []

    while p1_sets < sets_to_win and p2_sets < sets_to_win:
        result = _simulate_set(p1_win_prob)
        sets.append(result)
        if result.player1_games > result.player2_games:
            p1_sets += 1
        else:
            p2_sets += 1

    winner = p1 if p1_sets > p2_sets else p2
    match_result = MatchResult(booking=booking, sets=sets, winner=winner)

    winner.record_win()
    loser = p2 if winner is p1 else p1
    loser.record_loss()

    return match_result
