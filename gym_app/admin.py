from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Routine, Exercise, RoutineExercise, Schedule

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Campos adicionales en el formulario de detalle del usuario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Registrar el modelo de usuario personalizado
admin.site.register(User, CustomUserAdmin)



@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Muestra estos campos en la lista del admin
    search_fields = ['name']  # Barra de búsqueda para buscar por nombre

# Configuración para RoutineExercise (si quieres editar las relaciones directamente)
class RoutineExerciseInline(admin.TabularInline):
    model = RoutineExercise
    extra = 1  # Filas adicionales para agregar nuevas relaciones

# Configuración para Routine
@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer')  # Campos visibles en la lista
    list_filter = ('trainer',)  # Filtra por entrenador
    search_fields = ('name',)  # Barra de búsqueda
    inlines = [RoutineExerciseInline]  # Relación con RoutineExercise



@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'hour', 'routine', 'trainer')  # Columnas visibles en la lista del admin
    list_filter = ('day', 'trainer')  # Filtros laterales
    search_fields = ('trainer__username', 'routine__name')  # Campos para búsqueda
    ordering = ('day', 'hour')  # Orden por defecto