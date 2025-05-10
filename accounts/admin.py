from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player

@admin.register(Player)
class PlayerAdmin(UserAdmin):
    model = Player
    list_display = ('username', 'email', 'survival_score', 'time_attack_score', 'ha_score', 'hta_score', 'games_played', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Game Stats', {'fields': ('survival_score', 'time_attack_score', 'ha_score', 'hta_score', 'games_played')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
