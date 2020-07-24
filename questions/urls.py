from django.urls import path, include
from . import views

app_name = 'questions'
urlpatterns = [
    path('home/', views.userFeed, name='feed'),
    path('all-users/', views.get_all_users, name='get_all_users'),
    path('home/ques/<str:question_title>/', views.get_question, name='question_card'),
    path('<str:username>/all_questions/', views.get_profile_questions, name='user_questions'),
    path('<str:username>/all_answers/', views.get_profile_answers, name='user_answers'),
]