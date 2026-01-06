#!/usr/bin/env python3
"""
Google Tasks Operations

All operations for Google Tasks:
- lists: List task lists
- create-list: Create a task list
- delete-list: Delete a task list
- tasks: List tasks in a list
- get: Get task details
- create: Create a task
- update: Update a task
- complete: Mark task complete
- delete: Delete a task
- move: Reorder tasks
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Find Nexus root
def find_nexus_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists():
            return parent
    return Path.cwd()

NEXUS_ROOT = find_nexus_root()

# Import from google-master shared auth
sys.path.insert(0, str(NEXUS_ROOT / "00-system" / "skills" / "google" / "google-master" / "scripts"))
from google_auth import get_credentials, get_service as _get_service, check_dependencies

def get_service():
    """Get authenticated Tasks service."""
    return _get_service('tasks')

# =============================================================================
# TASK LIST OPERATIONS
# =============================================================================

def list_task_lists(max_results: int = 20):
    """
    List all task lists.

    Args:
        max_results: Maximum number of results

    Returns:
        List of task lists
    """
    service = get_service()

    results = service.tasklists().list(maxResults=max_results).execute()
    lists = results.get('items', [])

    return [{
        'id': tl['id'],
        'title': tl['title'],
        'updated': tl.get('updated', '')
    } for tl in lists]


def create_task_list(title: str):
    """
    Create a new task list.

    Args:
        title: Task list title

    Returns:
        Created task list
    """
    service = get_service()

    task_list = service.tasklists().insert(body={'title': title}).execute()

    return {
        'id': task_list['id'],
        'title': task_list['title']
    }


def delete_task_list(list_id: str):
    """
    Delete a task list.

    Args:
        list_id: Task list ID

    Returns:
        Deletion status
    """
    service = get_service()

    service.tasklists().delete(tasklist=list_id).execute()

    return {'id': list_id, 'status': 'deleted'}


def rename_task_list(list_id: str, new_title: str):
    """
    Rename a task list.

    Args:
        list_id: Task list ID
        new_title: New title

    Returns:
        Updated task list
    """
    service = get_service()

    task_list = service.tasklists().update(
        tasklist=list_id,
        body={'id': list_id, 'title': new_title}
    ).execute()

    return {
        'id': task_list['id'],
        'title': task_list['title']
    }

# =============================================================================
# TASK OPERATIONS
# =============================================================================

def list_tasks(list_id: str = '@default', show_completed: bool = False,
               show_hidden: bool = False, max_results: int = 100):
    """
    List tasks in a task list.

    Args:
        list_id: Task list ID (use '@default' for default list)
        show_completed: Include completed tasks
        show_hidden: Include hidden tasks
        max_results: Maximum number of results

    Returns:
        List of tasks
    """
    service = get_service()

    results = service.tasks().list(
        tasklist=list_id,
        showCompleted=show_completed,
        showHidden=show_hidden,
        maxResults=max_results
    ).execute()

    tasks = results.get('items', [])

    return [{
        'id': t['id'],
        'title': t.get('title', ''),
        'notes': t.get('notes', ''),
        'status': t.get('status', 'needsAction'),
        'due': t.get('due', ''),
        'completed': t.get('completed', ''),
        'parent': t.get('parent', ''),
        'position': t.get('position', '')
    } for t in tasks]


def get_task(list_id: str, task_id: str):
    """
    Get task details.

    Args:
        list_id: Task list ID
        task_id: Task ID

    Returns:
        Task details
    """
    service = get_service()

    task = service.tasks().get(tasklist=list_id, task=task_id).execute()

    return {
        'id': task['id'],
        'title': task.get('title', ''),
        'notes': task.get('notes', ''),
        'status': task.get('status', 'needsAction'),
        'due': task.get('due', ''),
        'completed': task.get('completed', ''),
        'updated': task.get('updated', ''),
        'parent': task.get('parent', ''),
        'position': task.get('position', ''),
        'links': task.get('links', [])
    }


def create_task(list_id: str, title: str, notes: str = None, due: str = None,
                parent: str = None):
    """
    Create a new task.

    Args:
        list_id: Task list ID
        title: Task title
        notes: Task notes/description
        due: Due date (RFC 3339 format, e.g., 2025-12-20T00:00:00Z)
        parent: Parent task ID (for subtasks)

    Returns:
        Created task
    """
    service = get_service()

    task_body = {'title': title}

    if notes:
        task_body['notes'] = notes
    if due:
        # Convert simple date to RFC 3339 if needed
        if len(due) == 10:  # YYYY-MM-DD format
            due = f"{due}T00:00:00.000Z"
        task_body['due'] = due

    task = service.tasks().insert(
        tasklist=list_id,
        body=task_body,
        parent=parent
    ).execute()

    return {
        'id': task['id'],
        'title': task.get('title', ''),
        'notes': task.get('notes', ''),
        'due': task.get('due', ''),
        'status': task.get('status', 'needsAction')
    }


def update_task(list_id: str, task_id: str, title: str = None, notes: str = None,
                due: str = None, status: str = None):
    """
    Update a task.

    Args:
        list_id: Task list ID
        task_id: Task ID
        title: New title (optional)
        notes: New notes (optional)
        due: New due date (optional)
        status: New status: needsAction or completed (optional)

    Returns:
        Updated task
    """
    service = get_service()

    # Get current task first
    task = service.tasks().get(tasklist=list_id, task=task_id).execute()

    if title is not None:
        task['title'] = title
    if notes is not None:
        task['notes'] = notes
    if due is not None:
        if len(due) == 10:
            due = f"{due}T00:00:00.000Z"
        task['due'] = due
    if status is not None:
        task['status'] = status

    updated = service.tasks().update(
        tasklist=list_id,
        task=task_id,
        body=task
    ).execute()

    return {
        'id': updated['id'],
        'title': updated.get('title', ''),
        'notes': updated.get('notes', ''),
        'due': updated.get('due', ''),
        'status': updated.get('status', '')
    }


def complete_task(list_id: str, task_id: str):
    """
    Mark a task as complete.

    Args:
        list_id: Task list ID
        task_id: Task ID

    Returns:
        Updated task
    """
    return update_task(list_id, task_id, status='completed')


def uncomplete_task(list_id: str, task_id: str):
    """
    Mark a task as incomplete.

    Args:
        list_id: Task list ID
        task_id: Task ID

    Returns:
        Updated task
    """
    return update_task(list_id, task_id, status='needsAction')


def delete_task(list_id: str, task_id: str):
    """
    Delete a task.

    Args:
        list_id: Task list ID
        task_id: Task ID

    Returns:
        Deletion status
    """
    service = get_service()

    service.tasks().delete(tasklist=list_id, task=task_id).execute()

    return {'id': task_id, 'status': 'deleted'}


def move_task(list_id: str, task_id: str, parent: str = None, previous: str = None):
    """
    Move/reorder a task.

    Args:
        list_id: Task list ID
        task_id: Task ID
        parent: New parent task ID (for making subtask)
        previous: Task ID to place after

    Returns:
        Moved task
    """
    service = get_service()

    task = service.tasks().move(
        tasklist=list_id,
        task=task_id,
        parent=parent,
        previous=previous
    ).execute()

    return {
        'id': task['id'],
        'title': task.get('title', ''),
        'parent': task.get('parent', ''),
        'position': task.get('position', '')
    }


def clear_completed(list_id: str):
    """
    Clear all completed tasks from a list.

    Args:
        list_id: Task list ID

    Returns:
        Status
    """
    service = get_service()

    service.tasks().clear(tasklist=list_id).execute()

    return {'list_id': list_id, 'status': 'completed_tasks_cleared'}

# =============================================================================
# CLI
# =============================================================================

def main():
    # Windows UTF-8 encoding fix
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        description="Google Tasks Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List task lists command
    lists_parser = subparsers.add_parser('lists', help='List task lists')
    lists_parser.add_argument('--max', type=int, default=20, help='Max results')

    # Create task list command
    create_list_parser = subparsers.add_parser('create-list', help='Create a task list')
    create_list_parser.add_argument('title', help='List title')

    # Delete task list command
    del_list_parser = subparsers.add_parser('delete-list', help='Delete a task list')
    del_list_parser.add_argument('list_id', help='Task list ID')

    # Rename task list command
    rename_list_parser = subparsers.add_parser('rename-list', help='Rename a task list')
    rename_list_parser.add_argument('list_id', help='Task list ID')
    rename_list_parser.add_argument('new_title', help='New title')

    # List tasks command
    tasks_parser = subparsers.add_parser('tasks', help='List tasks')
    tasks_parser.add_argument('--list', default='@default', help='Task list ID')
    tasks_parser.add_argument('--show-completed', action='store_true')
    tasks_parser.add_argument('--max', type=int, default=100, help='Max results')

    # Get task command
    get_parser = subparsers.add_parser('get', help='Get task details')
    get_parser.add_argument('task_id', help='Task ID')
    get_parser.add_argument('--list', default='@default', help='Task list ID')

    # Create task command
    create_parser = subparsers.add_parser('create', help='Create a task')
    create_parser.add_argument('title', help='Task title')
    create_parser.add_argument('--list', default='@default', help='Task list ID')
    create_parser.add_argument('--notes', help='Task notes')
    create_parser.add_argument('--due', help='Due date (YYYY-MM-DD)')
    create_parser.add_argument('--parent', help='Parent task ID (for subtask)')

    # Update task command
    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('task_id', help='Task ID')
    update_parser.add_argument('--list', default='@default', help='Task list ID')
    update_parser.add_argument('--title', help='New title')
    update_parser.add_argument('--notes', help='New notes')
    update_parser.add_argument('--due', help='New due date')
    update_parser.add_argument('--status', choices=['needsAction', 'completed'])

    # Complete task command
    complete_parser = subparsers.add_parser('complete', help='Mark task complete')
    complete_parser.add_argument('task_id', help='Task ID')
    complete_parser.add_argument('--list', default='@default', help='Task list ID')

    # Uncomplete task command
    uncomplete_parser = subparsers.add_parser('uncomplete', help='Mark task incomplete')
    uncomplete_parser.add_argument('task_id', help='Task ID')
    uncomplete_parser.add_argument('--list', default='@default', help='Task list ID')

    # Delete task command
    del_parser = subparsers.add_parser('delete', help='Delete a task')
    del_parser.add_argument('task_id', help='Task ID')
    del_parser.add_argument('--list', default='@default', help='Task list ID')

    # Move task command
    move_parser = subparsers.add_parser('move', help='Move/reorder a task')
    move_parser.add_argument('task_id', help='Task ID')
    move_parser.add_argument('--list', default='@default', help='Task list ID')
    move_parser.add_argument('--parent', help='New parent task ID')
    move_parser.add_argument('--after', help='Place after this task ID')

    # Clear completed command
    clear_parser = subparsers.add_parser('clear-completed', help='Clear completed tasks')
    clear_parser.add_argument('--list', default='@default', help='Task list ID')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'lists':
            result = list_task_lists(args.max)
        elif args.command == 'create-list':
            result = create_task_list(args.title)
        elif args.command == 'delete-list':
            result = delete_task_list(args.list_id)
        elif args.command == 'rename-list':
            result = rename_task_list(args.list_id, args.new_title)
        elif args.command == 'tasks':
            result = list_tasks(args.list, args.show_completed, max_results=args.max)
        elif args.command == 'get':
            result = get_task(args.list, args.task_id)
        elif args.command == 'create':
            result = create_task(args.list, args.title, args.notes, args.due, args.parent)
        elif args.command == 'update':
            result = update_task(args.list, args.task_id, args.title, args.notes,
                               args.due, args.status)
        elif args.command == 'complete':
            result = complete_task(args.list, args.task_id)
        elif args.command == 'uncomplete':
            result = uncomplete_task(args.list, args.task_id)
        elif args.command == 'delete':
            result = delete_task(args.list, args.task_id)
        elif args.command == 'move':
            result = move_task(args.list, args.task_id, args.parent, args.after)
        elif args.command == 'clear-completed':
            result = clear_completed(args.list)
        else:
            parser.print_help()
            return

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({'error': str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
