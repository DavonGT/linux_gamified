import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from game.models import Task, Chapter, Mission

def load_tasks_from_json(json_file):
    """Load tasks from a JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)

def clear_existing_data():
    """Delete all existing Task, Chapter, and Mission objects."""
    Mission.objects.all().delete()
    Chapter.objects.all().delete()
    Task.objects.all().delete()

def create_task_from_data(task_data):
    """Create and save a Task object from task data dictionary."""
    task = Task(
        task=task_data['task'],
        correct_commands=task_data['commands'],
        difficulty=task_data['difficulty'],
        category=task_data['category'],
        hint=task_data['hint']
    )
    task.save()
    return task

def create_chapters_and_missions():
    """
    Create sample chapters and missions linking existing tasks.
    This function creates Chapter objects and links Tasks via Mission objects.
    """
    # Sample chapters data
    chapters_data = [
        {'name': 'Introduction to File Operations', 'number': 1, 'description': 'Basic file management tasks.'},
        {'name': 'Process Management', 'number': 2, 'description': 'Managing system processes.'},
        {'name': 'Text Processing', 'number': 3, 'description': 'Working with text files and commands.'},
    ]

    # Create chapters
    chapters = []
    for ch_data in chapters_data:
        chapter = Chapter.objects.create(
            name=ch_data['name'],
            number=ch_data['number'],
            description=ch_data['description']
        )
        chapters.append(chapter)

    # Assign tasks to chapters by category mapping
    category_to_chapter = {
        'file_operations': chapters[0],
        'process_management': chapters[1],
        'text_processing': chapters[2],
    }

    # Sample mission names and instructor sentences (can be customized)
    default_mission_name = "Mission for task"
    default_instructor_sentence = "Complete the following task."

    # Link tasks to chapters via missions
    tasks = Task.objects.all()
    for task in tasks:
        chapter = category_to_chapter.get(task.category)
        if chapter:
            Mission.objects.create(
                chapter=chapter,
                task=task,
                mission_name=f"{default_mission_name}: {task.task}",
                instructor_sentence=default_instructor_sentence,
                is_completed=False
            )

class Command(BaseCommand):
    help = 'Populates the database with sample tasks, chapters, and missions'

    def handle(self, *args, **options):
        json_file = os.path.join(settings.BASE_DIR, 'game', 'fixtures', 'tasks.json')

        try:
            tasks = load_tasks_from_json(json_file)
            clear_existing_data()
            self.stdout.write(self.style.SUCCESS('Deleted existing tasks, chapters, and missions'))

            for task_data in tasks:
                task = create_task_from_data(task_data)
                self.stdout.write(self.style.SUCCESS(f'Added task: {task.task}'))

            create_chapters_and_missions()
            self.stdout.write(self.style.SUCCESS('Created sample chapters and missions'))

            self.stdout.write(self.style.SUCCESS(f'Successfully populated database with {len(tasks)} tasks from {json_file}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: Could not find tasks file at {json_file}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Error: Invalid JSON format in {json_file}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Error: Missing required field in task data: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
