from django.forms import ModelForm

from .models import *
from django.contrib.auth.models import User

class UsuarioForm(ModelForm):
	class Meta:
		model = User
		exclude = ['password', 'username', 'is_staff', 'is_superuser', 'last_login', 'is_active', 'date_joined', 'user_permissions', 'groups']

class PerfilForm(ModelForm):
	class Meta:
		model = Perfil
		exclude = ['completo' , 'usuario']