from django.core.paginator import Paginator
from examen.models import Examen, Pregunta, Respuesta
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import random

def examen(request):
    examen = Examen.objects.first()
    if examen is None:
        return render(request, 'examen/no_examen.html')

    tiempo_total = examen.tiempo_total
    numero_preguntas = examen.numero_preguntas

    # Obtener preguntas aleatorias
    preguntas = list(Pregunta.objects.all())
    if not preguntas:
        return render(request, 'examen/no_preguntas.html')  # En caso de no tener preguntas

    preguntas_seleccionadas = random.sample(preguntas, min(numero_preguntas, len(preguntas)))

    # Paginador
    paginator = Paginator(preguntas_seleccionadas, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Obtener la pregunta actual y sus respuestas
    pregunta_actual = page_obj.object_list[0] if page_obj.object_list else None
    respuestas = Respuesta.objects.filter(pregunta=pregunta_actual) if pregunta_actual else []

    data = {
        'page_obj': page_obj,
        'tiempo_total': tiempo_total,
        'pregunta_actual': pregunta_actual,
        'respuestas': respuestas
    }
    
    return render(request, 'examen/examen.html', data)


def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
        else:
            user = User.objects.create_user(username=nombre, email=email, password=password)
            user.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('home') 
    
    return redirect('home')

def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe.')
            return redirect('home') 

        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('examen') 
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    
    return redirect('home')

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
