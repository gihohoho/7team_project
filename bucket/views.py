from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from bucket.models import Bucket, Comment
from users.models import User
from django.db import models  # updated_at 설정을 위한 models import
from django.contrib import messages
from django.core.paginator import Paginator

# 메인페이지
def bucket(request):
    if request.method == "GET":
        buckets = Bucket.objects.all()
        users = User.objects.all()

        page = request.GET.get("page", 1)
        paginator = Paginator(buckets, 6)
        bucket = paginator.get_page(page)

        context = {
            "buckets": buckets,
            "users": users,
            "page": bucket,
        }
        return render(request, "bucket/bucket.html", context)


# 개인페이지
@login_required(login_url='/users/login/')
@csrf_exempt
def mypage(request):
    if request.method == "GET":
        buckets = Bucket.objects.all()
        buckets_list = buckets.filter(user_id=request.user.id)

        page = request.GET.get("page", 1)
        paginator = Paginator(buckets_list, 6)
        bucket = paginator.get_page(page)

        bookmarks = request.user.bookmark_buckets.all()

        context = {
            "buckets": buckets,
            "buckets_list": buckets_list,
            "bookmarks": bookmarks,
            "page": bucket,
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
            image=request.FILES.get("image"),
            user=request.user,
        )
        messages.info(request, 'Bucket 새로 만들기 완료!')
        return redirect("/bucket/mypage/")


# 게시글 사진 수정
@login_required(login_url='/users/login/')
@csrf_exempt
def update_image(request, bucket_id):
    if request.method == "GET":
        bucket = Bucket.objects.get(id=bucket_id)
        context = {
            'bucket': bucket,
        }
        return render(request, f'/bucket/{bucket_id}/', context)
    elif request.method == "POST":
        bucket = Bucket.objects.get(id=bucket_id)
        bucket.image = request.FILES.get("image")
        bucket.save()
        messages.info(request, '사진 수정 완료!')
        return redirect(f'/bucket/{bucket_id}/')


# 게시글 수정
@login_required(login_url='/users/login/')
@csrf_exempt
def update(request, bucket_id):
    bucket = Bucket.objects.get(id=bucket_id)
    context = {
        'bucket': bucket,
    }
    if request.method == "GET":
        if bucket.user == request.user:
            return render(request, "bucket/update.html", context)
        else:
            messages.info(request, '작성자만 가능한 기능입니다')
            return redirect(f'/bucket/{bucket_id}/')
    elif request.method == "POST":
        if bucket.user == request.user:
            bucket.title = request.POST.get('title')
            bucket.content = request.POST.get('content')
            bucket.updated_at = models.DateTimeField(auto_now=True)
            bucket.image = request.FILES.get("image")
            bucket.save()
            messages.info(request, 'Bucket 수정 완료!')
            return redirect(f'/bucket/{bucket_id}/')
        else:
            messages.info(request, '작성자만 가능한 기능입니다')
            return redirect(f'/bucket/{bucket_id}/')


# 게시글 삭제
@login_required(login_url='/users/login/')
@csrf_exempt
def bdelete(request, bucket_id):
    buckets = Bucket.objects.get(id=bucket_id)
    if buckets.user == request.user:
        buckets.delete()
        messages.info(request, 'Bucket 삭제 완료!')
        return redirect("/bucket/mypage/")
    else:
        messages.info(request, '작성자만 가능한 기능입니다')
        return redirect(f"/bucket/{bucket_id}/")


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
        messages.info(request, '프로필 사진 수정 완료!')
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
        return render(request, "bucket/profile.html", context)
    elif request.method == "POST":
        user = User.objects.get(id=user_id)
        user.username = request.POST["username"]
        user.mbti = request.POST["mbti"].upper()
        user.tmi = request.POST["tmi"]
        user.blog = request.POST["blog"]
        user.save()
        messages.info(request, '프로필 정보 수정 완료!')
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
        messages.info(request, '댓글 추가 완료')
        return redirect(f'/bucket/{bucket_id}/')
    else:
        messages.info(request, '잘못된 접근입니다')
        return redirect(f'/bucket/{bucket_id}/')


# 댓글삭제
@csrf_exempt
def comments_delete(request, bucket_id, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
            messages.info(request, '댓글 삭제 완료')
            return redirect(f'/bucket/{bucket_id}/')
        else:
            messages.info(request, '작성자만 가능한 기능입니다')
            return redirect(f'/bucket/{bucket_id}/')
    else:
        messages.info(request, '잘못된 접근입니다')
        return redirect(f'/bucket/{bucket_id}/')


# 좋아요
@login_required(login_url='/users/login/')
def likes(request, bucket_id):
    bucket = Bucket.objects.get(id=bucket_id)

    if request.method == "POST":
        if request.user in bucket.like_users.all():
            bucket.like_users.remove(request.user)
            messages.info(request, '좋아요 취소 완료')
        else:
            bucket.like_users.add(request.user)
            messages.info(request, '좋아요 완료')
        return redirect(f'/bucket/{bucket_id}/')
    else:
        messages.info(request, '잘못된 접근입니다')
        return redirect(f'/bucket/{bucket_id}/')


# 북마크
@login_required(login_url='/users/login/')
def bookmarks(request, bucket_id):
    bucket = Bucket.objects.get(id=bucket_id)

    if request.method == "POST":
        if request.user in bucket.bookmarks.all():
            bucket.bookmarks.remove(request.user)
            messages.info(request, '북마크 취소 완료')
        else:
            bucket.bookmarks.add(request.user)
            messages.info(request, '북마크 완료')
        return redirect(f'/bucket/{bucket_id}/')
    else:
        messages.info(request, '잘못된 접근입니다')
        return redirect(f'/bucket/{bucket_id}/')
