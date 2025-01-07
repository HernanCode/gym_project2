from django.urls import path
from django.urls import include
from . import views

app_name = 'gym_workouts'

urlpatterns = [
    path('', views.calendar, name='home'),
    path('plan/', views.select_plan, name='plan'),
    path('enroll/', views.enroll_schedule, name='enroll'),
    path('unenroll/', views.unenroll_schedule, name='unenroll')
]

