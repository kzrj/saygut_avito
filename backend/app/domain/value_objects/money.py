from dataclasses import dataclass


@dataclass(frozen=True)
class Coins:
    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Coins amount cannot be negative")

    def __add__(self, other: "Coins") -> "Coins":
        return Coins(self.amount + other.amount)

    def __sub__(self, other: "Coins") -> "Coins":
        return Coins(self.amount - other.amount)
