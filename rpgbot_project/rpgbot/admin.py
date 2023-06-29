from django.contrib import admin
from .models import Player, CharacterClass, Enemy
# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'character_class', 'max_health', 'current_health', 'attack', 'defense', 'money')

@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ('class_type', 'health', 'attack', 'defense')

@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_health', 'current_health', 'attack', 'defense')