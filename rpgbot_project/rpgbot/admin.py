from django.contrib import admin
from .models import Player, CharacterClass, Enemy, Location, Item, EnemyInstance, Shop
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
    list_display = ('name', 'description', 'enemies')

    def enemies(self, obj):
        return ', '.join([enemy.name for enemy in obj.enemy.all()])

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'attack', 'defense', 'health')

@admin.register(EnemyInstance)
class EnemiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'enemy', 'current_health')
    list_filter = ('enemy',)
    search_fields = ('enemy__name',)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name',)




