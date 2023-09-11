from django.urls import path
from . import views

urlpatterns = [
    path('bucket/', views.bucket),
    path('mypage/', views.mypage),
    path('<int:bucket_id>/comments_create/', views.comments_create),
    path('<int:bucket_id>/comments_delete/', views.comments_delete),
]