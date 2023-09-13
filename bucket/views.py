from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from bucket.models import Bucket, Comment, Bookmark
from users.models import User


# 메인페이지
def bucket(request):
    if request.method == "GET":
        buckets = Bucket.objects.all()
        users = User.objects.all()
        context = {
            "buckets": buckets,
            "users": users,
        }
        return render(request, "bucket/bucket.html", context)


# 개인페이지
@login_required(login_url='/users/login/')
@csrf_exempt
def mypage(request):
    if request.method == "GET":
        buckets = Bucket.objects.all()
        buckets_list = buckets.filter(user_id=request.user.id)
        bookmarks = Bookmark.objects.all()
        context = {
            "buckets" : buckets,
            "buckets_list": buckets_list,
            "bookmarks" : bookmarks,
        }
        return render(request, "bucket/mypage.html", context)


# 다른 유저 bucket 페이지
@csrf_exempt
def userbucket(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, id=user_id)
        buckets_list = Bucket.objects.filter(user=user)

        context = {
            'user': user,
            "buckets_list": buckets_list,
        }
        return render(request, "bucket/userbucket.html", context)


# 새로만들기
@login_required(login_url='/users/login/')
@csrf_exempt
def create(request):
    if request.method == "GET":
        return render(request, "bucket/create.html")
    elif request.method == "POST":
        Bucket.objects.create(
            title=request.POST["title"],
            content=request.POST["content"],
            user=request.user,
        )
        return redirect("/bucket/mypage/")


# 프로필 사진 수정
@login_required(login_url='/users/login/')
@csrf_exempt
def profile_image(request, user_id):
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        context = {
            'user': user
        }
        return render(request, "bucket/profile.html", context)
    elif request.method == "POST":
        user = User.objects.get(id=user_id)
        user.image = request.FILES.get("image")
        user.save()
        return redirect(f'/bucket/profile/{user_id}/')


# 프로필 수정
@login_required(login_url='/users/login/')
@csrf_exempt
def profile(request, user_id):
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        context = {
            'user': user,
        }
        return render(request, "bucket/profile.html",context)
    elif request.method == "POST":
        user = User.objects.get(id=user_id)
        user.username = request.POST["username"]
        user.mbti = request.POST["mbti"].upper()
        user.tmi = request.POST["tmi"]
        user.blog = request.POST["blog"]
        user.save()
        return redirect(f'/bucket/profile/{user_id}/')


# 개인 게시물 페이지
def detail(request, bucket_id):
    bucket = Bucket.objects.get(id=bucket_id)
    comments = bucket.comment_set.all()
    context = {
        'bucket': bucket,
        'comments': comments,
    }
    return render(request, "bucket/detail.html", context)


# 댓글생성
@login_required(login_url='/users/login/')
@csrf_exempt
def comments_create(request, bucket_id):
    if request.method == "POST":
        Comment.objects.create(
            content=request.POST["content"],
            user=request.user,
            bucket_id=bucket_id
        )
        return redirect(f'/bucket/{bucket_id}/')
    else:
        return HttpResponse('Invalid request method', status=405)


# 댓글삭제
@csrf_exempt
def comments_delete(request, bucket_id, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return redirect(f'/bucket/{bucket_id}/')
        else:
            return HttpResponse('not allowed to delete', status=403)
    else:
        return HttpResponse('Invalid request method', status=405)


# 좋아요
@login_required(login_url='/users/login/')
def likes(request, bucket_id):
    print(request.method)
    bucket = Bucket.objects.get(id=bucket_id)

    if request.method == "POST":
        if request.user in bucket.like_users.all():
            bucket.like_users.remove(request.user)
        else:
            bucket.like_users.add(request.user)

        return redirect(f'/bucket/{bucket_id}/')
    else:
        return HttpResponse('Invalid request method', status=405)


# 북마크
@login_required(login_url='/users/login/')
@csrf_exempt
def bookmark_create(request, bucket_id):
    if request.method == "POST":
        if request.user in bucket.like_users.all():
            bucket.like_users.remove(request.user)
        else:
            Bookmark.objects.create(
                user=request.user,
                bucket_id=bucket_id
            )
            return redirect(f'/bucket/{bucket_id}/')
    else:
        return HttpResponse('Invalid request method', status=405)

