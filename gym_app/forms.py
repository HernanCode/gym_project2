from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Exercise, RoutineExercise, Routine, Schedule
# Formulari de registre
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2']

# Formulari de login
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# Formulari de editar perfil


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        html_class = 'mt-1 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm'
        for field_name, field in self.fields.items():
            # Agregar la clase CSS a cada campo
            field.widget.attrs['class'] = html_class




class RoutineForm(forms.ModelForm):
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Ejercicios"
    )

    class Meta:
        model = Routine
        fields = ['name', 'description', 'duration', 'recommendations', 'exercises']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añade clases CSS a los widgets
        for field_name, field in self.fields.items():
            if field_name != 'exercises':  # CheckboxSelectMultiple ya tiene un diseño adecuado
                field.widget.attrs['class'] = 'mt-1 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 shadow-sm transition-all duration-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 hover:bg-white '

        # Ajuste opcional: Establecer texto de ayuda
        self.fields['exercises'].help_text = "Selecciona uno o más ejercicios para incluir en la rutina."



class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'hour', 'routine']
        widgets = {
            'day': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md'}),
            'hour': forms.TimeInput(attrs={'class': 'w-full border-gray-300 rounded-md', 'type': 'time'}),
            'routine': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md'}),
        }
    



class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'level', 'exercise_type', 'equipment', 'muscles']
    name = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Nombre del ejercicio"}))
    description = forms.CharField(label='Descripcion', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Descripción del ejercicio"}))
    level_choices = [
        ('Beginner', 'Básico'),
        ('Intermediate', 'Intermedio'),
        ('Advanced', 'Avanzado'),
    ]
    level = forms.ChoiceField(label='Nivel', choices=level_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    exercise_type_choices = [
        ('Strength', 'Fuerza'),
        ('Cardio', 'Cardio'),
        ('Flexibility', 'Flexibilidad'),
    ]
    exercise_type = forms.ChoiceField(label='Tipo de ejercicio', choices=exercise_type_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    equipment =  forms.CharField(label='Equipacion necesaria', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ej: Banco, Pesas"}))
    muscles = forms.CharField(label='Musculos', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Biceps, Triceps, Hombro, Espalda"}))
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Añade clases CSS a los widgets
            for field_name, field in self.fields.items():
                if field_name != 'exercises':  # CheckboxSelectMultiple ya tiene un diseño adecuado
                    field.widget.attrs['class'] = 'mt-1 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 shadow-sm transition-all duration-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 hover:bg-white'

            # # Ajuste opcional: Establecer texto de ayuda
            # self.fields['exercises'].help_text = "Selecciona uno o más ejercicios para incluir en la rutina."
