from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from bucket.models import Bucket

# 메인페이지
def bucket(request):
    if request.method == "GET":
        buckets = Bucket.objects.all()
        context ={
            "buckets":buckets,
        }
        return render(request, "bucket/bucket.html", context)

# 개인페이지
@login_required(login_url='/user/login/')    
@csrf_exempt 
def mypage(request):
    if request.method == "GET":
        buckets = Bucket.objects.all()
        buckets_list = buckets.filter(user_id=request.user.id)
        context = {
            "buckets_list":buckets_list,
        }
        return render(request, "mypage.html", context)

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
