from django.contrib.auth.models import AbstractUser
from django.db import models

class Player(AbstractUser):
    survival_score = models.IntegerField(default=0)  # Track player's survival score
    time_attack_score = models.IntegerField(default=0)  # Track player's time attack score
    ha_score = models.IntegerField(default=0)  # Track player's hardcore survival score
    hta_score = models.IntegerField(default=0)  # Track player's hardcore time attack score
    games_played = models.IntegerField(default=0)  # Track games played
    chapter_played = models.IntegerField(default=0)
   

