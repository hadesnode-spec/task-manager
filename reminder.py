import time
from datetime import datetime

from database import (
    create_table,
    get_due_tasks,
    mark_notified
)

from notifier import send_notification


CHECK_INTERVAL = 10


def check_tasks():

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    tasks = get_due_tasks(current_time)

    for task in tasks:

        task_id = task[0]
        title = task[1]
        description = task[2]
        due_datetime = task[3]

        message = (
            f"{title}\n"
            f"{description}\n"
            f"Due: {due_datetime}"
        )

        print(f"Found due task: {title}")

        send_notification(
            "Task Due!",
            message
        )

        mark_notified(task_id)

        print(f"Notification processed: {title}")


def main():

    create_table()

    print("Task reminder service started.")

    while True:

        try:
            check_tasks()
            time.sleep(CHECK_INTERVAL)

        except Exception as error:

            print(f"Reminder error: {error}")

            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()