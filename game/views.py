from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import random
from .models import Question
from accounts.models import Player
from django.db import models
from .constants import (
    SURVIVAL_MODE, TIME_ATTACK_MODE, 
    HARDCORE_SURVIVAL_MODE, HARDCORE_TIME_ATTACK_MODE,
    PRACTICE_MODE, GAME_MODES
)
from .utils import (
    initialize_game_session, clear_game_session,
    get_session_score, get_session_lives, get_session_time,
    update_session_score, decrement_session_lives
)

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
    if mode in GAME_MODES:
        initialize_game_session(request.session, mode)
        return redirect('game')
    elif mode == PRACTICE_MODE:
        return redirect('practice_mode')
    return redirect('select_mode')

@login_required
def game_view(request):
    
    # Ensure the mode is set before starting the game
    if 'mode' not in request.session:
        return redirect('select_mode')

    # Handle timing for time-based modes
    time = get_session_time(request.session)
    lives = get_session_lives(request.session)
    mode = request.session['mode']
    score = get_session_score(request.session)

    # Check for game over conditions
    if (mode in [SURVIVAL_MODE, HARDCORE_SURVIVAL_MODE] and lives <= 0):
        return redirect('game_over')

    # Get a random question
    question = random.choice(Question.objects.all())

    context = {
        'time': time,
        'question': question,
        'survival_score': score if mode == SURVIVAL_MODE else 0,
        'time_attack_score': score if mode == TIME_ATTACK_MODE else 0,
        'ha_score': score if mode == HARDCORE_SURVIVAL_MODE else 0,
        'hta_score': score if mode == HARDCORE_TIME_ATTACK_MODE else 0,
        'lives': lives,
        'mode': mode,
        'player': request.user.username,
    }
    
    return render(request, 'game/game.html', context)

@csrf_exempt
def validate_answer(request):
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    try:
        # Parse request data
        data = json.loads(request.body)
        question_id = data.get('question_id')
        user_command = data.get('user_command')
        current_time = data.get('current_time')
        
        if not all([question_id, user_command]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Update session time
        request.session['time'] = current_time
        
        # Get and validate question
        question = Question.objects.get(id=question_id)
        if question.is_correct(user_command):
            # Calculate points and update score
            points = question.get_points()
            if 'hardcore' in request.session.get('mode', ''):
                points += 10
            update_session_score(request.session, points)
            
            return JsonResponse({
                'result': 'correct',
                'score': get_session_score(request.session),
                'time': current_time,
                'lives': get_session_lives(request.session)
            })
        else:
            # Handle incorrect answer
            if 'survival' in request.session.get('mode', ''):
                lives = decrement_session_lives(request.session)
                if lives is not None and lives <= 0:
                    return JsonResponse({
                        'result': 'game_over',
                        'score': get_session_score(request.session),
                        'lives': 0
                    })
            
            return JsonResponse({
                'result': 'incorrect',
                'score': get_session_score(request.session),
                'lives': get_session_lives(request.session),
                'time': current_time
            })
            
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        data = json.loads(request.body)
        current_time = data.get('current_time')
        mode = request.session.get('mode', '')
        
        # Handle time attack modes
        if 'time_attack' in mode:
            return JsonResponse({
                'result': 'game_over',
                'score': get_session_score(request.session)
            })
            
        # Handle survival modes
        elif 'survival' in mode:
            lives = decrement_session_lives(request.session)
            
            if lives is not None and lives <= 0:
                return JsonResponse({
                    'result': 'game_over',
                    'score': get_session_score(request.session)
                })
                
            return JsonResponse({
                'result': 'timeout',
                'lives': lives,
                'time': current_time
            })
            
        return JsonResponse({'error': 'Invalid game mode'}, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def game_over(request):
    player = request.user
    final_score = get_session_score(request.session)
    mode = request.session.get('mode')

    # Update the player's high score if current score is higher
    if mode == SURVIVAL_MODE:
        player.survival_score = max(player.survival_score, final_score)
    elif mode == TIME_ATTACK_MODE:
        player.time_attack_score = max(player.time_attack_score, final_score)
    elif mode == HARDCORE_SURVIVAL_MODE:
        player.ha_score = max(player.ha_score, final_score)
    elif mode == HARDCORE_TIME_ATTACK_MODE:
        player.hta_score = max(player.hta_score, final_score)

    # Update games played and save
    player.games_played += 1
    player.save()

    # Clear game session
    clear_game_session(request.session)

    return render(request, 'game/game_over.html', {'score': final_score})

@login_required
def practice_mode(request):
    question = random.choice(Question.objects.all())
    return render(request, 'game/practice.html', {
        'question': question,
        'player': request.user.username,
    })

@csrf_exempt
def validate_practice_answer(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        data = json.loads(request.body)
        question_id = int(data.get('question_id'))
        user_command = data.get('user_command', '').strip()

        if not question_id or not user_command:
            return JsonResponse(
                {'error': 'Missing or invalid question_id or user_command'}, 
                status=400
            )

        question = Question.objects.get(id=question_id)
        return JsonResponse({
            'result': 'correct' if question.is_correct(user_command) else 'incorrect'
        })
        
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid input format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)