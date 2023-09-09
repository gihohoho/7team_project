from django.http import HttpResponse
from django.shortcuts import redirect, render

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
    pass


def logout(request):
    pass
