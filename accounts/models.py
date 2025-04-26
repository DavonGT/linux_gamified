from django.contrib.auth.models import AbstractUser
from django.db import models

class Player(AbstractUser):
    score = models.IntegerField(default=0)  # Track player's score
    games_played = models.IntegerField(default=0)  # Track games played
