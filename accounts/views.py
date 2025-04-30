from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import PlayerRegistrationForm

def register(request):
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.middle_name = form.cleaned_data.get('middle_name')
            user.student_id = form.cleaned_data.get('student_id')
            user.year_level = form.cleaned_data.get('year_level')
            user.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = PlayerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout