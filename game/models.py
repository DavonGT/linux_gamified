from django.db import models

class Chapter(models.Model):
    number = models.IntegerField(unique=True)  # Chapter number (e.g., "1")
    name = models.CharField(max_length=255)  # Chapter name (e.g., "Welcome to the terminal world")
    description = models.TextField()  # Chapter description (e.g., "This chapter introduces users to their virtual 'home'")

    def __str__(self):
        return f"Chapter {self.number}: {self.name}"


class Task(models.Model):
    CATEGORY_CHOICES = [
        ('file_operations', 'File Operations'),
        ('process_management', 'Process Management'),
        ('networking', 'Networking'),
        ('permissions', 'Permissions'),
        ('text_processing', 'Text Processing'),
        ('system_info', 'System Information'),
        ('other', 'Other'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', '10'),
        ('medium', '20'),
        ('hard', '30'),
    ]
    
    task = models.CharField(max_length=255)  # Task description (e.g., "Find out who you are")
    correct_commands = models.TextField()  # The correct command(s) for the task (e.g., "whoami")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')  # Difficulty level
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')  # Task category
    hint = models.TextField(default='No hints for this task', blank=True)  # Optional hint for the task

    def __str__(self):
        return self.task

    def get_hint(self):
        return [hint.strip() for hint in self.hint.split(',')]
    
    def get_correct_commands_list(self):
        # Return a list of correct commands, removing any extra spaces
        return [cmd.strip() for cmd in self.correct_commands.split(',')]
    
    def is_correct(self, user_command):
        # Check if the user's command matches any of the correct commands
        correct_commands_list = self.get_correct_commands_list()
        user_command = user_command.replace('"', '').replace("'", '')  # Remove quotes
        print(user_command, correct_commands_list)
        return user_command.strip() in correct_commands_list

    def get_points(self):
        # Return points based on difficulty
        return int(dict(self.DIFFICULTY_CHOICES).get(self.difficulty, 10))
    


class Mission(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)  # Connect mission to Chapter
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # Connect mission to Task
    mission_name = models.CharField(max_length=255)  # Mission name (e.g., "Meet your virtual self")
    instructor_sentence = models.TextField()  # Instructor's sentence for the mission (e.g., "Welcome to your very first day in the world of Linux!")
    is_completed = models.BooleanField(default=False)  # Track if the mission is completed
    
    def __str__(self):
        return f"{self.chapter.number}: {self.mission_name}"
