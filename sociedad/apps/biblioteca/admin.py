from django.contrib import admin
from sociedad.apps.biblioteca.models import Comentariolib, Libro, Categoria
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Libro)
admin.site.register(Comentariolib)
