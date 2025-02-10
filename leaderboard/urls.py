from django.urls import path, include
from .views import quiz_leaderboard,global_leaderboard


urlpatterns = [
      path('quiz/<int:quiz_id>/', quiz_leaderboard, name='quiz-leaderboard'),
      path('',global_leaderboard,name='global_leaderboard')
]

