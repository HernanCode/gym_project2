from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')
def register(request):
    """
    Vista que maneja el registro de un nuevo usuario.
    
    Si la solicitud es un POST, valida el formulario de registro. Si es válido, guarda al usuario,
    inicia sesión y redirige a la página principal con un mensaje de éxito.
    Si la solicitud es GET, muestra un formulario vacío de registro.

    Args:
        request: La solicitud HTTP recibida.

    Returns:
        render: Renderiza la plantilla 'register.html' con el formulario de registro.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registre completat amb èxit!')
            return verify_role(user)
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """
    Vista que maneja el inicio de sesión de un usuario existente.
    
    Si la solicitud es un POST, autentica al usuario usando el email y la contraseña proporcionados.
    Si las credenciales son correctas, inicia sesión y redirige a la página principal con un mensaje de éxito.
    Si las credenciales son incorrectas, muestra un mensaje de error.
    Si la solicitud es GET, muestra el formulario de inicio de sesión vacío.

    Args:
        request: La solicitud HTTP recibida.

    Returns:
        render: Renderiza la plantilla 'login.html' con el formulario de inicio de sesión.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciat sessió correctament!')
                return verify_role(user)
            else:
                messages.error(request, 'ERROR: Credencials incorrectes.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def verify_role(user):
    """
    Verifica el rol del usuario y redirige a la página correspondiente.

    Args:
        user: El objeto de usuario actual.

    Returns:
        redirect: Redirige a la página correspondiente según el rol del usuario.
    """
    if user.role == 'trainer':
        return redirect('gym_app:home')  # Cambia esto por la URL de trainer
    elif user.role == 'user':
        # return redirect('client_dashboard')  # Cambia esto por la URL de client
        return redirect('gym_workouts:home')
    else:
        # messages.error(request, 'Rol desconocido. Contacta con el administrador.')
        # return redirect('home')
        print("hola de nuevo")