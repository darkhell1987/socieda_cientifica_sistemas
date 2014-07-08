from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categoria(models.Model):
	tipo = models.CharField(max_length=100)

	def __unicode__(self):
		return self.tipo


class Libro(models.Model):
	titulo=models.CharField(max_length=100)
	editorial=models.CharField(max_length=100)
	autor=models.CharField(max_length=100)
	genero=models.CharField(max_length=100)
	pais_autor=models.CharField(max_length=100)
	num_paginas=models.IntegerField()
	publicacion=models.DateField()
	portada = models.ImageField(upload_to='img_libros')
	libro=models.FileField(upload_to='librospdf')
	descripcion = models.TextField()
	fecha_subida=models.DateTimeField(auto_now_add=True)
	requerir=models.ManyToManyField(Categoria)
	user1 = models.ForeignKey(User,null=True)

	def __unicode__(self):
		return '%s %s' %(self.titulo,self.user1.username)

class Comentariolib(models.Model):
	fechacreado = models.DateTimeField(auto_now_add=True)
	autor = models.CharField(max_length=100)
	mensaje = models.TextField()
	requerir = models.ForeignKey(Libro)

	def __unicode__(self):
		return self.autor