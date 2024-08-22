from django.db import models
from django.contrib.auth.models import User
from examen.models import Examen, Pregunta

# Create your models here.

class ResultadoExamen(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    puntuacion = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    preguntas_contestadas = models.JSONField() 

    def __str__(self):
        return f'Resultado de {self.usuario} en {self.examen}'

class Intento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    resultado_examen = models.OneToOneField(ResultadoExamen, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Intento de {self.usuario} en {self.fecha_hora}'
