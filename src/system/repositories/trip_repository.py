from src.database import get_connection
from src.system.models.trip import Trip

def _map(row) -> Trip:
    return Trip(
        TripID=row[0],
        name=row[1],
        cost=row[2],
        start_date=row[3],
        end_date=row[4],
        isavaliable=bool(row[5]),
        description=row[6]
    )

def get_all() -> list[Trip]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT TripID, name, cost, start_date, end_date, isavaliable, description FROM Trip")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(trip_id: int) -> Trip | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT TripID, name, cost, start_date, end_date, isavaliable, description FROM Trip WHERE TripID = ?", (trip_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(name: str, cost: float, start_date: str, end_date: str, description: str | None = None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Trip (name, cost, start_date, end_date, isavaliable, description)
        VALUES (?, ?, ?, ?, 1, ?)
    """, (name, cost, start_date, end_date, description))
    conn.commit()
    conn.close()

def update(trip_id: int, name: str, cost: float, start_date: str, end_date: str, isavaliable: bool, description: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Trip 
        SET name = ?, cost = ?, start_date = ?, end_date = ?, isavaliable = ?, description = ?
        WHERE TripID = ?
    """, (name, cost, start_date, end_date, int(isavaliable), description, trip_id))
    conn.commit()
    conn.close()

def delete(trip_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Trip WHERE TripID = ?", (trip_id,))
    conn.commit()
    conn.close()