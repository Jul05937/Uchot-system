import sqlite3
import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
DB_PATH = os.path.join(PROJECT_DIR, 'transport.db')
SQL_PATH = os.path.join(BASE_DIR, 'schema.sql')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    if Path(DB_PATH).exists():
        return

    conn = get_connection()
    with open(SQL_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("База данных создана.")