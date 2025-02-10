from django.shortcuts import render, redirect  
from django.http import HttpResponse
from .forms import TopicForm
from .models import Question,UserResponse,Quiz,Point,Attempt,Global_Points
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist





@login_required
def home(request):
    if request.method == "POST":    
        form = TopicForm(request.POST)  
        return redirect('quiz',quiz_id=int(request.POST['quiz_id']))  

    else:  
        form = TopicForm()  
    return render(request,'quiz/home.html',{'form': form})  

@login_required
def quiz_topic(request):  
    if request.method == "POST":  
        form = TopicForm(request.POST)
        return redirect('/')  
          
    else:  
        form = TopicForm()  
    return render(request,'quiz/quiz_topic.html',{'form': form})  

qsn_ans={}

@login_required
def question_list(request,quiz_id):

    
    page_number = request.GET.get("page")
    quiz = Quiz.objects.get(quiz_id=quiz_id)
    page_obj=pagination_on_questions(quiz_id,page_number)
    
   
    if request.method=="POST":
        tmp=request.POST.dict()
        
        qsn_ans[tmp['question_id']]=tmp['option']
       
        if page_obj.has_next():
           
            next_page = page_obj.next_page_number()
            base_url = reverse('quiz', kwargs={'quiz_id': quiz_id}) 

            return redirect(f"{base_url}?page={next_page}")
       
        else :
            if request.user.is_authenticated:
                user_id = request.user.id
            
            attempt = Attempt.objects.filter(user_id=request.user, quiz_id=quiz).first()

            if attempt:
                total_attempt = attempt.number_of_attempt+1
            else:
                total_attempt = 1

            total_points=user_response(qsn_ans,request.user,quiz,total_attempt)
            print(total_points)

            
            update_points(request.user,quiz,total_attempt,total_points)     
            update_attempt(request.user,quiz,total_attempt,total_points)
            print(quiz_id)
            total_points=0
            qsn_ans.clear()
         

            return redirect('quiz-leaderboard',quiz_id=quiz_id)

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

    try:
        attempt = Attempt.objects.get(user_id=user, quiz_id=quiz)
        attempt.number_of_attempt = total_attempt
        
        if total_points > attempt.best_point:  
            Global_Points.objects.update(
                total_points=F('total_points') + (total_points - attempt.best_point)
            )

            attempt.best_point = total_points
            
        attempt.save()
        created = False
   
    except Attempt.DoesNotExist:
        Attempt.objects.create(
            user_id=user,
            quiz_id=quiz,
            number_of_attempt=total_attempt,
            best_point=total_points,
        ).save()
        try:
            global_points=Global_Points.objects.get(user_id=user) 
        except ObjectDoesNotExist:
            global_points = None  

        
        
        
        if  global_points is None:
            Global_Points.objects.create(
                    user_id=user,  
                    total_points=total_points
            ).save() 
        else :
            Global_Points.objects.update(
                total_points=F('total_points') + total_points
            )


             
               
def user_response(qsn_ans,user,quiz,total_attempt):
    
        total_points=0
        NEGITIVE_PENELTY=0.25

        points={
            'E':1,
            'M':2,
            'H':3,
            'X':4
        }

        for x in qsn_ans.keys():
            qsn=Question.objects.get(question_id=x)  
            correct_ans=qsn.correct_ans
            curr_ans=qsn_ans[x]

            if curr_ans==correct_ans:
                total_points+=points[qsn.quiz_id.difficulty_level]
            else :
                    total_points-=(points[qsn.quiz_id.difficulty_level]*(NEGITIVE_PENELTY))
                    print(total_points)
       
            UserResponse.objects.create(
                user_id=user.id,
                user_ans=curr_ans,
                question_id=qsn,
                question_response_time=10,
                quiz_id=quiz,
                attempt_number=total_attempt
            ).save()
            
        
        
        
        return total_points


def pagination_on_questions(quiz_id,page):
    questions=Question.objects.filter(quiz_id=quiz_id)
    paginator = Paginator(questions, 1) 
    page_number = page
    return paginator.get_page(page_number)
