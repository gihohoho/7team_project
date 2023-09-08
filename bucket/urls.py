from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('bucket/', views.bucket),
    path('mypage/', views.mypage),  
]