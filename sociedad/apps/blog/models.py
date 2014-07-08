from django.db import models
from django.contrib.auth.models import User
from sociedad.apps.biblioteca.models import Categoria
# Create your models here.

class Entrada(models.Model):
	categoria=models.ForeignKey(Categoria,null=True)
	titulo=models.CharField(max_length=100)
	imagen=models.FileField(upload_to='img_entrada')
	descripcion = models.TextField()
	fecha_entrada=models.DateTimeField(auto_now_add=True)
	usuario = models.ForeignKey(User, unique=True, null=True)

	def __str__(self):
		return '%s' %(self.titulo)

class Comentario(models.Model):
	fechacreado = models.DateTimeField(auto_now_add=True)
	autor = models.CharField(max_length=100)
	mensaje = models.TextField()
	requerir = models.ForeignKey(Entrada)
	usuario = models.ForeignKey(User, unique=True, null=True)

	def __unicode__(self):
		return '%s %s ' %(self.requerir,self.mensaje)

class Votacion(models.Model):
	date = models.DateTimeField()
	total_point = models.IntegerField( default = 0)
	total_vote = models.IntegerField( default = 0)
	rvoto = models.ForeignKey(Entrada)
	uvoto = models.ForeignKey(User)

	def __unicode__( self):
		return self.date_meal

	def average_point( self):
		return self.total_point * 1.0 / self.total_vote