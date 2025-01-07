app_name = 'gym_main'
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='main_page' ),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    # path('', views.home, name='home'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.logout_view, name='logout'),
]