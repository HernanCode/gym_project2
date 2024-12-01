# Generated by Django 5.1.2 on 2024-11-26 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0002_exercise_routine_routineexercise_routine_exercises'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='default_duration',
        ),
        migrations.AlterField(
            model_name='routineexercise',
            name='duration',
            field=models.IntegerField(help_text='Duración específica minutos o repeticiones'),
        ),
    ]