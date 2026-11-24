from dataclasses import dataclass

@dataclass
class Ticket:
    TicketID: int
    TripID: int
    passengerID: int
    statusPayment: bool
    start_date: str