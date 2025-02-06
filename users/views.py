from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            UserProfile.objects.create(
                user=user,
                city=form.cleaned_data['city']
            )
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import UserRegisterForm 
# from .models import UserProfile

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         print(form)
#         print(form.cleaned_data if form.is_valid() else form.errors)  # Print cleaned data or errors


#         if form.is_valid():
#             user=form.save() 
#             UserProfile.objects.create(
#                 user=user,
#                 city=form.cleaned_data['city']
#             )
#             return redirect('home') 
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

