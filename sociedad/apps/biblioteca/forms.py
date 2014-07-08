from django.forms import ModelForm
from django import forms
from .models import *

class FormularioCategoria(ModelForm):
    class Meta:
        model = Categoria
	
class FormularioComentario(ModelForm):
    class Meta:
        model = Comentariolib
        exclude = ["requerir",'usuario']

class FormularioLibro(ModelForm):
    class Meta:
        model = Libro
        #exclude = ['usuario']

class buscarForm(forms.Form):
    buscar=forms.CharField(max_length=200)