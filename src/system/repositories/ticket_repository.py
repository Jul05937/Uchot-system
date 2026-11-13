from src.database import get_connection
from src.system.models.ticket import Ticket

def _map(row) -> Ticket:
    return Ticket(
        TicketID=row[0],
        TripID=row[1],
        passengerID=row[2],
        statusPayment=bool(row[3]),
        start_date=row[4]
    )

def create(trip_id: int, passenger_id: int, status_payment: bool = False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Ticket (TripID, passengerID, statusPayment)
        VALUES (?, ?, ?)
    """, (trip_id, passenger_id, int(status_payment)))
    conn.commit()
    conn.close()

def get_by_id(ticket_id: int) -> Ticket | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT TicketID, TripID, passengerID, statusPayment, start_date FROM Ticket WHERE TicketID = ?", (ticket_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update_status(ticket_id: int, status_payment: bool):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Ticket 
        SET statusPayment = ?
        WHERE TicketID = ?
    """, (int(status_payment), ticket_id))
    conn.commit()
    conn.close()

def delete(ticket_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Ticket WHERE TicketID = ?", (ticket_id,))
    conn.commit()
    conn.close()
#?
def get_by_passenger(passenger_id: int) -> list[Ticket]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT TicketID, TripID, passengerID, statusPayment, start_date 
        FROM Ticket 
        WHERE passengerID = ?
        ORDER BY start_date DESC
    """, (passenger_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]