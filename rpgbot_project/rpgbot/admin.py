from django.contrib import admin
from .models import Player, CharacterClass
# Register your models here.

@admin.register(Player)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('username', 'character_class')

@admin.register(CharacterClass)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('class_type',)