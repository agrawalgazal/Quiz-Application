import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from users.models import UserProfile

@pytest.mark.django_db
def test_register_user():
    """Test user registration with a valid POST request."""
    client = Client()
    url = reverse('register')  

    body = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
        "city": "Mumbai"
    }

    response = client.post(url, data=body, follow=True)

    
    print(User.objects.count())
    assert response.status_code == 200  
    assert User.objects.filter(username="testuser").exists() 
    assert UserProfile.objects.filter(user__username="testuser", city="Mumbai").exists()  

@pytest.mark.django_db
def test_register_user_get():
    """Test user registration with a valid POST request."""
    client = Client()
    url = reverse('register')  

    body = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
        "city": "Mumbai"
    }

    response = client.get(url)

    
    # print(User.objects.count())
    assert response.status_code == 200  
    # assert User.objects.filter(username="testuser").exists() 
    # assert UserProfile.objects.filter(user__username="testuser", city="Mumbai").exists()  













import pytest
from django.contrib.auth.models import User
from users.models import UserProfile
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from users.validators import validate_city
@pytest.mark.django_db
def test_create_user():
    user=User.objects.create_user(username="testuser",password="testpassword")
    assert user.username=="testuser"
    assert user.is_active
    # assert user.is_staff
    # assert user.is_superuser
    assert user.check_password("testpassword")
@pytest.mark.django_db
def test_create_superuser(db):
    admin_user=User.objects.create_superuser(username="admin", password="adminpass")
    assert admin_user.is_superuser
    assert admin_user.is_staff
    assert admin_user.is_active
@pytest.mark.django_db
def test_authenticate_user(django_user_model):
    user = django_user_model.objects.create_user(username="authuser", password="securepass")
    assert user.check_password("securepass")
    assert not user.check_password("wrongpass")
@pytest.mark.django_db
def test_username_uniqueness():
    User.objects.create_user(username="uniqueuser", password="password123")
    with pytest.raises(IntegrityError):
        User.objects.create_user(username="uniqueuser", password="anotherpass")
@pytest.mark.django_db
def test_password_is_hashed():
    user = User.objects.create_user(username="hashuser", password="plaintextpassword")
    assert user.password != "plaintextpassword"
    assert user.check_password("plaintextpassword")
@pytest.mark.django_db
def test_user_profile_creation():
    user = User.objects.create_user(username="testuser", password="testpassword")
    profile = UserProfile.objects.create(user=user, city="Nagpur")
    assert profile.user==user
    assert profile.city=="Nagpur"
    assert str(profile)=="testuser"
# Valid city names
@pytest.mark.parametrize("city", [
   "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego",
    "Dallas", "San Jose", "Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa", "Mexico City", "Guadalajara",
    "Monterrey", "Tijuana", "Leon", "Quebec City", "Edmonton", "Winnipeg", "Boston", "Seattle", "Denver",
    "Las Vegas", "San Francisco", "Miami", "Orlando", "Washington D.C.", "Atlanta", "Charlotte", "Detroit",
    "São Paulo", "Buenos Aires", "Lima", "Bogotá", "Santiago", "Caracas", "Medellín", "Quito",
    "London", "Paris", "Berlin", "Madrid", "Rome", "Amsterdam", "Lisbon", "Vienna", "Athens", "Brussels",
    "Lagos", "Cairo", "Johannesburg", "Cape Town", "Nairobi", "Casablanca", "Accra", "Addis Ababa",
    "Tokyo", "Seoul", "Beijing", "Shanghai", "Hong Kong", "Bangkok", "Jakarta", "Manila", "Singapore", "Taipei",
    "Kuala Lumpur", "Hanoi", "Ho Chi Minh City", "Dubai", "Abu Dhabi", "Riyadh", "Jeddah", "Doha", "Tehran",
    # All Cities in India
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur",
    "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna",
    "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli",
    "Vasai-Virar", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad",
    "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Raipur",
    "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubballi-Dharwad", "Bareilly", "Moradabad", "Mysore", "Gurgaon",
    "Aligarh", "Jalandhar", "Tiruchirappalli", "Bhubaneswar", "Salem", "Mira-Bhayandar", "Thiruvananthapuram",
    "Bhiwandi", "Saharanpur", "Gorakhpur", "Guntur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai",
    "Cuttack", "Firozabad", "Kochi", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Nanded", "Kolhapur",
    "Ajmer", "Akola", "Ujjain", "Tirunelveli", "Belgaum", "Jhansi", "Udaipur", "Siliguri", "Jammu", "Sangli",
    "Bokaro Steel City", "Nellore", "Mangalore", "Tiruppur", "Gaya", "Tirupati", "Shimoga", "Tumkur", "Hosur",
    "Kurnool", "Gandhinagar", "Gandhidham", "Erode", "Pondicherry", "Kollam", "Sagar", "Bardhaman", "Kharagpur",
    "Karimnagar", "Rajahmundry", "Bhusawal", "Hindupur", "Ratlam", "Hazaribagh", "Dhule", "Ambur", "Nizamabad",
    "Chittoor", "Bettiah", "Gangtok", "Shillong", "Aizawl", "Imphal", "Itanagar", "Kohima", "Dimapur",
    "Agartala", "Port Blair", "Panaji", "Margoa", "Puducherry", "Daman", "Silvassa", "Gangtok", "Aizawl",
    "Churu", "Fatehpur", "Dausa", "Gorakhpur", "Jalgaon", "Bilaspur", "Sagar", "Rewa", "Satna", "Bhilwara",
    "Raichur", "Hospet", "Kakinada", "Anantapur", "Bellary", "Hapur", "Shahjahanpur", "Rampur", "Mirzapur",
    "Munger", "Katihar", "Begusarai", "Purnia", "Bhagalpur", "Muzaffarpur", "Gopalganj", "Darbhanga",
    "Arrah", "Bettiah", "Motihari", "Chapra", "Saharsa", "Madhepura", "Supaul", "Sitamarhi", "Samastipur",
    "Siwan", "Vaishali", "Hajipur", "Nalanda", "Buxar", "Jehanabad", "Gaya", "Aurangabad", "Navsari",
    "Porbandar", "Bhuj", "Junagadh", "Jamnagar", "Surendranagar", "Bhavnagar", "Gandhidham", "Mehsana",
    "Anand", "Valsad", "Vapi", "Dahod", "Godhra", "Palanpur", "Morbi", "Modasa", "Amreli", "Gondal", "Botad",
    "Gariadhar", "Una", "Veraval", "Chhatarpur", "Datia", "Tikamgarh", "Sehore", "Vidisha", "Dhar", "Shivpuri",
    "Ashoknagar", "Raisen", "Dewas", "Hoshangabad", "Betul", "Itarsi", "Seoni", "Mandla", "Chhindwara",
    "Balaghat", "Jhabua", "Barwani", "Ratlam", "Mandsaur", "Neemuch", "Bharuch", "Karwar", "Hassan", "Mandya",
    "Chikmagalur", "Davanagere", "Gadag", "Bagalkot", "Haveri", "Dharwad", "Raichur", "Koppal", "Bijapur",
    "Chamarajanagar", "Udupi", "Karwar", "Madikeri", "Bidar", "Gulbarga", "Yadgir", "Shimoga", "Tumkur",
    "Chitradurga", "Chikkaballapur", "Ramanagara", "Chikmagalur", "Belthangady", "Karkala", "Puttur",
    "Sullia", "Sakleshpur", "Arsikere", "Tiptur", "Kundapura", "Sirsi", "Honnavar", "Ankola", "Dandeli",
    "Hubli", "Bhatkal", "Byndoor", "Ullal", "Mangalore", "Bantwal", "Moodbidri", "Mulki", "Kaup", "Udupi",
    "Karkala", "Padubidri", "Haliyal", "Supa", "Sirsi", "Mundgod", "Yellapur", "Ankola", "Karwar"
]
)
def test_valid_city(city):
        validate_city(city)
# Invalid city names
@pytest.mark.parametrize("city", [
    "Atlantis", "Gotham", "Springfield", "Metropolis", "Wakanda"
])
def test_invalid_city(city):
    with pytest.raises(ValidationError, match="Invalid city name. Please enter a valid city."):
        validate_city(city)
# City name exceeding 100 characters
def test_city_name_exceeds_limit():
    long_city_name = "A" * 101  # 101 characters long
    with pytest.raises(ValidationError, match="City name exceeded maximum limit."):
        validate_city(long_city_name)
# Case Insensitivity Check
@pytest.mark.parametrize("city", [
    "mumbai", "delhi", "new york", "london", "tokyo", "bangalore", "dubai"
])
def test_city_case_insensitivity(city):
        validate_city(city)
import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from quiz.models import Topic, Quiz, Question, UserResponse, Point, Attempt, Global_Points
from quiz.validators import validate_levels, validate_attempt, validate_question_response_time, validate_topic_name, validate_user_answer
@pytest.mark.django_db
def test_topic_creation():
    topic = Topic.objects.create(topic_name="Python Basics", rating=4.5, difficulty_level='M')
    assert topic.topic_name == "Python Basics"
    assert topic.rating == 4.5
    assert topic.difficulty_level == 'M'
    assert str(topic)=="Python Basics"
@pytest.mark.django_db
def test_topic_rating_validation():
    topic = Topic(topic_name="Python Advanced", rating=6.0, difficulty_level='H')
    with pytest.raises(ValidationError):
        topic.full_clean()
@pytest.mark.django_db
def test_quiz_creation():
    topic = Topic.objects.create(topic_name="Python Basics", rating=4.5, difficulty_level='E')
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=75.50)
    assert quiz.quiz_accuracy == 75.50
    assert quiz.quiz_id.topic_name == "Python Basics"
    assert str(quiz)=="Python Basics"
@pytest.mark.django_db
def test_question_creation():
    topic = Topic.objects.create(topic_name="Python Basics", rating=4.5, difficulty_level='E')
    question = Question.objects.create(
        quiz_id=topic,
        question="What is Python?",
        optionA="Language",
        optionB="Snake",
        optionC="Framework",
        optionD="IDE",
        correct_ans="Language"
    )
    assert question.correct_ans == "Language"
    assert str(question) == "What is Python?"
@pytest.mark.django_db
def test_user_response_creation():
    user = User.objects.create(username="testuser")
    topic = Topic.objects.create(topic_name="Python Basics", rating=4.5, difficulty_level='E')
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=85.0)
    question = Question.objects.create(
        quiz_id=topic,
        question="What is Python?",
        optionA="Language",
        optionB="Snake",
        optionC="Framework",
        optionD="IDE",
        correct_ans="Language"
    )
    response = UserResponse.objects.create(
        user=user, quiz_id=quiz, question_id=question,
        user_ans="Language", question_response_time=10, attempt_number=1
    )
    assert response.user_ans == "Language"
    assert response.question_id.question == "What is Python?"
    assert str(response) == "What is Python?  response is Language"
@pytest.mark.django_db
def test_point_creation():
    user = User.objects.create(username="testuser")
    topic = Topic.objects.create(topic_name="Python Basics", rating=4.5, difficulty_level='E')
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=85.0)
    point = Point.objects.create(user_id=user, quiz_id=quiz, attempt_number=1, quiz_points=10.5, quiz_time=50)
    assert point.quiz_points == 10.5
    assert point.user_id.username == "testuser"
    assert str(point) == "testuser"
@pytest.mark.django_db
def test_attempt_creation():
    user = User.objects.create(username="testuser")
    topic = Topic.objects.create(topic_name="Python Basics", rating=4.5, difficulty_level='E')
    quiz = Quiz.objects.create(quiz_id=topic, quiz_accuracy=85.0)
    attempt = Attempt.objects.create(user_id=user, quiz_id=quiz, number_of_attempt=3, best_point=20.0)
    assert attempt.number_of_attempt == 3
    assert attempt.best_point == 20.0
    assert str(attempt) == "testuser"
@pytest.mark.django_db
def test_global_points_creation():
    user = User.objects.create(username="testuser")
    global_points = Global_Points.objects.create(user_id=user, total_points=150.0)
    assert global_points.total_points == 150.0
def test_validate_levels():
    validate_levels('E')  # Should not raise an error
    with pytest.raises(ValidationError):
        validate_levels('A')
def test_validate_user_answer():
    validate_user_answer("Valid Answer")  # Should not raise an error
    with pytest.raises(ValidationError):
        validate_user_answer("A" * 201)
def test_validate_topic_name():
    validate_topic_name("MathM")  # Should not raise an error
    with pytest.raises(ValidationError):
        validate_topic_name("MathX")
def test_validate_question_response_time():
    validate_question_response_time(25)  # Should not raise an error
    with pytest.raises(ValidationError):
        validate_question_response_time(35)
def test_validate_attempt():
    validate_attempt(1)  # Should not raise an error
    with pytest.raises(ValidationError):
        validate_attempt(-1)


@pytest.mark.django_db
def test_get_user_city_try():
    # Step 1: Create a user
    user = User.objects.create_user(username='testuser', password='password')

    # Step 2: Create a UserProfile associated with the user, including a city
    city = 'New York'
    user_profile = UserProfile.objects.create(user=user, city=city)

    # Step 3: Call the getusercity method
    result = user_profile.getusercity()

    # Step 4: Assert that the method returns the correct city
    assert result == city, f"Expected {city}, but got {result}"

    # csrf token ohGjiagRp4zcXR9cjPEJLqY0nPucCVkT