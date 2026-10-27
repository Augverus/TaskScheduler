tasks = []
from datetime import datetime, timedelta
def add_task():
    name = input("Enter your task's name: ")
    starting_time = input("Enter when your task starts (ex: 12:00): ")
    duration = float(input("Enter how long your task lasts in hours: "))

    conflict = find_conflict(starting_time, duration)

    if conflict is None:
        task = {
            "name": name,
            "time": starting_time,
            "duration": duration,
            "done": False
        }

        tasks.append(task)
        print("Task added.")
        return

    print(f'\nConflict with "{conflict["name"]}"')

    original_start = to_datetime(starting_time)

    before = original_start - timedelta(hours=2)
    after = original_start + timedelta(hours=2)

    before_string = before.strftime("%H:%M")
    after_string = after.strftime("%H:%M")

    print(f"1. Put the new task at {before_string}")
    print(f"2. Put the new task at {after_string}")
    print("3. Neither")

    choice = input("Choose an option: ")

    if choice == "1":
        if time_is_available(before_string, duration):
            starting_time = before_string
        else:
            print("That earlier time also has a conflict.")
            return

    elif choice == "2":
        if time_is_available(after_string, duration):
            starting_time = after_string
        else:
            print("That later time also has a conflict.")
            return

    elif choice == "3":
        print(f'You need to move "{conflict["name"]}" to another time.')

        new_time = input(
            f'Enter a new starting time for "{conflict["name"]}": '
        )

        conflict["time"] = new_time

    else:
        print("Invalid option.")
        return

    task = {
        "name": name,
        "time": starting_time,
        "duration": duration,
        "done": False
    }

    tasks.append(task)
    print("Task added.")
def show_tasks():
    if len(tasks) == 0:
        print("no tassks here yet")
    else:
        for number, task in enumerate(tasks, start=1):
            start = datetime.strptime(task["time"], "%H:%M")
            end = start + timedelta(hours=task["duration"])
            if task["done"] == True:
                status = "DOME"
            else:
                status = "NOT DONE"
            print(f'{number}. [{status}] {task["name"]}')
            print(f'   {task["time"]} - {end.strftime("%H:%M")}')
def mark_done():
    show_tasks()
    number = int(input("Which task did you finish? "))
    if number < 1 or number > len(tasks):
        print("invalid number")
        return
    tasks[number - 1]["done"] = True
def edit_task():
    if len(tasks) == 0:
        print("You have no tassks to edit.")
        return
    show_tasks()
    number = int(input("Which task you want to eidt? "))
    if number < 1 or number > len(tasks):
        print("Invalid task number.")
        return
    task = tasks[number - 1]
    new_name = input(f'Task new name ({task["name"]}): ')
    new_time = input(f'Task new time ({task["time"]}): ')
    new_duration = input(f'Task new duration ({task["duration"]} hours): ')
    if new_name != "":
        task["name"] = new_name
    if new_time != "":
        task["time"] = new_time
    if new_duration != "":
        task["duration"] = float(new_duration)
    print("Task updated.")
def delete_task():
    if len(tasks) == 0:
        print("You have no tasks to delete.")
        return

    show_tasks()

    number = int(input("Which task do you want to delete? "))
    if number < 1 or number > len(tasks):
        print("invalid number")
        return
    deleted_task = tasks.pop(number - 1)

    print(f'Deleted: {deleted_task["name"]}')

def to_datetime(time_string):
    return datetime.strptime(time_string, "%H:%M")
def tasks_overlap(start1, end1, start2, end2):
    return start1 < end2 and end1 > start2
def find_conflict(starting_time, duration, ignore_task=None):
    new_start = to_datetime(starting_time)
    new_end = new_start + timedelta(hours=duration)

    for task in tasks:

        if task is ignore_task:
            continue

        old_start = to_datetime(task["time"])
        old_end = old_start + timedelta(hours=task["duration"])

        if tasks_overlap(new_start, new_end, old_start, old_end):
            return task

    return None
def time_is_available(starting_time, duration, ignore_task=None):
    return find_conflict(starting_time, duration, ignore_task) is None


while True:
    print("\n--- TASK MANAGER ---")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Mark task as done")
    print("4. Edit task")
    print("5. Delete task")
    print("6. Exit")

    choice = input("Choose an option: ")
    if choice == "1":
        add_task()
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        edit_task()     
    elif choice =="5":
        delete_task()
    elif choice == "6":
        print("ok exiting")
        break
    else:
        print("invalid option bro")
    