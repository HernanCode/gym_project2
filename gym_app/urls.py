from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import LogoutView

app_name = 'gym_app'
urlpatterns = [
    path('',views.home, name="home"),
    path('profile/', views.edit_profile, name="edit_profile"),
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout'),
    path('schedule/', views.schedule_view, name='schedule_view'),
    path('routines/', views.routines_list, name='routines_list'),
    path('routines/new', views.new_routine, name='new_routine'),
    path('routines/edit/<int:routine_id>/', views.edit_routine, name='edit_routine'),
    path('routines/delete/<int:routine_id>/', views.delete_routine, name='delete_routine'),
    path('exercises/',views.exercises_list, name='exercises_list'),
    path('exercises/new', views.new_exercise, name='new_exercise'),
    path('exercises/edit/<int:exercise_id>/', views.edit_exercise, name='edit_exercise'),
    path('exercises/delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),  
    path('delete_schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    # path('test-create/', views.test_create_user, name='test-create'),
]
