from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question
import random
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import Player
from django.db.models import Max
from django.db import models


def test(request):
    # Test view to check if the server is running
    return render(request, 'game/test.html',)


@login_required
def dashboard(request):
    # Fetch the highest score for each player in each game mode
    survival_leaderboard = Player.objects.values('username').annotate(
        survival_score=models.F('survival_score')
    ).order_by('-survival_score')[:10]

    time_attack_leaderboard = Player.objects.values('username').annotate(
        time_attack_score=models.F('time_attack_score')
    ).order_by('-time_attack_score')[:10]

    hardcore_survival_leaderboard = Player.objects.values('username').annotate(
        ha_score=models.F('ha_score')
    ).order_by('-ha_score')[:10]

    hardcore_time_attack_leaderboard = Player.objects.values('username').annotate(
        hta_score=models.F('hta_score')
    ).order_by('-hta_score')[:10]

    # Add rank to each player in each leaderboard
    survival_leaderboard = [
        {'rank': idx + 1, 'username': entry['username'], 'survival_score': entry['survival_score']}
        for idx, entry in enumerate(survival_leaderboard)
    ]

    time_attack_leaderboard = [
        {'rank': idx + 1, 'username': entry['username'], 'time_attack_score': entry['time_attack_score']}
        for idx, entry in enumerate(time_attack_leaderboard)
    ]

    hardcore_survival_leaderboard = [
        {'rank': idx + 1, 'username': entry['username'], 'ha_score': entry['ha_score']}
        for idx, entry in enumerate(hardcore_survival_leaderboard)
    ]

    hardcore_time_attack_leaderboard = [
        {'rank': idx + 1, 'username': entry['username'], 'hta_score': entry['hta_score']}
        for idx, entry in enumerate(hardcore_time_attack_leaderboard)
    ]

    return render(request, 'game/dashboard.html', {
        'player': request.user,
        'survival_leaderboard': survival_leaderboard,
        'time_attack_leaderboard': time_attack_leaderboard,
        'hardcore_survival_leaderboard': hardcore_survival_leaderboard,
        'hardcore_time_attack_leaderboard': hardcore_time_attack_leaderboard,
    })

@login_required
def select_mode(request):
    # Render the mode selection screen
    return render(request, 'game/select_mode.html')

def set_mode(request, mode):
    # Set the gameplay mode based on the selected option
    if mode in ['survival', 'time_attack', 'hardcore_survival', 'hardcore_time_attack']:
        request.session['mode'] = mode
        request.session['score'] = 0  # Reset the score
        if 'survival' in mode:
            request.session['lives'] = 3  # Initialize lives for survival modes
        elif 'time_attack' in mode:
            request.session['time'] = 20
            request.session['lives'] = None
        return redirect('game')
    elif 'practice' in mode:
        return redirect('practice_mode')
    return redirect('select_mode')  # Redirect to mode selection if invalid mode

@login_required
def game_view(request):
    print(request.session.items())
    # Set default time for time-based modes
    time = 20 if 'time_attack' in request.session['mode'] else None
    if time != None and request.session['time'] > time :
        time = request.session.get('time')

    # Ensure the mode is set before starting the game
    if 'mode' not in request.session:
        return redirect('select_mode')

    # Check for game over conditions
    if request.session['mode'] in ['survival', 'hardcore_survival'] and request.session['lives'] <= 0:
        return redirect('game_over')

    question = random.choice(Question.objects.all())  # Get a random question
    mode = request.session['mode']
    return render(request, 'game/game.html', {
        'time': time,
        'question': question,
        'survival_score': request.session['score'],
        'time_attack_score': request.session['score'],
        'ha_score': request.session['score'],
        'hta_score': request.session['score'],
        'lives': request.session.get('lives'),  # Pass lives to the template
        'mode': mode,
        'player': request.user.username,
    })

@csrf_exempt
def validate_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_id = data.get('question_id')
            user_command = data.get('user_command')
            current_time = data.get('current_time', None)

            question = Question.objects.get(id=question_id)
            if question.is_correct(user_command):
                points = question.get_points()
                if 'hardcore' in request.session.get('mode', ''):
                    points += 10
                request.session['score'] = request.session.get('score', 0) + points
                return JsonResponse({
                    'result': 'correct',
                    'score': request.session['score'],
                    'time': current_time,
                    'lives': request.session.get('lives')  # Added lives to response
                })
            else:
                if 'survival' in request.session.get('mode', ''):
                    request.session['lives'] -= 1
                    if request.session['lives'] <= 0:
                        return JsonResponse({
                            'result': 'game_over',
                            'score': request.session['score'],
                            'lives': 0  # Ensure lives is sent
                        })
                return JsonResponse({
                    'result': 'incorrect',
                    'score': request.session['score'],
                    'lives': request.session.get('lives'),  # Send updated lives
                    'time': current_time
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@csrf_exempt
def time_up(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            current_time = data.get('current_time', None)
            
            if 'time_attack' in request.session.get('mode', ''):
                return JsonResponse({
                    'result': 'game_over',
                    'score': request.session.get('score', 0),
                    'lives': 0  # Ensure lives is sent
                })
            elif 'survival' in request.session.get('mode', ''):
                request.session['lives'] -= 1
                if request.session['lives'] <= 0:
                    return JsonResponse({
                        'result': 'game_over',
                        'score': request.session.get('score', 0),
                        'lives': 0  # Ensure lives is sent
                    })
                return JsonResponse({
                    'result': 'timeout',
                    'lives': request.session['lives'],  # Send updated lives
                    'time': current_time
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@csrf_exempt
def time_up(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            current_time = data.get('current_time', None)
            
            if 'time_attack' in request.session.get('mode', ''):
                return JsonResponse({
                    'result': 'game_over',
                    'score': request.session.get('score', 0)
                })
            elif 'survival' in request.session.get('mode', ''):
                request.session['lives'] -= 1
                if request.session['lives'] <= 0:
                    return JsonResponse({
                        'result': 'game_over',
                        'score': request.session.get('score', 0)
                    })
                return JsonResponse({
                    'result': 'timeout',
                    'lives': request.session['lives'],
                    'time': current_time  # Return the same time for continuation
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def game_over(request):
    # Save the player's highest score to the database
    player = request.user
    final_score = request.session.get('score', 0)

    # Update the player's score only if the new score is higher

    if request.session['mode'] == 'survival':
        player.survival_score = max(player.survival_score, final_score)
    elif request.session['mode'] == 'time_attack':
        player.time_attack_score = max(player.time_attack_score, final_score)
    elif request.session['mode'] == 'hardcore_survival':
        player.hs_score = max(player.hs_score, final_score)
    elif request.session['mode'] == 'hardcore_time_attack':
        player.hta_score = max(player.hta_score, final_score)

    player.games_played += 1  # Increment the games played count
    player.save()  # Save the updated player data to the database

    # Clear the session data for the next game
    request.session['score'] = 0
    request.session['lives'] = 3

    # Render the game over screen
    return render(request, 'game/game_over.html', {
        'score': final_score
    })

@login_required
def practice_mode(request):
    question = random.choice(Question.objects.all())  # Get a random question
    return render(request, 'game/practice.html', {
        'question': question,
        'player': request.user.username,
    })

@csrf_exempt
def validate_practice_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_id = int(data.get('question_id'))
            user_command = data.get('user_command', '').strip()

            if not question_id or not user_command:
                return JsonResponse({'error': 'Missing or invalid question_id or user_command'}, status=400)

            question = Question.objects.get(id=question_id)
            if question.is_correct(user_command):
                return JsonResponse({'result': 'correct'})
            return JsonResponse({'result': 'incorrect'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)