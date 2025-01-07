from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm, RoutineForm,ScheduleForm, ExerciseForm
from .models import Routine, RoutineExercise,Exercise,Schedule
from django.contrib.auth.models import User

def home(request):
    # Días de la semana y horas
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = [16, 17, 18, 19, 20, 21]

    # Preparar la estructura de la tabla de la semana
    week_schedule = []
    schedules = Schedule.objects.all()
    routines = Routine.objects.all()
    
    for hour in hours:
        # Crear un diccionario por cada fila
        row = {'hour': hour}
        for day in days_of_week:
            # Buscar la entrada de horario para ese día y hora
            schedule_entry = schedules.filter(day=day, hour=hour).first()
            row[day] = schedule_entry if schedule_entry and schedule_entry.routine else None
        week_schedule.append(row)
    
    # Manejar POST request
    if request.method == 'POST':

        for row in week_schedule:
            hour = row['hour']
            for day in days_of_week:
                routine_id = request.POST.get(f'{day}_{hour}')
                if routine_id:
                    try:
                        # Obtener o crear un horario para el día y la hora
                        schedule, created = Schedule.objects.get_or_create(day=day, hour=hour,trainer=request.user)
                        
                        # Asociar la rutina al horario
                        routine = Routine.objects.get(id=routine_id)
                        schedule.routine = routine
                        schedule.save()
                    except (Routine.DoesNotExist, ValueError):
                        # Manejo de errores si la rutina no existe o hay un problema
                        messages.error(request, f'Error al procesar la rutina para {day} a las {hour}:00')
        
        messages.success(request, 'Horario actualizado exitosamente')
        return redirect('gym_app:home')
    return render(request, 'home.html', {
        'week_schedule': week_schedule,
        'days_of_week': days_of_week,
        'hours': hours,
        'routines': routines
    })

@login_required
def edit_profile(request):
    """
    Vista que permite a un usuario autenticado editar su perfil.
    
    Si la solicitud es un POST, valida y guarda el formulario de edición del perfil del usuario.
    Si la solicitud es GET, muestra el formulario con los datos actuales del usuario.
    Después de una edición exitosa, redirige a la página principal con un mensaje de éxito.

    Args:
        request: La solicitud HTTP recibida.

    Returns:
        render: Renderiza la plantilla 'edit_profile.html' con el formulario de edición del perfil.
    """
    user = request.user
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('gym_app:home')  
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})

def delete_schedule(request, schedule_id):
    print(schedule_id)
    """
    Vista que maneja la eliminación de un horario existente.

    Si la solicitud es un POST, elimina el horario con el ID proporcionado y redirige a la página principal con un mensaje de éxito.
    Si la solicitud es GET, muestra una confirmación de eliminación.

    Args:
        request: La solicitud HTTP recibida.
        schedule_id: El ID del horario a eliminar.

    Returns:
        render: Renderiza la plantilla 'delete_schedule.html' si es un GET, o redirige a la página principal si es un POST.
    """
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.delete()
    messages.success(request, 'Horario eliminado exitosamente.')
    return redirect('gym_app:home')

    return render(request, 'delete_schedule.html', {'schedule': schedule})

def new_routine(request):
    if request.method == 'POST':
        # Crea una copia mutable de request.POST
        post_data = request.POST.copy()
        series_fields = [key for key in post_data.keys() if key.startswith('series_repetitions_')]
        for field in series_fields:
            post_data.pop(field, None)
        form = RoutineForm(post_data)
        print(form.errors)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.trainer = request.user 
            routine.save()

            # Guardar ejercicios seleccionados
            exercises = form.cleaned_data['exercises']
            for exercise in exercises:
                # Obtén las series/repeticiones para este ejercicio
                series_key = f'series_repetitions_{exercise.name}'
                series_repetitions = request.POST.get(series_key, '')
                
                RoutineExercise.objects.create(
                    routine=routine,
                    exercise=exercise,
                    duration=series_repetitions  # Guarda las series/repeticiones
                )
            return redirect('gym_app:routines_list') 
            # return redirect('adjust_exercises', routine_id=routine.id)
        else:
            # Si el formulario no es válido, renderiza de nuevo con los errores
            exercises = Exercise.objects.all()
            return render(request, 'new_routine.html', {
                'form': form, 
                'exercises': exercises,
                'errors': form.errors
            })

    else:
        form = RoutineForm()

    exercises = Exercise.objects.all()
    return render(request, 'new_routine.html', {'form': form, 'exercises': exercises})

def edit_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)
    exercises = Exercise.objects.all()
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        series_fields = [key for key in post_data.keys() if key.startswith('series_repetitions_')]
        for field in series_fields:
            post_data.pop(field, None)
        form = RoutineForm(post_data, instance=routine)  # Pasa `instance` para editar en lugar de crear
        if form.is_valid():
            routine = form.save(commit=False)
            routine.trainer = request.user  # Asigna el trainer
            routine.save()

            # Borra los ejercicios existentes para evitar duplicados
            RoutineExercise.objects.filter(routine=routine).delete()

            # Guardar ejercicios seleccionados
            exercises = form.cleaned_data['exercises']
            for exercise in exercises:
                series_key = f'series_repetitions_{exercise.name}'
                series_repetitions = request.POST.get(series_key, '')
                print(f"Clave: {series_key}, Valor: {series_repetitions}")
                RoutineExercise.objects.create(
                    routine=routine,
                    exercise=exercise,
                    duration=series_repetitions  # Guarda las series/repeticiones
                )
            
            return redirect('gym_app:routines_list')  # Redirige a la lista de rutinas después de guardar
    else:
        form = RoutineForm(instance=routine)

    return render(request, 'edit_routine.html', {
        'form': form,
        'routine': routine,
        'exercises': exercises,
    })

def delete_routine (request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id)  
    routine.delete()
    messages.success(request, 'Rutina eliminada correctamente.')
    return redirect('gym_app:routines_list')  


def schedule_view(request):
    routines = Routine.objects.all()
    days =  ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = ['14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00']
    return render(request, 'schedule.html', {'routines': routines, 'schedules': Schedule.objects.all(), 'days': days, 'hours': hours})

def routines_list(request):
    routines = Routine.objects.all()
    return render(request, 'routines.html', {'routines': routines})

def exercises_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'exercises.html', {'exercises': exercises})


def new_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ejercicio creado correctamente.')
            return redirect('gym_app:exercises_list')
    else:
        form = ExerciseForm()

    return render(request, 'new_exercise.html', {'form': form})

def edit_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)  # Obtener el ejercicio por su ID
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ejercicio actualizado correctamente.')
            return redirect('gym_app:exercises_list')  # Redirigir a la lista de ejercicios
    else:
        form = ExerciseForm(instance=exercise)  # Prellenar el formulario con los datos actuales

    return render(request, 'edit_exercise.html', {'form': form, 'exercise': exercise})

def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)  
    exercise.delete()
    messages.success(request, 'Ejercicio eliminado correctamente.')
    return redirect('gym_app:exercises_list')  





def logout_view(request):
    """
    Vista que maneja el cierre de sesión de un usuario.
    
    Al hacer logout, se redirige al usuario a la página de inicio.

    Args:
        request: La solicitud HTTP recibida.

    Returns:
        redirect: Redirige a la vista 'home' después de hacer logout.
    """
    logout(request)
    return redirect('gym_main:main_page')
