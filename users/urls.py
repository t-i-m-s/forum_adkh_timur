from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.register_user, name='register_user'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('profile/<str:nickname>/', views.profile, name='profile'),
]
