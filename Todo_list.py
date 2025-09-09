import json  # For file storage
from datetime import datetime

# Load tasks from file
def load_tasks(filename="tasks.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to file
def save_tasks(tasks, filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, title, category=None, deadline=None, priority="Normal"):
    task = {
        "title": title,
        "category": category,
        "deadline": deadline,
        "priority": priority,
        "completed": False
    }
    tasks.append(task)
    print(f"Task '{title}' added!")

def edit_task(tasks, index, new_title=None, new_category=None, new_deadline=None, new_priority=None):
    if 0 <= index < len(tasks):
        if new_title:
            tasks[index]["title"] = new_title
        if new_category:
            tasks[index]["category"] = new_category
        if new_deadline:
            tasks[index]["deadline"] = new_deadline
        if new_priority:
            tasks[index]["priority"] = new_priority
        print("Task updated successfully.")
    else:
        print("Invalid task number!")

def mark_complete(tasks, index):
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        print("Task marked as complete!")
    else:
        print("Invalid task number!")

def delete_task(tasks, index):
    if 0 <= index < len(tasks):
        removed_task = tasks.pop(index)
        print(f"Task '{removed_task['title']}' deleted!")
    else:
        print("Invalid task number!")

def view_tasks(tasks, show_all=True, filter_category=None, search_keyword=None, show_overdue=False):
    filtered = tasks
    if not show_all:
        filtered = [t for t in tasks if not t["completed"]]
    if filter_category:
        filtered = [t for t in filtered if t["category"] == filter_category]
    if search_keyword:
        filtered = [t for t in filtered if search_keyword.lower() in t["title"].lower()]
    if show_overdue:
        today = datetime.today().date()
        filtered = [
            t for t in filtered
            if t["deadline"] and not t["completed"] and
            datetime.strptime(t["deadline"], "%Y-%m-%d").date() < today
        ]
    if not filtered:
        print("No tasks available.")
    else:
        print("\nTo-Do List:")
        for i, task in enumerate(filtered, 1):
            status = "✓" if task["completed"] else "✗"
            overdue = ""
            if task["deadline"] and not task["completed"]:
                try:
                    due = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                    if due < datetime.today().date():
                        overdue = " (Overdue!)"
                except Exception:
                    pass
            print(f"{i}. {task['title']} [{status}] - {task['category']} (Deadline: {task['deadline']}) [Priority: {task.get('priority','Normal')}] {overdue}")

def list_categories(tasks):
    categories = set(t["category"] for t in tasks if t["category"])
    if categories:
        print("Categories:")
        for cat in categories:
            print(f"- {cat}")
    else:
        print("No categories found.")

def clear_completed(tasks):
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["completed"]]
    print(f"Cleared {before - len(tasks)} completed tasks.")

tasks = load_tasks()

while True:
    print("\n--- To-Do List Menu ---")
    print("1. View All Tasks")
    print("2. Add a Task")
    print("3. Edit a Task")
    print("4. Mark Task as Complete")
    print("5. Delete a Task")
    print("6. View Overdue Tasks")
    print("7. List Categories")
    print("8. Search Tasks")
    print("9. Clear All Completed Tasks")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        view_tasks(tasks)
    elif choice == "2":
        title = input("Enter task title: ")
        category = input("Enter category (optional): ")
        deadline = input("Enter deadline (YYYY-MM-DD, optional): ")
        priority = input("Enter priority (Low/Normal/High, default Normal): ") or "Normal"
        add_task(tasks, title, category, deadline, priority)
    elif choice == "3":
        view_tasks(tasks)
        index = int(input("Enter task number to edit: ")) - 1
        new_title = input("Enter new title (or leave blank): ")
        new_category = input("Enter new category (or leave blank): ")
        new_deadline = input("Enter new deadline (YYYY-MM-DD, or leave blank): ")
        new_priority = input("Enter new priority (Low/Normal/High, or leave blank): ")
        edit_task(tasks, index, new_title, new_category, new_deadline, new_priority)
    elif choice == "4":
        view_tasks(tasks, show_all=False)
        index = int(input("Enter task number to mark as complete: ")) - 1
        mark_complete(tasks, index)
    elif choice == "5":
        view_tasks(tasks)
        index = int(input("Enter task number to delete: ")) - 1
        delete_task(tasks, index)
    elif choice == "6":
        view_tasks(tasks, show_overdue=True)
    elif choice == "7":
        list_categories(tasks)
    elif choice == "8":
        keyword = input("Enter keyword to search: ")
        view_tasks(tasks, search_keyword=keyword)
    elif choice == "9":
        clear_completed(tasks)
    elif choice == "0":
        save_tasks(tasks)
        print("Tasks saved. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")