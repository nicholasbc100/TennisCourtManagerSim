# TennisCourtManagerSim

A Python simulation of a tennis court management system. Register courts and players, schedule bookings, and simulate match outcomes based on player skill levels.

## Features

- **Court management** — Register courts with name and surface type (Hard, Clay, Grass, Carpet). Track availability as courts are booked and released.
- **Player management** — Register players with a skill level (1–10) and track win/loss statistics.
- **Booking system** — Book courts for two-player matches with configurable time slots and durations. Cancel bookings to release courts.
- **Match simulation** — Simulate best-of-3 or best-of-5 matches using a skill-based probability model (logistic function). Results are reproducible with a seed.
- **Schedule & statistics** — Print the upcoming schedule, individual player stats, and a history of match results.

## Project Structure

```
TennisCourtManagerSim/
├── src/
│   ├── court.py      # Court model (id, name, surface, availability)
│   ├── player.py     # Player model (id, name, skill, win/loss stats)
│   ├── booking.py    # Booking model (court, players, time slot)
│   ├── match.py      # Match simulation logic
│   └── manager.py    # CourtManager orchestration class
├── tests/
│   ├── test_court.py
│   ├── test_player.py
│   ├── test_booking.py
│   ├── test_match.py
│   └── test_manager.py
├── main.py           # Demo entry point
├── pyproject.toml
└── requirements-dev.txt
```

## Quick Start

```bash
# Install dev dependencies (pytest)
pip install -r requirements-dev.txt

# Run the demo
python main.py

# Run the test suite
pytest
```

## Usage Example

```python
from datetime import datetime
from src.court import Surface
from src.manager import CourtManager

manager = CourtManager()

# Register courts and players
court = manager.add_court("Court 1", Surface.HARD)
alice = manager.add_player("Alice", skill_level=8.0)
bob   = manager.add_player("Bob",   skill_level=6.5)

# Book a court
booking = manager.book_court(
    court.court_id,
    alice.player_id,
    bob.player_id,
    start_time=datetime(2026, 4, 1, 10, 0),
)

# Simulate the match
result = manager.simulate_match(booking.booking_id, best_of=3)
print(result)
# Alice vs Bob | Winner: Alice | Score: 6-3, 7-5

# View stats
manager.print_player_stats()
```

## Simulation Model

Each game is decided by a Bernoulli trial using the win probability:

```
P(player1 wins game) = 1 / (1 + 10^(-Δskill / 4))
```

where `Δskill = skill1 − skill2`. A set is played to 6 games (win by 2; tiebreak at 6-6). The player who wins the majority of sets wins the match.
