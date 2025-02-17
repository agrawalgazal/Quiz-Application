import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from quiz.models import Quiz,Topic,Question,Attempt,Global_Points,Point,UserResponse



@pytest.mark.django_db
def test_quiz_leaderboard(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Create Topic
    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    # Create Quiz linked to the topic
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    
    Attempt.objects.create(user_id=user,quiz_id=quiz,number_of_attempt=1,best_point=-9)
    response = client.get(reverse("quiz-leaderboard", kwargs={"quiz_id": 1}))

@pytest.mark.django_db
def test_global_leaderboard(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    Global_Points.objects.create(user_id=user,total_points=0)
    response = client.get(reverse("global_leaderboard"))






