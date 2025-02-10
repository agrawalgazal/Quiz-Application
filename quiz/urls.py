from django.urls import path
from . import views as quiz_views
from leaderboard import views as leaderboard_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',quiz_views.home,name='quiz-home'),
    path('topic/',quiz_views.quiz_topic,name='quiz-topic'),
    path('quiz/<int:quiz_id>', quiz_views.question_list, name='quiz'), 
    path('quizhistory/',quiz_views.quiz_history,name='quizhistory'),
    path('quiz_history_table/<int:quiz_id>',quiz_views.quiz_history_table,name='quiz_history_table'),
    path('view_attempt_response/<int:quiz_id>/<int:attempt_number>',quiz_views.view_attempt_response,name='view_attempt_response'),
]