
from datetime import datetime, timedelta

from database import create_table, add_task, get_all_tasks
from tasks import Task

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_duration(duration):
    duration = duration.strip().lower()
    if not duration:
        raise ValueError("Duration cannot be empty.")

    total = timedelta()

    for part in duration.split():
        if len(part) < 2 or not part[:-1].isdigit():
            raise ValueError(f"Invalid duration: {part}")

        value = int(part[:-1])
        unit = part[-1]

        if value <= 0:
            raise ValueError("Duration must be greater than zero.")

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
            raise ValueError("Use s,m,h,d, or w.")
    Task.validate_duration(total)
    return total


def get_duration_input(prompt, allow_never=False):
    while True:
        value=input(prompt).strip().lower()
        if allow_never and value == "never":
            return None
        try:
            return parse_duration(value)
        except ValueError as error:
            print(f"Invalid duration: {error}")


def get_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False

        print("Please enter y/yes or n/no.")


def add_task_menu():
    title = input("Enter task title:").strip()
    description = input("Enter task description:").strip()

    due_duration = get_duration_input("Due after: ")
    delete_duration = get_duration_input(
        "Delete after (or 'never'): ",
        allow_never=True
    )
    recurring = get_yes_no("Repeat every day? (y/n): ")

    created_time = datetime.now()
    due_datetime = created_time + due_duration

    delete_datetime = (
        created_time + delete_duration
        if delete_duration is not None
        else None
    )

    try:
        task = Task(
            task_id=None,
            title=title,
            description=description,
            due_datetime=due_datetime,
            delete_datetime=delete_datetime,
            recurring=recurring,
        )

        task_id=add_task(task)

    except ValueError as error:
        print(f"Could not create task: {error}")
        return

    print(f"\nTask added successfully! ID: {task_id}")
    print(f"Due: {due_datetime.strftime(DATETIME_FORMAT)}")
    print("Delete: " f"{delete_datetime.strftime(DATETIME_FORMAT) if delete_datetime else 'Never'}")
    print(f"Repeat: {'Every day' if recurring else 'No'}")


def view_tasks_menu():
    tasks = get_all_tasks()

    if not tasks:
        print("No tasks found.\n")
        return

    for task in tasks:
        print(f"ID          : {task.id}")
        print(f"Title       : {task.title}")
        print(f"Description : {task.description or ''}")
        print(f"Due         : {task.due_datetime}")
        print(f"Delete      : {task.delete_datetime or 'Never'}")
        print(f"Repeat      : {'Daily' if task.recurring else 'No'}")
        print(f"Status      : {'Completed' if task.completed else 'Pending'}")
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
            break
        else:
            print("Invalid choice.")


if __name__=="__main__":
    main()
