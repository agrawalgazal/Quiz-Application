from django.urls import path
from . import views as quiz_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',quiz_views.home,name='quiz-home'),
    path('topic/',quiz_views.quiz_topic,name='quiz-topic'),
    path('quiz/<int:quiz_id>', quiz_views.question_list, name='quiz'),
]