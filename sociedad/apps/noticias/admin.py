from django.contrib import admin

# Register your models here.
from sociedad.apps.noticias.models import Noticia, ComentarNoticia
# Register your models here.

admin.site.register(Noticia)
admin.site.register(ComentarNoticia)