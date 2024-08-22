from django.db import models

# Create your models here.
class Pregunta(models.Model):
    enunciado = models.TextField()

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField()
    es_correcta = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.pregunta.id}, {self.texto}, {self.es_correcta}" 

class Examen(models.Model):
    tiempo_total = models.IntegerField(default=600)
    numero_preguntas = models.IntegerField(default=10)
