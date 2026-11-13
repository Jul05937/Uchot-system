from src.database import get_connection
from src.system.models.user import User

def _map(row) -> User:
    # (passengerID, name, surname, patronymic, password_hash, roleID, balance)
    return User(
        passengerID=row[0],
        name=row[1],
        surname=row[2],
        patronymic=row[3],
        password_hash=row[4],
        roleID=row[5],
        balance=row[6]
    )

def create(name: str, surname: str, patronymic: str, password_hash: str, roleID: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO User (name, surname, patronymic, password_hash, roleID)
        VALUES (?, ?, ?, ?, ?)
    """, (name, surname, patronymic, password_hash, roleID))
    conn.commit()
    conn.close()

def get_by_id(passengerID: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT passengerID, name, surname, patronymic, password_hash, roleID, balance
        FROM User
        WHERE passengerID = ?
    """, (passengerID,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT passengerID, name, surname, patronymic, password_hash, roleID, balance
        FROM User
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update_balance(passengerID: int, new_balance: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE User
        SET balance = ?
        WHERE passengerID = ?
    """, (new_balance, passengerID))
    conn.commit()
    conn.close()

def delete(passengerID: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM User WHERE passengerID = ?", (passengerID,))
    conn.commit()
    conn.close()