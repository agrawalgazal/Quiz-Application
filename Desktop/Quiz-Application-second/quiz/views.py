from django.shortcuts import render, redirect  
from django.http import HttpResponse
from .forms import TopicForm
from .models import Question,UserResponse,Quiz,Point,Attempt
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
    # print(quiz_id)
    questions=Question.objects.filter(quiz_id=quiz_id)
    
    quiz = Quiz.objects.get(quiz_id=quiz_id)
    # quiz = Quiz.objects.get(name="harry porter") 
    print(quiz.quiz_id.quiz_id)


    if request.method=="POST":
        print("get the post method")
        tmp=request.POST.dict()
        print(tmp)
        print(request.POST.dict())
        leng=(len(tmp)-1)//2
        user_id=1
        if request.user.is_authenticated:
            user_id = request.user.id
            print(user_id)
        total_points=0
        points={
            'E':1,
            'M':2,
            'H':3,
            'X':4
        }
        for x in range(1,leng+1):
            cur_qsn=tmp[f"question_id_{x}"]
            qsn=Question.objects.get(question_id=cur_qsn)
            print(qsn.quiz_id.difficulty_level)
    
            correct_ans=qsn.correct_ans
    
            curr_ans=tmp[f"option_{x}"]

            if curr_ans==correct_ans:
                total_points+=points[qsn.quiz_id.difficulty_level]
            print(correct_ans,curr_ans)
            UserResponse.objects.create(
                user_id=request.user,
                user_ans=curr_ans,
                question_id=qsn,
                question_response_time=10,
                quiz_id=quiz
            ).save()
        print(total_points)
        attempt = Attempt.objects.filter(user_id=request.user, quiz_id=quiz).first()

        if attempt:
            total_attempt = attempt.number_of_attempt+1
        else:
            total_attempt = 1
        print(total_attempt)
        

        print("total attempts  are %d",total_attempt)
        Point.objects.create(
            user_id=request.user,
            quiz_id=quiz,
            attempt_number=total_attempt,
            quiz_time=1000,
            quiz_points=total_points
        )

        return redirect('quiz-home')

    return render(request, 'quiz/questions.html', {'question_form_list': questions})

