# Generated by Django 5.1.2 on 2024-12-16 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0007_alter_exercise_exercise_type_alter_schedule_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='plan',
            field=models.CharField(choices=[('no_plan', 'Sin Plan'), ('basic', 'Plan Básico'), ('standard', 'Plan Estándar'), ('premium', 'Plan Premium')], default='no_plan', max_length=20),
        ),
    ]
