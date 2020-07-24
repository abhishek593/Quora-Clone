from django.shortcuts import render
from django.http import HttpResponse
from .forms import QuoraUserCreationForm, QuoraUserChangeForm, UserLoginForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import UserFollowing

User = get_user_model()


def userProfile(request, username):
    user = User.objects.get(username=username)
    if request.user.is_authenticated:
        if request.GET.get('follow') is not None:
            UserFollowing.objects.create(user_id=request.user, following_user_id=user)
        elif request.GET.get('unfollow') is not None:
            UserFollowing.objects.get(user_id=request.user, following_user_id=user).delete()

    if user is not None:
        context = {
            'user': user,
            'errors': None,
            'following_count': user.following.all().count(),
            'followers_count': user.followers.all().count(),
        }
        return render(request, 'accounts/user-profile.html', context=context)
    return render(request, 'accounts/user-profile.html', {'errors': 'This account does not exists.'})


def registerUser(request):
    form = QuoraUserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        return HttpResponse("<h2>User created</h2>")
    return render(request, 'accounts/register.html', {'form': form})


def loginUser(request):
    if request.user.is_authenticated:
        return HttpResponse('<h2>You are already logged in </h2>')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('<h2>You are logged in </h2>')
        else:
            return HttpResponse('<h2>Email or password did not match.</h2>')
    return render(request, 'accounts/login.html', {'form': form})


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'accounts/logout.html', {'logged_out': 'logged_out'})
    return render(request, 'accounts/logout.html', {'first_login': 'first_login'})


def changePassword(request):
    form = PasswordChangeForm(request.POST or None)
    if form.is_valid():
        email = request.POST['email']
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        user = authenticate(email=email, password=current_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            return HttpResponse("<h2>Password successfully changed.</h2>")
    return render(request, 'accounts/change-password.html', {'form': form})








