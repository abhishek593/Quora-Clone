from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/<str:username>/', views.userProfile, name='profile'),
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('change-password/', views.changePassword, name='changePassword'),

]