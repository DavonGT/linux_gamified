"""Constants used throughout the game application."""

# Game Modes
SURVIVAL_MODE = 'survival'
TIME_ATTACK_MODE = 'time_attack'
HARDCORE_SURVIVAL_MODE = 'hardcore_survival'
HARDCORE_TIME_ATTACK_MODE = 'hardcore_time_attack'
PRACTICE_MODE = 'practice'

GAME_MODES = [
    SURVIVAL_MODE,
    TIME_ATTACK_MODE,
    HARDCORE_SURVIVAL_MODE,
    HARDCORE_TIME_ATTACK_MODE,
]

# Game Settings
DEFAULT_LIVES = 3
DEFAULT_TIME = 60
DEFAULT_SCORE = 0

# Point System
POINTS = {
    'easy': 10,
    'medium': 20,
    'hard': 30,
}

# Categories
CATEGORY_CHOICES = [
    ('file_operations', 'File Operations'),
    ('process_management', 'Process Management'),
    ('networking', 'Networking'),
    ('permissions', 'Permissions'),
    ('text_processing', 'Text Processing'),
    ('system_info', 'System Information'),
    ('other', 'Other'),
]

# Difficulty Levels
DIFFICULTY_CHOICES = [
    ('easy', '10'),
    ('medium', '20'),
    ('hard', '30'),
]
