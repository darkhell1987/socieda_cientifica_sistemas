from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
	foto = models.ImageField(upload_to='img_usuarios', verbose_name='Selecciones su foto', null=True)
	intereses = models.TextField(verbose_name=u'Descripcion de Interese', null=True)
	paices = (
		('BOLIVIA', 'BOLIVIA'),
		)
	pais = models.CharField(max_length='50', verbose_name='Seleccione su Pais', choices=paices, null=True)
	ciudades = (
		('CHUQUISACA', 'CHUQUISACA'),
		('LA PAZ', 'LA PAZ'),
		('POTOSI', 'POTOSI'),
		('ORURO','ORURO'),
		('COCHABAMBA','COCHABAMBA'),
		('TARIJA','TARIJA'),
		('SANTA CRUZ','SANTA CRUZ'),
		('PANDO','PANDO'),
		('BENI','BENI'),
		)
	ciudad = models.CharField(max_length='50', verbose_name=u'Seleccione su Ciudad', choices=ciudades, null=True)
	completo = models.IntegerField(default=0)
	usuario = models.ForeignKey(User, unique=True, null=True)
	def __unicode__(self):
		return self.usuario.username