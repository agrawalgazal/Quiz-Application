from django.shortcuts import render, redirect  
from django.http import HttpResponse
from .forms import TopicForm  

def home(request):
    return render(request, 'quiz/home.html')

def quiz_topic(request):  
    if request.method == "POST":  
        form = TopicForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/')  
            except:  
                pass  
    else:  
        form = TopicForm()  
    return render(request,'quiz/quiz_topic.html')  
