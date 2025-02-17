# users/factories.py
import factory
from faker import Faker
from django.contrib.auth.models import User
from users.models import UserProfile

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    password = fake.password()

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    city = "Ahmedabad"
