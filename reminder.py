import time
from datetime import datetime, timedelta

from database import (
    create_table,
    get_due_tasks,
    mark_notified,
    update_recurring_task,
    delete_expired_tasks
)

from notifier import send_notification
CHECK_INTERVAL = 10


def check_tasks():

    current_datetime = datetime.now()

    current_time = current_datetime.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    tasks = get_due_tasks(
        current_time
    )

    for task in tasks:

        task_id = task[0]
        title = task[1]
        description = task[2]
        due_datetime_string = task[3]
        recurring = task[4]

        message = (
            f"{title}\n"
            f"{description}\n"
            f"Due: {due_datetime_string}"
        )

        print(
            f"Found due task: {title}"
        )

        # Send notification
        send_notification(
            "Task Due!",
            message
        )

        if recurring:

            current_due = datetime.strptime(
                due_datetime_string,
                "%Y-%m-%d %H:%M:%S"
            )

            # Move to tomorrow at the same time
            next_due = current_due + timedelta(
                days=1
            )

            next_due_string = (
                next_due.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            update_recurring_task(
                task_id,
                next_due_string
            )

            print(
                f"Next occurrence: "
                f"{next_due_string}"
            )

        else:

            mark_notified(task_id)

        print(
            f"Notification processed: {title}"
        )


    deleted_count = delete_expired_tasks(
        current_time
    )

    if deleted_count > 0:

        print(
            f"Deleted {deleted_count} "
            f"expired task(s)."
        )


def main():

    create_table()

    print(
        "Task reminder service started."
    )

    print(
        f"Checking every "
        f"{CHECK_INTERVAL} seconds."
    )

    while True:

        try:

            check_tasks()

            time.sleep(
                CHECK_INTERVAL
            )

        except Exception as error:

            print(
                f"Reminder error: {error}"
            )

            time.sleep(
                CHECK_INTERVAL
            )


if __name__ == "__main__":
    main()