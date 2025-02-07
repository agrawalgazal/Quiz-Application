from django.shortcuts import render, redirect  
from django.http import HttpResponse
from .forms import TopicForm
from .models import Question,UserResponse,Quiz,Point,Attempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



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
    
    page_number = request.GET.get("page")
    quiz = Quiz.objects.get(quiz_id=quiz_id)
    page_obj=pagination_on_questions(quiz_id,page_number)
    
   
    if request.method=="POST":
       
        tmp=request.POST.dict()
        if request.user.is_authenticated:
            user_id = request.user.id
        
        attempt = Attempt.objects.filter(user_id=request.user, quiz_id=quiz).first()

        if attempt:
            total_attempt = attempt.number_of_attempt+1
        else:
            total_attempt = 1

        total_points=user_response(tmp,request.user,quiz,total_attempt)

        
        update_points(request.user,quiz,total_attempt,total_points)     
        update_attempt(request.user,quiz,total_attempt,total_points)

        return redirect('quiz-home')

    return render(request, 'quiz/questions.html', {"page_obj": page_obj})



def update_points(user,quiz,total_attempt,total_points):
    
    Point.objects.create(
            user_id=user,
            quiz_id=quiz,
            attempt_number=total_attempt,
            quiz_time=1000,
            quiz_points=total_points
        )
    
def update_attempt(user,quiz,total_attempt,total_points):

        attempt, created = Attempt.objects.update_or_create(
            user_id=user,  
            quiz_id=quiz,         
            defaults={
                'number_of_attempt': total_attempt, 
                'best_point': total_points           
            }
        )

        if not created :
            attempt.best_point = max(attempt.best_point, total_points)  
            attempt.save()
               
def user_response(tmp,user,quiz,total_attempt):
    
        total_points=0
        points={
            'E':1,
            'M':2,
            'H':3,
            'X':4
        }

        leng=(len(tmp)-1)//2
        for x in range(1,leng+1):
            cur_qsn=tmp[f"question_id_{x}"]
            qsn=Question.objects.get(question_id=cur_qsn)    
            correct_ans=qsn.correct_ans
            curr_ans=tmp[f"option_{x}"]

            if curr_ans==correct_ans:
                total_points+=points[qsn.quiz_id.difficulty_level]
            
            
            UserResponse.objects.create(
                user_id=user,
                user_ans=curr_ans,
                question_id=qsn,
                question_response_time=10,
                quiz_id=quiz
            ).save()
        
        return total_points


def pagination_on_questions(quiz_id,page):
    questions=Question.objects.filter(quiz_id=quiz_id)
    paginator = Paginator(questions, 1) 
    page_number = page
    return paginator.get_page(page_number)
       

     

