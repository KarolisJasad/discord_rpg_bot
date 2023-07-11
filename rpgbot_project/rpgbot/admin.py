from django.contrib import admin
from .models import Player, CharacterClass, Enemy, Location, Item, EnemyInstance
# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'character_class', 'max_health', 'current_health', 'attack', 'defense', 'money', 'location')

@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ('class_type', 'health', 'attack', 'defense')

@admin.register(Enemy)
class StaticEnemyAdmin(admin.ModelAdmin):
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

@admin.register(EnemyInstance)
class EnemiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'enemy', 'current_health')
    list_display_links = ('id', 'enemy')  # Make the ID and enemy name clickable
    list_filter = ('enemy',)
    search_fields = ('enemy__name',)  # Enable searching by enemy name

    def current_health(self, obj):
        return obj.current_health  # Replace with the actual field representing current health

    current_health.short_description = 'Current Health'  # Customize the column header name
