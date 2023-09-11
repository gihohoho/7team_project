from django.urls import path
from . import views

urlpatterns = [
    path('', views.bucket),
    path('mypage/', views.mypage),
    path('create/', views.create),
    path('<int:bucket_id>/comments_create/', views.comments_create),
    path('<int:bucket_id>/comments_delete/', views.comments_delete),
]