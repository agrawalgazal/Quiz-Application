import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from quiz.models import Quiz,Topic,Question,Attempt,Global_Points,Point,UserResponse
from quiz.forms import TopicForm


from django.core.exceptions import ValidationError
from quiz.validators import validate_levels, validate_user_answer, validate_topic_name, validate_question_response_time, validate_attempt


@pytest.mark.django_db
def test_home_get_request(client):
    
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    response = client.get(reverse('quiz-home'))  

    assert response.status_code == 200




@pytest.mark.django_db
def test_home_post_valid_submission(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)
    

    response = client.post(reverse("quiz-home"), {
        "quiz_id": topic.quiz_id,
        "difficulty-level": "E"  
    })

    assert response.status_code == 302 
    assert response.url == reverse("quiz", kwargs={"quiz_id": topic.quiz_id})


@pytest.mark.django_db
def test_home_post_valid_submission_wrong_level(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)
    

    response = client.post(reverse("quiz-home"), {
        "quiz_id": topic.quiz_id,
        "difficulty-level": "M"  
    })

    assert response.status_code == 302 



@pytest.mark.django_db
def test_question_list_get_request(client):
    # Create and login a test user
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Create Topic
    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    # Create Quiz linked to the topic
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    for i in range(1, 6):  # Creating 5 questions
        Question.objects.create(
            quiz_id=topic,
            question=f"Sample question {i}?",
            optionA="A",
            optionB="B",
            optionC="C",
            optionD="D",
            correct_ans="A"
        )

    # Make GET request (first page)
    response = client.get(reverse("quiz", kwargs={"quiz_id": topic.quiz_id}), {"page": 1})

    # Assertions
    assert response.status_code == 200  # Successful response


@pytest.mark.django_db
def test_quiz_post_request(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Create Topic
    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    # Create Quiz linked to the topic
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    for i in range(1, 6):  # Creating 5 questions
        Question.objects.create(
            quiz_id=topic,
            question=f"Sample question {i}?",
            optionA="A",
            optionB="B",
            optionC="C",
            optionD="D",
            correct_ans="A"
        )

    response = client.post(reverse("quiz", kwargs={"quiz_id": topic.quiz_id}), {
        "question_id": 1,
        "option": "A"
    })

    assert response.status_code == 302





@pytest.mark.django_db
def test_quiz_post_request_page_last(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Create Topic
    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    # Create Quiz linked to the topic
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    for i in range(1, 2):  # Creating 5 questions
        Question.objects.create(
            quiz_id=topic,
            question=f"Sample question {i}?",
            optionA="A",
            optionB="B",
            optionC="C",
            optionD="D",
            correct_ans="A"
        )

    response = client.post(reverse("quiz", kwargs={"quiz_id": topic.quiz_id}), {
        "question_id": 1,
        "option": "A"
    })

    assert response.status_code == 302


@pytest.mark.django_db
def test_quiz_post_request_page_last_wrong(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Create Topic
    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    # Create Quiz linked to the topic
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    for i in range(1, 2):  # Creating 5 questions
        Question.objects.create(
            quiz_id=topic,
            question=f"Sample question {i}?",
            optionA="A",
            optionB="B",
            optionC="C",
            optionD="D",
            correct_ans="A"
        )

    response = client.post(reverse("quiz", kwargs={"quiz_id": topic.quiz_id}), {
        "question_id": 1,
        "option": "B"
    })

    assert response.status_code == 302

@pytest.mark.django_db
def test_quiz_post_request_cur_pnt_total_pnt(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Create Topic
    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    # Create Quiz linked to the topic
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    for i in range(1, 2):  # Creating 5 questions
        Question.objects.create(
            quiz_id=topic,
            question=f"Sample question {i}?",
            optionA="A",
            optionB="B",
            optionC="C",
            optionD="D",
            correct_ans="A"
        )

    
    Attempt.objects.create(user_id=user,quiz_id=quiz,number_of_attempt=1,best_point=-9)
    Global_Points.objects.create(user_id=user,total_points=0)

    response = client.post(reverse("quiz", kwargs={"quiz_id": topic.quiz_id}), {
        "question_id": 1,
        "option": "A"
    })


@pytest.mark.django_db
def test_quiz_post_request_cur_pnt_total_pnt_glb_else(client):
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Create Topic
    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    # Create Quiz linked to the topic
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    for i in range(1, 2):  # Creating 5 questions
        Question.objects.create(
            quiz_id=topic,
            question=f"Sample question {i}?",
            optionA="A",
            optionB="B",
            optionC="C",
            optionD="D",
            correct_ans="A"
        )

    
    # Attempt.objects.create(user_id=user,quiz_id=quiz,number_of_attempt=1,best_point=-9)
    Global_Points.objects.create(user_id=user,total_points=0)

    response = client.post(reverse("quiz", kwargs={"quiz_id": topic.quiz_id}), {
        "question_id": 1,
        "option": "A"
    })



@pytest.mark.django_db
def test_quiz_history_get(client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    response = client.get(reverse('quizhistory'))  

    assert response.status_code == 200


@pytest.mark.django_db
def test_quiz_history_post(client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)

    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    response = client.post(reverse("quizhistory"), {
        "quiz_id": topic.quiz_id,
        "difficulty-level": "E"  
    })

    assert response.status_code == 302 

@pytest.mark.django_db
def test_quiz_history_table(client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)
    points=Point.objects.create(user_id=user,quiz_id=quiz,attempt_number=1,quiz_points=3,quiz_time=30)


    response = client.get(reverse("quiz_history_table", kwargs={"quiz_id": 1}))
    assert response.status_code == 200 




@pytest.mark.django_db
def test_quiz_history_table_no_record(client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)

    response = client.get(reverse("quiz_history_table", kwargs={"quiz_id": quiz.quiz_id.quiz_id}))

    assert 200


@pytest.mark.django_db
def test_view_attempt_response(client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')

    topic = Topic.objects.create(quiz_id=1, topic_name="historyE", difficulty_level="E", rating=2.0)
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=30.0)
    q=Question.objects.create(
            quiz_id=topic,
            question=f"Sample question?",
            optionA="A",
            optionB="B",
            optionC="C",
            optionD="D",
            correct_ans="A"
        )
    points = Point.objects.create(user_id=user, quiz_id=quiz, attempt_number=1, quiz_points=3, quiz_time=30)

    UserResponse.objects.create(
        user_id=user.id,
        quiz_id=quiz,
        question_id=q,
        question_response_time=10,
        user_ans="a",
        attempt_number=1
    )


    response = client.get(reverse("view_attempt_response", kwargs={"quiz_id": quiz.quiz_id.quiz_id,"attempt_number":1}))
    assert response.status_code == 200 


def test_validate_levels_valid():
        validate_levels('E')
        validate_levels('M')
        validate_levels('H')
        validate_levels('X')

def test_validate_levels_invalid():
    with pytest.raises(ValidationError):
        validate_levels('A')

    with pytest.raises(ValidationError):
        validate_levels('Z')

    with pytest.raises(ValidationError):
        validate_levels('123')
def test_validate_user_answer_valid():
    # Test valid answer length
        validate_user_answer("A valid answer")

def test_validate_user_answer_invalid():
    # Test invalid answer length (> 200 characters)
    long_answer = "A" * 201  # Answer longer than 200 characters
    with pytest.raises(ValidationError):
        validate_user_answer(long_answer)
def test_validate_topic_name_valid():
    # Test valid topic name ending
        validate_topic_name("HistoryE")
        validate_topic_name("MathM")
        validate_topic_name("ScienceH")

def test_validate_topic_name_invalid():
    # Test invalid topic name ending
    with pytest.raises(ValidationError):
        validate_topic_name("HistoryX")

    with pytest.raises(ValidationError):
        validate_topic_name("MathZ")
def test_validate_question_response_time_valid():
    # Test valid response times (<= 30 seconds)
        validate_question_response_time(30)
        validate_question_response_time(10)

def test_validate_question_response_time_invalid():
    # Test invalid response time (> 30 seconds)
    with pytest.raises(ValidationError):
        validate_question_response_time(31)
    
    with pytest.raises(ValidationError):
        validate_question_response_time(100)
def test_validate_attempt_valid():
    # Test valid attempt values (>= 0)
        validate_attempt(0)
        validate_attempt(1)

def test_validate_attempt_invalid():
    # Test invalid attempt values (< 0)
    with pytest.raises(ValidationError):
        validate_attempt(-1)

    with pytest.raises(ValidationError):
        validate_attempt(-100)
