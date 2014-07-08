from django.contrib import admin
from sociedad.apps.blog.models import Entrada, Comentario,Votacion
# Register your models here.

admin.site.register(Entrada)
admin.site.register(Comentario)
admin.site.register(Votacion)