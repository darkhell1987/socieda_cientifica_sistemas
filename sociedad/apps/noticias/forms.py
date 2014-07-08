from django.forms import ModelForm
from django import forms
from .models import *

class FormularioComentarioNoticia(ModelForm):
    class Meta:
        model = ComentarNoticia
        exclude = ["requerir",'usuario']

class FormularioNoticia(ModelForm):
    class Meta:
        model = Noticia
       # exclude = ['usuario']