import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("app.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        password_hash TEXT NOT NULL,
        consent INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        last_login TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT NOT NULL,
        email TEXT,
        ip TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    )
    """)
    conn.commit()
    conn.close()

def log_event(event: str, email: str | None, ip: str | None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO audit_logs(event, email, ip) VALUES(?,?,?)",
        (event, email, ip)
    )
    conn.commit()
    conn.close()
