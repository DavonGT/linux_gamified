import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from game.models import Task, Chapter, Mission

def load_json(json_file):
    """Load data from a JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)

def clear_existing_data():
    """Delete all existing Task, Chapter, and Mission objects."""
    Mission.objects.all().delete()
    Chapter.objects.all().delete()
    Task.objects.all().delete()

def create_task_from_data(task_data):
    """Create and save a Task object from task data dictionary."""
    fields = task_data.get('fields', {})
    task = Task(
        task=fields.get('task'),
        correct_commands=fields.get('correct_commands') or fields.get('commands'),
        difficulty=fields.get('difficulty'),
        category=fields.get('category'),
        hint=fields.get('hint')
    )
    task.save()
    return task

def create_chapters_and_missions():
    """
    Create chapters and missions linking existing tasks.
    This function creates Chapter objects from chapters.json and links Tasks via Mission objects.
    """
    chapters_file = os.path.join(settings.BASE_DIR, 'game', 'fixtures', 'chapters.json')
    chapters_data = load_json(chapters_file)

    # Create chapters
    chapters = []
    for ch_data in chapters_data:
        fields = ch_data.get('fields', {})
        chapter = Chapter.objects.create(
            name=fields.get('name'),
            number=fields.get('number'),
            description=fields.get('description')
        )
        chapters.append(chapter)

    # Map categories to chapters by chapter name lowercased and underscores
    category_to_chapter = {}
    for chapter in chapters:
        category_key = chapter.name.lower().replace(' ', '_')
        category_to_chapter[category_key] = chapter

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
        tasks_file = os.path.join(settings.BASE_DIR, 'game', 'fixtures', 'tasks.json')

        try:
            tasks = load_json(tasks_file)
            clear_existing_data()
            self.stdout.write(self.style.SUCCESS('Deleted existing tasks, chapters, and missions'))

            for task_data in tasks:
                task = create_task_from_data(task_data)
                self.stdout.write(self.style.SUCCESS(f'Added task: {task.task}'))

            create_chapters_and_missions()
            self.stdout.write(self.style.SUCCESS('Created chapters and missions'))

            self.stdout.write(self.style.SUCCESS(f'Successfully populated database with {len(tasks)} tasks from {tasks_file}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: Could not find tasks file at {tasks_file}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Error: Invalid JSON format in {tasks_file}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Error: Missing required field in task data: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
