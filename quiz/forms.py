from django import forms  
from .models import  Topic,Quiz
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.core.exceptions import ValidationError
 


from django import forms
from django.core.exceptions import ValidationError
from .models import Quiz

class TopicForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"  
        labels = {
            'quiz_id': 'Topic Name',
        }
        






















