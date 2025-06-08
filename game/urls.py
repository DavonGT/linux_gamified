from django.urls import path
from . import views

urlpatterns = [
    path('select_mode/', views.select_mode, name='select_mode'),
    path('', views.dashboard, name='dashboard'),
    path('set_mode/<str:mode>/', views.set_mode, name='set_mode'),
    path('game/', views.game_view, name='game'),
    path('update_hint_index/', views.update_hint_index, name='update_hint_index'),
    path('validate/', views.validate_answer, name='validate_answer'),
    path('time_up/', views.time_up, name='time_up'),  # New route for time up logic
    path('game_over/', views.game_over, name='game_over'),
    path('practice/', views.practice_mode, name='practice_mode'),
    path('validate_practice_answer/', views.validate_practice_answer, name='validate_practice_answer'),
    path('story_mode/', views.story_mode, name='story_mode'),
]