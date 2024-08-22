from django.urls import path
from .views import examen, crear_usuario, iniciar_sesion, cerrar_sesion


urlpatterns = [
    path('examen/', examen, name='examen'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('iniciar_sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
]
