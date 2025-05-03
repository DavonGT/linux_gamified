from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player

@admin.register(Player)
class PlayerAdmin(UserAdmin):
    model = Player
    list_display = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'student_id', 'year_level', 'survival_score', 'time_attack_score', 'ha_score', 'hta_score', 'games_played', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'year_level')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'middle_name', 'last_name', 'student_id', 'year_level')}),
        ('Game Stats', {'fields': ('survival_score', 'time_attack_score', 'ha_score', 'hta_score', 'games_played')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'middle_name', 'last_name', 'student_id', 'year_level', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('username', 'email', 'student_id')
    ordering = ('username',)
