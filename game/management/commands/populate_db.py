from django.core.management.base import BaseCommand
from game.models import Question

class Command(BaseCommand):
    help = 'Populates the database with sample questions'

    def handle(self, *args, **options):
        questions = [
            {
                'task': 'List all files in the current directory',
                'commands': 'ls, dir',
                'difficulty': 'easy',
                'hint': 'Use the command that lists directory contents'
            },
            {
                'task': 'Create a new directory called "test"',
                'commands': 'mkdir test',
                'difficulty': 'easy',
                'hint': 'Use the make directory command'
            },
            {
                'task': 'Change to the parent directory',
                'commands': 'cd .., cd..',
                'difficulty': 'easy',
                'hint': 'Use cd with two dots to go up one directory'
            },
            {
                'task': 'Display the current working directory',
                'commands': 'pwd',
                'difficulty': 'easy',
                'hint': 'Use the command that prints working directory'
            },
            {
                'task': 'Create a file named "example.txt"',
                'commands': 'touch example.txt',
                'difficulty': 'easy',
                'hint': 'Use the touch command to create an empty file'
            },
            {
                'task': 'Display the contents of a file called "data.txt"',
                'commands': 'cat data.txt, type data.txt, more data.txt, less data.txt',
                'difficulty': 'medium',
                'hint': 'Use commands that can display file contents'
            },
            {
                'task': 'Find all .txt files in the current directory and subdirectories',
                'commands': 'find . -name "*.txt"',
                'difficulty': 'medium',
                'hint': 'Use the find command with appropriate arguments'
            },
            {
                'task': 'Count the number of lines in a file called "data.txt"',
                'commands': 'wc -l data.txt',
                'difficulty': 'medium',
                'hint': 'Use the word count command with the line option'
            },
            {
                'task': 'Search for the word "error" in all .log files',
                'commands': 'grep error *.log',
                'difficulty': 'hard',
                'hint': 'Use grep to search for text patterns'
            },
            {
                'task': 'List all running processes',
                'commands': 'ps aux, ps -ef, top, htop',
                'difficulty': 'hard',
                'hint': 'Use process status or task manager commands'
            }
        ]

        # Clear existing questions
        Question.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted existing questions'))

        # Add new questions
        for q in questions:
            question = Question(
                task=q['task'],
                correct_commands=q['commands'],
                difficulty=q['difficulty'],
                hint=q['hint']
            )
            question.save()
            self.stdout.write(self.style.SUCCESS(f'Added question: {q["task"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample questions'))