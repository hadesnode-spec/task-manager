import re
from datetime import datetime, timedelta

from database import (
    create_table,
    add_task,
    get_all_tasks
)


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_duration(duration):
    duration = duration.strip().lower()

    if not duration:
        raise ValueError(
            "Duration cannot be empty."
        )

    parts = duration.split()

    total = timedelta()

    for part in parts:

        if len(part) < 2:
            raise ValueError(
                f"Invalid duration: {part}"
            )

        value = part[:-1]
        unit = part[-1]

        if not value.isdigit():
            raise ValueError(
                f"Invalid duration"
            )

        value = int(value)

        if value <= 0:
            raise ValueError(
                "Duration values must be greater than 0."
            )

        if unit == "w":
            total += timedelta(weeks=value)

        elif unit == "d":
            total += timedelta(days=value)

        elif unit == "h":
            total += timedelta(hours=value)

        elif unit == "m":
            total += timedelta(minutes=value)

        elif unit == "s":
            total += timedelta(seconds=value)

        else:
            raise ValueError(
                f"Unknown time unit '{unit}'. "
                "Use s, m, h, d, or w."
            )

    if total.total_seconds() <= 0:
        raise ValueError(
            "Duration must be greater than 0."
        )

    return total


def get_duration_input(prompt, allow_never=False):

    while True:

        value = input(prompt).strip().lower()

        if allow_never and value == "never":
            return None

        try:
            return parse_duration(value)

        except ValueError as error:
            print(f"\n❌ {error}\n")


def get_yes_no(prompt):

    while True:

        answer = input(prompt).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print(
            "\nPlease enter y/yes or n/no.\n"
        )


def add_task_menu():

    print("\n========== ADD TASK ==========\n")

    title = input(
        "Enter task title: "
    ).strip()

    if not title:

        print(
            "\nTask title cannot be empty.\n"
        )

        return

    description = input(
        "Enter task description: "
    ).strip()

    print("""
Duration examples:

30s        = 30 seconds
90m        = 90 minutes
4h         = 4 hours
2d         = 2 days
1w         = 1 week
1h 30m     = 1 hour 30 minutes
2d 4h      = 2 days 4 hours
1d 12h 30m = 1 day 12 hours 30 minutes
""")


    due_duration = get_duration_input(
        "\nDue after: "
    )

    delete_duration = get_duration_input(
        "Delete after (or 'never'): ",
        allow_never=True
    )

    recurring = get_yes_no(
        "Repeat every day? "
    )

    created_time = datetime.now()

    due_datetime = (
        created_time + due_duration
    )

    if delete_duration is not None:

        delete_datetime = (
            created_time + delete_duration
        )

        if delete_datetime <= due_datetime:

            print(
                "\n Delete time must be AFTER "
                "the due time.\n"
            )

            return

        delete_datetime_string = (
            delete_datetime.strftime(
                DATETIME_FORMAT
            )
        )

    else:

        delete_datetime_string = None

    due_datetime_string = (
        due_datetime.strftime(
            DATETIME_FORMAT
        )
    )

    add_task(
        title,
        description,
        due_datetime_string,
        delete_datetime_string,
        int(recurring)
    )

    print(
        "\n✓ Task added successfully!\n"
    )

    print(
        f"Created : "
        f"{created_time.strftime(DATETIME_FORMAT)}"
    )

    print(
        f"First due: {due_datetime_string}"
    )

    if delete_datetime_string:

        print(
            f"Delete   : {delete_datetime_string}"
        )

    else:

        print(
            "Delete   : Never"
        )

    print(
        f"Repeat   : "
        f"{'Every day' if recurring else 'No'}"
    )

    print()


def view_tasks_menu():

    tasks = get_all_tasks()


    if not tasks:

        print(
            "No tasks found.\n"
        )

        return

    for task in tasks:

        task_id = task[0]
        title = task[1]
        description = task[2]
        due_datetime = task[3]
        delete_datetime = task[4]
        completed = task[5]
        recurring = task[6]

        status = (
            "Completed"
            if completed
            else "Pending"
        )

        repeat_status = (
            "Daily"
            if recurring
            else "No"
        )

        print(
            f"ID          : {task_id}"
        )

        print(
            f"Title       : {title}"
        )

        print(
            f"Description : {description}"
        )

        print(
            f"Due         : {due_datetime}"
        )

        print(
            f"Delete      : "
            f"{delete_datetime or 'Never'}"
        )

        print(
            f"Repeat      : {repeat_status}"
        )

        print(
            f"Status      : {status}"
        )

        print("-" * 45)


def main():

    create_table()

    while True:

        print("""

1. Add Task
2. View Tasks
3. Exit
""")

        choice = input("Enter choice: ").strip()

        if choice == "1":

            add_task_menu()

        elif choice == "2":

            view_tasks_menu()

        elif choice == "3":

            print(
                "\nGoodbye!"
            )

            break

        else:

            print(
                "\nInvalid choice. "
            )


if __name__ == "__main__":
    main()