from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import PlayerRegistrationForm, PlayerLoginForm

def register(request):
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.middle_name = form.cleaned_data.get('middle_name')
            user.student_id = form.cleaned_data.get('student_id')
            user.year_level = form.cleaned_data.get('year_level')
            user.save()
            return redirect('login')
    else:
        form = PlayerRegistrationForm()
    return render(request, 'accounts/login.html', {'form': form, 'mode': 'register'})

def login_view(request):
    if request.method == 'POST':
        form = PlayerLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = PlayerLoginForm(request, data=request.POST)
    return render(request, 'accounts/login.html', {'form': form, 'mode': 'login'})

def logout_view(request):
    logout(request)
    return redirect('login')
