from django.shortcuts import render
from quiz.models import Attempt,Global_Points
from django.contrib.auth.decorators import login_required



@login_required
def quiz_leaderboard(request,quiz_id):
  
    if not quiz_id:
        return render(request, 'leaderboard/leaderboard.html', {"error": "Quiz ID is required"})

    rank_list = Attempt.objects.filter(quiz_id=quiz_id).order_by('-best_point')

    return render(request, 'leaderboard/leaderboard.html', {'rank_list': rank_list})



def global_leaderboard(request):
    leaderboard_data = Global_Points.objects.all().order_by('-total_points') 

    return render(request, 'leaderboard/leaderboard.html', {'rank_list': leaderboard_data})

    

