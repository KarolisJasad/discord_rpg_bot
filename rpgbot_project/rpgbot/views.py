from django.views import View
from django.shortcuts import render
from .models import Player, Item
from django.db.models import F

class AboutView(View):
    def get(self, request):
        return render(request, 'rpgbot/about.html')

class LeaderboardView(View):
    def get(self, request):
        players = Player.objects.order_by('-level')
        return render(request, 'rpgbot/leaderboard.html', {'players': players})

class ItemsView(View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'rpgbot/items.html', {'items': items})

class StatsExplanationView(View):
    def get(self, request):
        return render(request, 'rpgbot/stats.html')
