from django.urls import path
from . import views

urlpatterns = [
    path('', views.bucket),  # 전체 글 리스트
    path('mypage/', views.mypage),  # 내 글 리스트
    path('create/', views.create),
    path('<int:bucket_id>/', views.detail),  # 게시물 1개 보기
    path('comments_create/<int:bucket_id>/', views.comments_create),  # 댓글쓰기
    path('comments_delete/<int:bucket_id>/', views.comments_delete),  # 댓글삭제
]
