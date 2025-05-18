from django.db import models

class Question(models.Model):
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
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text='Category of the question'
    )

    task = models.TextField()  # The task/question for the player
    correct_commands = models.TextField()  # Store multiple correct commands as a comma-separated list
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')  # Difficulty level
    hint = models.TextField(default='No hints for this task', blank=True)  # Optional hint for the question
    def __str__(self):
        return self.task

    
    def is_correct(self, user_command):
        # Check if the user's command matches any of the correct commands
        correct_commands_list = [cmd.strip() for cmd in self.correct_commands.split(',')]
        user_command = user_command.replace('"', '').replace("'", '')  # Remove quotes\
        print(user_command, correct_commands_list)
        return user_command.strip() in correct_commands_list

    def get_points(self):
        # Return points based on difficulty
        return int(dict(self.DIFFICULTY_CHOICES).get(self.difficulty, 10))
