from datetime import datetime

from database import (
    create_table,
    add_task,
    get_all_tasks
)


def add_task_menu():


    title = input("Enter task title: ").strip()

    description = input("Enter task description: ").strip()

    while True:

        due_datetime = input(
            "Enter due date and time "
            "(YYYY-MM-DD HH:MM:SS): "
        ).strip()

        try:

            datetime.strptime(
                due_datetime,
                "%Y-%m-%d %H:%M:%S"
            )

            break

        except ValueError:

            print(
                "Invalid format."
                " Use YYYY-MM-DD HH:MM:SS"
            )

    add_task(
        title,
        description,
        due_datetime
    )

    print("\n Task added successfully!\n")


def view_tasks_menu():

    tasks = get_all_tasks()


    if not tasks:

        print("No tasks found.\n")
        return

    for task in tasks:

        task_id = task[0]
        title = task[1]
        description = task[2]
        due_datetime = task[3]
        completed = task[4]

        status = (
            "Completed"
            if completed
            else "Pending"
        )

        print(f"ID          : {task_id}")
        print(f"Title       : {title}")
        print(f"Description : {description}")
        print(f"Due         : {due_datetime}")
        print(f"Status      : {status}")

        print("-" * 40)


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

            print("\nGoodbye!")
            break

        else:

            print("\nInvalid choice.\n")


if __name__ == "__main__":
    main()