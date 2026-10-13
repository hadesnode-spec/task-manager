
import sqlite3
from datetime import datetime
from pathlib import Path

from tasks import Task


DB_NAME = Path(__file__).resolve().parent / "tasks.db"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_connection():
    return sqlite3.connect(DB_NAME)


def format_datetime(value):
    if value is None:
        return None

    return value.strftime(DATETIME_FORMAT)


def parse_datetime(value):
    if value is None:
        return None

    return datetime.strptime(value, DATETIME_FORMAT)


def row_to_task(row):
    return Task(
        task_id=row[0],
        title=row[1],
        description=row[2],
        due_datetime=parse_datetime(row[3]),
        delete_datetime=parse_datetime(row[4]),
        completed=bool(row[5]),
        notified=bool(row[6]),
        recurring=bool(row[7]),
    )


def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_datetime TEXT NOT NULL,
                delete_datetime TEXT,
                completed INTEGER DEFAULT 0,
                notified INTEGER DEFAULT 0,
                recurring INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_task(task):
    if not isinstance(task, Task):
        raise TypeError("add_task expects a Task object.")

    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO tasks (
                title,
                description,
                due_datetime,
                delete_datetime,
                completed,
                notified,
                recurring
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            task.title,
            task.description,
            format_datetime(task.due_datetime),
            format_datetime(task.delete_datetime),
            int(task.completed),
            int(task.notified),
            int(task.recurring),
        ))

        return cursor.lastrowid


def get_all_tasks():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                id,
                title,
                description,
                due_datetime,
                delete_datetime,
                completed,
                notified,
                recurring
            FROM tasks
            ORDER BY due_datetime
        """).fetchall()

    return [row_to_task(row) for row in rows]


def get_due_tasks(current_time):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                id,
                title,
                description,
                due_datetime,
                delete_datetime,
                completed,
                notified,
                recurring
            FROM tasks
            WHERE due_datetime <= ?
              AND completed = 0
              AND notified = 0
            ORDER BY due_datetime
        """, (format_datetime(current_time),)).fetchall()

    return [row_to_task(row) for row in rows]


def save_task(task):
    with get_connection() as conn:
        conn.execute("""
            UPDATE tasks
            SET
                title = ?,
                description = ?,
                due_datetime = ?,
                delete_datetime = ?,
                completed = ?,
                notified = ?,
                recurring = ?
            WHERE id = ?
        """, (
            task.title,
            task.description,
            format_datetime(task.due_datetime),
            format_datetime(task.delete_datetime),
            int(task.completed),
            int(task.notified),
            int(task.recurring),
            task.id,
        ))


def delete_expired_tasks(current_time):
    tasks=get_all_tasks()
    expired_ids=[task.id
        for task in tasks
        if task.is_expired(current_time)
    ]

    if not expired_ids:
        return 0

    with get_connection() as conn:
        conn.executemany(
            "DELETE FROM tasks WHERE id = ?",
            [(task_id,) for task_id in expired_ids],
        )

    return len(expired_ids)
