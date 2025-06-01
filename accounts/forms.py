from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Player


#kanan mga effects chenelenz la in ha login/register :)))
class PlayerRegistrationForm(UserCreationForm):
    class Meta:
        model = Player
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'placeholder': ' '}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = ' '
        self.fields['password2'].widget.attrs['placeholder'] = ' '

class PlayerLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ' '
        self.fields['password'].widget.attrs['placeholder'] = ' '
