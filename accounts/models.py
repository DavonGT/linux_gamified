from django.contrib.auth.models import AbstractUser
from django.db import models

class Player(AbstractUser):
    score = models.IntegerField(default=0)  # Track player's score
    games_played = models.IntegerField(default=0)  # Track games played
    middle_name = models.CharField(max_length=150, blank=True)  # Optional middle name
    student_id = models.CharField(max_length=9, unique=True, default="00-00000")  # Unique student ID
    year_level = models.IntegerField(default=1)  # Year level (e.g., 1st, 4th)

