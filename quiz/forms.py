from django import forms  
from .models import  Topic,Quiz
from django.contrib.auth.models import User
from django.views.generic import ListView


class TopicForm(forms.ModelForm):
    class Meta:
        model =  Quiz
        fields = "__all__"  
        labels = {
            'quiz_id': 'Topic Name',
        }











