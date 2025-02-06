from django.shortcuts import render, redirect  
from django.http import HttpResponse
from .forms import TopicForm,UserResponseForm
from .models import Question,UserResponse,Quiz
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    if request.method == "POST":    
        form = TopicForm(request.POST)  
        print(int(request.POST['quiz_id']))
        return redirect('quiz',quiz_id=int(request.POST['quiz_id']))  

    else:  
        form = TopicForm()  
    return render(request,'quiz/home.html',{'form': form})  

@login_required
def quiz_topic(request):  
    if request.method == "POST":  
        form = TopicForm(request.POST)
        print(request.POST)
        return redirect('/')  
          
    else:  
        form = TopicForm()  
    return render(request,'quiz/quiz_topic.html',{'form': form})  

@login_required
def question_list(request,quiz_id):
    print(quiz_id)
    questions=Question.objects.filter(topic_id=quiz_id)
    
    quiz = Quiz.objects.get(quiz_id=quiz_id)
    # quiz = Quiz.objects.get(name="harry porter") 
    print(quiz.quiz_id.quiz_id)


    if request.method=="POST":
        print("get the post method")
        tmp=request.POST.dict()
        print(request.POST.dict())
        leng=(len(tmp)-1)//2
        user_id=1
        if request.user.is_authenticated:
            user_id = request.user.id
            print(user_id)

        for x in range(1,leng+1):
            cur_qsn=tmp[f"question_id_{x}"]
            qsn=Question.objects.get(question_id=cur_qsn)
            cur_res=tmp[f"option_{x}"]
            print(cur_qsn,cur_res)
            UserResponse.objects.create(
                user_id=request.user,
                user_ans=cur_res,
                question_id=qsn,
                question_response_time=10,
                quiz_id=quiz
            ).save()

        return redirect('quiz-home')
   

    return render(request, 'quiz/questions.html', {'question_form_list': questions})

    





