# Task Tracker

# Import
import argparse
import json
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

# Task Load Function
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

# Task Save Function
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Task Add Function
def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added successfully (ID: {task_id})')

# Task Update Function
def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task {task_id} updated successfully.')
            return
    print(f'Task {task_id} not found.')

# Task Delete Function
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f'Task {task_id} deleted successfully.')

# Task Mark Function
def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task {task_id} marked as {status}.')
            return
    print(f'Task {task_id} not found.')

# Task List Function
def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    
    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        print(f'ID: {task["id"]}, Description: {task["description"]}, Status: {task["status"]}, Created At: {task["createdAt"]}, Updated At: {task["updatedAt"]}')

# Main Function
def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Add task
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', type=str, help='Description of the task')

    # Update task
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('id', type=int, help='Task ID')
    update_parser.add_argument('description', type=str, help='New description of the task')

    # Delete task
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID')

    # Mark as in progress
    mark_in_progress_parser = subparsers.add_parser('mark-in-progress', help='Mark a task as in progress')
    mark_in_progress_parser.add_argument('id', type=int, help='Task ID')

    # Mark as done
    mark_done_parser = subparsers.add_parser('mark-done', help='Mark a task as done')
    mark_done_parser.add_argument('id', type=int, help='Task ID')

    # List tasks
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('status', nargs='?', choices=['todo', 'in-progress', 'done'], help='Status of the tasks to list')

    args = parser.parse_args()

    # Call the following function as command
    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'update':
        update_task(args.id, args.description)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'mark-in-progress':
        mark_task(args.id, 'in-progress')
    elif args.command == 'mark-done':
        mark_task(args.id, 'done')
    elif args.command == 'list':
        list_tasks(args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
