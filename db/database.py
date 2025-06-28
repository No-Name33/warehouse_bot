import sqlite3
import os
from datetime import datetime

DB_PATH = "data/database.db"  # можно изменить путь, если хочешь

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Создаёт папку, если её нет
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            reset_time TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def save_action(user_id: int, action: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO actions (user_id, action, timestamp) VALUES (?, ?, ?)",
        (user_id, action, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_user_stats(user_id: int) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT action, COUNT(*) 
        FROM actions 
        WHERE user_id = ? 
        GROUP BY action
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    return {action: count for action, count in rows}

def get_user_last_reset(user_id: int) -> datetime:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reset_time FROM user_resets
        WHERE user_id = ?
        ORDER BY reset_time DESC
        LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return datetime.fromisoformat(row[0])
    return datetime.fromisoformat("2000-01-01T00:00:00")  # если сброса не было


def set_user_reset(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_resets (user_id, reset_time)
        VALUES (?, ?)
    """, (user_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    
def get_user_stats_since(user_id: int, since: datetime) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT action, COUNT(*) FROM actions
        WHERE user_id = ? AND timestamp >= ?
        GROUP BY action
    """, (user_id, since.isoformat()))
    rows = cursor.fetchall()
    conn.close()
    return {action: count for action, count in rows}


