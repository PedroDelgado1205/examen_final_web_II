from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Intento, ResultadoExamen
from examen.models import Examen
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def home(request):
    data = {}
    return render(request, 'examen/inicio.html', data)

@login_required
def finalizar_examen(request):
    examen = Examen.objects.first()
    total_preguntas = examen.numero_preguntas
    calificacion_base = examen.calificacion_base 
    respuestas_usuario = obtener_respuestas_usuario(request)

    aciertos = sum(1 for r in respuestas_usuario if r['respuesta_correcta'])
    fallos = total_preguntas - aciertos

    puntuacion_final = calcular_puntuacion(aciertos, total_preguntas, calificacion_base)

    resultado_examen = ResultadoExamen.objects.create(
        usuario=request.user,
        examen=examen,
        puntuacion=puntuacion_final,
        fecha_hora=timezone.now(),
        preguntas_contestadas=respuestas_usuario
    )

    intento = Intento.objects.filter(usuario=request.user, examen=examen).last()
    intento.resultado_examen = resultado_examen
    intento.save()

    return redirect('historial_intentos')

def calcular_puntuacion(aciertos, total_preguntas, calificacion_base):
    return (calificacion_base * aciertos) / total_preguntas

@login_required
def historial_intentos(request):
    intentos = Intento.objects.filter(usuario=request.user).order_by('-fecha_hora')
    return render(request, 'usuarios/historial_intentos.html', {'intentos': intentos})

@login_required
def detalle_evaluacion(request, examen_id):
    resultado_examen = ResultadoExamen.objects.get(examen_id=examen_id, usuario=request.user)
    preguntas_contestadas = resultado_examen.preguntas_contestadas

    return render(request, 'usuarios/detalle_evaluacion.html', {
        'resultado_examen': resultado_examen,
        'preguntas_contestadas': preguntas_contestadas
    })

def usuarios(request):
    usuarios_registrados = User.objects.all()   
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios_registrados})

@login_required
def perfil(request):
    usuario = request.user
    return render(request, 'usuarios/perfil.html', {'usuario': usuario})