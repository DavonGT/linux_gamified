from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Player

class PlayerRegistrationForm(UserCreationForm):
    middle_name = forms.CharField(required=False, max_length=150, label="Middle Name")
    student_id = forms.CharField(max_length=20, label="Student ID")
    year_level = forms.CharField(max_length=10, label="Year Level")

    class Meta:
        model = Player
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'middle_name', 'last_name', 'student_id', 'year_level']