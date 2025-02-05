from django.urls import path
# from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views as quiz_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('',PostListView.as_view(), name='quiz-home'),
    # path('post/<int:pk>/',PostDetailView.as_view(), name='quiz-detail'),
    # path('post/new/',PostCreateView.as_view(), name='quiz-create'),
    # path('post/<int:pk>/update/',PostUpdateView.as_view(), name='quiz-update'),
    # path('post/<int:pk>/delete/',PostDeleteView.as_view(), name='quiz-delete'),
    path('',quiz_views.home,name='quiz-home'),
    path('topic',quiz_views.quiz_topic,name='quiz-topic')
]