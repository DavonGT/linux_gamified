import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from game.models import Task

class Command(BaseCommand):
    help = 'Populates the database with sample tasks'

    def handle(self, *args, **options):
        # Path to the tasks JSON file
        json_file = os.path.join(settings.BASE_DIR, 'game', 'fixtures', 'tasks.json')
        
        try:
            # Read tasks from JSON file
            with open(json_file, 'r') as f:
                tasks = json.load(f)
            
            # Clear existing tasks
            Task.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Deleted existing tasks'))
            
            # Add new tasks
            for q in tasks:
                task = Task(
                    task=q['task'],
                    correct_commands=q['commands'],
                    difficulty=q['difficulty'],
                    category=q['category'],
                    hint=q['hint']
                )
                task.save()
                self.stdout.write(self.style.SUCCESS(f'Added task: {q["task"]}'))
            
            self.stdout.write(self.style.SUCCESS(f'Successfully populated database with {len(tasks)} tasks from {json_file}'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: Could not find tasks file at {json_file}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Error: Invalid JSON format in {json_file}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Error: Missing required field in task data: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))