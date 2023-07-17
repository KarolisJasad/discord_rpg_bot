from django.views import View
from django.shortcuts import render

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class LeaderboardView(View):
    def get(self, request):
        return render(request, 'leaderboard.html')

class ItemsView(View):
    def get(self, request):
        return render(request, 'items.html')