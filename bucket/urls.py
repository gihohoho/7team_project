from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.bucket),  # 전체 글 리스트
    path('mypage/', views.mypage),  # 내 글 리스트
    path('create/', views.create),  # 새로 만들기
    path('userbucket/<int:user_id>/', views.userbucket),  # 유저 bucket page
    path('profile/<int:user_id>/', views.profile),  # 프로필페이지
    path('profile_image/<int:user_id>/', views.profile_image),  # 프로필 사진 변경
    path('<int:bucket_id>/', views.detail),  # 게시물 1개 보기
    path('comments_create/<int:bucket_id>/', views.comments_create),  # 댓글쓰기
    path('comments_delete/<int:bucket_id>/<int:comment_id>/',
         views.comments_delete),  # 댓글삭제
    path('likes/<int:bucket_id>/', views.likes, name='likes'),  # 좋아요
    path('bookmarks/<int:bucket_id>/', views.bookmarks, name='bookmarks'),  # 북마크
    path('update/<int:bucket_id>/', views.update, name="update"), #게시글 수정
    path('bdelete/<int:bucket_id>/', views.bdelete), #게시글 삭제
]