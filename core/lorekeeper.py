import sqlite3
from pathlib import Path
import logging

data_folder = Path(__file__).resolve().parent.parent / "data"
data_folder.mkdir(parents=True, exist_ok=True)  # <-- this ensures the directory exists

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "lore.sqlite"

def init_db():
    """Initialize database and create tables if not exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Basic table to track orchestrator awakenings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS awakenings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    logging.info("📜 Lorekeeper: Database ready.")

def log_awaken(message: str):
    """Log orchestrator awakenings into the database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO awakenings (message) VALUES (?)", (message,))
    conn.commit()
    conn.close()
    logging.info(f"📜 Lorekeeper: Logged awakening → {message}")
