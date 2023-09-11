from django.http import HttpResponse
from django.shortcuts import render

from bucket.models import Bucket

def bucket(request):
    pass

def mypage(request):
    pass

# 댓글
def comments_create(request, bucket_id):
    if request.method == "POST":
        bucket = Bucket.objects.get(id=bucket_id)
        pass
    elif request.method == "GET":
        bucket = Bucket.objects.get(id=bucket_id)
        pass
    else:
        return HttpResponse('Invalid request method', status=405)

def comments_delete(request, bucket_id):
    if request.method == "POST":
        bucket = Bucket.objects.get(id=bucket_id)
        pass
    elif request.method == "GET":
        bucket = Bucket.objects.get(id=bucket_id)
        pass
    else:
        return HttpResponse('Invalid request method', status=405)
