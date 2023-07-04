from django.contrib import admin
from .models import Player, CharacterClass, Enemy, Location, Item
# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'character_class', 'max_health', 'current_health', 'attack', 'defense', 'money', 'location')

@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ('class_type', 'health', 'attack', 'defense')

@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_health', 'current_health', 'attack', 'defense')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'display_enemies')

    def display_enemies(self, obj):
        return ', '.join([enemy.name for enemy in obj.enemy.all()])

    display_enemies.short_description = 'Enemies'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'attack', 'defense', 'health')