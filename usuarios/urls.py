from django.urls import path
from .views import home, historial_intentos, finalizar_examen, detalle_evaluacion, usuarios, perfil

urlpatterns = [
    path('', home, name='home'),
    path('historial/', historial_intentos, name='historial_intentos'),
    path('finalizar_examen/', finalizar_examen, name='finalizar_examen'),
    path('detalle_evaluacion/<int:examen_id>/', detalle_evaluacion, name='detalle_evaluacion'),
    path('usuarios', usuarios, name='usuarios'),
    path('perfil', perfil, name='perfil'),
]
