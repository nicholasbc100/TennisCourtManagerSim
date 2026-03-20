"""Tennis Court Manager Simulator — entry point.

Run this script to see an interactive demo of the simulator.
"""

from datetime import datetime

from src.court import Surface
from src.manager import CourtManager


def main():
    print("=" * 60)
    print("    Tennis Court Manager Simulator")
    print("=" * 60)

    manager = CourtManager()

    # Add courts
    c1 = manager.add_court("Court 1", Surface.HARD)
    c2 = manager.add_court("Court 2", Surface.CLAY)
    c3 = manager.add_court("Court 3", Surface.GRASS)
    print(f"\nRegistered courts: {manager.list_courts()}")

    # Add players
    alice = manager.add_player("Alice", skill_level=8.0)
    bob = manager.add_player("Bob", skill_level=6.5)
    carol = manager.add_player("Carol", skill_level=9.0)
    dave = manager.add_player("Dave", skill_level=5.0)
    print(f"\nRegistered players: {manager.list_players()}")

    # Book courts
    t1 = datetime(2026, 4, 1, 10, 0)
    t2 = datetime(2026, 4, 1, 12, 0)
    t3 = datetime(2026, 4, 2, 9, 0)
    b1 = manager.book_court(c1.court_id, alice.player_id, bob.player_id, t1)
    b2 = manager.book_court(c2.court_id, carol.player_id, dave.player_id, t2)
    b3 = manager.book_court(c3.court_id, alice.player_id, carol.player_id, t3)

    print("\n--- Upcoming Schedule ---")
    manager.print_schedule()

    print(f"\nAvailable courts: {manager.available_courts()}")

    # Simulate matches
    print("\n--- Simulating Matches ---")
    r1 = manager.simulate_match(b1.booking_id, best_of=3, seed=42)
    r2 = manager.simulate_match(b2.booking_id, best_of=3, seed=7)
    r3 = manager.simulate_match(b3.booking_id, best_of=5, seed=99)

    manager.print_match_results()

    print("\n--- Player Statistics ---")
    manager.print_player_stats()

    # Remaining schedule (should be empty now)
    print("\n--- Remaining Schedule ---")
    manager.print_schedule()


if __name__ == "__main__":
    main()
