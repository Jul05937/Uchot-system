from dataclasses import dataclass

@dataclass
class Trip:
    TripID: int
    name: str
    cost: float
    start_date: str
    end_date: str
    seats: int
    isavaliable: bool
    description: str | None = None