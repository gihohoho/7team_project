from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from users.models import User


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        User.objects.create_user(
            email=request.POST['email'],
            username=request.POST['nickname'],
            password=request.POST['password'],
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
            return HttpResponse('로그인성공')
        else:
            return HttpResponse('Invalid auth', status=401)
    else:
        return HttpResponse('Invalid request method', status=405)


def logout(request):
    pass
