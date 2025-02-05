from django import forms  
from .models import Quiz  


class TopicForm(forms.ModelForm):
    class Meta:
        model =  Quiz
        fields = "__all__"  




