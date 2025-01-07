from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuari del Gimnàs'),
        ('trainer', 'Entrenador'),
        ('director', 'Director')
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    PLAN_CHOICES = [
        ('no_plan', 'Sin Plan'),
        ('basic', 'Plan Básico'),
        ('standard', 'Plan Estándar'),
        ('premium', 'Plan Premium'),
    ]
    
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='no_plan')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    REQUIRED_FIELDS = ['role']
    USERNAME_FIELD = 'email'


class Exercise(models.Model):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'
    LEVEL_CHOICES = [
        (BEGINNER, 'Principiante'),
        (INTERMEDIATE, 'Intermedio'),
        (ADVANCED, 'Avanzado'),
    ]

    STRENGTH = 'Strength'
    CARDIO = 'Cardio'
    FLEXIBILITY = 'Flexibility'
    TYPE_CHOICES = [
        (STRENGTH, 'Fuerza'),
        (CARDIO, 'Cardio'),
        (FLEXIBILITY, 'Flexibilidad'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default=BEGINNER,
    )
    exercise_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=STRENGTH,
    )
    equipment = models.CharField(max_length=200, blank=True, null=True)  
    muscles = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'exercises'

    def __str__(self):
        return self.name
    
class Routine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    recommendations = models.TextField()
    exercises = models.ManyToManyField(Exercise, through='RoutineExercise')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routines')

    class Meta:
        db_table = 'routines'

    def __str__(self):
        return self.name


class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration = models.TextField(help_text="Duración específica minutos o repeticiones")

    class Meta:
        db_table = 'routine_exercises'



class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Lunes'),
        ('Tuesday', 'Martes'),
        ('Wednesday', 'Miércoles'),
        ('Thursday', 'Jueves'),
        ('Friday', 'Viernes'),
    ]

    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    hour = models.IntegerField(
        validators=[
            MinValueValidator(16),
            MaxValueValidator(21)
        ]
    )
    routine = models.ForeignKey('Routine', on_delete=models.CASCADE, null=True, blank=True)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    max_enrolls = models.IntegerField(default=10)
    enrollments = models.ManyToManyField(User, related_name="schedules", blank=True)
    def __str__(self):
        return f"{self.routine}"
    @property 
    def get_id(self):
        return self._id
