from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gym_app.models import Routine, RoutineExercise,Exercise,Schedule
from datetime import datetime, timedelta
# En tu archivo utils.py o decorators.py
from django.shortcuts import redirect
from django.contrib import messages

def check_plan_selected(view_func):
    def wrapper(request, *args, **kwargs):
        # Asumiendo que tienes un modelo de perfil o usuario con un campo de plan
        if request.user.plan == "no_plan":
            messages.warning(request, "Debes seleccionar un plan primero")
            return redirect('gym_workouts:plan')  # Redirige a la página de selección de plan
        return view_func(request, *args, **kwargs)
    return wrapper



@check_plan_selected


def calendar(request):
    # Obtener la fecha actual
    from datetime import datetime, timedelta

def calendar(request):
    today = datetime.now()
    
    # Calcula el inicio de la semana actual
    start_of_week = today.date() - timedelta(days=today.weekday())
    
    days_of_week = []
    for i in range(5):  # 5 días laborables
        current_day = start_of_week + timedelta(days=i)
        days_of_week.append({
            'name': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][i],
            'date': current_day.day,
            'full_date': current_day,
            'is_today': current_day == today.date()
        })

    hours = [16, 17, 18, 19, 20, 21]
    user = request.user
    user_schedules = Schedule.objects.filter(enrollments=user)

    return render(request, 'calendar.html', {
        'days_of_week': days_of_week,
        'hours': hours,
        'week_schedule': Schedule.objects.all(),
        'user_schedules': user_schedules,
        'routines': Routine.objects.all()
    })


def check_limit_plan(user):
    if user.plan == 'basic':
        return 1
    elif user.plan == 'standard':
        return 2
    elif user.plan == 'premium':
        return 3
    else:
        return 0
    

@check_plan_selected
def enroll_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        schedule = get_object_or_404(Schedule, id=schedule_id)
        
        # Verifica si el usuario ya está inscrito
        if request.user in schedule.enrollments.all():
            messages.error(request, "You are already enrolled in this schedule.")
        else:
            enrolled_schedules = Schedule.objects.filter(enrollments=request.user)
            limit_plan = check_limit_plan(request.user)
            if enrolled_schedules.count() >= limit_plan:
                # Si el usuario está inscrito en 3 o más horarios, muestra un mensaje de error
                messages.error(request, f"Tu plan solo permite apuntarte a {limit_plan} rutina/s")
            else:
                if schedule.enrollments.count() < schedule.max_enrolls:
                    schedule.enrollments.add(request.user)
                    messages.success(request, "Apuntado correctamente!")
                else:
                    messages.error(request, "No quedan plazas.")

    return redirect('gym_workouts:home')
@check_plan_selected
def unenroll_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        schedule = get_object_or_404(Schedule, id=schedule_id)
        
        if request.user in schedule.enrollments.all():
            schedule.enrollments.remove(request.user)
            messages.success(request, "Desapuntado correctamente")
        else:
            messages.error(request, "No estas apuntado a este curso.")
    
    return redirect('gym_workouts:home')

def select_plan(request):
    """
    Vista que maneja el cambio de plan de un usuario.
    Si el método es POST, cambia el plan del usuario y redirige.
    """
    user = request.user
    if request.method == 'POST':
        new_plan = request.POST.get('plan') 
        valid_plans = ['no_plan', 'basic', 'standard','premium']
        if new_plan in valid_plans:
            user.plan = new_plan 
            user.save()  
            messages.success(request, f'¡Tu plan ha sido cambiado a {new_plan}!')
        else:
            messages.error(request, 'Plan no válido.')
        return redirect('gym_workouts:home') 
    return render(request, 'select_plan.html')