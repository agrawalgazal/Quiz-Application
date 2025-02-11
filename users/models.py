from django.db import models
from django.contrib.auth.models import User
from .validators import validate_city


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=100,validators=[validate_city]) 

    def __str__(self):
        return self.user.username
    