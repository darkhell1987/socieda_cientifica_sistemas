from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Noticia(models.Model):
	titulo=models.CharField(max_length=100)
	imagen=models.FileField(upload_to='img_noticias')
	descripcion = models.TextField()
	fecha_entrada=models.DateTimeField(auto_now_add=True)
	usuario = models.ForeignKey(User, unique=True, null=True)

	def __unicode__(self):
		return '%s %s' %(self.titulo,self.usuario.id)

class ComentarNoticia(models.Model):
	fechacreado = models.DateTimeField(auto_now_add=True)
	autor = models.CharField(max_length=100)
	mensaje = models.TextField()
	requerir = models.ForeignKey(Noticia)
	usuario = models.ForeignKey(User, unique=True, null=True)

	def __unicode__(self):
		return '%s %s ' %(self.requerir,self.mensaje)