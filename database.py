import datetime
import sqlite3
def create_table():
    conn=sqlite3.connect("tasks.db")

    cursor=conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_datetime TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            notified INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
def add_task(title, description, due_datetime):
    conn=sqlite3.connect("tasks.db")
    cursor=conn.cursor()
    cursor.execute("""
        INSERT INTO tasks
        (title, description, due_datetime, created_at)
        VALUES (?, ?, ?, ?)
    """, (title, description, due_datetime, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()


def get_all_tasks():
    conn=sqlite3.connect("tasks.db")

    cursor=conn.cursor()
    cursor.execute("""
        SELECT id, title, description, due_datetime, completed
        FROM tasks
        ORDER BY due_datetime
    """)

    tasks = cursor.fetchall()
    print("\nAll Tasks:")
    for task in tasks:
        if task[4] == 0:
            status = "Pending"
        else:
            status = "Completed"
        print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Due: {task[3]}, Status: {status}")
    conn.close()

    return tasks


def get_due_tasks(current_time):
    conn=sqlite3.connect("tasks.db")
    cursor=conn.cursor()

    cursor.execute("""
        SELECT id, title, description, due_datetime
        FROM tasks
        WHERE due_datetime <= ?
        AND completed = 0
        AND notified = 0
    """, (current_time,))

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def mark_notified(task_id):
    conn=sqlite3.connect("tasks.db")

    cursor=conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET notified = 1
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()