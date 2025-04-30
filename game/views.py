from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question
import random
from django.views.decorators.csrf import csrf_exempt
import json
from accounts.models import Player
from django.db.models import Max


def test(request):
    # Test view to check if the server is running
    return render(request, 'game/test.html',)


@login_required
def dashboard(request):
    # Fetch the highest score for each player
    leaderboard_queryset = Player.objects.values('username').annotate(highest_score=Max('score')).order_by('-highest_score')[:10]
    
    # Add rank to each player
    leaderboard = [
        {'rank': idx + 1, 'username': entry['username'], 'score': entry['highest_score']}
        for idx, entry in enumerate(leaderboard_queryset)
    ]
    
    return render(request, 'game/dashboard.html', {
        'player': request.user,
        'leaderboard': leaderboard,  # Pass the leaderboard as a list of dictionaries
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
        else:
            request.session['lives'] = None  # No lives for time attack modes
        return redirect('game')
    return redirect('select_mode')  # Redirect to mode selection if invalid mode

@login_required
def game_view(request):
    # Set default time for time-based modes
    time = 20 if 'time_attack' in request.session['mode'] else None

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
        'score': request.session['score'],
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

            question = Question.objects.get(id=question_id)
            if question.is_correct(user_command):
                points = question.get_points()
                if 'hardcore' in request.session.get('mode', ''):
                    points += 10  # Bonus points for hardcore modes
                request.session['score'] = request.session.get('score', 0) + points
                return JsonResponse({'result': 'correct', 'score': request.session['score'], 'lives': request.session.get('lives')})
            else:
                if 'survival' in request.session.get('mode', ''):
                    request.session['lives'] -= 1
                    if request.session['lives'] <= 0:
                        return JsonResponse({'result': 'game_over', 'score': request.session['score'], 'lives': 0})
                return JsonResponse({'result': 'incorrect', 'score': request.session['score'], 'lives': request.session.get('lives')})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def time_up(request):
    if request.method == 'POST':
        if 'time_attack' in request.session.get('mode', ''):
            return JsonResponse({'result': 'timeout', 'score': request.session.get('score', 0)})
        elif 'survival' in request.session.get('mode', ''):
            request.session['lives'] -= 1
            if request.session['lives'] <= 0:
                return JsonResponse({'result': 'game_over', 'score': request.session.get('score', 0), 'lives': 0})
            return JsonResponse({'result': 'timeout', 'lives': request.session['lives']})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def game_over(request):
    # Save the player's highest score to the database
    player = request.user
    final_score = request.session.get('score', 0)

    # Update the player's score only if the new score is higher
    if final_score > player.score:
        player.score = final_score

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