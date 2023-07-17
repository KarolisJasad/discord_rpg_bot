from django.contrib import admin
from django.urls import path
from rpgbot.views import AboutView, LeaderboardView, ItemsView

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('items/', ItemsView.as_view(), name='items'),
]