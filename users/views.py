from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from users.models import User


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        User.objects.create_user(
            email=request.POST['email'],
            username=request.POST['nickname'],
            password=request.POST['password'],
            mbti=request.POST['mbti'].upper(),
            tmi=request.POST['tmi'],
            blog=request.POST['blog'],
        )
        return redirect('/users/login/')
    else:
        return HttpResponse('Invalid request method', status=405)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/bucket/')
        else:
            return HttpResponse('Invalid auth', status=401)
    else:
        return HttpResponse('Invalid request method', status=405)


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('/bucket/')
    else:
        return HttpResponse('Invalid request method', status=405)
