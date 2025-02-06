from django import forms  
from .models import  Topic,Quiz,UserResponse
from django.contrib.auth.models import User
from django.views.generic import ListView


class TopicForm(forms.ModelForm):
    class Meta:
        model =  Quiz
        fields = "__all__"  


class UserResponseForm(forms.ModelForm):
    selected_option = forms.ChoiceField(choices=[], widget=forms.RadioSelect) 
    class Meta:
        model=UserResponse
        fields = ['selected_option']








