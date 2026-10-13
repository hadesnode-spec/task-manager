
import time
from datetime import datetime, timedelta

from database import (
    create_table,
    get_due_tasks,
    save_task,
    delete_expired_tasks,
)

from notifier import send_notification


CHECK_INTERVAL = 10


def check_tasks():
    current_datetime = datetime.now()

    deleted_count = delete_expired_tasks(current_datetime)

    if deleted_count > 0:
        print(
            f"Deleted {deleted_count} "
            f"expired task(s)."
        )

    tasks = get_due_tasks(current_datetime)

    for task in tasks:
        title = task.title
        description = task.description
        due_datetime = task.due_datetime

        message = (
            f"{title}\n"
            f"{description or ''}\n"
            f"Due: {due_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        print(f"Found due task: {title}")
        send_notification("Task Due!", message)

        if task.recurring:
            next_due = due_datetime+timedelta(days=1)
            while next_due<=current_datetime:
                next_due+=timedelta(days=1)
            try:
                task.reschedule(next_due)

                print(
                    "Next occurrence: "
                    f"{task.due_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
                )

            except ValueError:
                task.mark_notified()

                print(
                    f"No further occurrence scheduled: {title}"
                )

        else:
            task.mark_notified()

        save_task(task)

        print(f"Notification processed: {title}")


def main():
    create_table()

    print("Task reminder service started.")
    print(
        f"Checking every {CHECK_INTERVAL} seconds."
    )

    while True:
        try:
            check_tasks()

        except Exception as error:
            print(f"Reminder error: {error}")

        time.sleep(CHECK_INTERVAL)


if __name__=="__main__":
    main()
