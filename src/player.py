"""Tennis player model."""


class Player:
    """Represents a tennis player with a skill level and match statistics."""

    def __init__(self, player_id: int, name: str, skill_level: float = 5.0):
        if not 1.0 <= skill_level <= 10.0:
            raise ValueError("skill_level must be between 1.0 and 10.0.")
        self.player_id = player_id
        self.name = name
        self.skill_level = skill_level
        self.wins = 0
        self.losses = 0

    @property
    def matches_played(self) -> int:
        return self.wins + self.losses

    @property
    def win_rate(self) -> float:
        if self.matches_played == 0:
            return 0.0
        return self.wins / self.matches_played

    def record_win(self) -> None:
        self.wins += 1

    def record_loss(self) -> None:
        self.losses += 1

    def __repr__(self) -> str:
        return (
            f"Player({self.player_id}, '{self.name}', "
            f"skill={self.skill_level:.1f}, "
            f"W/L={self.wins}/{self.losses})"
        )
