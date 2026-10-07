import sqlite3
from pathlib import Path


DB_NAME = Path(__file__).resolve().parent / "tasks.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]

    if "delete_datetime" not in columns:
        cursor.execute("""
            ALTER TABLE tasks
            ADD COLUMN delete_datetime TEXT
        """)

    if "recurring" not in columns:
        cursor.execute("""
            ALTER TABLE tasks
            ADD COLUMN recurring INTEGER DEFAULT 0
        """)

    conn.commit()
    conn.close()


def add_task(
    title,
    description,
    due_datetime,
    delete_datetime,
    recurring
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (
            title,
            description,
            due_datetime,
            delete_datetime,
            recurring
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        description,
        due_datetime,
        delete_datetime,
        recurring
    ))

    conn.commit()
    conn.close()


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            description,
            due_datetime,
            delete_datetime,
            completed,
            recurring
        FROM tasks
        ORDER BY due_datetime
    """)

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def get_due_tasks(current_time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            description,
            due_datetime,
            recurring
        FROM tasks
        WHERE due_datetime <= ?
        AND completed = 0
        AND notified = 0
    """, (current_time,))

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def mark_notified(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET notified = 1
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


def update_recurring_task(task_id, next_due_datetime):
    """
    Move a recurring task to its next occurrence.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET
            due_datetime = ?,
            notified = 0
        WHERE id = ?
    """, (
        next_due_datetime,
        task_id
    ))

    conn.commit()
    conn.close()


def delete_expired_tasks(current_time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE delete_datetime IS NOT NULL
        AND delete_datetime <= ?
    """, (current_time,))

    deleted_count = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted_count