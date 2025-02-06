from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    city=forms.CharField( required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','city']



