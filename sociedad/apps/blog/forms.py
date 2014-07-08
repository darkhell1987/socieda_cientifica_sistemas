from django.forms import ModelForm
from django import forms
from .models import *

class FormularioComentario(ModelForm):
    class Meta:
        model = Comentario
        exclude = ["requerir",'usuario']

class FormularioEntrada(ModelForm):
    class Meta:
        model = Entrada
        exclude = ['usuario']