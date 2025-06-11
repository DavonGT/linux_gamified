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

class Command(BaseCommand):
    help = 'Populates the database with data from fixtures: tasks, chapters, and missions'

    def handle(self, *args, **options):
        tasks_file = os.path.join(settings.BASE_DIR, 'game', 'fixtures', 'tasks.json')
        chapters_file = os.path.join(settings.BASE_DIR, 'game', 'fixtures', 'chapters.json')
        missions_file = os.path.join(settings.BASE_DIR, 'game', 'fixtures', 'missions.json')

        try:
            # Load fixture data
            tasks_data = load_json(tasks_file)
            chapters_data = load_json(chapters_file)
            missions_data = load_json(missions_file)

            # Clear existing data
            clear_existing_data()
            self.stdout.write(self.style.SUCCESS('Deleted existing tasks, chapters, and missions'))

            # Create tasks and map old pk to new Task objects
            task_pk_map = {}
            for task_entry in tasks_data:
                old_pk = task_entry.get('pk')
                fields = task_entry.get('fields', {})
                task = Task.objects.create(
                    task=fields.get('task'),
                    correct_commands=fields.get('correct_commands') or fields.get('commands'),
                    difficulty=fields.get('difficulty'),
                    category=fields.get('category'),
                    hint=fields.get('hint')
                )
                task_pk_map[old_pk] = task
                self.stdout.write(self.style.SUCCESS(f'Added task: {task.task}'))

            # Create chapters and map old pk to new Chapter objects
            chapter_pk_map = {}
            for chapter_entry in chapters_data:
                old_pk = chapter_entry.get('pk')
                fields = chapter_entry.get('fields', {})
                chapter = Chapter.objects.create(
                    name=fields.get('name'),
                    number=fields.get('number'),
                    description=fields.get('description')
                )
                chapter_pk_map[old_pk] = chapter
                self.stdout.write(self.style.SUCCESS(f'Added chapter: {chapter.name}'))

            # Create missions using mapped Chapter and Task objects
            for mission_entry in missions_data:
                fields = mission_entry.get('fields', {})
                old_chapter_pk = fields.get('chapter')
                old_task_pk = fields.get('task')
                chapter = chapter_pk_map.get(old_chapter_pk)
                task = task_pk_map.get(old_task_pk)
                if chapter and task:
                    Mission.objects.create(
                        chapter=chapter,
                        task=task,
                        mission_name=fields.get('mission_name'),
                        instructor_sentence=fields.get('instructor_sentence'),
                        is_completed=fields.get('is_completed', False)
                    )
                    self.stdout.write(self.style.SUCCESS(f'Added mission: {fields.get("mission_name")}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Skipped mission with chapter pk {old_chapter_pk} and task pk {old_task_pk} due to missing references'))

            self.stdout.write(self.style.SUCCESS('Successfully populated database from fixtures'))

        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f'Error: Could not find file - {str(e)}'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error: Invalid JSON format - {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
